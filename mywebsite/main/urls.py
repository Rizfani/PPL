from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/',views.login, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('materi/', views.materi, name='materi'),
    path('materi/bilangan-bulat/', views.materi_bulat, name='materi_bulat'),
    path('materi/bilangan-desimal/', views.materi_desimal, name='materi_desimal'),
    path('profile/', views.edit_profile_view, name='edit_profile'),
    path('latihan/', views.latihan, name='latihan'),
    path('tentang/', views.tentang, name='tentang'),

]
