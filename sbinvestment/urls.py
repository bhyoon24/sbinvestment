from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('member', views.sb_member, name='sb-member'),
    path('sms', views.sms, name="sms"),
]