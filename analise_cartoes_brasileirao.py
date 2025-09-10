#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Configuração da página
st.set_page_config(
    page_title="Dashboard de Cartões no Brasileirão",
    page_icon="⚽",
    layout="wide"
)

st.title("📊 Análise de Cartões no Campeonato Brasileiro (2003-2023)")

# Carregar dados
@st.cache_data
def carregar_dados():
    dados = pd.read_csv('./campeonato-brasileiro-cartoes.csv', sep=',')
    dados.rename(columns={'rodata': 'rodada'}, inplace=True)
    dados_sem_nulos = dados.dropna()
    dados_sem_nulos['num_camisa'] = dados_sem_nulos['num_camisa'].astype(pd.Int64Dtype())
    return dados_sem_nulos

dados = carregar_dados()
dados["posicao"] = dados["posicao"].replace("Zagueira", "Zagueiro")

# Criando abas no centro da tela
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📌 Visão Geral",
    "⚽ Posições",
    "📅 Rodadas",
    "⏱️ Tempo de Jogo",
    "🏟️ Clube Top",
    "🏆 Top 20 Clubes",
    "👕 Top 20 Jogadores",
    "🏅 Jogador Top",
    "🔥 Partidas",
    "⏳ Minutos"
])

# 1) Visão geral
with tab1:
    st.subheader("📌 Estrutura dos Dados")
    st.write(dados)

# 2) Cartões por posição
with tab2:
    st.subheader("⚽ Cartões por Posição de Jogador")
    posicoes = dados['posicao'].value_counts().sort_values(ascending=True)
    st.bar_chart(posicoes)

# 3) Cartões por rodada
with tab3:
    st.subheader("📅 Cartões por Rodada")
    freq_rodadas = dados['rodada'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(freq_rodadas.index, freq_rodadas.values, color="gray")
    ax.set_title("Quantidade de Cartões por Rodada")
    ax.set_xlabel("Quantidade")
    ax.set_ylabel("Rodada")
    st.pyplot(fig)

# 4) Cartões por tempo
with tab4:
    st.subheader("⏱️ Cartões por Tempo de Jogo")
    primeiro_tempo = dados[dados['minuto'].str.contains(r'^(45\+|\d+)$') &
                           (dados['minuto'].str.extract(r'^(\d+)')[0].astype(float) <= 45)]
    segundo_tempo = dados[dados['minuto'].str.extract(r'(\d+)')[0].astype(float) >= 46]

    col1, col2 = st.columns(2)
    col1.metric("Cartões no 1º tempo", len(primeiro_tempo))
    col2.metric("Cartões no 2º tempo", len(segundo_tempo))

# 5) Clube com mais cartões
with tab5:
    st.subheader("🏟️ Clube com Mais Cartões")
    clubes = dados['clube'].value_counts()
    clube_top = clubes.idxmax()
    total = clubes.max()
    vermelhos = len(dados.query(f'clube == "{clube_top}" and cartao == "Vermelho"'))
    amarelos = total - vermelhos

    st.write(f"**{clube_top}** tomou o maior número de cartões: **{total}**")
    st.write(f"🔴 Vermelhos: {vermelhos}")
    st.write(f"🟨 Amarelos: {amarelos}")

# 6) Top 20 clubes (ordem crescente)
with tab6:
    st.subheader("🏆 Top 20 Clubes com Mais Cartões (ordem crescente)")
    top_clubes = dados['clube'].value_counts().head(20).sort_values(ascending=True)
    st.bar_chart(top_clubes)

# 7) Top 20 jogadores (ordem crescente)
with tab7:
    st.subheader("👕 Top 20 Jogadores com Mais Cartões (ordem crescente)")
    top_jogadores = dados['atleta'].value_counts().head(20).sort_values(ascending=True)
    st.write(top_jogadores)
    st.bar_chart(top_jogadores)

# 8) Jogador com mais cartões
with tab8:
    st.subheader("🏅 Jogador com Mais Cartões")
    top_jogador = dados['atleta'].value_counts().idxmax()
    total = dados['atleta'].value_counts().max()
    vermelhos = len(dados.query(f'atleta == "{top_jogador}" and cartao == "Vermelho"'))
    amarelos = total - vermelhos

    st.write(f"O jogador que mais levou cartões foi **{top_jogador}** ({total} no total).")
    st.write(f"🔴 Vermelhos: {vermelhos}")
    st.write(f"🟨 Amarelos: {amarelos}")

# 9) Partidas com mais cartões (ordem crescente)
with tab9:
    st.subheader("🔥 Partidas com Mais Cartões (ordem crescente)")
    dados['duelo'] = dados.groupby('partida_id')['clube'].transform(lambda x: ' x '.join(sorted(x.unique())))
    duelos = dados.groupby('duelo').size().reset_index(name='total').sort_values('total', ascending=True).tail(20)
    st.dataframe(duelos)

# 10) Minuto com mais cartões
with tab10:
    st.subheader("⏳ Minutos com Mais Cartões")
    minutos = dados.groupby('minuto').size().sort_values(ascending=False)
    st.write(f"📍 Minuto com mais cartões: {minutos.idxmax()} ({minutos.max()})")
    st.bar_chart(minutos.head(10).sort_values(ascending=True))


