# Exploracao_de_dados.py
import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configurações gerais
st.set_page_config(page_title='Análise de Dados Agrícolas', layout='wide')
st.title('Análise de Dados de Sensoriamento Agrícola')

# ================================================
# 1. Carregar os Dados
# ================================================
st.header('1. Carregar os Dados')
df = pd.read_csv('data.csv')

# Converter timestamp para datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp')

# Verificar e remover colunas duplicadas
df = df.loc[:, ~df.columns.duplicated()]

# Resetar o índice para evitar problemas
df = df.reset_index(drop=True)

# Mostrar os primeiros registros
st.subheader('Visualização dos Dados')
st.dataframe(df.head())

# ================================================
# 2. Visão Geral dos Dados
# ================================================
st.header('2. Visão Geral dos Dados')

# Informações básicas
st.subheader('Informações do DataFrame')
st.write(f'**Linhas:** {df.shape[0]}')
st.write(f'**Colunas:** {df.shape[1]}')
st.write(f'**Período dos Dados:** {df["timestamp"].min().date()} a {df["timestamp"].max().date()}')

# Tipos de dados
st.subheader('Tipos de Dados')
df_types = pd.DataFrame({
    'Coluna': df.columns,
    'Tipo': df.dtypes.astype(str)
})
st.dataframe(df_types)

# ================================================
# 3. Análise Univariada
# ================================================
st.header('3. Análise Univariada')
numeric_columns = ['temperatura_c', 'umidade_percent', 'ph', 'fosforo_mg_kg', 'potassio_mg_kg']

# Histogramas com destaque para pH em azul
st.subheader('Distribuições das Variáveis')
for col in numeric_columns:
    fig = px.histogram(
        df,
        x=col,
        nbins=30,
        title=f'Distribuição de {col}',
        marginal='box',
        color_discrete_sequence=['#1f77b4'] if col == 'ph' else px.colors.qualitative.Plotly
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráficos temporais
st.subheader('Evolução Temporal das Variáveis')

def criar_grafico_temporal(df, coluna, titulo):
    fig = go.Figure()
    line_color = '#1f77b4'  # Azul para todas as variáveis
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df[coluna],
        mode='lines',
        name=coluna,
        line=dict(color=line_color, width=2)
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title='Data e Hora',
        yaxis_title=coluna,
        template='plotly_white',
        hovermode='x unified'
    )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig

for col in numeric_columns:
    fig = criar_grafico_temporal(df, col, f'Evolução de {col} ao longo do tempo')
    st.plotly_chart(fig, use_container_width=True)

# ================================================
# 4. Análise Bivariada
# ================================================
st.header('4. Análise Bivariada')

# Gráficos de dispersão com pH 
st.subheader('Relações entre Variáveis')
st.markdown("""
**Escala de Cores do pH:**
- <span style='color:#a1c9f4;'>Azul Claro</span>: Valores mais baixos
- <span style='color:#1f77b4;'>Azul Médio</span>: Valores intermediários
- <span style='color:#014182;'>Azul Escuro</span>: Valores mais altos
""", unsafe_allow_html=True)

variable_pairs = [
    ('temperatura_c', 'umidade_percent'),
    ('ph', 'fosforo_mg_kg'),
    ('potassio_mg_kg', 'fosforo_mg_kg'),
    ('temperatura_c', 'potassio_mg_kg')
]

for x_var, y_var in variable_pairs:
    fig = px.scatter(
        df,
        x=x_var,
        y=y_var,
        color='ph',
        color_continuous_scale='Blues',
        title=f'{y_var} vs {x_var} (Colorido por pH)',
        labels={
            x_var: x_var.replace('_', ' ').title(),
            y_var: y_var.replace('_', ' ').title(),
            'ph': 'pH'
        },
        hover_data=['timestamp']
    )
    fig.update_coloraxes(
    colorbar=dict(
        title='pH',
        orientation='v',  # Vertical
        x=1.1,           # Posição à direita do gráfico
        y=0.5,           # Centralizada verticalmente
        thickness=20,    # Largura da barra
        len=1         
    )
)

    st.plotly_chart(fig, use_container_width=True)
    
    corr = df[x_var].corr(df[y_var])
    st.write(f"**Correlação entre {x_var} e {y_var}:** {corr:.2f}")

# Matriz de dispersão com cor do pH em azul
st.subheader('Matriz de Dispersão (Colorido por pH)')
fig = px.scatter_matrix(
    df,
    dimensions=numeric_columns,
    color='ph',
    color_continuous_scale='Blues',
    title='Relações entre Todas as Variáveis (Colorido por pH)',
    hover_data=['timestamp']
)
fig.update_coloraxes(
    colorbar=dict(
        title='pH',
        orientation='v',
        x=1.02,
        y=0.5,
        thickness=20,
        len=1
    )
)

fig.update_layout(
    margin=dict(r=100) 
)

# ================================================
# 5. Análise de Correlação
# ================================================
st.header('5. Análise de Correlação')

# Mapa de calor
st.subheader('Mapa de Calor de Correlação')
corr = df[numeric_columns].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='Blues', ax=ax, center=0,
            annot_kws={"size": 10, "weight": "bold"})
plt.title('Correlação entre Variáveis', pad=20)
st.pyplot(fig)

# ================================================
# 7. Análise Interativa
# ================================================
st.header('7. Análise Interativa')

st.markdown("""
### Explore as relações entre variáveis
Selecione as variáveis para análise e observe como o pH influencia as relações.
""")

col1, col2 = st.columns(2)
with col1:
    x_var = st.selectbox('Selecione o Eixo X:', options=numeric_columns)
with col2:
    y_var = st.selectbox('Selecione o Eixo Y:', options=numeric_columns)

if x_var == y_var:
    st.warning("Por favor, selecione variáveis diferentes para os eixos X e Y.")
else:
    fig = px.scatter(
        df,
        x=x_var,
        y=y_var,
        color='ph',
        color_continuous_scale='Blues',
        title=f'Relação entre {x_var} e {y_var} (Colorido por pH)',
        labels={
            x_var: x_var.replace('_', ' ').title(),
            y_var: y_var.replace('_', ' ').title(),
            'ph': 'pH'
        },
        hover_data=['timestamp'],
        size_max=15
    )
    
    fig.update_coloraxes(
    colorbar=dict(
        title='pH',
        orientation='v',
        x=1.1,
        y=0.5,
        thickness=20,
        len= 1
    )
)
    fig.update_layout(
    margin=dict(r=100)  # Aumenta a margem direita para acomodar a barra
)
    fig.update_traces(marker=dict(size=10, opacity=0.7))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise estatística
    st.subheader('Análise Estatística')
    corr_value = df[x_var].corr(df[y_var])
    st.write(f"**Correlação de Pearson:** {corr_value:.2f}")
    
    # Mostrar estatísticas por faixa de pH
    st.write("**Estatísticas por Faixa de pH:**")
    df['pH Category'] = pd.cut(df['ph'], 
                              bins=[df['ph'].min(), df['ph'].median(), df['ph'].max()], 
                              labels=['Baixo', 'Alto'])
    stats = df.groupby('pH Category')[[x_var, y_var]].mean()
    st.dataframe(stats.style.format("{:.2f}").background_gradient(cmap='Blues'))