# main/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    kelas = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(default='profile_pics/default.jpg', 
                             upload_to='profile_pics')


    # --- Field Foto Profil ---
    foto = models.ImageField(default='profile_pics/default.jpg', 
                             upload_to='profile_pics')
    # --- Field Tambahan (Kelas) ---
    kelas = models.CharField(max_length=5, default='7A') # Tambahkan ini jika kelas perlu disimpan
    # ---------------------------


    def __str__(self):
        return f'{self.user.username} Profile'
    
    
class Nilai(models.Model):
    KATEGORI_CHOICES = [
        ('bulat', 'Bilangan Bulat'),
        ('desimal', 'Bilangan Desimal'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    skor = models.IntegerField(default=0) # Nilai 0-100
    tanggal = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.kategori}: {self.skor}"

# 2. MODEL UNTUK FEEDBACK
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isi_pesan = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"
    
class Kuis(models.Model):
    nama = models.CharField(max_length=100) # Contoh: "Latihan 1"
    kategori_materi = models.CharField(max_length=50) # Contoh: "bulat", "desimal"
    minimal_nilai = models.IntegerField(default=60) # KKM
    
    def __str__(self):
        return self.nama

class ButirSoal(models.Model):
    kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE, related_name='soal_soal')
    teks_soal = models.TextField() # Soal Cerita
    # Pilihan Jawaban
    opsi_a = models.CharField(max_length=200)
    opsi_b = models.CharField(max_length=200)
    opsi_c = models.CharField(max_length=200)
    opsi_d = models.CharField(max_length=200)
    # Kunci Jawaban (a, b, c, atau d)
    kunci = models.CharField(max_length=1, choices=[('a','A'), ('b','B'), ('c','C'), ('d','D')])

    def __str__(self):
        return self.teks_soal[:50]

# Mencatat status penyelesaian materi oleh user
class StatusMateri(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materi_bulat_selesai = models.BooleanField(default=False)
    materi_desimal_selesai = models.BooleanField(default=False)

    def __str__(self):
        return f"Status {self.user.username}"
    
class RiwayatSimulasi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    angka_1 = models.FloatField() # Misal: 0.917
    angka_2 = models.FloatField() # Misal: 0.97
    jawaban_siswa = models.CharField(max_length=10) # 'lebih_besar' atau 'lebih_kecil'
    is_benar = models.BooleanField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.angka_1} vs {self.angka_2}"