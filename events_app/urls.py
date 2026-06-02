from django.urls import path
from . import views

app_name = 'events_app'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('<int:pk>/pdf/', views.EventPDFView.as_view(), name='event_pdf'),
    path('<int:pk>/volunteer/', views.VolunteerForEventView.as_view(), name='event_volunteer'),
]
