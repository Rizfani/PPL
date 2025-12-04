from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User  
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile  
from .forms import ProfileForm, UserForm
from django.db.models import Sum, Avg
from .models import Profile, Nilai, Feedback
from .models import Kuis, ButirSoal, StatusMateri, Nilai
from .models import RiwayatSimulasi
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404 # <-- Tambah get_object_or_404
from .models import Kuis, ButirSoal, Nilai

# --- HALAMAN DEPAN ---
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "main/home.html")

# --- REGISTER (DAFTAR) ---
def register(request):
    # Jika sudah login, lempar ke dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        # Ambil data dari form HTML manual
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        kelas = request.POST.get('kelas')

        # 1. Cek apakah username sudah ada
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan, silakan pilih yang lain.")
            return redirect('register')

        # 2. Buat User Baru
        # create_user otomatis meng-hash password (aman)
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # 3. Buat Profile (Simpan Kelas)
            Profile.objects.create(user=user, kelas=kelas)

            # 4. BERHASIL -> ARAHKAN KE LOGIN (Bukan Dashboard)
            messages.success(request, "Pendaftaran berhasil! Silakan login dengan akun baru Anda.")
            return redirect('login')

        except Exception as e:
            # Jaga-jaga jika ada error database
            messages.error(request, f"Terjadi kesalahan saat mendaftar: {e}")
            return redirect('register')

    return render(request, "main/register.html")

# --- LOGIN (MASUK) ---
def login(request):
    # Jika sudah login, lempar ke dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Cek kecocokan username & password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login Sukses
            auth_login(request, user)
            
            # (Opsional) Set tanda user baru untuk pop-up jika perlu
            # request.session['is_new_user'] = True 
            
            messages.success(request, f"Selamat datang kembali, {username}!")
            return redirect('dashboard')
        else:
            # Login Gagal
            messages.error(request, "Username atau password salah. Silakan coba lagi.")
            return redirect('login')

    return render(request, "main/login.html")

# --- DASHBOARD ---
@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # --- LOGIKA 1: PROGRES SAYA (STATISTIK) ---
    # Ambil nilai terakhir user untuk setiap kategori
    nilai_bulat_obj = Nilai.objects.filter(user=request.user, kategori='bulat').last()
    nilai_desimal_obj = Nilai.objects.filter(user=request.user, kategori='desimal').last()

    # Jika belum ada nilai, set ke 0
    skor_bulat = nilai_bulat_obj.skor if nilai_bulat_obj else 0
    skor_desimal = nilai_desimal_obj.skor if nilai_desimal_obj else 0
    
    # Hitung rata-rata total (untuk level user)
    rata_rata = (skor_bulat + skor_desimal) / 2

    # --- LOGIKA 2: PAPAN PERINGKAT (LEADERBOARD) ---
    # Mengambil 5 user dengan total skor tertinggi
    leaderboard = User.objects.annotate(
        total_skor=Sum('nilai__skor')
    ).order_by('-total_skor')[:5]

    # --- LOGIKA 3: FEEDBACK ---
    if request.method == "POST":
        print(f"DEBUG: Ada POST request! Data: {request.POST}") # <-- Cek Terminal nanti

        if 'btn_feedback' in request.POST:
            print("DEBUG: Tombol Feedback Ditekan!") # <-- Cek Terminal nanti
            pesan = request.POST.get('pesan')
            if pesan:
                Feedback.objects.create(user=request.user, isi_pesan=pesan)
                messages.success(request, "Masukan berhasil dikirim!")
                return redirect('dashboard')

    # --- LOGIKA 4: ONBOARDING (YANG LAMA) ---
    show_onboarding = False
    if request.session.get('is_new_user'):
        show_onboarding = True
        del request.session['is_new_user']

    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
        'show_onboarding': show_onboarding,
        
        # Data Baru
        'skor_bulat': skor_bulat,
        'skor_desimal': skor_desimal,
        'rata_rata': rata_rata,
        'leaderboard': leaderboard,


        'profile' : profile,
        'show_onboarding': show_onboarding 

    }
    return render(request, 'main/dashboard.html', context)

# --- LOGOUT ---
def logout_view(request):
    logout(request)
    messages.success(request, "Anda telah logout.")
    return redirect('home')

