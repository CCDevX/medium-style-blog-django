from django.urls import path, include
from . import views

urlpatterns = [
    path('/register/', views.auth_register, name='authenticated-register'),
    path('/login/', views.auth_login, name='authenticated-login'),
    path('/logout/', views.auth_logout, name='authenticated-logout'),
]