from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey
from profiles.models import User

class Room(models.Model):
	user1=models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='user1')
	user2=models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='user2')
	room_name=models.CharField(max_length=200, null=True, blank=True)

	def save(self, *args, **kwargs):
		self.room_name=self.user1.username+"-"+self.user2.username
		super(Room, self).save(*args, **kwargs)

class Message(models.Model):
	sender=models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='sender')
	room=models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
	content=models.TextField()
	date_added=models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('date_added',)

