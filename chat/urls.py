from django.urls import path

from . import views

app_name='chat'

urlpatterns = [
	path('room/', views.ChatRoom.as_view(), name='room'),
	path('room/<str:user>/', views.ChatRoom.as_view(), name='room'),
]