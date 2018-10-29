from django.urls import path

from .views import report_details, ReportUpload, ReportList

urlpatterns = [
    path('', ReportList.as_view(), name='report-list'),
    path('<report_id>/', report_details, name='report-details'),
    path('upload', ReportUpload.as_view(), name='report-upload'),
]
