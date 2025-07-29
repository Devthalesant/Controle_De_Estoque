import streamlit as st
import pandas as pd
import datetime
from Functions.treating_data_from_sheets import *
from Functions.get_data_from_sheets import *
from Functions.mongo import *

today = datetime.datetime.now()
formated_today = today.strftime("%d/%m/%Y")

st.title("Controle de Estoque - Praia Grande 🏖️")
st.header(f"📅 Data de Análise: {formated_today}")
st.divider()

## Df de análise D e D-1 
st.subheader("Verificação do Estoque💉:")

## Usando função para pegar dados do Mongo, função complexa. entender depois.
df = pegar_ultimas_duas_datas_mongodb("controle_de_estoque","contagens_diarias")

# Formatando a data
df["data_estoque"] = pd.to_datetime(df["data_estoque"])
df["data_estoque"] = df["data_estoque"].dt.strftime("%d/%m/%Y")

#Pivotando a tebela para visualização de comparação 
df_pivot = df.pivot_table(
    index='procedimento',
    columns='data_estoque',
    values='quantidade',
    aggfunc='first'
)

# Renomeando Index para reaporveitar a função de merging_stocks_outputs_and_counts
df_pivot.index.name = "Produto"

ultima_data = df_pivot.columns[1]
penultima_data = df_pivot.columns[0]

# Formatando as datas
ultima_data = pd.to_datetime(ultima_data).date()
penultima_data = pd.to_datetime(penultima_data).date()

# Gera todas as datas no intervalo (de penúltima até um dia antes da última)
datas_intervalo = pd.date_range(
    start=penultima_data,
    end=ultima_data - pd.Timedelta(days=1),  # Exclui a última data
    freq='D'  # Frequência diária
).date.tolist()  # Converte para lista de datas

# formatando as datas da lista  - List comprehension
datas_formatadas = [data.strftime('%d/%m/%Y') for data in datas_intervalo]

# CHamando a função que faz merge das contagens com as bauxas do período e compara.
df_analise = merging_stocks_outputs_and_counts(df_pivot,datas_formatadas)
st.dataframe(df_analise)
