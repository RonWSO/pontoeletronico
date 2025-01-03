from django import forms
from . import models
from django.contrib.auth.forms import AuthenticationForm

class CreateEmpresa(forms.ModelForm):
    class Meta:
        model = models.Empresa
        fields = ['nome','endereco','telefone']

        widgets = {
            'nome':forms.TextInput(attrs={'class':'form-control','name':'nome_empresa', 'placeholder':'Digite nome da Empresa'}),
            'endereco':forms.TextInput(attrs={'class':'form-control','name':'nome_empresa', 'placeholder':'Digite endereço da Empresa'}),
            'telefone':forms.TextInput(attrs={'class':'form-control','name':'nome_empresa', 'placeholder':'Digite telefone da Empresa'})
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Usuário',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Senha',
    }))