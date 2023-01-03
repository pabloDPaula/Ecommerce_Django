from django.template import Library
# Pasta utils tem arquivos .py com funções que serão uasadas no site_todo
from utils import utils

register = Library()

@register.filter
def formata_preco(valor):
    return utils.formata_preco(valor)

@register.filter
def parcela(valor):
    return utils.formata_preco(round(valor/10))

@register.filter
def carrinho_quantidade_total(carrinho):
    return utils.carrinho_quantidade_total(carrinho)

@register.filter
def carrinho_valor_total(carrinho):
    return utils.carrinho_valor_total(carrinho)
