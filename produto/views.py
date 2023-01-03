from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Produto, Variacao
from perfil.models import Perfil
from django.db.models import Q


class ListaProdutos(ListView):
    model = Produto
    paginate_by = 10
    template_name = 'produto/lista.html'
    # Dentro da página lista.html terá um contexto com o nome produto
    # iremos pegar tudo relacionado a produto dentro desse contexto
    context_object_name = 'produtos'


class DetalheProdutos(DetailView):
    model = Produto
    template_name = 'produto/detalhes.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarinho(View):
    def get(self, *args, **kwargs):
        # HTTP_REFERER - Podemos pegar a url anterior a essa nova por ele. Ex: DetalheProdutos era a URL antiga
        http_referer = self.request.META.get('HTTP_REFERER', reverse('listaProdutos'))
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'ERRO, Produto não existe')
            return redirect(http_referer)
        variacao = get_object_or_404(Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(self.request, 'Produto esgotado!!')
            return redirect(http_referer)

        # Cada usuário logado terá sua própria sessão
        # Sessão é tipo um dicionário e agora estamos buscando a chave 'carrinho'
        if not self.request.session.get('carrinho'):
            # Estamos criando a chave carrinho e salvando na sessão do usuário
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        # Variação existe na chave 'carrinho'
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(self.request,
                                 f'Estoque insuficiente para {quantidade_carrinho}x no produto {produto_nome}.'
                                 f'Adicionamos {variacao_estoque}x no seu carrinho')
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = round(preco_unitario * quantidade_carrinho)
            carrinho[variacao_id]['preco_quantitativo_promocional'] = round(
                preco_unitario_promocional * quantidade_carrinho)
        # Variação NÃO existe na chave 'carrinho'
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_id': variacao_id,
                'variacao_nome': variacao_nome,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem
            }

        self.request.session.save()
        messages.success(self.request, f'{produto_nome} {variacao_nome} foi adicionado ao seu carrinho.')
        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('listaProdutos'))
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]
        messages.success(self.request, f'Produto {carrinho["produto_nome"]} removido do seu carrinho')

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            contexto = {
                'user': None,
                'carrinho': self.request.session.get('carrinho')
            }
        else:
            perfil = Perfil.objects.filter(usuario=self.request.user).exists()

            if not perfil:
                messages.error(self.request, 'Usuário sem perfil, atualize seus dados!!')
                return redirect('atualizar')
            contexto = {
                'user': self.request.user,
                'carrinho': self.request.session.get('carrinho')
            }
        return render(self.request, 'produto/carrinho.html', contexto)


class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        palavra = self.request.GET.get('palavra') or self.request.session['palavra']
        qs = super().get_queryset()

        if not palavra:
            return qs

        self.request.session['palavra'] = palavra

        qs = qs.filter(
            Q(nome__icontains=palavra)
        )
        self.request.session.save()
        return qs


class ListaProdutosCategoria(ListaProdutos):
    template_name = 'produto/categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria',None)
        if not categoria:
            return qs
        qs = qs.filter(categoria__icontains=categoria)
        return qs

class ListaProdutosSubcategoria(ListaProdutosCategoria):

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria',None)
        subcategoria = self.kwargs.get('subcategoria', None)
        if not subcategoria:
            return qs
        qs = qs.filter(categoria__icontains=categoria, nome__icontains=subcategoria)
        return qs