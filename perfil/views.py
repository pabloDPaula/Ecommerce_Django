from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views import View
from django.http import HttpResponse
import copy
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.forms import ValidationError
from . import models
from . import forms_criar, forms_atualizar, forms_autenticar


class Criar(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:
            self.renderizar = redirect('atualizar')
        else:
            self.contexto = {
                'userform': forms_criar.UserForm(data=self.request.POST or None),
                'perfilform': forms_criar.PerfilForm(data=self.request.POST or None)
            }

            self.userform = self.contexto['userform']
            self.perfilform = self.contexto['perfilform']

            self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar

        password = self.userform.cleaned_data.get('password')
        print(self.request.POST)

        # Antes de salvarmos o usuario,senha e email, iremos usar o set_password para criptografar a senha
        usuario = self.userform.save(commit=False)
        usuario.set_password(password)
        usuario.save()

        perfil = self.perfilform.save(commit=False)
        perfil.usuario = usuario
        perfil.save()

        # Verifica se existe esse usuario e senha
        autentica = authenticate(
            self.request,
            username=usuario,
            password=password
        )
        # Se existir, faz login
        if autentica:
            login(self.request, user=usuario)

        messages.success(self.request, 'Seu cadastro foi realizado com sucesso')
        return redirect('atualizar')


class Atualizar(View):
    template_name = 'perfil/atualizar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        self.perfil = None

        if not self.request.user.is_authenticated:
            self.renderizar = redirect('criar')
        else:
            self.perfil = models.Perfil.objects.filter(usuario=self.request.user).first()
            self.contexto = {
                'userform': forms_atualizar.UserForm(data=self.request.POST or None, usuario=self.request.user,
                                                     instance=self.request.user),
                'perfilform': forms_atualizar.PerfilForm(data=self.request.POST or None, instance=self.perfil)
            }

            self.userform = self.contexto['userform']
            self.perfilform = self.contexto['perfilform']

            self.renderizar = render(self.request, self.template_name, self.contexto)

    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        firstname = self.userform.cleaned_data.get('first_name')
        lastname = self.userform.cleaned_data.get('last_name')

        usuario = get_object_or_404(models.User, username=self.request.user.username)
        usuario.username = username
        usuario.email = email
        usuario.first_name = firstname
        usuario.last_name = lastname

        if password:
            usuario.set_password(password)
        usuario.save()

        if not self.perfil:
            # Estamos pegando todos os dados do formulario mais um campo novo que não tem lá
            # Que é o usuario = usuario logado
            self.perfilform.cleaned_data['usuario'] = usuario
            perfil = models.Perfil(**self.perfilform.cleaned_data)
            perfil.save()
        else:
            # Pega todos os dados do formulário enviado e salva as alterações
            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            # Verifica se existe esse usuario e senha
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )
            # Se existir, faz login
            if autentica:
                login(self.request, user=usuario)

        # Quando atualiza a senha de um usuario, perdemos a sessão com tudo dentro
        # então estamos copiando ela na BasePerfil e criando uma nova sessão e colando tudo que tava lá para essa nova
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        messages.success(self.request, 'Seus dados foram alterados com sucesso')
        return redirect('atualizar')

    def get(self, *args, **kwargs):
        return self.renderizar


class Login(View):
    template_name = 'perfil/login.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'loginform': forms_autenticar.LoginForm(data=self.request.POST or None)
        }

        self.loginform = self.contexto['loginform']
        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):

        if not self.loginform.is_valid():
            return self.renderizar

        usuario = self.loginform.cleaned_data.get('username')
        senha = self.loginform.cleaned_data.get('password')

        usuario = authenticate(
            self.request,
            username=usuario,
            password=senha
        )

        login(self.request,user=usuario)
        return redirect('listaProdutos')


class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('listaProdutos')
