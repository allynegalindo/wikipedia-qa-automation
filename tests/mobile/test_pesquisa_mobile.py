"""Testes da camada Mobile (app Android da Wikipedia).

Assim como no Web, a API é a fonte da verdade: o resultado esperado
vem da API e o teste verifica se o app exibe a mesma informação.
"""

import pytest

from data.artigos import ARTIGOS_PADRAO, PAGINA_DE_DESAMBIGUACAO

pytestmark = pytest.mark.mobile


@pytest.mark.parametrize("titulo", [*ARTIGOS_PADRAO, PAGINA_DE_DESAMBIGUACAO])
def test_resultado_da_pesquisa_exibe_a_descricao_informada_pela_api(
    wikipedia_api, app_na_home, pesquisa_screen, titulo
):
    resumo = wikipedia_api.obter_resumo(titulo)
    app_na_home.abrir_pesquisa()

    pesquisa_screen.pesquisar(titulo)

    assert pesquisa_screen.descricao_do_resultado(resumo.title) == resumo.description


def test_tocar_no_resultado_abre_o_artigo(wikipedia_api, app_na_home, pesquisa_screen, artigo_screen):
    resumo = wikipedia_api.obter_resumo(ARTIGOS_PADRAO[0])
    app_na_home.abrir_pesquisa()
    pesquisa_screen.pesquisar(resumo.title)

    pesquisa_screen.abrir_resultado(resumo.title)

    assert artigo_screen.esta_aberto()
