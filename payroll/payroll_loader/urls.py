from django.urls import path

from payroll_loader.views import IndexView
from payroll_loader.views import CSVUploaderView
from payroll_loader.views import WorkDayList

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('upload/', CSVUploaderView.as_view(), name='upload_csv'),
    path('report/', WorkDayList.as_view(), name='payroll_report'),
]
