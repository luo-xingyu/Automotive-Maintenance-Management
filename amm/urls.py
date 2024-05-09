from django.urls import path,re_path
from . import views

app_name = 'amm'

urlpatterns = [
    path('', views.home, name='home'),
    path('entry/', views.entry, name='entry'), 
    path('register/', views.register, name='register'),
    path('logout/', views.userlogout, name='logout'),

    # Module: service_man
    path('service/', views.service,name='service'),
    path('service/project',views.showProject,name='project'),
    path('service/entrust',views.entrust,name='entrust'),

    # function
    path('service/get_cars/',views.get_cars,name='get_cars'),

    # Module: repair_manager
    path('repair_manage/', views.manageIndex,name='repair_manager'),
    path('repair_manage/work',views.manageTask,name='manageTask'),

    # Module: user
    path('user_login/',views.user_login,name="user_login"),
    path('get_csrf/',views.get_csrf,name="get_csrf")
]