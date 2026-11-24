import allure
from playwright.sync_api import Page


class PaginaInicial:
    """Página inicial da Wikipedia, usada como ponto de partida da busca."""

    def __init__(self, page: Page):
        self.page = page
        self.campo_busca = page.get_by_role("searchbox")

    @allure.step("Web: abrir a página inicial")
    def abrir(self) -> None:
        self.page.goto("/")

    @allure.step("Web: buscar {termo}")
    def buscar(self, termo: str) -> None:
        self.campo_busca.fill(termo)
        self.campo_busca.press("Enter")
