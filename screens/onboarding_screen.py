import allure
from appium.webdriver.common.appiumby import AppiumBy

from screens.base_screen import BaseScreen


class OnboardingScreen(BaseScreen):
    """Telas de boas-vindas exibidas na primeira abertura do app."""

    BOTAO_AVANCAR = (AppiumBy.ACCESSIBILITY_ID, "Avançar")
    BOTAO_PULAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Pular")')

    @allure.step("Mobile: concluir o onboarding")
    def concluir(self):
        # Três telas com "Avançar" (boas-vindas, privacidade e idiomas),
        # e a última, de tópicos de interesse, com "Pular".
        while not self.esta_visivel(self.BOTAO_PULAR, tempo=2):
            self.tocar(self.BOTAO_AVANCAR)
        self.tocar(self.BOTAO_PULAR)
