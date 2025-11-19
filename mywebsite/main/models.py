from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kelas = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(default='profile_pics/default.jpg', 
                             upload_to='profile_pics')


    def __str__(self):
        return self.user.username