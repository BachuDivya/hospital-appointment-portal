
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),
    path('book/', views.book_appointment, name='book_appointment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'manage-appointments/',
        views.manage_appointments,
        name='manage_appointments'
    ),
]
