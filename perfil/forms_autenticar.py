from django import forms
from django.contrib.auth.models import User
from . import models
from django.shortcuts import get_object_or_404


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome de usuário'}),
        label='Usuário'
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self, *args, **kargs):
        # cleaned pega os dados 'limpos' do formulario
        cleaned = self.cleaned_data
        validation_erros_messages = {}

        usuario_data = cleaned.get('username')
        senha_data = cleaned.get('password')

        # Verifica se realmente existe esse usuário no banco de dados
        # Depois pega esse usuário e verifica se a senha dele é realmente essa
        username_db = User.objects.filter(username=usuario_data).first()

        error_message_username_not_exists = 'Nome de usuário incorreto ou inexistente'
        error_message_password_not_exists = 'Senha incorreta ou inexistente'

        if not username_db:
            validation_erros_messages['username'] = error_message_username_not_exists
            validation_erros_messages['password'] = error_message_password_not_exists
        else:
            password_db = username_db.check_password(senha_data)
            print(password_db)
            if not password_db:
                validation_erros_messages['password'] = error_message_password_not_exists

        if validation_erros_messages:
            raise (
                forms.ValidationError(validation_erros_messages)
            )
