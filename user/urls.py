from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('ticket-login/', views.ticket_login, name='ticket-login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('/<str:name>/', views.profile, name='profile'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    path('chatbot/', views.chatbox, name='chatbot'),
    path('tickets/', views.view_tickets, name='tickets'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket-detail'),
    path('staff-dashboard/', views.staff_dashboard, name='staff-dashboard'),
    path('notification', views.notification, name='notification'),
]