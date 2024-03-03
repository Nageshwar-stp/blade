from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('master/', views.master, name='master'),
    path('master-login/', views.master_login, name='master_login'),
    path('download-report/', views.download_report, name='download_report'),
    path('logout/', views.logout, name='logout'),
    path('coordinators/', views.coordinators, name='coordinators')
]
