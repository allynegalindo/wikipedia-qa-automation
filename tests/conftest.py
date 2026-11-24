import pytest

from config.settings import carregar_settings
from services.wikipedia_api import WikipediaApi


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Guarda o resultado de cada fase do teste, para as fixtures saberem se ele falhou."""
    relatorio = yield
    setattr(item, f"resultado_{relatorio.when}", relatorio)
    return relatorio


@pytest.fixture(scope="session")
def settings():
    return carregar_settings()


@pytest.fixture(scope="session")
def wikipedia_api(settings):
    api = WikipediaApi(settings.api_base_url, settings.user_agent, settings.timeout)
    yield api
    api.fechar()
