async function selecionaFiltro( filtro ){
    var root = location.protocol + '//' + location.host + "/anuncios/filtros/";

    var filtroTipo = document.getElementById('filtro-tipo')
    var filtroMarca = document.getElementById('filtro-marca')
    var filtroModelo = document.getElementById('filtro-modelo')

    if (filtro == 'tipo') {
        var url = root + 'tipo/' + filtroTipo.value
        var response = await fetch(url).then(resposta => resposta.json());
        response = response.marcas

        $("#filtro-marca option").remove();
        var first_option1 = document.createElement("option");
        first_option1.value = "Todos";
        first_option1.text = "Selecione";
        filtroMarca.add(first_option1, filtroMarca.options[0]);

        $("#filtro-modelo option").remove();
        var first_option2 = document.createElement("option");
        first_option2.value = "Todos";
        first_option2.text = "Modelo";
        filtroModelo.add(first_option2, filtroModelo.options[0]);

        for (i = 0; i < response.length; i = i + 1) {
            var option = document.createElement("option");
            option.value = response[i].id;
            option.text = response[i].nome;
            filtroMarca.add(option, filtroMarca.options[i + 1]);
        }

    }
    else if (filtro == 'marca') {
        var url = root + 'tipo/' + filtroTipo.value + '/marca/' + filtroMarca.value
        var response = await fetch(url).then(response => response.json());
        response = response.modelos

        $("#filtro-modelo option").remove();

        var first_option = document.createElement("option");
        first_option.value = "Todos";
        first_option.text = "Selecione";
        filtroModelo.add(first_option, filtroModelo.options[0]);

        for (i = 0; i < response.length; i = i + 1) {
            var option = document.createElement("option");
            option.value = response[i].id;
            option.text = response[i].nome;
            filtroModelo.add(option, filtroModelo.options[i + 1]);
        }
    }
    else {
        return
    }
}

function selecionaAnoDe(){
    var anoDe = document.getElementById('ano-de').value
    var filtroAnoAte = document.getElementById('ano-ate')

    $("#ano-ate option").remove();

    var condicao = (anoDe == 'Todos');

    var first_option = document.createElement("option");
    first_option.value = "Todos";
    first_option.text = condicao ? "Até" : "Selecione";
    filtroAnoAte.add(first_option, filtroAnoAte.options[0]);

    if (condicao) { return };

    anoDe = parseInt(anoDe);
    var anoAtual = new Date().getFullYear();

    var length = anoAtual - anoDe + 1
    var anos = Array.from({ length }, (_, i) => anoDe + i).reverse();

    for (i = 0; i < anos.length; i = i + 1) {
        var option = document.createElement("option");
        option.value = anos[i];
        option.text = anos[i];
        filtroAnoAte.add(option, filtroAnoAte.options[i + 1]);
    }
}

function selecionaOrdem(){
    var ordemSelecionada = document.getElementById('ordem').value;  // maior/menor-ano/valor

    var url = location.href;

    if (url.includes('ordem')) {
        var index = url.indexOf('ordem');
        url = url.slice(0, index);
    }

    if (url.slice(-1) != '&') {
        url += '&';
    }

    url += 'ordem=' + ordemSelecionada;

    location.href = url
}
