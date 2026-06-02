from django.urls import path
from . import views

app_name = 'offerings'

urlpatterns = [
    path('', views.OfferingListView.as_view(), name='list'),
    path('create/', views.OfferingCreateView.as_view(), name='create'),
    path('<int:pk>/', views.OfferingDetailView.as_view(), name='detail'),
    path('<int:pk>/receipt/', views.OfferingReceiptView.as_view(), name='receipt'),
    path('<int:pk>/send-whatsapp/', views.OfferingSendWhatsAppView.as_view(), name='send_whatsapp'),
]
