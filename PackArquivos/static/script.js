function rolarScrollSuave() {
    var tabelaContainer = document.querySelector('.table-container');
    var tabela = document.getElementById('tabela');
    var posicaoFinal = tabela.scrollHeight - tabelaContainer.clientHeight;

    // Aumentar a duração para 30 segundos (30000 ms)
    var duracao = 30000;
    var intervalo = 20; // Intervalo fixo de 20 ms para uma rolagem mais suave
    var passos = duracao / intervalo;
    var distanciaPorPasso = posicaoFinal / passos;
    var posicaoAtual = 0;

    var rolar = function () {
        if (posicaoAtual < posicaoFinal) {
            posicaoAtual += distanciaPorPasso;
            tabelaContainer.scrollTop = posicaoAtual;
            setTimeout(rolar, intervalo);
        } else {
            posicaoAtual = posicaoFinal;
            setTimeout(voltarAoTopo, 3000); // Espera 3 segundos antes de chamar a função para voltar ao topo
        }
    };

    var voltarAoTopo = function () {
        var posicaoInicial = tabelaContainer.scrollTop;
        var duracaoRetorno = 1000; // Tempo total do retorno ao topo em milissegundos
        var intervaloRetorno = 10; // Intervalo entre cada passo do retorno ao topo em milissegundos
        var passosRetorno = duracaoRetorno / intervaloRetorno;
        var distanciaPorPassoRetorno = posicaoInicial / passosRetorno;
        var posicaoAtualRetorno = posicaoInicial;

        var retorno = function () {
            if (posicaoAtualRetorno > 0) {
                posicaoAtualRetorno -= distanciaPorPassoRetorno;
                tabelaContainer.scrollTop = posicaoAtualRetorno;
                setTimeout(retorno, intervaloRetorno);
            } else {
                tabelaContainer.scrollTop = 0;
            }
        };

        retorno();
    };

    rolar();
}

window.onload = function () {
    setTimeout(rolarScrollSuave, 3000);
}

function recarregarPagina() {
    location.reload();
}

setTimeout(recarregarPagina, 3600000);
