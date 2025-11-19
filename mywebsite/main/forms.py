from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['kelas', 'foto']

        widgets = {
            'kelas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan kelas'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan username baru'
            })
        }
