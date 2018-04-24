import datetime
from dateutil.relativedelta import relativedelta

from payroll_loader.models import (
    Employee,
    EmployeeJobGroup,
    JobGroup,
    PayCheque,
    Report,
    WorkDay,
)


def populate_job_groups():
    JobGroup.objects.get_or_create(
        type='A',
        pay_rate=20,
    )

    JobGroup.objects.get_or_create(
        type='B',
        pay_rate=30,
    )


def get_period_start_and_end(pay_date):
    if pay_date.day >= 1 and pay_date.day < 16:
        pay_period_start = datetime.datetime.strptime(
            f'{pay_date.year}-{pay_date.month}-01', '%Y-%m-%d'
        )
        pay_period_end = datetime.datetime.strptime(
            f'{pay_date.year}-{pay_date.month}-15', '%Y-%m-%d'
        )
    else:
        pay_period_start = datetime.datetime.strptime(
            f'{pay_date.year}-{pay_date.month}-16', '%Y-%m-%d'
        )
        pay_period_end = pay_date + relativedelta(
            day=1, months=+1, days=-1
        )

    return pay_period_start, pay_period_end
