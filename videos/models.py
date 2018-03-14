from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    video_title = models.CharField(max_length=250)
    file_file = models.FileField(default='null')