# --- HALAMAN LAINNYA (MATERI, DLL) ---
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
    
    if request.method == "POST":
        try:
            # Ambil input
            s1 = request.POST.get('angka1')
            s2 = request.POST.get('angka2')
            a1 = float(s1)
            a2 = float(s2)
            jawaban = request.POST.get('pilihan')

            # Logika Perbandingan
            if a1 > a2:
                kunci = "A"
                tanda = ">"
                besar = s1
            elif a2 > a1:
                kunci = "B"
                tanda = "<"
                besar = s2
            else:
                kunci = "Sama"
                tanda = "="

            # Logika Penjelasan (Analisis Digit)
            analisis = "Angka sama persis."
            max_len = max(len(s1), len(s2))
            s1_pad = s1.ljust(max_len, '0')
            s2_pad = s2.ljust(max_len, '0')

            for i in range(max_len):
                if s1_pad[i] != s2_pad[i]:
                    koma_index = s1.find('.')
                    jarak = i - koma_index
                    nama_posisi = "angka depan"
                    if jarak == 1: nama_posisi = "persepuluhan"
                    elif jarak == 2: nama_posisi = "perseratusan"
                    elif jarak == 3: nama_posisi = "perseribuan"
                    
                    analisis = f"Lihat posisi <b>{nama_posisi}</b>: Angka <b>{s1_pad[i]}</b> vs <b>{s2_pad[i]}</b>. Karena itu, {besar} lebih besar."
                    break

            is_correct = (jawaban == kunci)
            
            # Simpan Riwayat (Opsional, aktifkan jika perlu)
            # RiwayatSimulasi.objects.create(...)

            # 👇 PERUBAHAN UTAMA: Return JSON, bukan render HTML
            return JsonResponse({
                'status': 'success',
                'benar': is_correct,
                'text_hasil': f"Hasil: {a1} {tanda} {a2}",
                'detail_penjelasan': analisis
            })

        except ValueError:
            return JsonResponse({'status': 'error', 'msg': 'Input tidak valid'})

    # GET Request (Buka Halaman Pertama Kali)
    return render(request, "main/materi_desimal.html", {
        'username': request.user.username,
        'kelas': profile.kelas,
        'active': 'materi',
        'profile' : profile
    })
    
@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

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
    profile, created = Profile.objects.get_or_create(user=request.user)
    status, created = StatusMateri.objects.get_or_create(user=request.user)
    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
        'status': status,
    }
    return render(request, 'main/latihan.html', context)

@login_required
def tandai_selesai(request, kategori):
    status, created = StatusMateri.objects.get_or_create(user=request.user)
    
    if kategori == 'bulat':
        status.materi_bulat_selesai = True
    elif kategori == 'desimal':
        status.materi_desimal_selesai = True
    
    status.save()
    messages.success(request, f"Hebat! Materi {kategori} selesai. Latihan soal terbuka!")
    return redirect('latihan')

@login_required
def kerjakan_kuis(request, kuis_id):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    kuis = get_object_or_404(Kuis, id=kuis_id)
    soal_list = ButirSoal.objects.filter(kuis=kuis)

    # Variabel untuk menampung hasil (defaultnya Kosong/None)
    hasil_data = None 

    if request.method == 'POST':
        skor_benar = 0
        total_soal = soal_list.count()

        # Cek Jawaban
        for soal in soal_list:
            jawaban_user = request.POST.get(f'soal_{soal.id}')
            if jawaban_user == soal.kunci:
                skor_benar += 1
        
        # Hitung Nilai
        nilai_akhir = 0
        if total_soal > 0:
            nilai_akhir = int((skor_benar / total_soal) * 100)
        
        # Simpan ke Database
        Nilai.objects.update_or_create(
            user=request.user,
            kategori=kuis.kategori_materi,
            defaults={'skor': nilai_akhir}
        )

        # --- BAGIAN PENTING: JANGAN REDIRECT ---
        # Kita siapkan datanya untuk ditampilkan langsung di HTML
        hasil_data = {
            'skor': nilai_akhir,
            'benar': skor_benar,
            'total': total_soal,
            'lulus': nilai_akhir >= kuis.minimal_nilai,
            'kkm': kuis.minimal_nilai
        }

    return render(request, 'main/quiz_interface.html', {
        'kuis': kuis, 
        'soal_list': soal_list,
        'hasil_data': hasil_data, # <-- Kita kirim data hasil ke sini
        
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile
    })
# --- FUNGSI LATIHAN BULAT (BARU) ---
@login_required
def latihan_bulat(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
    }
    return render(request, 'main/latihan_bulat.html', context)

# --- FUNGSI LATIHAN DESIMAL (BARU) ---
@login_required
def latihan_desimal(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
    }
    return render(request, 'main/latihan_desimal.html', context)

@login_required
def tentang(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'username': request.user.username,
        'kelas': profile.kelas,
        'profile': profile,
    }
    return render(request, 'main/tentang.html', context)