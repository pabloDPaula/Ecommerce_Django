from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.validacpf import valida_cpf

class Perfil(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='Usuário')
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14,unique=True)
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30,blank=True,null=True)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.usuario}'

    def clean(self):
        perfil_cpf = Perfil.objects.filter(cpf=self.cpf).first()

        # Dicionário de erros dos campos, exemplo: 'idade' = 'Idade inválida'
        error_message = {}
        if not valida_cpf(self.cpf):
            error_message['cpf'] = 'Digite um CPF válido'

        # Verifica se existe um perfil com aquele cpf digitado e se chave primaria desse perfil encontrado
        # é diferente da nossa, ou seja, não é nosso cpf que estamos atualizando
        if perfil_cpf and self.pk != perfil_cpf.pk:
            error_message['cpf'] = 'Este CPF já existe'

        # Pega o cep sem o símbolo - da máscara que eu coloquei no campo
        cep = self.cep.replace('-','')

        # Expresão regular, se digitar algo diferente de 0 a 9 no cep, guarda a mensagem de erro no dicionário
        if re.search(r'[^0-9]',cep) or len(cep) < 8:
            error_message['cep'] = 'CEP inválido, digite os 8 dígitos do CEP'

        # Pega o dicionário com os campos e seus erros e lança ( raise ) para a página
        if error_message:
            raise ValidationError(error_message)


    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
