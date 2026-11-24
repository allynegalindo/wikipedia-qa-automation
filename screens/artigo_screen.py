from appium.webdriver.common.appiumby import AppiumBy

from screens.base_screen import BaseScreen


class ArtigoScreen(BaseScreen):
    """Tela de leitura de um artigo.

    O conteúdo do artigo é exibido dentro de uma WebView. Na versão publicada
    do app, a WebView não permite inspeção, então a verificação usa os
    elementos nativos da tela (conteúdo carregado e barra de ações).
    """

    CONTEUDO = (AppiumBy.ID, "org.wikipedia:id/page_web_view")
    BOTAO_SALVAR = (AppiumBy.ID, "org.wikipedia:id/page_save")

    def esta_aberto(self):
        return self.esta_visivel(self.CONTEUDO) and self.esta_visivel(self.BOTAO_SALVAR)
