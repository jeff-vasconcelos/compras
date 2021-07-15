from django import forms
from core.models.parametros_models import Email


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']

        widgets = {
            'periodo': forms.TextInput(attrs={'class': 'form-control'})
        }