# main/models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # --- Field Foto Profil ---
    foto = models.ImageField(default='profile_pics/default.jpg', 
                             upload_to='profile_pics')
    # --- Field Tambahan (Kelas) ---
    kelas = models.CharField(max_length=5, default='7A') # Tambahkan ini jika kelas perlu disimpan
    # ---------------------------

    def __str__(self):
        return f'{self.user.username} Profile'