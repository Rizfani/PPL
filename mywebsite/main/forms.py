from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    # Form ini akan secara otomatis menangani field 'foto' dan 'kelas'
    class Meta:
        model = Profile
        fields = ['foto', 'kelas']
        widgets = {
            # Menambahkan class form-control pada field kelas
            'kelas': forms.TextInput(attrs={'class': 'form-control'}),
        }