
from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.index, name='index'),
    path('chat/<int:pk>',views.chat, name='chat'),
    path('register/',views.register, name='register'),
    
    path('login/',views.Login, name='login'),

    path('logout/',views.Logout, name='logout'),
    
    path('profile/',views.profile, name='profile'),
    

    path('sent_msg/<int:pk>',views.sent_msg, name='sent_msg'),

    path('recv_msg/<int:pk>',views.receivedMessages, name='recv_msg'),

    path('notification',views.chatNotification, name='notification'),
    
    path('settings/', views.settings, name='settings'),




]




