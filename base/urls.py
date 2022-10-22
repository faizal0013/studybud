from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('profile/<int:pk>', views.useProfile, name='user-profile'),
    path('delete-message/<int:pk>', views.deleteMessage, name='delete-message'),
    path('', views.home, name='home'),
    path('room/<int:pk>', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<int:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>', views.deleteRoom, name='delete-room'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicPage, name='topics'),
    path('activity/', views.activitiesPage, name='activity'),
]
