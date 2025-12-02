# main/admin.py
from django.contrib import admin
from .models import Profile, Nilai, Feedback, Kuis, ButirSoal, StatusMateri

# Agar bisa edit soal langsung di dalam menu Kuis
class SoalInline(admin.TabularInline):
    model = ButirSoal
    extra = 5 # Langsung sediakan 5 slot soal

class KuisAdmin(admin.ModelAdmin):
    inlines = [SoalInline]

admin.site.register(Profile)
admin.site.register(Nilai)
admin.site.register(Feedback)
admin.site.register(StatusMateri)
admin.site.register(Kuis, KuisAdmin)
# admin.site.register(ButirSoal) # Tidak perlu karena sudah di-inline