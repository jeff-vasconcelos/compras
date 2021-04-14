from django import forms
from core.models import Empresa


""" Form para empresas """
class EmpresasForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome_fantasia', 'razao_social', 'cnpj', 'iestadual', 'resp_tec', 'resp_leg', 'telefone',
                  'email', 'ativo', 'endereco', 'cidade', 'bairro', 'numero', 'estado', 'cep']

        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'data-mask': '00.000.000/0000-00', 'class': 'form-control'}),
            'iestadual': forms.TextInput(attrs={'class': 'form-control'}),
            'resp_tec': forms.TextInput(attrs={'class': 'form-control'}),
            'resp_leg': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'data-mask': '(00)00000-0000', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'data-mask': '00000-000', 'class': 'form-control'})
        }