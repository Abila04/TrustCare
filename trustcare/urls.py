from django.urls import include, path
from . import views

urlpatterns =[
    path('',views.index,name='index'),
    path('user_reg/',views.user_reg,name='user_reg'), 
    path('about/', views.about, name='about'),
    path('volunteer/register/', views.volunteer_register, name='volunteer_register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),  
    path('admin_view_vol/', views.admin_view_vol, name='admin_view_vol'),
    path('admin_view_approved_vol/', views.admin_view_approved_vol, name='admin_view_approved_vol'),
    path('admin_reject_vol/', views.admin_reject_vol, name='admin_reject_vol'),
    path('admin_approve_vol/', views.admin_approve_vol, name='admin_approve_vol'),
    path('admin_view_rejected_vol/', views.admin_view_rejected_vol, name='admin_view_rejected_vol'), 
    path('admin_view_user/',views.admin_view_user,name='admin_view_user'),
    path('services/', views.service_list, name='service_list'),
    path('logout/', views.logout, name='logout'),   
    path('adm_addserv/', views.adm_addserv, name='adm_addserv'),
    path('user_view_service/', views.user_view_service, name='user_view_service'),
    path('user_view_booking/', views.user_view_booking, name='user_view_booking'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin_view_booking/', views.admin_view_booking, name='admin_view_booking'),
    path('admin_view_allocated_booking/', views.admin_view_allocated_booking, name='admin_view_allocated_booking'),
    path('admin_booking_view/', views.admin_view_booking, name='admin_booking_view'),
    path('allocate/<int:booking_id>/', views.allocate_volunteer, name='allocate_volunteer'),
    path('assigned_tasks/', views.vol_view_assigned_tasks, name='assigned_tasks'),
    path('volunteer/availability/<int:volunteer_id>/', views.volunteer_availability, name='volunteer_availability'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('success/<int:payment_id>/', views.success_page, name='success_page'),  # Add success page view
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
]