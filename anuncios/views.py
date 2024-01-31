from django.template.defaulttags import register
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Anuncio, TipoVeiculo, ModeloVeiculo
from datetime import date


@register.filter
def get_range(value):
    return range(value)


# Isso deve ir para todos os base_site.html
def get_filters_context(request):
    tipos = TipoVeiculo.objects.all()
    modelos = ModeloVeiculo.objects.all()

    tipo_selecionado = request.GET.get('tipo', 'Todos')
    marca_selecionado = request.GET.get('marca', 'Todos')
    modelo_selecionado = request.GET.get('modelo', 'Todos')

    if tipo_selecionado.isdigit(): tipo_selecionado = int(tipo_selecionado)
    if marca_selecionado.isdigit(): marca_selecionado = int(marca_selecionado)
    if modelo_selecionado.isdigit(): modelo_selecionado = int(modelo_selecionado)

    tipo_valores = list(tipos)

    if tipo_selecionado == 'Todos':
        marca_valores = []
        modelo_valores = []
    else:
        modelo_valores = [modelo for modelo in modelos if str(modelo.tipo_id) == str(tipo_selecionado)]
        marca_valores = list(set(modelo.marca for modelo in modelo_valores))

        if marca_selecionado:
            modelo_valores = [modelo for modelo in modelos if str(modelo.marca_id) == str(marca_selecionado)]
        else:
            modelo_valores = []

    ano_de_selecionado = request.GET.get('ano-de', 'Todos')
    if not ano_de_selecionado or ano_de_selecionado == 'Todos': ano_de_selecionado = 1950

    ano_atual = date.today().year

    ano_ate_selecionado = request.GET.get('ano-ate', 'Todos')
    if not ano_ate_selecionado or ano_ate_selecionado == 'Todos': ano_ate_selecionado = ano_atual

    anos = [ano for ano in reversed(range(1950, ano_atual + 1))]
    anos_de_valores = [str(ano) for ano in anos]
    anos_ate_valores = [str(ano) for ano in anos if int(ano) >= int(ano_de_selecionado)]

    pesquisa = request.GET.get('pesquisa', '')

    ordem_selecionado = request.GET.get('ordem', 'menor-ano')
    ordem_valores = [
        {'id': 'menor-ano', 'nome': 'Menor Ano'},
        {'id': 'maior-ano', 'nome': 'Maior Ano'},
        {'id': 'menor-valor', 'nome': 'Menor Valor'},
        {'id': 'maior-valor', 'nome': 'Maior Valor'},
    ]

    context = {
        'tipos': {'selecionado': tipo_selecionado, 'valores': tipo_valores},
        'marcas': {'selecionado': marca_selecionado, 'valores': marca_valores},
        'modelos': {'selecionado': modelo_selecionado, 'valores': modelo_valores},
        'anos_de': {'selecionado': ano_de_selecionado, 'valores': anos_de_valores},
        'anos_ate': {'selecionado': ano_ate_selecionado, 'valores': anos_ate_valores},
        'pesquisa': pesquisa,
        'ordem': {'selecionado': ordem_selecionado, 'valores': ordem_valores}
    }

    return context


def listar_anuncios(request):
    context = get_filters_context(request)

    tipo_selecionado = context['tipos']['selecionado']
    marca_selecionado = context['marcas']['selecionado']
    modelo_selecionado = context['modelos']['selecionado']
    ano_de_selecionado = context['anos_de']['selecionado']
    ano_ate_selecionado = context['anos_ate']['selecionado']
    pesquisa = context['pesquisa']
    ordem_selecionado = context['ordem']['selecionado']

    # Filtragem dos anuncios conforme os filtros
    anuncios = Anuncio.objects.all(
        ).select_related('marca').select_related('modelo').select_related('cor').select_related('vendedor')

    if tipo_selecionado != 'Todos':
        anuncios = [anuncio for anuncio in anuncios if anuncio.modelo.tipo_id == tipo_selecionado]
    if marca_selecionado != 'Todos':
        anuncios = [anuncio for anuncio in anuncios if anuncio.marca_id == marca_selecionado]
    if modelo_selecionado != 'Todos':
        anuncios = [anuncio for anuncio in anuncios if anuncio.modelo_id == modelo_selecionado]

    anuncios = [anuncio for anuncio in anuncios if int(ano_de_selecionado) <= anuncio.ano <= int(ano_ate_selecionado)]

    anuncios = [anuncio for anuncio in anuncios if pesquisa.lower() in str(anuncio).lower()]

    match ordem_selecionado:
        case 'menor-ano':
            anuncios = list(sorted(anuncios, key=lambda anuncio: anuncio.ano))
        case 'menor-valor':
            anuncios = list(sorted(anuncios, key=lambda anuncio: anuncio.valor))
        case 'maior-valor':
            anuncios = list(sorted(anuncios, key=lambda anuncio: anuncio.valor, reverse=True))
        case _:  # Padrão == 'maior-ano'
            anuncios = list(sorted(anuncios, key=lambda anuncio: anuncio.ano, reverse=True))

    context['anuncios'] = anuncios

    return render(request, 'lista_anuncios.html', context)


def ver_anuncio(request, anuncio_id: int):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)

    context = get_filters_context(request)
    context['anuncio'] = anuncio

    return render(request, 'ver_anuncio.html', context)


# Rota API -> Marcas que tem o Tipo
def pegar_marcas_tipo(request, tipo_id):
    # Retorna as Marcas que tem o Tipo

    if not tipo_id or tipo_id == 'Todos':
        return JsonResponse({'marcas': []})

    modelos = ModeloVeiculo.objects.all()

    modelos_tipo = modelos.filter(tipo=tipo_id)

    marcas = set(modelo.marca for modelo in modelos_tipo)
    marcas = [{'id': marca.id, 'nome': marca.nome} for marca in marcas]

    return JsonResponse({'marcas': marcas})


# Rota API -> Modelos que são da Marca e do Tipo
def pegar_modelos_marca(request, tipo_id, marca_id):
    # Retorna os Modelos da Marca que tem o Tipo

    if not tipo_id or tipo_id == 'Todos' or not marca_id or marca_id == 'Todos':
        return JsonResponse({'modelos': []})

    modelos = ModeloVeiculo.objects.all()

    modelos = modelos.filter(tipo=tipo_id, marca=marca_id)

    modelos = [{'id': modelo.id, 'nome': modelo.nome} for modelo in modelos]

    return JsonResponse({'modelos': modelos})
