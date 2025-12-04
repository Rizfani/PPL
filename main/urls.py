from django.urls import path
from . import views

urlpatterns = [
    # --- Main Pages ---
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.edit_profile_view, name='edit_profile'),
    path('tentang/', views.tentang, name='tentang'),

    # --- Menu Materi Utama ---
    path('materi/', views.materi, name='materi'),

    # --- MATERI BILANGAN DESIMAL (Masih 1 File) ---
    path('materi/bilangan-desimal/', views.materi_desimal, name='materi_desimal'),

    # --- MATERI BILANGAN BULAT (DIPISAH-PISAH) ---
    # Redirect link lama ke halaman pertama (pengertian)
    path('materi/bilangan-bulat/', views.bulat_pengertian, name='materi_bulat'), 
    
    path('materi/bulat/pengertian/', views.bulat_pengertian, name='bulat_pengertian'),
    path('materi/bulat/membandingkan/', views.bulat_membandingkan, name='bulat_membandingkan'),
    path('materi/bulat/penjumlahan/', views.bulat_penjumlahan, name='bulat_penjumlahan'),
    path('materi/bulat/pengurangan/', views.bulat_pengurangan, name='bulat_pengurangan'),
    path('materi/bulat/perkalian/', views.bulat_perkalian, name='bulat_perkalian'),
    path('materi/bulat/pembagian/', views.bulat_pembagian, name='bulat_pembagian'),
    path('materi/bulat/latihan/', views.bulat_latihan, name='bulat_latihan'),
   

    # --- Latihan & Kuis (Logic) ---
    path('latihan/', views.latihan, name='latihan'),
    path('tandai-selesai/<str:kategori>/', views.tandai_selesai, name='tandai_selesai'),
    path('kuis/<int:kuis_id>/', views.kerjakan_kuis, name='kerjakan_kuis'),
]