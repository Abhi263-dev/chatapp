from pydoc import describe
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	photo = models.ImageField(upload_to='images/', default='images/default.jpg', blank="True")
	dob=models.DateField(null=True,blank=True)
	bio=models.TextField(blank=True,null=True, default="")

class Friends(models.Model):
	friend1=models.ForeignKey(User,on_delete=models.CASCADE, related_name='friend1')
	friend2=models.ForeignKey(User,on_delete=models.CASCADE, related_name='friend2')
	date_added=models.DateField(auto_now_add=True, null=True)

class Requests(models.Model):
	requester=models.ForeignKey(User,on_delete=models.CASCADE, related_name='requester')
	requestee=models.ForeignKey(User,on_delete=models.CASCADE, related_name='requestee')
	date_added=models.DateField(auto_now_add=True, null=True)

class Interest(models.Model):
	name=models.CharField(max_length=200, unique=True)

class UserInterest(models.Model):
	interest=models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='interest')
	u=models.ForeignKey(User, on_delete=models.CASCADE, related_name='u')
