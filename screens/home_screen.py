import allure
from appium.webdriver.common.appiumby import AppiumBy

from screens.base_screen import BaseScreen


class HomeScreen(BaseScreen):
    """Tela inicial, com a barra de navegação inferior."""

    ABA_PESQUISAR = (AppiumBy.ID, "org.wikipedia:id/nav_tab_search")
    FECHAR_PROMOCAO_DO_WIDGET = (AppiumBy.ACCESSIBILITY_ID, "Fechar")

    def esta_aberta(self):
        return self.esta_visivel(self.ABA_PESQUISAR)

    @allure.step("Mobile: abrir a pesquisa")
    def abrir_pesquisa(self):
        self.tocar(self.ABA_PESQUISAR)

    @allure.step("Mobile: dispensar a sugestão do widget de pesquisa")
    def dispensar_sugestao_do_widget(self):
        # Na primeira vez que a pesquisa é aberta, o app sugere instalar o widget.
        # O tempo até ela aparecer varia muito no emulador, por isso a espera é longa.
        # Isso é feito uma vez só, ao preparar a sessão, e não em cada teste.
        self.abrir_pesquisa()
        self.tocar_se_aparecer(self.FECHAR_PROMOCAO_DO_WIDGET, tempo=20)
