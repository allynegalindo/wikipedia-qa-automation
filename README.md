# Testes de API, Web e Mobile da Wikipédia com Python

[![Testes](https://github.com/allynegalindo/wikipedia-qa-automation/actions/workflows/testes.yml/badge.svg)](https://github.com/allynegalindo/wikipedia-qa-automation/actions/workflows/testes.yml)
[![Relatório](https://img.shields.io/badge/relat%C3%B3rio-GitHub%20Pages-2ea44f)](https://allynegalindo.github.io/wikipedia-qa-automation/)

Automação de testes da [Wikipédia em português](https://pt.wikipedia.org) em três camadas: **API**, **site (Web)** e **app Android (Mobile)**, com uma base única em Python e Pytest. O projeto foi feito para responder a uma pergunta: **como garantir que o site e o app mostram a mesma informação que a API entrega, sem deixar valores fixos nos testes?**

📊 **[Ver o último relatório de execução](https://allynegalindo.github.io/wikipedia-qa-automation/)**

## Destaques

- **A API como fonte da verdade:** os testes de Web e Mobile buscam o resultado esperado na API e verificam se a tela mostra a mesma informação.
- **Contrato validado com modelos tipados:** as respostas da API são validadas com [Pydantic](https://docs.pydantic.dev). Se um campo sumir ou mudar de tipo, o teste quebra.
- **Uma base para três camadas:** configuração, massa de dados, cliente da API e fixtures compartilhados entre API, Web e Mobile.
- **Page Object (Web) e Screen Object (Mobile):** locators e ações ficam nas páginas e telas. As verificações ficam nos testes.
- **Testes independentes:** a API e o site só são lidos, nada é criado nem alterado. No Mobile, o app é reiniciado antes de cada teste.
- **Defeito real encontrado:** um erro de digitação na tradução pt-BR do app oficial, documentado em [`docs/achados`](docs/achados/ACHADO-001-erro-de-digitacao-no-onboarding.md).
- **Pipeline por prioridade:** lint → API → Web e Mobile em paralelo → relatório único do [Allure](https://allurereport.org) publicado no GitHub Pages.

## A API como fonte da verdade

Em vez de escrever no teste o texto que a tela deveria mostrar, o teste pergunta à API:

```python
def test_resultado_da_pesquisa_exibe_a_descricao_informada_pela_api(
    wikipedia_api, app_na_home, pesquisa_screen, titulo
):
    resumo = wikipedia_api.obter_resumo(titulo)  # o esperado vem da API
    app_na_home.abrir_pesquisa()

    pesquisa_screen.pesquisar(titulo)  # a ação acontece no app

    assert pesquisa_screen.descricao_do_resultado(resumo.title) == resumo.description
```

Se alguém editar o artigo e a descrição mudar, o teste continua passando, porque a API e o app mudam juntos. O teste só falha quando **o app mostra algo diferente da API**, que é justamente o defeito que interessa.

## O que é testado

| Camada | Ferramentas | O que verifica |
| --- | --- | --- |
| **API** | HTTPX + Pydantic | Contrato do endpoint `/page/summary`, normalização do título, redirecionamento, página de desambiguação, títulos com caracteres especiais e página inexistente (404) |
| **Web** | Playwright + Page Object | O site mostra o mesmo título da API, o aviso de redirecionamento, a categoria de desambiguação, o aviso de página inexistente e o resultado da busca |
| **Mobile** | Appium + Screen Object | O app mostra a mesma descrição da API nos resultados da pesquisa, e tocar no resultado abre o artigo |

## Estrutura

```
config/settings.py      → URLs, User-Agent e caminhos, lidos de variáveis de ambiente
models/resumo.py        → modelos Pydantic: o contrato da resposta da API
services/               → camada de serviço: toda a comunicação HTTP com a API
pages/                  → Page Objects do site
screens/                → Screen Objects do app Android
data/artigos.py         → massa de dados única para as três camadas
utils/                  → codificação de títulos e anexos do relatório
tests/
  conftest.py           → fixtures compartilhadas (configuração e cliente da API)
  api/  web/  mobile/   → testes de cada camada, com as fixtures próprias
docs/achados/           → defeitos encontrados durante os testes
scripts/baixar_apk.py   → baixa a versão do app usada nos testes
Makefile                → comandos padronizados
```

## Como executar

### Pré-requisitos

- Python 3.12
- Node.js (para o relatório do Allure e o Appium)
- `make` (no Windows: `winget install ezwinports.make`)

### API e Web

```bash
make instalar   # cria o ambiente virtual e instala as dependências
make api        # testes da API
make web        # testes do site
make testes     # lint + API + Web
```

Para ver o navegador durante os testes: `.venv\Scripts\python -m pytest -m web --headed`

### Mobile

Precisa de um emulador Android e do Appium rodando:

1. Instale o [Android SDK](https://developer.android.com/tools) com as ferramentas de linha de comando, uma imagem do Android 15 (`system-images;android-35;google_apis;x86_64`) e crie um emulador.
2. Instale o Appium e o driver Android:
   ```bash
   npm install -g appium
   appium driver install uiautomator2
   ```
3. Baixe o app: `make apk`
4. Abra o emulador e, em outro terminal, o Appium: `appium`
5. Rode os testes: `make mobile`

Se o Appium não estiver rodando, os testes de Mobile são **pulados** com uma mensagem explicando o motivo. Na pipeline, eles **falham**, para o problema não passar despercebido.

### Relatório

```bash
make relatorio         # gera o relatório do Allure a partir dos resultados
make abrir-relatorio   # abre no navegador
```

Quando um teste de Web ou Mobile falha, o print da tela é anexado ao relatório.

## Pipeline

```
lint ──► api ──┬──► web ────┐
               └──► mobile ─┴──► relatório (Allure) ──► GitHub Pages
```

- **Lint e API primeiro:** são rápidos. Se a API, que é a fonte da verdade, falhar, não faz sentido gastar minutos subindo navegador e emulador.
- **Web e Mobile em paralelo**, cada um na sua máquina.
- **Mobile num emulador Android** dentro do próprio GitHub Actions.
- **Relatório único:** os resultados das três camadas são juntados num relatório do Allure, publicado mesmo quando algum teste falha.

## Decisões técnicas

**User-Agent com contato.** A [política da Wikimedia](https://meta.wikimedia.org/wiki/User-Agent_policy) exige que clientes automatizados se identifiquem com um contato. Sem isso, a API responde `403`. O projeto usa a URL do próprio repositório.

**Títulos codificados na URL.** Sem codificação, o `?` de "Onde Está Wally?" é lido como início de uma query string e a página não é encontrada. Existe um teste para esse caso.

**O que não é comparado entre a API e o site.** O primeiro parágrafo do artigo e o campo `extract` da API não são iguais: o site mostra pronúncia e referências (`[16]`), que a API remove. Comparar os dois geraria um teste que falha sem existir defeito.

**O título do artigo no app.** O texto do artigo é exibido dentro de uma WebView, e a versão publicada do app não permite inspecionar o conteúdo dela. Por isso o Mobile compara a descrição na lista de resultados, que é um elemento nativo.

**Uma sessão do Appium por execução.** Abrir uma sessão leva vários segundos, então ela é compartilhada. Para os testes continuarem independentes, o app é reiniciado antes de cada teste.

**Dicas de primeiro uso resolvidas na preparação.** Na primeira vez, o app mostra o onboarding e uma sugestão para instalar o widget de pesquisa. No emulador, o tempo até essa sugestão aparecer varia muito: numa das execuções, ela surgiu depois que o teste já estava digitando, e o teste falhou. Por isso as dicas são resolvidas uma vez, ao preparar a sessão, com uma espera longa. Os testes começam sempre com o app pronto para uso.

**Versões fixas.** As dependências estão fixadas no `requirements.txt` e a versão do app em `scripts/baixar_apk.py`, para que o resultado não mude sozinho de uma execução para outra.

## Limitações conhecidas

- **Os testes usam dados reais.** A Wikipédia é editada o tempo todo. Os artigos usados foram escolhidos por serem estáveis, mas se um deles mudar de característica (por exemplo, "Mercúrio" deixar de ser página de desambiguação), o teste correspondente vai quebrar. O primeiro passo, nesse caso, é conferir o artigo.
- **Só Android.** Testes de iOS precisam de um Mac.
