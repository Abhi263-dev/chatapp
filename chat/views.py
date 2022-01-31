from django.shortcuts import render
from profiles.models import Friends
from .models import Room, Message
from django.db.models import Q
from profiles.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ChatRoom(LoginRequiredMixin, View):
	def get(self, request, user=None):
		friends1=Friends.objects.filter(friend1__id=request.user.id).values('friend2__username')
		friends2= Friends.objects.filter(friend2__id=request.user.id).values('friend1__username')
		if not user:
			return render(request, 'chatroom.html', {'f1': friends1, 'f2': friends2})
		user2=User.objects.get(username=user)
		room=Room.objects.filter(Q(user1=request.user, user2=user2) | Q(user2=request.user, user1=user2))
		if not room:
			new_room=Room.objects.create(user1=request.user, user2=user2)
			new_room.save()
			room=new_room.room_name
		else:
			room=room.first().room_name
		messages=Message.objects.filter(room__room_name=room)
		return render(request, 'chatroom.html', {'room_name': room, 'username': request.user.username, 'rec': user, 'pic':user2.photo.url ,'messages':messages, 'f1': friends1, 'f2': friends2})