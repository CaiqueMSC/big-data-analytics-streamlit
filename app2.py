# --------------------------------------------------------------
# Projeto: Trabalho Espaço Terapêutico Neuro 7 Vidas - Big Data em Python (Estácio)
# Empresa fictícia: Espaço Terapêutico Neuro 7 Vidas
# Autor: San
# Data: 24/09/2025
# --------------------------------------------------------------

import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random
import os

# --- Configurações do dashboard ---
st.set_page_config(page_title="Dashboard Neuro 7 Vidas", layout="wide")
st.title("Espaço Terapêutico Neuro 7 Vidas")

# --- 1. GERAR CSV FICTÍCIO AUTOMATICAMENTE ---
if not os.path.exists('dados_clientes.csv'):
    random.seed(42)
    servicos = [
        'Terapia Integrativa - Individual',
        'Terapia Integrativa - Casal',
        'Terapia Integrativa - Online'
    ]
    generos_base = ['Feminino', 'Masculino', 'Não-binário', 'Outro']
    generos_restantes = random.choices(
        ['Feminino', 'Masculino', 'Não-binário', 'Outro'],
        weights=[0.5, 0.4, 0.07, 0.03],
        k=26
    )
    generos = generos_base + generos_restantes
    random.shuffle(generos)

    feedbacks = [
        "Excelente atendimento e ambiente acolhedor",
        "Senti muita melhora nas sessões",
        "Profissional muito atenciosa e competente",
        "Ótimo custo-benefício, recomendo!",
        "Ambiente tranquilo e energia positiva",
        "Me senti ouvido e compreendido",
        "Voltarei com certeza",
        "Resultados transformadores desde a primeira sessão",
        "A experiência foi única e enriquecedora",
        "Espaço que transmite paz e confiança"
    ]

    dados = []
    for i in range(30):
        dados.append({
            'id_cliente': i + 1,
            'idade': random.randint(18, 65),
            'gênero': generos[i],
            'tipo_serviço': random.choice(servicos),
            'valor_atendimento': round(random.uniform(120, 250), 2),
            'data_atendimento': f"2025-{random.randint(1, 9):02d}-{random.randint(1, 28):02d}",
            'feedback': random.choice(feedbacks)
        })

    df = pd.DataFrame(dados)
    df.to_csv('dados_clientes.csv', index=False, encoding='utf-8-sig')
    st.success("✅ Arquivo 'dados_clientes.csv' criado com sucesso!")

# --- 2. LER O ARQUIVO CSV ---
df = pd.read_csv('dados_clientes.csv')
df['mês'] = pd.to_datetime(df['data_atendimento']).dt.month
df['mês_nome'] = pd.to_datetime(df['data_atendimento']).dt.strftime('%B')

# --- 3. FILTROS INTERATIVOS ---
st.sidebar.header("Filtros")
tipo_serviço_filter = st.sidebar.multiselect("Escolha o tipo de serviço", options=df['tipo_serviço'].unique(), default=df['tipo_serviço'].unique())
mês_filter = st.sidebar.multiselect("Escolha o mês", options=df['mês_nome'].unique(), default=df['mês_nome'].unique())

df_filtrado = df[(df['tipo_serviço'].isin(tipo_serviço_filter)) & (df['mês_nome'].isin(mês_filter))]

# --- 4. GRÁFICOS EM COLUNAS ---
col1, col2 = st.columns(2)

# --- Gráfico de barras ---
with col1:
    st.subheader("Valor médio por tipo de serviço")
    valor_medio = df_filtrado.groupby('tipo_serviço')['valor_atendimento'].mean().sort_values()
    fig_bar = px.bar(valor_medio.reset_index(), x='tipo_serviço', y='valor_atendimento',
                     color='tipo_serviço', text='valor_atendimento',
                     labels={'tipo_serviço': 'Tipo de Serviço', 'valor_atendimento': 'Valor médio (R$)'},
                     title="Valor médio por tipo de serviço")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Gráfico de pizza ---
with col2:
    st.subheader("Distribuição por gênero")
    genero_counts = df_filtrado['gênero'].value_counts()
    fig_pie = px.pie(values=genero_counts.values, names=genero_counts.index,
                     title="Distribuição de clientes por gênero")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- Word Cloud ---
st.subheader("Palavras mais citadas nos feedbacks")
texto_feedbacks = " ".join(df_filtrado['feedback'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='plasma', max_words=50).generate(texto_feedbacks)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

# --- Gráfico comparativo ---
st.subheader("Evolução mensal dos atendimentos por tipo de serviço")
evolucao = df_filtrado.groupby(['mês_nome', 'tipo_serviço']).size().unstack(fill_value=0)
fig_comp = px.bar(evolucao.reset_index(), x='mês_nome', y=evolucao.columns,
                  title='Evolução mensal dos atendimentos por tipo de serviço',
                  labels={'mês_nome': 'Mês', 'value': 'Quantidade de atendimentos'})
st.plotly_chart(fig_comp, use_container_width=True)

st.success("✅ Dashboard completo e interativo!")
