import streamlit as st
import pandas as pd
from datetime import datetime
from Functions.treating_data_from_sheets import *
from Functions.get_data_from_sheets import *
from Functions.dictionaries import *

st.title("Entradas no Estoque 🚚")

select_options = ['Recebi um Pedido','Recebi um Empréstimo']

unidades_options = [
            "ALPHAVILLE","GUARULHOS","JARDINS", "LAPA",
            "MOOCA", "MOEMA", "OSASCO", "IPIRANGA",
            "ITAIM","SÃO BERNARDO", "SANTO AMARO", "SANTOS",
            "TATUAPÉ", "TUCURUVI","VILA MASCOTE"]

suplier_dict = procedimentos_fornecedores
fornecedores_unicos = sorted(set(procedimentos_fornecedores.values()))

enterie_option = st.selectbox("Selecione o tipo de Entrada ⬆️", select_options,index= None)

if enterie_option:
    if enterie_option == "Recebi um Pedido":
        st.text_input("Favor preencher o número da Nota Fiscal 📑")
        fornecedor_selecionado = st.selectbox("Escolha um Fornecedor 🤝: ",options=fornecedores_unicos,index= None)
        procedimentos = [p for p, f in procedimentos_fornecedores.items() if f == fornecedor_selecionado]
        produtos = st.multiselect("Escolha um produto 💊: ",options=procedimentos)

    else:
        branch_optin = st.selectbox("Selecione a Unidade que Emprestou 🌐",unidades_options,index= None)
        fornecedor_selecionado = st.selectbox("Escolha um Fornecedor 🤝: ",options=fornecedores_unicos,index= None)
        procedimentos = [p for p, f in procedimentos_fornecedores.items() if f == fornecedor_selecionado]
        produtos = st.multiselect("Escolha um produto 💊: ",options=procedimentos)
else:
    st.warning("Selecione uma Opção")
    