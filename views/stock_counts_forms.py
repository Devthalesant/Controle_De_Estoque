import streamlit as st
import pandas as pd
from datetime import datetime, date
from Functions.mongo import subir_dados_mongodb

# Configuração da página
st.set_page_config(layout="wide")
st.title("📊 Controle de Estoque Diário")
st.markdown("Preencha a data e as quantidades abaixo")

# Lista de procedimentos
procedimentos = [
    "BOTOX - ALLERGAN", "DERMAROLLER", "DYSPORT", "ENZIMA MELASMA", "GLICOSE",
    "GLÚTEO MAX", "MILIMETRIC INTENSO", "MILIMETRIC LEVE", "MILIMETRIC MODERADO",
    "PRÓ-BELLA", "PRÓ-LIPO", "PRÓ-MESO (M)", "PRÓ-MESO (F)", "RADIESSE",
    "RENNOVA SHAPE-LIDO", "RESTYLANE GEL", "RESTYLANE LYFT", 
    "RESTYLANE SKINBOOSTER VITAL", "RESTYLANE SKINBOOSTER VITAL LIGHT", "SCULPTRA"
]

# Seção de registro
st.subheader("Registro de Quantidades")

# Seletor de data
col_data, _ = st.columns([1, 3])
with col_data:
    data_selecionada = st.date_input(
        "Selecione a data:",
        value=date.today(),
        min_value=date.today(),
        max_value=date.today()
        )

st.markdown("---")

# Dividindo em 2 colunas para os procedimentos
col1, col2 = st.columns(2)
quantidades = {}

with col1:
    for proc in procedimentos[:10]:
        quantidades[proc] = st.number_input(
            f"{proc}",
            min_value=0,
            step=1,
            key=proc,
            format="%d"
        )

with col2:
    for proc in procedimentos[10:]:
        quantidades[proc] = st.number_input(
            f"{proc}",
            min_value=0,
            step=1,
            key=proc,
            format="%d"
        )

st.markdown("---")

if st.button("💾 Salvar Contagem", use_container_width=True):
    # Criar documento para o MongoDB
    documento = {
        "metadata": {
            "data_registro": datetime.now(),  # Quando foi registrado
            "data_estoque": datetime.combine(data_selecionada, datetime.min.time())  # Data do estoque
        },
        "estoque": [
            {"procedimento": proc, "quantidade": qtd} 
            for proc, qtd in quantidades.items()
        ]
    }
    
    # Enviar para o MongoDB
    if subir_dados_mongodb("controle_de_estoque", "contagens_diarias", [documento]):
        st.success(f"Contagem de {data_selecionada.strftime('%d/%m/%Y')} registrada com sucesso!")
    else:
        st.error("Erro ao salvar no banco de dados")