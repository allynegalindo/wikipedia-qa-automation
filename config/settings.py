"""Configurações do projeto, lidas de variáveis de ambiente com valores padrão."""

import os
from dataclasses import dataclass
from pathlib import Path

RAIZ_DO_PROJETO = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    api_base_url: str
    web_base_url: str
    user_agent: str
    timeout: float
    appium_url: str
    caminho_apk: str


def carregar_settings() -> Settings:
    return Settings(
        api_base_url=os.getenv("WIKI_API_BASE_URL", "https://pt.wikipedia.org/api/rest_v1"),
        web_base_url=os.getenv("WIKI_WEB_BASE_URL", "https://pt.wikipedia.org"),
        # A política da Wikimedia exige um contato no User-Agent de clientes automatizados.
        # Sem ele, a API responde 403. https://meta.wikimedia.org/wiki/User-Agent_policy
        user_agent=os.getenv(
            "WIKI_USER_AGENT",
            "wikipedia-qa-automation/0.1 (https://github.com/allynegalindo/wikipedia-qa-automation)",
        ),
        timeout=float(os.getenv("WIKI_TIMEOUT", "10")),
        appium_url=os.getenv("APPIUM_URL", "http://127.0.0.1:4723"),
        caminho_apk=os.getenv("WIKI_APK", str(RAIZ_DO_PROJETO / "apps" / "wikipedia.apk")),
    )
