from django.urls import path,re_path
from . import views

app_name = 'amm'

urlpatterns = [
    path('entry/', views.entry, name='entry'),  # 定义 /entry/ 也为 entry 视图，这里可能要用不同的名字以避免冲突
]