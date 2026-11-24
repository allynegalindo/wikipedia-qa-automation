import pytest

from data.artigos import ARTIGOS_PADRAO, PAGINA_DE_DESAMBIGUACAO
from models.resumo import ResumoArtigo

pytestmark = pytest.mark.api


@pytest.mark.parametrize("titulo", [*ARTIGOS_PADRAO, PAGINA_DE_DESAMBIGUACAO])
def test_resumo_respeita_o_contrato(wikipedia_api, titulo):
    resposta = wikipedia_api.buscar_resumo(titulo)

    assert resposta.status_code == 200
    assert resposta.headers["content-type"].startswith("application/json")
    ResumoArtigo.model_validate(resposta.json())
