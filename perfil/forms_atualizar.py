from django import forms
from django.contrib.auth.models import User
from . import models


# Usuario para acessar nosso site
class PerfilForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['cpf'].widget.attrs.update({'class':"mask-cpf"})
        
    class Meta:
        # Estamos pegando todos os campos do model menos o 'usuario' para esse nosso form ( formulario )
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


# Usuario do django ( incluindo permissões, data de login e _todo resto )
class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    def __init__(self, usuario=None, *args, **kargs):
        super().__init__(*args, **kargs)
        self.usuario = usuario
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')

    # Por esse método iremos validar nossos campos para verificar se existe algum erro
    def clean(self, *args, **kargs):
        # data pega os dados 'crus' do formulario
        data = self.data
        # cleaned pega os dados 'limpos' do formulario
        cleaned = self.cleaned_data
        validation_erros_messages = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        erro_msg_user_exists = 'Usuário já existe'
        erro_msg_email_exists = 'Email já existe'

        # Usuario logado: Editar campos
        if usuario_db:
            if usuario_data != usuario_db.username:
                validation_erros_messages['username'] = erro_msg_user_exists

        if email_db:
            if email_data != email_db.email:
                validation_erros_messages['email'] = erro_msg_email_exists

        if validation_erros_messages:
            raise (
                forms.ValidationError(validation_erros_messages)
            )
