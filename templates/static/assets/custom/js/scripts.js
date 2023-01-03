(function () {
    select_variacao = document.getElementById('select-variacoes');
    variation_preco = document.getElementById('variation-preco');
    variation_preco_promocional = document.getElementById('variation-preco-promocional');
    desconto_campo = document.getElementById('desconto');

    if (!select_variacao) {
        return;
    }

    if (!variation_preco) {
        return;
    }

    select_variacao.addEventListener('change', function () {
        preco = this.options[this.selectedIndex].getAttribute('data-preco');
        preco_promocional = this.options[this.selectedIndex].getAttribute('data-preco-promocional');
        desconto = this.options[this.selectedIndex].getAttribute('data-desconto');

        variation_preco.innerHTML = preco;
        desconto_campo.innerHTML = desconto+'% OFF';

        if (desconto) {
            variation_preco_promocional.innerHTML = preco_promocional;
        }
    })
})();


