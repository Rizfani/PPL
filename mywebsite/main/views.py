# main/views.py

from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
# --- IMPOR WAJIB UNTUK PROFIL DAN FOTO ---
from .forms import ProfileUpdateForm 
from .models import Profile 
# ------------------------------------------

# --- Bagian Login dan Register ---

def home(request):
    """View untuk halaman utama."""
    return render(request, 'main/home.html', {})

def register(request):
    """View placeholder untuk halaman registrasi."""
    return render(request, 'main/register.html', {})

def login(request):
    """View yang menangani proses login dan autentikasi."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            pass 
            
    return render(request, 'main/login.html', {})

# --- Bagian Setelah Login (Memerlukan autentikasi) ---

@login_required 
def dashboard(request):
    """View untuk halaman dashboard. Mengambil data foto dan kelas."""
    # Ambil atau buat objek Profile. Ini memastikan setiap user memiliki profile.
    profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        'username': request.user.username,
        'kelas': profile.kelas,     # Mengambil kelas dari Model Profile
        'profile': profile          # Mengirim objek profile untuk mengakses foto
    }
    return render(request, 'main/dashboard.html', context)

@login_required 
def edit_profile_view(request):
    """View untuk memproses form update foto dan kelas."""
    # Ambil atau buat objek Profile.
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # request.FILES WAJIB disertakan untuk form file upload (foto)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES,
                                   instance=profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('dashboard') # Redirect ke dashboard setelah simpan
    else:
        # Inisialisasi form dengan data yang sudah ada
        p_form = ProfileUpdateForm(instance=profile) 

    context = {
        'p_form': p_form,
        'user_display_name': request.user.username,
        'profile': profile # Mengirim objek profile untuk menampilkan foto saat ini
    }
    return render(request, 'main/edit_profile.html', context)


def logout_view(request):
    """Fungsi untuk log out pengguna."""
    logout(request)
    return redirect('home')