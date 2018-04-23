from django.db import models


class Report(models.Model):
    """
    Report footer ID and date uploaded
    """

    # Report ID from report footer
    report_footer = models.IntegerField()
    # Date report loaded
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Report {0} uploaded on {1}'.format(
            self.report_footer,
            self.date_uploaded
        )


class JobGroup(models.Model):
    """
    Job group type (e.g. A or B) and hourly pay rate
    """

    # Job group type (e.g. A, B)
    type = models.CharField(max_length=128)
    # Pay rate of job group
    pay_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return 'Job group {0} with pay rate {1}'.format(
            self.type,
            self.pay_rate
        )


class Employee(models.Model):
    """
    Employee number from uploaded payroll file
    """

    # Employee ID number from payroll file
    employee_number = models.CharField(primary_key=True, max_length=128)

    def __str__(self):
        return 'Employee number {0}'.format(
            self.employee_number
        )


class EmployeeJobGroup(models.Model):
    '''
    Employees are members of job groups
    '''

    # Employee of this job group
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job_group = models.ForeignKey(JobGroup, on_delete=models.CASCADE)

    def __str__(self):
        return 'Employee {0} belongs to job group {1}'.format(
            self.employee,
            self.job_group
        )


class PayCheque(models.Model):
    """
    Pay cheque calculated for pay period from uploaded payroll file
    """

    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Inclusive
    start_date = models.DateField()
    # Inclusive
    end_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return 'Employee {0} paid {1} for pay period starting {2} and ending {3}'.format(
            self.employee,
            self.pay_amount,
            self.start_date,
            self.end_date
        )


class WorkDay(models.Model):
    """
    Hours worked on date for employee and job group relation
    """
    
    employee_job_group = models.ForeignKey(EmployeeJobGroup, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    pay_cheque = models.ForeignKey(PayCheque, on_delete=models.CASCADE)

    def __str__(self):
        return 'Worked {0} hours on {1}'.format(
            self.hours,
            self.date
        )
