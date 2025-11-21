from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User  
from django.contrib import messages
from django.contrib.auth.decorators import login_required # <-- Tambahkan ini
from .models import Profile  
from .forms import ProfileForm, UserForm

def home(request):
    return render(request, "main/home.html")

# --- UPDATE FUNGSI REGISTER ---
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

        # 1. Buat User
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # 2. Simpan Profile
        Profile.objects.create(user=user, kelas=kelas)

        # 3. LOGIN OTOMATIS (Auto-Login)
        # Gunakan 'auth_login' agar tidak error (karena kita mengimpornya sebagai auth_login)
        auth_login(request, user) 

        # 4. SET TANDA USER BARU
        # Disimpan di session agar bisa dibaca di dashboard
        request.session['is_new_user'] = True 

        messages.success(request, "Pendaftaran berhasil! Selamat datang.")
        
        # 5. LANGSUNG KE DASHBOARD
        return redirect('dashboard') 
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

            
            request.session['is_new_user'] = True
            
            messages.success(request, "Login berhasil!")

            return redirect('dashboard')
        else:
            pass 
            
    return render(request, 'main/login.html', {})


# --- UPDATE FUNGSI DASHBOARD ---
@login_required # Gunakan decorator ini agar lebih aman
def dashboard(request):
    # (Pengecekan manual 'if not request.user...' bisa dihapus jika pakai decorator)

    try:
        profile = Profile.objects.get(user=request.user)
        kelas = profile.kelas
    except Profile.DoesNotExist:
        profile = None
        kelas = "-"

# --- Bagian Setelah Login (Memerlukan autentikasi) ---

@login_required 
def dashboard(request):
    """View untuk halaman dashboard. Mengambil data foto dan kelas."""
    # Ambil atau buat objek Profile. Ini memastikan setiap user memiliki profile.
    profile, created = Profile.objects.get_or_create(user=request.user)


    # LOGIKA ONBOARDING POP-UP
    show_onboarding = False
    if request.session.get('is_new_user'):
        show_onboarding = True
        # Hapus tanda agar pop-up tidak muncul terus menerus saat refresh
        del request.session['is_new_user']

    context = {
        'username': request.user.username,

        'profile' : profile,
        'show_onboarding': show_onboarding, # Kirim ke HTML
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

    messages.success(request, "Anda telah logout.")
    return redirect('home')

@login_required
def materi(request):
    profile = Profile.objects.get(user=request.user) # Gunakan .get jika yakin profile ada
    return render(request, "main/materi.html", {
        'username': request.user.username,
        'kelas': profile.kelas,
        'active': 'materi',
        'profile' : profile
    })

@login_required
def materi_bulat(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "main/materi_bulat.html", {
        'username': request.user.username,
        'kelas': profile.kelas,
        'active': 'materi',
        'profile' : profile
    })

@login_required
def materi_desimal(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "main/materi_desimal.html", {
        'username': request.user.username,
        'kelas': profile.kelas,
        'active': 'materi',
        'profile' : profile
    })
    
@login_required
def edit_profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid() and u_form.is_valid(): 
            u_form.save()
            p_form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('edit_profile')
    else:
        p_form = ProfileForm(instance=profile)
        u_form = UserForm(instance=request.user)

    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
        'p_form': p_form, 
        'u_form': u_form,
        'user_display_name': request.user.username 
    }
    return render(request, 'main/edit_profile.html', context)

@login_required  
def latihan(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
    }
    return render(request, 'main/latihan.html', context)

@login_required
def tentang(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
    }
    return render(request, 'main/tentang.html', context)

    return redirect('home')

