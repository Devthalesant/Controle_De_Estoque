import streamlit as st
import pandas as pd
from datetime import datetime
from Functions.treating_data_from_sheets import *
from Functions.get_data_from_sheets import *
from Functions.setting_today_counts_mongo import contagem_mais_recente
from Functions.mongo import *

today = datetime.now()
formated_today = today.strftime("%d/%m/%Y")

st.title("Controle de Estoque - Praia Grande 🏖️")
st.header(f"📅 Data de Análise: {formated_today}")
st.divider()

## Df de análise D e D-1 
st.subheader("Verificação do Estoque💉:")

# Pegando os dados das planilhas e tratando
df_contagens_final, datas_formatadas = treating_counts_date()
#Pegando os dados tratados e merging
df_analise = merging_stocks_outputs_and_counts(df_contagens_final,datas_formatadas)

st.dataframe(df_analise)