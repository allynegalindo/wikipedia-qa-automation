import pytest

from pages.artigo_page import ArtigoPage
from pages.pagina_inicial import PaginaInicial
from utils.relatorio import anexar_print, teste_falhou


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, settings):
    """Complementa a configuração padrão do pytest-playwright para todos os testes Web."""
    return {**browser_context_args, "base_url": settings.web_base_url, "locale": "pt-BR"}


@pytest.fixture(autouse=True)
def print_em_caso_de_falha(request, page):
    yield
    if teste_falhou(request):
        # Só a área visível: em artigos longos, o print da página inteira passa de 30 s.
        anexar_print(page.screenshot())


@pytest.fixture
def artigo_page(page):
    return ArtigoPage(page)


@pytest.fixture
def pagina_inicial(page):
    return PaginaInicial(page)
