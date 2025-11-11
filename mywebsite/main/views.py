from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User  
from django.contrib import messages
from .models import Profile  

def home(request):
    return render(request, "main/home.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        kelas = request.POST.get('kelas')

        # Cek apakah username sudah ada
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('register')

        # Buat user baru pakai Django User (password otomatis di-hash)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Simpan kelas ke model Profile (relasi one-to-one dengan User)
        Profile.objects.create(user=user, kelas=kelas)

        messages.success(request, "Pendaftaran berhasil! Silakan login.")
        return redirect('login')

    return render(request, "main/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentikasi bawaan Django (password otomatis diverifikasi hash-nya)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login berhasil!")
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah.")
            return redirect('login')

    return render(request, "main/login.html")


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Ambil data kelas dari model Profile
    try:
        profile = Profile.objects.get(user=request.user)
        kelas = profile.kelas
    except Profile.DoesNotExist:
        kelas = "-"

    context = {
        'username': request.user.username,
        'kelas': kelas
    }
    return render(request, "main/dashboard.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Anda telah logout.")
    return redirect('home')
