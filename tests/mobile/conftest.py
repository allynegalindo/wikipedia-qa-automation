import os

import allure
import httpx
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from screens.artigo_screen import ArtigoScreen
from screens.home_screen import HomeScreen
from screens.onboarding_screen import OnboardingScreen
from screens.pesquisa_screen import PesquisaScreen
from utils.relatorio import anexar_print, teste_falhou

PACOTE_DO_APP = "org.wikipedia"


def _appium_esta_rodando(url):
    try:
        return httpx.get(f"{url}/status", timeout=3).status_code == 200
    except httpx.HTTPError:
        return False


@pytest.fixture(scope="session")
def driver(settings):
    """Abre uma sessão do Appium por execução, com o app instalado do zero.

    Criar a sessão leva vários segundos, por isso ela é compartilhada.
    As dicas de primeiro uso são resolvidas uma vez aqui, e cada teste
    recomeça da tela inicial pela fixture app_na_home.
    """
    if not _appium_esta_rodando(settings.appium_url):
        mensagem = f"Appium não está rodando em {settings.appium_url}. Veja o README para subir o emulador e o Appium."
        # Na pipeline (o GitHub Actions define CI=true), pular esconderia um problema: lá, falha.
        if os.getenv("CI"):
            pytest.fail(mensagem)
        pytest.skip(mensagem)

    opcoes = UiAutomator2Options()
    opcoes.app = settings.caminho_apk
    opcoes.app_package = PACOTE_DO_APP
    opcoes.app_activity = "org.wikipedia.main.MainActivity"
    opcoes.language = "pt"
    opcoes.locale = "BR"
    opcoes.no_reset = False
    opcoes.auto_grant_permissions = True
    opcoes.new_command_timeout = 120
    opcoes.set_capability("appium:uiautomator2ServerLaunchTimeout", 120000)

    driver = webdriver.Remote(settings.appium_url, options=opcoes)
    try:
        # Dicas que o app mostra só no primeiro uso: resolvidas uma vez, aqui.
        OnboardingScreen(driver).concluir()
        HomeScreen(driver).dispensar_sugestao_do_widget()
    except Exception:
        # Sem isto, uma falha na preparação não deixaria nenhuma evidência no relatório.
        anexar_print(driver.get_screenshot_as_png(), "Tela quando a preparação do app falhou")
        allure.attach(driver.page_source, name="Elementos da tela", attachment_type=allure.attachment_type.XML)
        driver.quit()
        raise
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def print_em_caso_de_falha(request, driver):
    yield
    if teste_falhou(request):
        anexar_print(driver.get_screenshot_as_png())


@pytest.fixture
def app_na_home(driver):
    """Reinicia o app antes de cada teste, para que um teste não dependa de onde o outro parou."""
    driver.terminate_app(PACOTE_DO_APP)
    driver.activate_app(PACOTE_DO_APP)
    home = HomeScreen(driver)
    assert home.esta_aberta(), "O app não abriu na tela inicial"
    return home


@pytest.fixture
def pesquisa_screen(driver):
    return PesquisaScreen(driver)


@pytest.fixture
def artigo_screen(driver):
    return ArtigoScreen(driver)
