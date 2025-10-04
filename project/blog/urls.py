from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='blog-home'),
    path('/post/', views.post, name='blog-post'),
    path('/post/<str:id>/', views.single_post, name='blog-single-post'),
    path('/contact/', views.contact, name='blog-contact'),
    path('/dashboard/', views.dashboard, name='blog-dashboard'),
    path('/dashboard/view-post/<str:id>', views.dashboard_view_post, name='blog-dashboard-view-post'),
    path('/dashboard/new-post/', views.dashboard_new_post, name='blog-dashboard-new-post'),
    path('/dashboard/edit-post/<str:id>', views.dashboard_edit_post, name='blog-dashboard-edit-post'),
    path('/dashboard/delete-post/<str:id>', views.dashboard_delete_post, name='blog-dashboard-delete-post'),
    path('/dashboard/blog-dashboard-edit-profile/', views.dashboard_edit_profil, name='blog-dashboard-edit-profile'),
]