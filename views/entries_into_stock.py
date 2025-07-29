import streamlit as st
import pandas as pd
from datetime import datetime, date
import time
from Functions.treating_data_from_sheets import *
from Functions.get_data_from_sheets import *
from Functions.dictionaries import *
from Functions.mongo import atualizar_estoque
from pymongo import MongoClient 

st.title("Entradas no Estoque 🚚")

# Seletor de data
col_data, _ = st.columns([1, 3])
with col_data:
    data_selecionada = st.date_input(
        "Selecione a data:",
        value=date.today(),
        min_value=date.today(),
        max_value=date.today()
        )
    

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
        st.number_input("Favor preencher o número da Nota Fiscal 📑",min_value=0,step=1)
        fornecedor_selecionado = st.selectbox("Escolha um Fornecedor 🤝: ",options=fornecedores_unicos,index= None)
        procedimentos = [p for p, f in suplier_dict.items() if f == fornecedor_selecionado]
        produtos = st.multiselect("Escolha um produto 💊: ",options=procedimentos)

        # Dicionário para armazenar as quantidades
        quantidades = {}

        for produto in produtos:
            # Cria um campo de texto para cada produto selecionado #f"qtd_{produto}" cria uma chave única para cada produto
            quantidade = st.number_input(f"Quantidade de {produto}", key=f"qtd_{produto}",min_value=0,step=1)
            quantidades[produto] = quantidade

        st.write(quantidades)


    else:
        branch_optin = st.selectbox("Selecione a Unidade que Emprestou 🌐",unidades_options,index= None)
        fornecedor_selecionado = st.selectbox("Escolha um Fornecedor 🤝: ",options=fornecedores_unicos,index= None)
        procedimentos = [p for p, f in suplier_dict.items() if f == fornecedor_selecionado]
        produtos = st.multiselect("Escolha um produto 💊: ",options=procedimentos)

        # Dicionário para armazenar as quantidades
        quantidades = {}

        for produto in produtos:
            # Cria um campo de texto para cada produto selecionado #f"qtd_{produto}" cria uma chave única para cada produto
            quantidade = st.number_input(f"Quantidade de {produto}", key=f"qtd_{produto}",min_value=0,step=1)
            quantidades[produto] = quantidade

else:
    st.warning("Selecione uma Opção")

if enterie_option and quantidades:
    if st.button("✅ Confirmar Entrada no Estoque"):
        try:
            # Converter quantidades para inteiro
            produtos_quantidades = {
                produto: int(qtd) 
                for produto, qtd in quantidades.items() 
                if qtd > 0  # Ignora quantidades zero/negativas
            }
            
            # Data no formato MongoDB
            data_mongo = datetime.combine(data_selecionada, datetime.min.time())
                    
            # Atualizar o estoque geral
            atualizar_estoque(data_mongo, produtos_quantidades)
            
            success_placeholder = st.empty()
            success_placeholder.success("✅ Entrada registrada com sucesso!")
            
            countdown_placeholder = st.empty()
            for i in range(5, 0, -1):
                countdown_placeholder.markdown(f"🔄 Atualizando página em **{i}** segundos...")
                time.sleep(1)
            
            # Força um refresh completo da aplicação
            st.session_state.refresh = True
            st.rerun()
            
        except Exception as e:
            st.error(f"Erro: {e}")

# Adicione no início do script, após os imports
if 'refresh' in st.session_state:
    del st.session_state.refresh
    st.rerun()