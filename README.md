# Monitoramento de Processos e IA

Sistema desenvolvido para **monitorar, analisar e aprimorar o comportamento de um bot de atendimento baseado em Inteligência Artificial**.

O projeto utiliza conversas reais entre clientes e o bot para identificar padrões, falhas e pontos de melhoria ao longo do processo de contratação.

Além de gerar relatórios sobre os atendimentos, o sistema utiliza IA para **sugerir prompts e instruções que podem ser utilizados para melhorar o próprio comportamento do bot**.

---

## Objetivo

O objetivo do projeto é transformar as conversas realizadas pelo bot em informações úteis para evolução contínua do atendimento.

O sistema busca responder perguntas como:

* Em qual etapa do processo os clientes estão parando?
* O bot está conduzindo corretamente a negociação?
* Existem respostas repetitivas ou inadequadas?
* Existem falhas recorrentes durante o processo?
* O SMS está sendo enviado corretamente?
* O cliente está recebendo e acessando o link?
* Quais problemas estão impedindo a assinatura?
* Como o comportamento do bot pode ser melhorado?

A proposta é criar um ciclo contínuo de análise:

```text
Conversa real
      ↓
Análise da IA
      ↓
Identificação de padrões
      ↓
Identificação de problemas
      ↓
Sugestões de melhoria
      ↓
Novos prompts para o bot
      ↓
Bot aprimorado
      ↓
Novas conversas
```

---

## Como funciona

O sistema possui duas etapas principais.

### 1. Análise individual

O usuário informa o **ID do cliente** e insere a conversa realizada entre o cliente e o bot.

A IA analisa a conversa considerando o fluxo do processo:

```text
NEGOCIAÇÃO
     ↓
ACORDO
     ↓
CONTRATO/TERMO
     ↓
SMS
     ↓
RECEBIMENTO DO SMS
     ↓
LINK
     ↓
ASSINATURA
```

A partir da conversa, o sistema identifica informações como:

* Etapa da negociação
* Acordo aceito
* Situação do contrato/termo
* SMS enviado
* Recebimento do SMS
* Acesso ao link
* Situação da assinatura
* Falhas identificadas
* Comportamento da IA
* Observações
* Resultado do atendimento

O resultado pode então ser salvo no Google Sheets.

---

## 2. Análise geral

Além da análise individual, o sistema permite analisar os registros acumulados na planilha.

A IA procura identificar:

* Principais padrões
* Pontos de interrupção do processo
* Falhas recorrentes
* Comportamentos do bot
* Problemas relacionados ao SMS
* Problemas relacionados à assinatura
* Oportunidades de melhoria

A partir desses dados, o objetivo é evoluir para uma segunda camada de inteligência:

### Geração de prompts de melhoria

A IA poderá analisar os problemas encontrados e gerar **prompts específicos para melhorar o comportamento do bot**.

Exemplo:

```text
Problema identificado:
O bot repete a mesma resposta quando ocorre uma falha
na geração do contrato.

Prompt de melhoria:
Quando ocorrer uma falha na geração do contrato, informe
o cliente sobre a instabilidade, realize uma nova tentativa
e, caso o problema persista, siga o procedimento de
encaminhamento definido para situações de erro.

Objetivo:
Evitar respostas repetitivas e melhorar a condução do
cliente durante falhas do sistema.

Prioridade:
Alta
```

Dessa forma, o sistema não apenas monitora o bot, mas também contribui para sua evolução.

---

# Arquitetura

A estrutura atual do projeto utiliza:

```text
                    ┌──────────────────┐
                    │   Conversa real  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Streamlit     │
                    │    Dashboard     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │       Groq       │
                    │   Modelo de IA   │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
       Análise individual        Análise dos registros
                │                         │
                └────────────┬────────────┘
                             ▼
                    ┌──────────────────┐
                    │  Google Sheets   │
                    │     Dados        │
                    └──────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Melhorias do    │
                    │       Bot        │
                    └──────────────────┘
```

---

# Tecnologias utilizadas

## Python

Linguagem principal utilizada no desenvolvimento do sistema.

## Streamlit

Utilizado para construção do dashboard e interação com o sistema.

## Groq

Utilizado para processamento das conversas e geração das análises por Inteligência Artificial.

## Google Sheets

Utilizado como base para armazenamento e acompanhamento dos registros analisados.

## Google Apps Script

Utilizado como ponte entre o dashboard e o Google Sheets para permitir o envio dos resultados.

## Pandas

Utilizado para leitura, tratamento e análise dos dados armazenados na planilha.

## Python-dotenv

Utilizado para gerenciamento das variáveis de ambiente e proteção das credenciais.

---

# Estrutura dos dados

Os registros armazenados no Google Sheets possuem as seguintes informações:

| Campo               | Descrição                                |
| ------------------- | ---------------------------------------- |
| ID                  | Identificador do cliente                 |
| Data                | Data da análise                          |
| Hora                | Horário da análise                       |
| Etapa da negociação | Etapa atual do processo                  |
| Acordo aceito       | Indica se o cliente aceitou o acordo     |
| Contrato/Termo      | Situação do contrato                     |
| SMS                 | Situação do envio do SMS                 |
| Recebimento SMS     | Indica se o SMS foi recebido             |
| Link acessado       | Indica se o cliente acessou o link       |
| Assinatura          | Situação da assinatura                   |
| Falha identificada  | Problemas encontrados durante o processo |
| Comportamento da IA | Avaliação do comportamento do bot        |
| Observação da IA    | Observações adicionais da análise        |
| Resultado           | Resultado final do atendimento           |

