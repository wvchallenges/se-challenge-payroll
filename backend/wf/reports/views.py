import csv
import datetime
import json
from calendar import monthrange
from collections import defaultdict

from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .models import TimeReport, TimeReportEntry
from .serializers import TimeReportSerializer

START_OF_SECOND_HALF_MONTH_PAY_PERIOD = 16

class ReportList(ListAPIView):
    serializer_class = TimeReportSerializer
    queryset = TimeReport.objects.all()


def _get_pay_period_end(pay_period_start):
    if (pay_period_start.day < START_OF_SECOND_HALF_MONTH_PAY_PERIOD):
        return pay_period_start.replace(
            day=START_OF_SECOND_HALF_MONTH_PAY_PERIOD - 1,
        )
    (_, days_in_month) = monthrange(
        pay_period_start.year,
        pay_period_start.month,
    )
    return pay_period_start.replace(day=days_in_month)


def report_details(request, report_id):
    report_entries_by_employee = defaultdict(lambda: defaultdict(int))
    for time_report_entry in TimeReportEntry.objects.filter(
        time_report_id=report_id,
    ):
        employee_id = time_report_entry.employee_id
        report_date = time_report_entry.date
        pay_period_start = report_date.replace(
            day=
            1 if report_date.day < START_OF_SECOND_HALF_MONTH_PAY_PERIOD
            else START_OF_SECOND_HALF_MONTH_PAY_PERIOD
        )
        amount_paid = time_report_entry.hours_worked * (
            20 if time_report_entry.job_group == 'A' else 30
        )
        report_entries_by_employee[employee_id][pay_period_start] += amount_paid

    time_report_rows = []
    for (employee_id, pay_periods) in report_entries_by_employee.items():
        for (pay_period_start, amount_paid) in pay_periods.items():
            time_report_rows.append({
                'employee_id': employee_id,
                'pay_period_start': pay_period_start.isoformat(),
                'pay_period_end': _get_pay_period_end(pay_period_start).isoformat(),
                'amount_paid': amount_paid,
            })
    return JsonResponse(json.dumps(time_report_rows), safe=False)


class ReportUpload(APIView):
    def post(self, request):
        decoded_file = request.data['file'].read().decode('utf-8').splitlines()

        time_report_entries = []
        time_report_id = None
        for row in csv.reader(decoded_file):
            if row[0] == 'date':
                continue
            if row[0] == 'report id':
                time_report_id = row[1]
                if TimeReport.objects.filter(pk=time_report_id):
                    return HttpResponse(
                        'Time Report with id {} already exists'.format(time_report_id),
                        status=409,
                    )
                for entry in time_report_entries:
                    entry.time_report_id = time_report_id
            else:
                (date_string, hours_worked, employee_id, job_group) = row
                date = datetime.datetime.strptime(
                    date_string,
                    '%d/%m/%Y',
                ).date()
                time_report_entries.append(
                    TimeReportEntry(
                        date=date,
                        employee_id=employee_id,
                        hours_worked=hours_worked,
                        job_group=job_group,
                    ),
                )
        TimeReport.objects.create(pk=time_report_id)
        TimeReportEntry.objects.bulk_create(time_report_entries)
        return JsonResponse({'time_report_id': time_report_id})
