from django.urls import path, include
from . import views
urlpatterns = [
    path('pagar/<int:pk>',views.Pagar.as_view(),name='pagar'),
    path('salvarpedido/',views.SalvarPedido.as_view(),name='salvarPedido'),
    path('lista/',views.Lista.as_view(),name='lista'),
    path('detalhe/<int:pk>',views.Detalhe.as_view(),name='detalhe'),
]