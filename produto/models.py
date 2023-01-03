import os.path
from django.conf import settings
from django.db import models
from PIL import Image
from django.utils.text import slugify
from random import randint
from utils import utils

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    informacao_tecnica = models.TextField()
    imagem = models.ImageField(upload_to='produto/imagens/%Y/%m/',blank=True,null=True)
    categoria = models.CharField(
        max_length=16,
        choices=(
            ('smartphone','Smartphone'),
            ('hardware', 'Hardware'),
            ('periferico', 'Perifericos'),
            ('game', 'Games'),
            ('eletrodomestico', 'Eletrodomesticos'),
            ('tv', 'TV'),
        )
    )
    slug = models.SlugField(unique=True,blank=True,null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    desconto = models.PositiveIntegerField(default=0)
    preco_marketing_promocional = models.FloatField(default=0,verbose_name='Preço Promo')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V','Variável'),
            ('S','Simples'),
        )
    )

    def calcula_desconto(self,preco_marketing,desconto=0):
        preco_desconto = preco_marketing * (desconto/100)
        self.preco_marketing_promocional = round(preco_marketing - preco_desconto,2)

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promo'

    def save(self,*args,**kargs):
        # Calcula desconto
        self.calcula_desconto(self.preco_marketing, self.desconto)

        # Gera Slug
        random_number = randint(1,999)
        if not self.slug:
            slug = f'{slugify(self.nome)}-{random_number}'
            self.slug = slug

        super().save(*args,**kargs)

        # Diminui tamanho imagem
        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem.name, max_image_size)



    @staticmethod
    def resize_image(img_name,new_width=800):
        path_image = os.path.join(settings.MEDIA_ROOT,img_name)
        image_pil = Image.open(path_image)
        original_width,original_height = image_pil.size
        print('*'*50)
        print(path_image)
        if original_width < new_width:
            image_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_img = image_pil.resize((new_width,new_height),Image.ANTIALIAS)

        new_img.save(
            path_image,
            optimaze=True,
            quality=60
        )

        new_img.close()

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    # Quando deletar produto, irá deletar todas as suas variações também ( CASCADE )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50,blank=True,null=True)
    preco = models.FloatField()
    desconto = models.PositiveIntegerField(default=0)
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    def calcula_desconto(self,preco,desconto=0):
        preco_desconto = preco * (desconto/100)
        self.preco_promocional = round(preco - preco_desconto,2)

    def save(self,*args,**kargs):
        # Calcula desconto
        self.calcula_desconto(self.preco,self.desconto)
        super().save(*args,**kargs)

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'