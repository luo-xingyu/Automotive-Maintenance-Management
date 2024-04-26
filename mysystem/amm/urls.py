from django.urls import path,re_path
from . import views

app_name = 'amm'

urlpatterns = [
    path('', views.home, name='home'),
    path('entry/', views.entry, name='entry'), 
    path('register/', views.register, name='register'),
]