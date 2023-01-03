$(document).ready(function() {
    $("#id_cep").blur(function(){
            var cep = $(this).val().replace(/\D/g, '');
             $.getJSON("https://viacep.com.br/ws/"+ cep +"/json/?callback=?", function(dados) {
                    if (!("erro" in dados)) {
                        //Atualiza os campos com os valores da consulta.
                        $("#id_endereco").val(dados.logradouro);
                        $("#id_complemento").val(dados.complemento);
                        $("#id_bairro").val(dados.bairro);
                        $("#id_cidade").val(dados.localidade);
                        $("#id_estado").val(dados.uf);
                        //Vamos incluir para que o Número seja focado automaticamente
                        //melhorando a experiência do usuário
                        $("#id_numero").focus();
                    } //end if.
                    else {
                        //CEP pesquisado não foi encontrado.
                        alert("CEP não encontrado.");
                    }
             });
    });
});