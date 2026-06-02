from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('church-info/', views.church_info_view, name='church_info'),
    path('church-info/edit/', views.church_info_edit, name='church_info_edit'),
]
