import streamlit as st
import pandas as pd
from datetime import datetime
from Functions.treating_data_from_sheets import *
from Functions.get_data_from_sheets import *

today = datetime.now()
today = today.strftime("%d/%m/%Y")

st.title("Controle de Estoque - Praia Grande 🏖️")
st.header(f"📅 Data de Análise: {today}")
st.divider()

## Df de análise D e D-1 
st.subheader("Verificação do Estoque💉:")

# Pegando os dados das planilhas e tratando
df_contagens_final, datas_formatadas = treating_counts_date()
#Pegando os dados tratados e merging
df_analise = merging_stocks_outputs_and_counts(df_contagens_final,datas_formatadas)

st.dataframe(df_analise)



