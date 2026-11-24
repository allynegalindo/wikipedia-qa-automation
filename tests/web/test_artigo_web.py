"""Testes da camada Web.

A API é a fonte da verdade: cada teste busca o dado esperado na API
e verifica se o site exibe a mesma informação, sem valores fixos no teste.
"""

import pytest
from playwright.sync_api import expect

from data.artigos import (
    ARTIGO_COM_REDIRECIONAMENTO,
    ARTIGO_INEXISTENTE,
    ARTIGOS_PADRAO,
    PAGINA_DE_DESAMBIGUACAO,
)

pytestmark = pytest.mark.web


@pytest.mark.parametrize("titulo", ARTIGOS_PADRAO)
def test_artigo_exibe_o_titulo_informado_pela_api(wikipedia_api, artigo_page, titulo):
    resumo = wikipedia_api.obter_resumo(titulo)

    artigo_page.abrir(titulo)

    expect(artigo_page.titulo).to_have_text(resumo.title)


def test_redirecionamento_exibe_o_artigo_de_destino_e_o_aviso(wikipedia_api, artigo_page):
    resumo = wikipedia_api.obter_resumo(ARTIGO_COM_REDIRECIONAMENTO)

    artigo_page.abrir(ARTIGO_COM_REDIRECIONAMENTO)

    expect(artigo_page.titulo).to_have_text(resumo.title)
    expect(artigo_page.aviso_redirecionamento).to_contain_text(ARTIGO_COM_REDIRECIONAMENTO)


def test_pagina_de_desambiguacao_e_identificada_no_site(wikipedia_api, artigo_page):
    resumo = wikipedia_api.obter_resumo(PAGINA_DE_DESAMBIGUACAO)

    artigo_page.abrir(PAGINA_DE_DESAMBIGUACAO)

    assert resumo.type == "disambiguation"
    expect(artigo_page.categorias).to_contain_text("Desambiguação")


def test_artigo_inexistente_exibe_aviso_no_site(wikipedia_api, artigo_page):
    resposta = wikipedia_api.buscar_resumo(ARTIGO_INEXISTENTE)

    artigo_page.abrir(ARTIGO_INEXISTENTE)

    assert resposta.status_code == 404
    expect(artigo_page.aviso_pagina_inexistente).to_be_visible()


def test_busca_pelo_titulo_leva_ao_artigo(wikipedia_api, pagina_inicial, artigo_page):
    resumo = wikipedia_api.obter_resumo(ARTIGOS_PADRAO[0])
    pagina_inicial.abrir()

    pagina_inicial.buscar(ARTIGOS_PADRAO[0])

    expect(artigo_page.titulo).to_have_text(resumo.title)
