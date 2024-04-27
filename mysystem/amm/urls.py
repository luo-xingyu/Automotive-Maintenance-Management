from django.urls import path,re_path
from . import views

app_name = 'amm'

urlpatterns = [
    path('', views.home, name='home'),
    path('entry/', views.entry, name='entry'), 
    path('register/', views.register, name='register'),
    path('logout/', views.userlogout, name='logout'),

    # =============================================================================
    # Module: user
    # =============================================================================
    path('user/', views.user, name='user'),

    # =============================================================================
    # Module: service_man
    # =============================================================================
    path('service/', views.service,name='service'),
    path('service/project',views.showProject,name='project'),

]