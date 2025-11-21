from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User  
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile  
# Pastikan nama form di forms.py Anda sesuai (UserForm atau ProfileUpdateForm?)
# Saya asumsikan namanya ProfileForm dan UserForm sesuai kode awal Anda
from .forms import ProfileForm, UserForm 

# --- HALAMAN DEPAN (LANDING PAGE) ---
def home(request):
    # Jika user sudah login, redirect ke dashboard agar tidak perlu login lagi
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "main/home.html")

# --- FUNGSI REGISTER (DAFTAR) ---
def register(request):
    # Jika user sudah login, tidak perlu daftar lagi
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        kelas = request.POST.get('kelas')

        # Cek apakah username sudah ada
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('register')

        # 1. Buat User Baru
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # 2. Simpan Profile (Kelas)
        Profile.objects.create(user=user, kelas=kelas)

        # 3. LOGIN OTOMATIS (Auto-Login)
        auth_login(request, user) 

        # 4. SET TANDA USER BARU (Untuk Pop-up Onboarding)
        request.session['is_new_user'] = True 

        messages.success(request, "Pendaftaran berhasil! Selamat datang.")
        
        # 5. LANGSUNG KE DASHBOARD
        return redirect('dashboard') 

    return render(request, "main/register.html")

# --- FUNGSI LOGIN ---
def login(request):
    # Jika user sudah login, redirect ke dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentikasi user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            
            # (Opsional: Hapus komentar di bawah ini jika ingin tes pop-up muncul tiap login)
            # request.session['is_new_user'] = True 

            messages.success(request, "Login berhasil!")
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah.")
            return redirect('login')

    return render(request, "main/login.html")

# --- FUNGSI LOGOUT ---
def logout_view(request):
    logout(request)
    messages.success(request, "Anda telah logout.")
    return redirect('home')

# --- FUNGSI DASHBOARD (PUSAT) ---
@login_required
def dashboard(request):
    # Ambil data profile user
    # get_or_create mencegah error jika user lama belum punya profile
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
        'show_onboarding': show_onboarding 
    }
    return render(request, "main/dashboard.html", context)

# --- FITUR EDIT PROFIL ---
@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        # request.FILES wajib ada untuk upload foto
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if p_form.is_valid() and u_form.is_valid(): 
            u_form.save()
            p_form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('edit_profile') # Tetap di halaman edit agar user bisa lihat hasilnya
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

# --- HALAMAN MATERI ---
@login_required
def materi(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "main/materi.html", {
        'username': request.user.username,
        'kelas': profile.kelas,
        'active': 'materi',
        'profile' : profile
    })

@login_required
def materi_bulat(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "main/materi_bulat.html", {
        'username': request.user.username,
        'kelas': profile.kelas,
        'active': 'materi',
        'profile' : profile
    })

@login_required
def materi_desimal(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "main/materi_desimal.html", {
        'username': request.user.username,
        'kelas': profile.kelas,
        'active': 'materi',
        'profile' : profile
    })

# --- HALAMAN LAINNYA ---
@login_required  
def latihan(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
    }
    return render(request, 'main/latihan.html', context)

@login_required
def tentang(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
    }
    return render(request, 'main/tentang.html', context)