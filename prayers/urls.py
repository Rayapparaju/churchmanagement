from django.urls import path
from . import views

app_name = 'prayers'

urlpatterns = [
    path('', views.PrayerRequestListView.as_view(), name='prayer_list'),
    path('create/', views.PrayerRequestCreateView.as_view(), name='prayer_create'),
    path('<int:pk>/', views.PrayerRequestDetailView.as_view(), name='prayer_detail'),
    path('<int:pk>/update/', views.PrayerRequestUpdateView.as_view(), name='prayer_update'),
    path('report/pdf/', views.PrayerRequestPDFView.as_view(), name='prayer_pdf'),
]
