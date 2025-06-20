import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configurações gerais
st.set_page_config(page_title='Modelagem Preditiva Agrícola', layout='wide')
st.title('Modelagem Preditiva para Parâmetros Agrícolas')

# Carregar os dados
df = pd.read_csv('data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# ================================================
# 1. Filtros na Barra Lateral
# ================================================
st.sidebar.title('Filtros de Dados')
st.sidebar.subheader('Seleção de Intervalos')

# Criar filtros para todas as variáveis numéricas
filters = {}
numeric_columns = ['temperatura_c', 'umidade_percent', 'ph', 'fosforo_mg_kg', 'potassio_mg_kg']

for col in numeric_columns:
    min_val = float(df[col].min())
    max_val = float(df[col].max())
    filters[col] = st.sidebar.slider(
        f'{col.replace("_", " ").title()}:',
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val)
    )

# Filtro de data
min_date = df['timestamp'].min()
max_date = df['timestamp'].max()
date_range = st.sidebar.date_input(
    'Intervalo de Datas:',
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Aplicar filtros
filtered_df = df.copy()
for col, (min_val, max_val) in filters.items():
    filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]

# Filtrar por data
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['timestamp'] >= pd.Timestamp(start_date)) & 
        (filtered_df['timestamp'] <= pd.Timestamp(end_date))
    ]

# Mostrar estatísticas dos dados filtrados
st.sidebar.subheader('Dados Filtrados')
st.sidebar.write(f"Registros: {len(filtered_df)}")
st.sidebar.write(f"Período: {filtered_df['timestamp'].min().date()} a {filtered_df['timestamp'].max().date()}")

# ================================================
# 2. Preparar os Dados para Modelagem
# ================================================
st.header('2. Preparação dos Dados')

# Selecionar variável alvo
st.subheader('Seleção de Variável Alvo')
target_var = st.selectbox(
    'Selecione a variável para prever:', 
    options=numeric_columns,
    index=2  # Seleciona pH por padrão
)

# Explicar a seleção
st.info(f"Você está modelando para prever: **{target_var.replace('_', ' ').title()}**")

# Selecionar features - apenas colunas numéricas originais (exceto target)
feature_options = [col for col in numeric_columns if col != target_var]
selected_features = st.multiselect(
    'Selecione as features para o modelo:',
    options=feature_options,
    default=feature_options
)

# Verificar seleção
if not selected_features:
    st.error("Por favor, selecione pelo menos uma feature para o modelo.")
    st.stop()

# Separar variáveis (AGORA DEFININDO X_train, X_test, etc.)
X = filtered_df[selected_features]
y = filtered_df[target_var]

# Dividir dados ANTES de mostrar estatísticas
test_size = st.slider('Proporção para teste:', 0.1, 0.5, 0.2, 0.05)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

# Agora mostrar estatísticas (DEPOIS da divisão)
st.subheader('Dados Selecionados para Modelagem')
st.write(f"**Features selecionadas:** {', '.join(selected_features)}")
st.write(f"**Total de registros:** {len(X)}")
st.write(f"**Dados de treino:** {len(X_train)} registros ({100*(1-test_size):.0f}%)")
st.write(f"**Dados de teste:** {len(X_test)} registros ({100*test_size:.0f}%)")

# ================================================
# 3. Treinar e Avaliar o Modelo
# ================================================
st.header('3. Treinamento e Avaliação do Modelo')

# Configurar modelo
st.subheader('Configuração do Modelo')
n_estimators = st.slider('Número de Árvores:', 10, 200, 100, 10)
max_depth = st.slider('Profundidade Máxima:', 1, 20, 10, 1)
min_samples_split = st.slider('Mínimo de Amostras para Divisão:', 2, 20, 2, 1)

# Treinar modelo
model = RandomForestRegressor(
    n_estimators=n_estimators,
    max_depth=max_depth,
    min_samples_split=min_samples_split,
    random_state=42
)

with st.spinner('Treinando o modelo...'):
    model.fit(X_train, y_train)
    st.success('Modelo treinado com sucesso!')

# Avaliar modelo
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Métricas de avaliação
st.subheader('Desempenho do Modelo')
col1, col2 = st.columns(2)
col1.metric("R² (Coeficiente de Determinação)", f"{r2:.3f}")
col2.metric("RMSE (Raiz do Erro Quadrático Médio)", f"{rmse:.3f}")

# Gráfico de valores reais vs preditos
st.subheader('Valores Reais vs Preditos')
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=y_test, y=y_pred, 
    mode='markers',
    name='Predições',
    marker=dict(color='royalblue', opacity=0.6)
))
fig.add_trace(go.Scatter(
    x=[y.min(), y.max()], y=[y.min(), y.max()],
    mode='lines',
    name='Linha de Referência',
    line=dict(color='red', dash='dash')
))
fig.update_layout(
    title='Comparação entre Valores Reais e Preditos',
    xaxis_title='Valor Real',
    yaxis_title='Valor Predito',
    showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

# Importância das features
st.subheader('Importância das Features')
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': selected_features,
    'Importância': importances
}).sort_values('Importância', ascending=False)

fig = px.bar(
    feature_importance_df,
    x='Importância',
    y='Feature',
    orientation='h',
    title='Importância Relativa das Features'
)
st.plotly_chart(fig, use_container_width=True)

# ================================================
# 4. Previsões em Tempo Real
# ================================================
st.header('4. Simulação de Previsão')

st.subheader('Insira os valores para previsão:')
input_data = {}

# Criar colunas para inputs
cols = st.columns(3)
for i, feature in enumerate(selected_features):
    with cols[i % 3]:
        min_val = float(X[feature].min())
        max_val = float(X[feature].max())
        default_val = float(X[feature].median())
        
        input_data[feature] = st.number_input(
            f"{feature.replace('_', ' ').title()}:",
            min_value=min_val,
            max_value=max_val,
            value=default_val,
            step=0.1
        )

# Botão de previsão
if st.button('Realizar Previsão'):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    
    st.success(f"**Previsão de {target_var.replace('_', ' ').title()}:** {prediction:.2f}")
    
    # Mostrar comparação com valores médios
    st.subheader('Comparação com Valores Médios')
    avg_value = filtered_df[target_var].mean()
    diff = prediction - avg_value
    
    col1, col2 = st.columns(2)
    col1.metric("Valor Previsto", f"{prediction:.2f}")
    col2.metric("Valor Médio no Conjunto", f"{avg_value:.2f}", f"{diff:.2f}")