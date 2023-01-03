from django import forms
from django.contrib.auth.models import User
from . import models


# Usuario para acessar nosso site
class PerfilForm(forms.ModelForm):
    class Meta:
        # Estamos pegando todos os campos do model menos o 'usuario' para esse nosso form ( formulario )
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


# Usuario do django ( incluindo permissões, data de login e _todo resto )
class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirmar senha'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    # Por esse método iremos validar nossos campos para verificar se existe algum erro
    def clean(self, *args, **kargs):
        # data pega os dados 'crus' do formulario
        data = self.data
        # cleaned pega os dados 'limpos' do formulario
        cleaned = self.cleaned_data
        validation_erros_messages = {}

        usuario_data = cleaned.get('username')
        senha_data = cleaned.get('password')
        confirmar_senha_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        erro_msg_user_exists = 'Usuário já existe'
        erro_msg_email_exists = 'Email já existe'
        erro_msg_password_match = 'As senhas digitadas são diferentes'
        erro_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        erro_msg_required_field = 'Este campo é obrigatório'

        # Usuario logado: Editar campos
        if usuario_db:
            validation_erros_messages['username'] = erro_msg_user_exists

        if email_db:
            validation_erros_messages['email'] = erro_msg_email_exists

        if not senha_data:
            validation_erros_messages['password'] = erro_msg_required_field

        if not senha_data:
            validation_erros_messages['password2'] = erro_msg_required_field

        if senha_data != confirmar_senha_data:
            validation_erros_messages['password'] = erro_msg_password_match
            validation_erros_messages['password2'] = erro_msg_password_match
        if len(senha_data) < 6:
            validation_erros_messages['password'] = erro_msg_password_short

        if validation_erros_messages:
            raise (
                forms.ValidationError(validation_erros_messages)
            )
