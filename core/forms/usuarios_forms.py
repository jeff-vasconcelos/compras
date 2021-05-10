from django import forms
from django.contrib.auth.models import User
from core.models.usuarios_models import Usuario
from django.forms.widgets import ClearableFileInput


""" Form para usuários """
class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['tipo', 'imagem']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'imagem': ClearableFileInput(),
        }

class UsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