O **ID é fornecido pelo sistema de origem/usuário e representa o cliente**. O dashboard não cria um novo ID para cada registro.

---

# Fluxo de contratação monitorado

O sistema acompanha o processo desde a negociação até a assinatura:

```text
┌───────────────┐
│  Negociação   │
└───────┬───────┘
        ↓
┌───────────────┐
│    Acordo     │
└───────┬───────┘
        ↓
┌───────────────┐
│ Contrato/Termo│
└───────┬───────┘
        ↓
┌───────────────┐
│      SMS      │
└───────┬───────┘
        ↓
┌───────────────┐
│ Recebimento   │
└───────┬───────┘
        ↓
┌───────────────┐
│     Link      │
└───────┬───────┘
        ↓
┌───────────────┐
│   Assinatura  │
└───────────────┘
```

Um dos objetivos do monitoramento é identificar **em qual ponto desse fluxo ocorre a perda ou interrupção do processo**.

---

# Exemplo de análise

Uma conversa pode apresentar o seguinte comportamento:

```text
Negociação
    ↓
Acordo aceito
    ↓
Contrato não gerado
    ↓
Falha do sistema
    ↓
Processo interrompido
```

Nesse caso, o sistema deve identificar que:

* O cliente aceitou o acordo;
* O processo chegou à etapa de contrato;
* O contrato não foi gerado;
* O SMS não deveria ser considerado enviado;
* A assinatura não ocorreu;
* O principal problema está na geração do contrato.

Isso evita conclusões incorretas, como classificar o atendimento simplesmente como "cliente não assinou".

---

# Dashboard

O dashboard permite:

* Inserir o ID do cliente;
* Inserir uma conversa;
* Solicitar análise da IA;
* Visualizar o resultado;
* Salvar o resultado no Google Sheets;
* Visualizar os registros existentes;
* Acompanhar indicadores gerais;
* Gerar uma análise geral dos processos.

A interface foi projetada para manter o foco na **análise do processo e do comportamento da IA**, evitando excesso de informações visuais desnecessárias.

---

# Segurança

As credenciais utilizadas pelo sistema são armazenadas em variáveis de ambiente.

Exemplo:

```env
GROQ_API_KEY=sua_chave
SHEETS_WEBAPP_URL=sua_url
SHEETS_WEBAPP_TOKEN=seu_token
```

O arquivo `.env` não deve ser enviado para o GitHub.

O projeto utiliza `.gitignore` para evitar o versionamento dessas informações.

---

# Instalação

Clone o repositório:

```bash
git clone https://github.com/lucasgesini45-coder/monitoramento_IA.git
```

Entre na pasta:

```bash
cd monitoramento_IA
```

Instale as dependências:

```bash
pip install streamlit pandas requests python-dotenv groq
```

Configure o arquivo `.env`:

```env
GROQ_API_KEY=sua_chave
SHEETS_WEBAPP_URL=sua_url
SHEETS_WEBAPP_TOKEN=seu_token
```

Execute o dashboard:

```bash
python -m streamlit run dashboard_ai.py --server.port 8502
```

O Streamlit disponibilizará o dashboard localmente.

---

# Integração com Google Sheets

O Google Sheets funciona como uma camada simples de armazenamento dos registros.

O processo de gravação ocorre da seguinte maneira:

```text
Dashboard
    ↓
Python
    ↓
Google Apps Script
    ↓
Google Sheets
```

O Apps Script recebe os dados enviados pelo dashboard e adiciona uma nova linha na planilha.

---

# Evolução planejada

O projeto está sendo desenvolvido de forma incremental.

Entre as próximas melhorias estão:

* [ ] Geração automática de prompts para melhoria do bot
* [ ] Classificação de prioridade das melhorias
* [ ] Identificação automática de comportamentos recorrentes
* [ ] Comparação entre versões do comportamento do bot
* [ ] Avaliação da evolução do atendimento após mudanças nos prompts
* [ ] Histórico das melhorias aplicadas
* [ ] Detecção de padrões novos nas conversas
* [ ] Análise mais avançada do funil de contratação
* [ ] Identificação de situações que devem ser encaminhadas para atendimento humano
* [ ] Criação de um ciclo contínuo de monitoramento e melhoria

---

# Visão do projeto

O objetivo final é transformar o sistema em uma ferramenta capaz de acompanhar continuamente o comportamento do bot e auxiliar sua evolução.

A visão é:

```text
ATENDIMENTO
     ↓
MONITORAMENTO
     ↓
ANÁLISE
     ↓
IDENTIFICAÇÃO DE PROBLEMAS
     ↓
SUGESTÃO DE MELHORIAS
     ↓
APLICAÇÃO DOS PROMPTS
     ↓
NOVO ATENDIMENTO
     ↓
NOVA ANÁLISE
```

Assim, o projeto deixa de ser apenas um dashboard de acompanhamento e passa a funcionar como uma **camada de inteligência para melhoria contínua do atendimento automatizado**.

---

# Status

**Em desenvolvimento**

A versão atual já possui:

* Análise de conversas com IA
* Identificação do cliente por ID
* Registro de data e hora
* Classificação das etapas do processo
* Identificação de falhas
* Análise do comportamento da IA
* Integração com Google Sheets
* Dashboard em Streamlit
* Análise geral dos registros
* Estrutura preparada para geração de prompts de melhoria do bot

---

# Projeto

**Monitoramento de Processos e IA**

Desenvolvido para análise e evolução contínua de processos de atendimento automatizados por Inteligência Artificial.
