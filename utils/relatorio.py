import allure


def teste_falhou(request) -> bool:
    """Lê o resultado guardado pelo hook pytest_runtest_makereport (tests/conftest.py)."""
    resultado = getattr(request.node, "resultado_call", None)
    return bool(resultado and resultado.failed)


def anexar_print(imagem_png: bytes, nome: str = "Tela no momento da falha") -> None:
    allure.attach(imagem_png, name=nome, attachment_type=allure.attachment_type.PNG)
