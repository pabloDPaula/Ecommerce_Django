def formata_preco(valor):
    return f'R$ {valor:.2f}'.replace('.',',')

def carrinho_quantidade_total(carrinho):
    # Guarda em uma lista a quantidade, uma em cada linha e depois usa a função sum() para somar a lista toda
    return sum([item['quantidade'] for item in carrinho.values()])

def carrinho_valor_total(carrinho):
    return sum([item['preco_quantitativo_promocional'] for item in carrinho.values()])