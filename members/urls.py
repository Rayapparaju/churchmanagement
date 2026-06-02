from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    # Member URLs
    path('', views.MemberListView.as_view(), name='member_list'),
    path('members/', views.MemberListView.as_view(), name='member_list'),
    path('members/create/', views.MemberCreateView.as_view(), name='member_create'),
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    path('members/<int:pk>/update/', views.MemberUpdateView.as_view(), name='member_update'),
    path('members/<int:pk>/delete/', views.MemberDeleteView.as_view(), name='member_delete'),
    path('members/<int:pk>/pdf/', views.MemberPDFView.as_view(), name='member_pdf'),
    path('members/<int:pk>/id-card/', views.MemberIDCardPDFView.as_view(), name='member_id_card'),
    path('members/import/', views.MemberImportView.as_view(), name='member_import'),
    path('members/import/sample/', views.MemberImportSampleView.as_view(), name='member_import_sample'),

    # Staff URLs
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    path('staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),
    path('staff/<int:pk>/pdf/', views.StaffPDFView.as_view(), name='staff_pdf'),

    # Baptism Certificate URLs
    path('members/<int:member_pk>/baptism-certificate/create/', views.BaptismCertificateCreateView.as_view(), name='baptism_certificate_create'),
    path('baptism-certificate/<int:pk>/pdf/', views.BaptismCertificatePDFView.as_view(), name='baptism_certificate_pdf'),
    path('baptism-certificate/<int:pk>/delete/', views.BaptismCertificateDeleteView.as_view(), name='baptism_certificate_delete'),
]
