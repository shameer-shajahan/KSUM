from django.urls import path
from . import views

urlpatterns = [
    path('', views.yipform_create, name='yipform_create'),
    path('yipform/', views.yipform_list, name='yipform_list'),
    path('admin/login/local/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    # path('admin/create/', views.admin_create, name='admin_create'),
    # path('admin/', views.admin_list, name='admin_list'),
]



