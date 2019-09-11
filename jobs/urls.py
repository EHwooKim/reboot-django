from django.urls import path
from . import views
# 서버 실행하면 settings.py 체크하고 urls.py를 체크한다 그렇기 때문에 urlpatterns를 안쓰면 계속 오류만 뜬다.

app_name = 'jobs'
urlpatterns = [
    path('', views.index, name='index'),
    path('pastlife/',views.pastlife, name='pastlife'),
    
]