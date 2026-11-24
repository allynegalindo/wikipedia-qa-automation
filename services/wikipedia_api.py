"""Camada de serviço: concentra toda a comunicação HTTP com a API REST da Wikipedia."""

import allure
import httpx

from models.resumo import ResumoArtigo
from utils.titulos import codificar_titulo


class WikipediaApi:
    def __init__(self, base_url: str, user_agent: str, timeout: float):
        self._client = httpx.Client(
            base_url=base_url,
            headers={"User-Agent": user_agent, "Accept": "application/json"},
            timeout=timeout,
        )

    @allure.step("API: buscar o resumo de {titulo}")
    def buscar_resumo(self, titulo: str) -> httpx.Response:
        """Devolve a resposta crua, para testes que verificam status, headers e erros."""
        return self._client.get(f"/page/summary/{codificar_titulo(titulo)}")

    def obter_resumo(self, titulo: str) -> ResumoArtigo:
        """Devolve o resumo já validado pelo contrato. As camadas Web e Mobile usam este método."""
        resposta = self.buscar_resumo(titulo)
        resposta.raise_for_status()
        return ResumoArtigo.model_validate(resposta.json())

    def fechar(self) -> None:
        self._client.close()
