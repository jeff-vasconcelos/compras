from django import forms
from core.models.parametros_models import Parametro


class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = ['periodo', 'curva_a', 'curva_b', 'curva_c', 'curva_d', 'curva_e']

        widgets = {
            'periodo': forms.TextInput(attrs={'class': 'form-control'}),
            'curva_a': forms.TextInput(attrs={'class': 'form-control'}),
            'curva_b': forms.TextInput(attrs={'class': 'form-control'}),
            'curva_c': forms.TextInput(attrs={'class': 'form-control'}),
            'curva_d': forms.TextInput(attrs={'class': 'form-control'}),
            'curva_e': forms.TextInput(attrs={'class': 'form-control'}),
        }