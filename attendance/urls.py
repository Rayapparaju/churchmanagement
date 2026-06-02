from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='attendance_list'),
    path('mark/', views.MarkAttendanceView.as_view(), name='mark_attendance'),
    path('report/', views.AttendanceReportView.as_view(), name='attendance_report'),
    path('report/pdf/', views.attendance_report_pdf, name='attendance_report_pdf'),
]
