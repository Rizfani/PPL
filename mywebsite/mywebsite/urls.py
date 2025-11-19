from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import views dari aplikasi 'main' HANYA jika view tersebut digunakan di sini
# Karena Anda menggunakan include('main.urls'), view dashboard, login, dll., 
# Seharusnya didefinisikan di main/urls.py.
# Kita hanya menyisakan path 'edit_profile' di sini karena Anda meletakkannya di sini.
from main import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Semua URL aplikasi 'main' (home, dashboard, login, logout, dll.)
    path('', include('main.urls')),
    
    # URL Edit Profile (dibiarkan di sini sesuai permintaan Anda, tetapi idealnya di main/urls.py)
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]

# --- PENTING: KONFIGURASI UNTUK MEDIA FILES (FOTO PROFIL) ---
# Tambahkan ini agar foto yang di-upload bisa tampil saat development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)