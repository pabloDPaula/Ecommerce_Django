from django.shortcuts import render,redirect,reverse
from django.views.generic import ListView,DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from utils import utils
from .models import Pedido,ItemPedido

class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('listaProdutos')
        return super().dispatch(*args, **kwargs)

class Pagar(DispatchLoginRequired,DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset()
        # Busca o pedido no banco de dados onde a primary key é a que está na URL e o dono do pedido é o USUARIO LOGADO
        # Logo se vc colocar na url uma primary key de um pedido que NÃO é seu, ele derá erro
        qs = qs.filter(usuario=self.request.user)
        print(qs)
        return qs


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho')


        if not self.request.user.is_authenticated:
            messages.error(self.request,'Você precisa fazer login!')
            return redirect('login')

        if not carrinho:
            messages.error(self.request,'Carrinho vazio!')
            return redirect('listaProdutos')

        # Carrinho é um dicionário com chave e valor
        # chave = variacao_id e valor = dicionário com informações sobre o produto
        carrinho_variacao_id = [v for v in carrinho.keys()]

        variacoes_db = list( Variacao.objects.select_related('produto').filter(id__in=carrinho_variacao_id) )

        error_msg_estoque = ''

        for variacao in variacoes_db:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unitario = carrinho[vid]['preco_unitario']
            preco_unitario_promocional = carrinho[vid]['preco_unitario_promocional']

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_unitario'] = estoque * preco_unitario
                carrinho[vid]['preco_unitario_promocional'] = estoque * preco_unitario_promocional
                error_msg_estoque = 'Estoque insuficiente para alguns produtos em seu carrinho. ' \
                                    'Reduzimos a quantidade desses produtos. '

                if error_msg_estoque:
                    messages.error(self.request,error_msg_estoque)
                    self.request.session.save()
                    return redirect('carrinho')

        qtd_total_carrinho = utils.carrinho_quantidade_total(carrinho)
        valor_total_carrinho = utils.carrinho_valor_total(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status="C"
        )
        pedido.save()

        ItemPedido.objects.bulk_create(
           [
               ItemPedido(
                    pedido=pedido,
                    nome_produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_unitario_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
               ) for v in carrinho.values()
           ]
        )

        del self.request.session['carrinho']
        return redirect(reverse('pagar',kwargs={'pk':pedido.pk}))

class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhes')

class Lista(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Lista')