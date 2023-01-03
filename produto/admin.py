from django.contrib import admin
from .models import Produto,Variacao
from django_summernote.admin import SummernoteModelAdmin

# Graças ao TabularInline iremos poder editar as variações na página de produto, tudo na mesma página
class VariacaoInline(admin.TabularInline):
    model = Variacao
    readonly_fields = ('preco_promocional',)
    extra = 0

# Em inlines estou falando quais modelos iremos poder editar na página de produto junto com ele
class ProdutoAdmin(SummernoteModelAdmin):
    list_display = ['nome','get_preco_formatado','get_preco_promocional_formatado','tipo',]
    inlines = [
        VariacaoInline
    ]
    readonly_fields = ('preco_marketing_promocional',)
    summernote_fields = ('descricao','informacao_tecnica',)

admin.site.register(Produto,ProdutoAdmin)
admin.site.register(Variacao)
