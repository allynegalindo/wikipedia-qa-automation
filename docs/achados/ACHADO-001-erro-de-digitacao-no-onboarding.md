# ACHADO-001: Erro de digitação no título da tela de privacidade do onboarding

| | |
| --- | --- |
| **Severidade** | Baixa (cosmético) |
| **Prioridade** | Baixa |
| **Status** | Aberto, ainda não reportado à Wikimedia |
| **Componente** | App Android, onboarding, tela "Dados e privacidade" (texto `onboarding_data_privacy_title`) |
| **Ambiente** | App Wikipédia `50617-r-2026-11-12`, emulador Android 15 (API 35), idioma do aparelho pt-BR |
| **Encontrado em** | 17/11/2026, durante o mapeamento das telas para a automação de Mobile |
| **Reportado por** | Allyne Galindo |

## Descrição

Na segunda tela do onboarding, o título aparece como **"Dados e privadade"**. O correto é **"Dados e privacidade"**.

O erro existe só na tradução para português do Brasil. A tradução para português de Portugal está correta.

## Passos para reproduzir

1. Configure o idioma do aparelho como **Português (Brasil)**.
2. Instale o app da Wikipédia (ou limpe os dados dele) e abra.
3. Na primeira tela, toque em **Avançar**.

## Resultado esperado

O título da tela é **"Dados e privacidade"**.

## Resultado obtido

O título da tela é **"Dados e privadade"**.

## Evidência

Os textos traduzidos ficam dentro do próprio app. Lendo os recursos do APK com o `aapt2` (ferramenta do Android SDK), o texto `onboarding_data_privacy_title` aparece assim:

```
$ aapt2 dump resources wikipedia-50617-r-2026-11-12.apk
resource 0x7f13052b string/onboarding_data_privacy_title
  (pt)     "Dados e Privacidade"
  (pt-rBR) "Dados e privadade"
```

Isso confirma que o erro está no texto da tradução, e não na forma como a tela é exibida.

## Impacto

- Não impede o uso do app.
- É a segunda tela que toda pessoa nova vê, e justamente no assunto **privacidade**. Um erro de digitação ali passa uma impressão de descuido num tema que pede confiança.

## Como corrigir

As traduções dos apps da Wikimedia são feitas pela comunidade no [translatewiki.net](https://translatewiki.net). A correção é editar a mensagem `onboarding_data_privacy_title` em pt-BR por lá. Na versão seguinte do app, o texto corrigido entra automaticamente.
