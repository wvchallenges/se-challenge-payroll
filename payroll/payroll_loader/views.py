import datetime
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from django.views.generic.list import ListView
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from payroll_loader.models import (
    Employee,
    EmployeeJobGroup,
    JobGroup,
    PayCheque,
    Report,
    WorkDay,
)
from payroll_loader.utilities import (
    get_period_start_and_end,
)

class IndexView(TemplateView):

    template_name = 'index.html'


class WorkDayList(ListView):

    model = PayCheque
    template_name = 'report.html'

    report_data_pack = PayCheque.objects.all().order_by('-start_date', '-end_date')

    def get_queryset(self, **kwargs):
        return self.report_data_pack


class CSVUploaderView(TemplateView):

    template_name = 'import.html'

    def post(self, request, *args, **kwargs):

        # read csv
        csv_file = request.FILES['csv_file']
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[1:]
        lines = [l for l in lines if l]

        populate_job_groups()

        _, rid, _, _ = tuple(lines.pop().split(','))

        if Report.objects.filter(report_footer=rid).exists():
            return HttpResponse(
                'Payroll report {rid} has already been loaded'.format(rid=rid)
            )

        report = Report.objects.create(report_footer=rid)

        for line in lines:
            date_input, hours_worked_input, employee_id_input, job_group_input = tuple(line.split(','))
            date_input = datetime.datetime.strptime(date_input, '%d/%m/%Y')
            job_group_input = job_group_input.strip('\r')

            job_group = JobGroup.objects.filter(type=job_group_input)

            if not job_group.exists():
                return HttpResponse(
                    f'Job Group {job_group_input} does not exist'
                )

            pay_rate = job_group.values_list('pay_rate', flat=True)[0]
            job_group = job_group[0]

            employee, _ = Employee.objects.get_or_create(
                employee_number=employee_id_input,
            )

            employee_job_group_id, _ = EmployeeJobGroup.objects.get_or_create(
                employee=employee,
                job_group=job_group,
            )

            pay_period_start, pay_period_end = get_period_start_and_end(date_input)

            pay_cheque = PayCheque.objects.filter(
                employee=employee,
                start_date=pay_period_start,
                end_date=pay_period_end,
            )

            if not pay_cheque.exists():
                pay_cheque = PayCheque.objects.create(
                    employee=employee,
                    pay_amount=0,
                    start_date=pay_period_start,
                    end_date=pay_period_end,
                )
            else:
                pay_cheque = pay_cheque[0]

            pay_cheque.pay_amount = float(pay_cheque.pay_amount) + (float(hours_worked_input) * float(pay_rate))
            pay_cheque.save()

            work_day, _ = WorkDay.objects.get_or_create(
                employee_job_group=employee_job_group_id,
                date=date_input,
                hours=hours_worked_input,
                report=report,
                pay_cheque=pay_cheque,
            )

        return redirect('payroll_report')
        # return HttpResponse(OK)
