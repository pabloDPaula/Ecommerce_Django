from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.ListaProdutos.as_view(),name="listaProdutos"),
    path('<slug>',views.DetalheProdutos.as_view(),name="detalheProdutos"),
    path('adicionaraocarinho/', views.AdicionarAoCarinho.as_view(), name="adicionarAoCarinho"),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name="removerDoCarrinho"),
    path('carrinho/', views.Carrinho.as_view(), name="carrinho"),
    path('busca/', views.Busca.as_view(), name="busca"),
    path('categoria/<str:categoria>',views.ListaProdutosCategoria.as_view(),name="listaProdutos_categoria"),
    path('categoria/<str:categoria>/<str:subcategoria>',views.ListaProdutosSubcategoria.as_view(),name="listaProdutos_subcategoria")
]