
# ============================================================
# DASHBOARD DE MONITORAMENTO DA IA
# Executar no VS Code:
#
# python -m streamlit run dashboard.py --server.port 8501
# ============================================================

from groq import Groq
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import gspread
import google.auth
import os
from pyngrok import ngrok


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Monitoramento da IA",
    page_icon="🤖",
    layout="wide"
)

SHEET_ID = "1OkGp2mevcG5UFsDdpuZ87_2nFXHAdbmHWQwlb7g_IAI"


# ============================================================
# GROQ
# ============================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error(
        "Chave da Groq não encontrada no ambiente."
    )
    st.info(
        "Configure a variável GROQ_API_KEY no Windows "
        "antes de executar o dashboard."
    )
    st.stop()

client = Groq(
    api_key=api_key
)


# ============================================================
# GOOGLE SHEETS
# ============================================================

try:

    creds, _ = google.auth.default()

    gc = gspread.authorize(creds)

    planilha = gc.open_by_key(SHEET_ID)

    aba = planilha.sheet1

    dados = aba.get_all_records()

    df = pd.DataFrame(dados)

except Exception as erro:

    st.error(
        f"Erro ao acessar o Google Sheets: {erro}"
    )

    st.stop()


# ============================================================
# TÍTULO
# ============================================================

st.title("Monitoramento da IA")

st.write(
    "Acompanhamento dos atendimentos realizados pelos agentes."
)


# ============================================================
# VERIFICAR DADOS
# ============================================================

if df.empty:

    st.warning(
        "Nenhum dado encontrado na planilha."
    )

    st.stop()


# ============================================================
# TRATAMENTO DOS DADOS
# ============================================================

colunas_numericas = [
    "Concluídos",
    "Futuro",
    "Humano"
]

for coluna in colunas_numericas:

    if coluna in df.columns:

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        ).fillna(0)

    else:

        df[coluna] = 0


# ============================================================
# CÁLCULO DOS RESULTADOS
# ============================================================

concluido = int(
    df["Concluídos"].sum()
)

futuro = int(
    df["Futuro"].sum()
)

humano = int(
    df["Humano"].sum()
)

total = concluido + futuro + humano


# ============================================================
# INDICADORES
# ============================================================

st.header("Dados")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total analisado",
        total
    )

with col2:

    st.metric(
        "Concluídos",
        concluido
    )

with col3:

    st.metric(
        "Futuro",
        futuro
    )

with col4:

    st.metric(
        "Humano",
        humano
    )


# ============================================================
# GRÁFICO
# ============================================================

st.header("Gráfico")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=[
            "Concluído",
            "Futuro",
            "Humano"
        ],
        y=[
            concluido,
            futuro,
            humano
        ],
        text=[
            concluido,
            futuro,
            humano
        ],
        textposition="auto"
    )
)

fig.update_layout(
    height=450,
    xaxis_title="Resultado",
    yaxis_title="Quantidade",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# ANÁLISE DA IA
# ============================================================

st.header("Análise da IA")

observacoes = []

if "Observação" in df.columns:

    for observacao in df["Observação"].dropna():

        texto = str(observacao).strip()

        if texto:
            observacoes.append(texto)


st.write(
    f"{len(observacoes)} observações disponíveis para análise."
)


# ============================================================
# BOTÃO DA IA
# ============================================================

if st.button("Gerar relatório da IA"):

    with st.spinner(
        "A IA está analisando os dados..."
    ):

        try:

            # ------------------------------------------------
            # Indicadores
            # ------------------------------------------------

            taxa_conclusao = (
                (concluido / total) * 100
                if total > 0
                else 0
            )


            # ------------------------------------------------
            # Observações
            # ------------------------------------------------

            observacoes = []

            if "Observação" in df.columns:

                for observacao in df["Observação"].dropna():

                    texto = str(observacao).strip()

                    if texto:
                        observacoes.append(texto)


            # ------------------------------------------------
            # Transformar observações em texto
            # ------------------------------------------------

            casos = "\n".join(
                f"- {observacao}"
                for observacao in observacoes
            )


            # ------------------------------------------------
            # Prompt
            # ------------------------------------------------

            prompt = f"""
Analise o desempenho de agentes de inteligência artificial
em uma operação empresarial.

DADOS:

Total de casos: {total}
Concluídos: {concluido}
Futuro: {futuro}
Humano: {humano}
Taxa de conclusão: {taxa_conclusao:.1f}%

OBSERVAÇÕES:

{casos}

Crie um relatório profissional para um gestor.

O relatório deve conter:

1. RESUMO EXECUTIVO

Explique de forma geral o comportamento da IA.

2. DESEMPENHO

Analise os números apresentados.

3. PRINCIPAIS PADRÕES

Identifique padrões recorrentes nas observações.

4. PRINCIPAIS FALHAS

Identifique os principais problemas encontrados.

5. PONTOS POSITIVOS

Identifique comportamentos positivos observados.
Se não houver evidências suficientes, diga isso.

6. IMPACTO OPERACIONAL

Explique como os problemas encontrados podem afetar
a operação.

7. RECOMENDAÇÕES

Apresente recomendações práticas para melhorar os agentes.

8. CONCLUSÃO

Faça uma avaliação geral do período.

REGRAS:

- Não invente informações.
- Não invente números.
- Use somente os dados fornecidos.
- Diferencie fatos de interpretações.
- Use linguagem profissional.
- Seja claro e detalhado.
- Não mencione empréstimos ou concessão de dinheiro.

Existem dois agentes:

- Agente de cobrança/atendimento.
- Agente de triagem documental.
"""


            # ------------------------------------------------
            # Chamada para Groq
            # ------------------------------------------------

            resposta = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "Você é um analista de qualidade "
                            "de inteligência artificial."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0.2
            )


            # ------------------------------------------------
            # Resultado
            # ------------------------------------------------

            resultado = (
                resposta
                .choices[0]
                .message
                .content
            )


            # ------------------------------------------------
            # Mostrar relatório
            # ------------------------------------------------

            st.subheader(
                "Relatório de análise"
            )

            st.markdown(
                resultado
            )


        except Exception as erro:

            st.error(
                f"Erro ao gerar relatório: {erro}"
            )


# ============================================================
# ÚLTIMA ATUALIZAÇÃO
# ============================================================

if (
    "Data" in df.columns
    and "Hora" in df.columns
):

    ultimo = df.iloc[-1]

    st.divider()

    st.caption(
        f"Último registro: "
        f"{ultimo['Data']} às {ultimo['Hora']}"
    )


# ============================================================
# NGROK
# ============================================================
#
# O Streamlit já está rodando na porta 8501.
#
# Para criar um link público pelo Windows:
#
# 1. Configure o token do ngrok.
# 2. Execute este arquivo.
#
# ============================================================

if st.button("Gerar link público"):

    try:

        ngrok.kill()

        tunnel = ngrok.connect(
            8501,
            "http"
        )

        st.success(
            "Dashboard publicado!"
        )

        st.code(
            tunnel.public_url
        )

        st.markdown(
            f"[Abrir dashboard público]({tunnel.public_url})"
        )

    except Exception as erro:

        st.error(
            f"Erro ao iniciar ngrok: {erro}"
        )

