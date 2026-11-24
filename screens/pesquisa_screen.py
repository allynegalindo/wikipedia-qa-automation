import allure
from appium.webdriver.common.appiumby import AppiumBy

from screens.base_screen import BaseScreen

LISTA_DE_RESULTADOS = '//*[@resource-id="org.wikipedia:id/fragment_search_results"]'


class PesquisaScreen(BaseScreen):
    """Tela de pesquisa e lista de resultados."""

    CAMPO_ABRIR_PESQUISA = (AppiumBy.ID, "org.wikipedia:id/search_card")
    CAMPO_PESQUISA = (AppiumBy.ID, "org.wikipedia:id/search_src_text")

    @allure.step("Mobile: pesquisar {termo}")
    def pesquisar(self, termo):
        self.tocar(self.CAMPO_ABRIR_PESQUISA)
        self.digitar(self.CAMPO_PESQUISA, termo)

    def descricao_do_resultado(self, titulo):
        return self.ler_texto(self._descricao(titulo))

    @allure.step("Mobile: abrir o resultado {titulo}")
    def abrir_resultado(self, titulo):
        self.tocar(self._resultado(titulo))

    @staticmethod
    def _resultado(titulo):
        # O título é buscado dentro da lista de resultados, porque o campo
        # de pesquisa também contém o mesmo texto digitado.
        return (AppiumBy.XPATH, f'{LISTA_DE_RESULTADOS}//android.widget.TextView[@text="{titulo}"]')

    @staticmethod
    def _descricao(titulo):
        # Em cada resultado, a descrição é o texto logo abaixo do título.
        return (
            AppiumBy.XPATH,
            f'{LISTA_DE_RESULTADOS}//android.widget.TextView[@text="{titulo}"]'
            "/following-sibling::android.widget.TextView[1]",
        )
