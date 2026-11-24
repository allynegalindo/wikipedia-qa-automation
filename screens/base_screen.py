from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TEMPO_PADRAO = 20


class BaseScreen:
    """Ações comuns a todas as telas: esperar, tocar, digitar e ler texto.

    Toda interação espera o elemento ficar pronto. No emulador, a tela
    demora a responder, e agir antes disso gera testes instáveis.
    """

    def __init__(self, driver):
        self.driver = driver

    def _esperar(self, locator, tempo=TEMPO_PADRAO):
        return WebDriverWait(self.driver, tempo).until(EC.visibility_of_element_located(locator))

    def tocar(self, locator):
        self._esperar(locator).click()

    def digitar(self, locator, texto):
        self._esperar(locator).send_keys(texto)

    def ler_texto(self, locator):
        return self._esperar(locator).text

    def esta_visivel(self, locator, tempo=TEMPO_PADRAO):
        try:
            self._esperar(locator, tempo)
            return True
        except TimeoutException:
            return False

    def tocar_se_aparecer(self, locator, tempo=3):
        """Para pop-ups que às vezes aparecem e às vezes não."""
        if self.esta_visivel(locator, tempo):
            self.tocar(locator)
