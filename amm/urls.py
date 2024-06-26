from django.urls import path,re_path
from . import views

app_name = 'amm'

urlpatterns = [
    # web #
    path('', views.home, name='home'),
    path('entry/', views.entry, name='entry'), 
    path('register/', views.register, name='register'),
    path('logout/', views.userlogout, name='logout'),

    # Module: service_man
    path('service/', views.service,name='service'),
    path('service/project',views.showProject,name='project'),
    path('service/entrust',views.entrust,name='entrust'),
    
    path('service/entrust_details',views.entrust_details,name='entrust_details'),
    
    # function
    path('service/entrust_pay',views.entrust_pay,name='entrust_pay'),
    path('service/entrust_delete',views.entrust_delete,name='entrust_delete'),
    path('service/get_cars/',views.get_cars,name='get_cars'),

    # Module: repair_manager
    path('repair_manage/', views.manageIndex,name='repair_manager'),
    path('repair_manage/work',views.manageTask,name='manageTask'),
    path('repair_manage/check_cost',views.check_cost,name='check_cost'),
    # wechat applet #

    # Module: user
    path('user_login/',views.user_login,name="user_login"),
    path('user_managecar/',views.user_managecar,name='user_managecar'),
    path('user_commission/',views.commission,name='user_commission'),
    path('user_progressquery/',views.progressquery,name='user_progressquery'),
    path('user_commissionhistory/',views.get_commissionhistory,name='user_commissionhistory'),
    path('user_pay/',views.pay,name='user_pay'),
    path('user_message/',views.user_message,name='user_message'),
    path('clear_message/',views.clear_message,name='clear_message'),
    path('read_message/',views.read_message,name='read_message'),
    
    # Module: repair_man
    path('repair_getorder/',views.get_order,name='getorder'),
    path('repair_finish/',views.repair_finsh,name='repair_finish'),
]