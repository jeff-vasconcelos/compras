from django import forms
from api.models.fornecedor import Fornecedor


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['leadtime', 'ciclo_reposicao']

        widgets = {
            'leadtime': forms.TextInput(attrs={'class': 'form-control'}),
            'ciclo_reposicao': forms.TextInput(attrs={'class': 'form-control'}),
        }