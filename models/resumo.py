"""Modelos Pydantic que descrevem o contrato do endpoint /page/summary.

Os nomes dos campos seguem exatamente o JSON da API (em inglês),
porque é isso que o Pydantic compara ao validar a resposta.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, PositiveInt


class Titulos(BaseModel):
    canonical: str
    normalized: str
    display: str


class Imagem(BaseModel):
    source: HttpUrl
    width: PositiveInt
    height: PositiveInt


class UrlsDaPagina(BaseModel):
    page: HttpUrl
    revisions: HttpUrl
    edit: HttpUrl
    talk: HttpUrl


class UrlsDeConteudo(BaseModel):
    desktop: UrlsDaPagina
    mobile: UrlsDaPagina


class ResumoArtigo(BaseModel):
    type: Literal["standard", "disambiguation", "no-extract", "mainpage"]
    title: str = Field(min_length=1)
    titles: Titulos
    pageid: PositiveInt
    lang: str
    dir: Literal["ltr", "rtl"]
    revision: str
    timestamp: datetime
    description: str | None = None
    extract: str
    extract_html: str
    thumbnail: Imagem | None = None
    content_urls: UrlsDeConteudo


class ErroApi(BaseModel):
    status: int
    type: str
