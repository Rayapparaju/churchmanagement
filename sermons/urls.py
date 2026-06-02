from django.urls import path
from . import views

app_name = 'sermons'

urlpatterns = [
    path('', views.SermonListView.as_view(), name='sermon_list'),
    path('create/', views.SermonCreateView.as_view(), name='sermon_create'),
    path('<int:pk>/', views.SermonDetailView.as_view(), name='sermon_detail'),
    path('<int:pk>/update/', views.SermonUpdateView.as_view(), name='sermon_update'),
    path('<int:pk>/delete/', views.SermonDeleteView.as_view(), name='sermon_delete'),
    path('<int:pk>/pdf/', views.SermonPDFView.as_view(), name='sermon_pdf'),
]
