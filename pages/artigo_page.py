import allure
from playwright.sync_api import Page

from utils.titulos import codificar_titulo


class ArtigoPage:
    """Página de um artigo da Wikipedia (/wiki/<titulo>)."""

    def __init__(self, page: Page):
        self.page = page
        self.titulo = page.locator("#firstHeading")
        self.aviso_redirecionamento = page.locator(".mw-redirectedfrom")
        self.categorias = page.locator("#catlinks")
        self.aviso_pagina_inexistente = page.locator(".noarticletext")

    @allure.step("Web: abrir o artigo {titulo}")
    def abrir(self, titulo: str) -> None:
        self.page.goto(f"/wiki/{codificar_titulo(titulo)}")
