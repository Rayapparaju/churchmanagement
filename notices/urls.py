from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice_list'),
    path('create/', views.NoticeCreateView.as_view(), name='notice_create'),
    path('<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('<int:pk>/update/', views.NoticeUpdateView.as_view(), name='notice_update'),
    path('<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice_delete'),
    path('pdf/', views.NoticePDFView.as_view(), name='notice_pdf'),
]
