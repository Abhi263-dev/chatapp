from django.db import models
from profiles.models import User

class Post(models.Model):
    picture=models.ImageField(upload_to='images/', default='')
    date_added=models.DateField(auto_now_add=True)
    caption=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    private=models.BooleanField(default=False)
