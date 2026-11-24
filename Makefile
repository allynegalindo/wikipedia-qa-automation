# Comandos padronizados do projeto. Funcionam no Windows (local) e no Linux (pipeline).
# Na pipeline, as dependências são instaladas direto no Python do runner: make api PY=python

ifeq ($(OS),Windows_NT)
SHELL := cmd.exe
.SHELLFLAGS := /c
PY ?= .venv\Scripts\python.exe
else
PY ?= .venv/bin/python
endif

RESULTADOS := allure-results
RELATORIO := allure-report
ALLURE := npx --yes allure@3.33.0
PYTEST := $(PY) -m pytest --alluredir=$(RESULTADOS)

.PHONY: help instalar lint formatar api web mobile apk testes relatorio abrir-relatorio limpar

help:
	@echo Comandos disponiveis:
	@echo   make instalar         cria o ambiente virtual e instala as dependencias
	@echo   make lint             verifica estilo e erros comuns no codigo (ruff)
	@echo   make formatar         corrige a formatacao do codigo
	@echo   make api              testes da camada de API
	@echo   make web              testes da camada Web
	@echo   make mobile           testes da camada Mobile (precisa do emulador e do Appium)
	@echo   make testes           lint + API + Web
	@echo   make apk              baixa o app da Wikipedia usado nos testes de Mobile
	@echo   make relatorio        gera o relatorio do Allure
	@echo   make abrir-relatorio  abre o relatorio no navegador
	@echo   make limpar           apaga resultados e relatorios anteriores

instalar:
	python -m venv .venv
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt
	$(PY) -m playwright install chromium

lint:
	$(PY) -m ruff check .
	$(PY) -m ruff format --check .

formatar:
	$(PY) -m ruff check --fix .
	$(PY) -m ruff format .

api:
	$(PYTEST) -m api

web:
	$(PYTEST) -m web

mobile:
	$(PYTEST) -m mobile

testes: lint api web

apk:
	$(PY) -m scripts.baixar_apk

relatorio:
	$(ALLURE) generate $(RESULTADOS) --output $(RELATORIO)

abrir-relatorio:
	$(ALLURE) open $(RELATORIO)

limpar:
	$(PY) -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ('$(RESULTADOS)', '$(RELATORIO)', 'test-results')]"
