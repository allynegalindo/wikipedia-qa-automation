from urllib.parse import quote


def codificar_titulo(titulo: str) -> str:
    """Converte um título de artigo no formato usado nas URLs da Wikipedia.

    A Wikipedia usa "_" no lugar de espaço. Codificar o título impede que
    caracteres como "?" e "#" sejam lidos como parte da URL: sem isso,
    "Onde Está Wally?" vira uma query string e a página não é encontrada.
    """
    return quote(titulo.replace(" ", "_"), safe="")
