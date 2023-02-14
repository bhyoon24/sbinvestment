from django.urls import path
from . import views

urlpatterns = [
    path('', views.sms, name="sms"),
    path('index', views.index, name='index'),
    path('member', views.sb_member, name='sb-member'),
]