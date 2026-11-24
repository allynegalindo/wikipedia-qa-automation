import pytest

from data.artigos import (
    ARTIGO_COM_INTERROGACAO,
    ARTIGO_COM_REDIRECIONAMENTO,
    ARTIGO_INEXISTENTE,
    ARTIGOS_PADRAO,
    PAGINA_DE_DESAMBIGUACAO,
)
from models.resumo import ErroApi

pytestmark = pytest.mark.api


@pytest.mark.parametrize(
    ("titulo_digitado", "titulo_esperado"),
    [
        ("brasil", "Brasil"),
        ("São_Paulo", "São Paulo"),
    ],
)
def test_titulo_digitado_e_normalizado(wikipedia_api, titulo_digitado, titulo_esperado):
    resumo = wikipedia_api.obter_resumo(titulo_digitado)

    assert resumo.titles.normalized == titulo_esperado


def test_redirecionamento_devolve_o_artigo_de_destino(wikipedia_api):
    resumo = wikipedia_api.obter_resumo(ARTIGO_COM_REDIRECIONAMENTO)

    assert resumo.title == "Python"


@pytest.mark.parametrize(
    ("titulo", "tipo_esperado"),
    [
        (ARTIGOS_PADRAO[0], "standard"),
        (PAGINA_DE_DESAMBIGUACAO, "disambiguation"),
    ],
)
def test_tipo_da_pagina_e_identificado(wikipedia_api, titulo, tipo_esperado):
    resumo = wikipedia_api.obter_resumo(titulo)

    assert resumo.type == tipo_esperado


def test_resumo_aponta_para_a_wikipedia_em_portugues(wikipedia_api):
    resumo = wikipedia_api.obter_resumo(ARTIGOS_PADRAO[0])

    assert resumo.lang == "pt"
    assert resumo.content_urls.desktop.page.host == "pt.wikipedia.org"


def test_titulo_com_interrogacao_e_encontrado(wikipedia_api):
    resposta = wikipedia_api.buscar_resumo(ARTIGO_COM_INTERROGACAO)

    assert resposta.status_code == 200


def test_artigo_inexistente_retorna_404(wikipedia_api):
    resposta = wikipedia_api.buscar_resumo(ARTIGO_INEXISTENTE)

    assert resposta.status_code == 404
    assert ErroApi.model_validate(resposta.json()).status == 404
