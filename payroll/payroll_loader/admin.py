from django.contrib import admin

from payroll_loader.models import (
    Employee,
    EmployeeJobGroup,
    JobGroup,
    PayCheque,
    Report,
    WorkDay,
)


admin.site.register(Employee)
admin.site.register(EmployeeJobGroup)
admin.site.register(JobGroup)
admin.site.register(PayCheque)
admin.site.register(Report)
admin.site.register(WorkDay)
