"""Baixa a versão do app da Wikipedia usada nos testes de Mobile.

A versão fica fixa aqui, para que o resultado dos testes não mude quando
sair uma versão nova do app. Para atualizar, troque VERSAO_DO_APP.
"""

from pathlib import Path

import httpx

from config.settings import carregar_settings

VERSAO_DO_APP = "wikipedia-50617-r-2026-11-12.apk"
URL_DO_APP = f"https://releases.wikimedia.org/mobile/android/wikipedia/stable/{VERSAO_DO_APP}"


def baixar_apk() -> None:
    settings = carregar_settings()
    destino = Path(settings.caminho_apk)
    if destino.exists():
        print(f"O app já existe em {destino}")
        return

    destino.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream(
        "GET", URL_DO_APP, headers={"User-Agent": settings.user_agent}, follow_redirects=True, timeout=120
    ) as resposta:
        resposta.raise_for_status()
        with destino.open("wb") as arquivo:
            for parte in resposta.iter_bytes():
                arquivo.write(parte)
    print(f"App baixado em {destino}")


if __name__ == "__main__":
    baixar_apk()
