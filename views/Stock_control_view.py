import streamlit as st
import pandas as pd
import datetime
from Functions.treating_data_from_sheets import *
from Functions.get_data_from_sheets import *
from Functions.mongo import *
from Functions.dictionaries import procedimentos_fornecedores
import pyperclip

today = datetime.datetime.now()
formated_today = today.strftime("%d/%m/%Y")

st.title("Controle de Estoque - Praia Grande 🏖️")
st.header(f"📅 Data de Análise: {formated_today}")
st.divider()

## Seção de Verificação de Estoque
with st.container(border=True):
    st.subheader("Verificação do Estoque 💉", help="Comparação entre as últimas contagens de estoque")
    
    df = pegar_ultimas_duas_datas_mongodb("controle_de_estoque", "contagens_diarias")
    df["data_estoque"] = pd.to_datetime(df["data_estoque"]).dt.strftime("%d/%m/%Y")

    df_pivot = df.pivot_table(
        index='procedimento',
        columns='data_estoque',
        values='quantidade',
        aggfunc='first'
    ).rename_axis("Produto")

    # Processamento das datas
    ultima_data = pd.to_datetime(df_pivot.columns[-1]).date()
    penultima_data = pd.to_datetime(df_pivot.columns[-2]).date()
    
    datas_formatadas = [
        d.strftime('%d/%m/%Y') 
        for d in pd.date_range(penultima_data, ultima_data - pd.Timedelta(days=1), freq='D').date
    ]

    df_analise = merging_stocks_outputs_and_counts(df_pivot, datas_formatadas)

    # Estilização condicional
    def highlight_diff(val):
        if val > 0:
            return 'background-color: #ffebee; color: #c62828; font-weight: bold'
        elif val < 0:
            return 'background-color: #fff8e1; color: #ff8f00; font-weight: bold'
        return ''

    styled_df = df_analise.style.map(highlight_diff, subset=df_analise.columns[5:])

    # Métricas
    total_itens = len(df_analise)
    itens_com_diff = (df_analise.iloc[:, 5:] != 0).any(axis=1).sum()
    diff_recentes = (df_analise.iloc[:, -1] != 0).sum()

    cols = st.columns(3)
    cols[0].metric("📦 Total Itens", total_itens)
    cols[1].metric("⚠️ Itens com Divergências", itens_com_diff)
    cols[2].metric("🔄 Divergências Recentes", diff_recentes)

    st.divider()

    # Tabela principal
    st.dataframe(
        styled_df.set_properties(**{'text-align': 'center'})
                .set_table_styles([{
                    'selector': 'th',
                    'props': [('text-align', 'center'), ('background-color', '#f5f5f5')]
                }]),
        use_container_width=True,
        height=min(400, 35*(len(df_analise)+1))
    )

# Lista de divergências no estilo da lista de compras
divergencias_df = df_analise[(df_analise.iloc[:, -1] != 0)]  # Pega apenas itens com diferença na última coluna

if not divergencias_df.empty:
    with st.expander("📝 Itens com Divergências Finais", expanded=True):
        # Cabeçalho
        cols = st.columns([5, 2])
        cols[0].markdown("**Produto**")
        cols[1].markdown("**Diferença**")
        st.divider()
        
        # Itens
        for _, row in divergencias_df.iterrows():
            saldo = row.iloc[-1]  # Pega o valor da última coluna (diferença final)
            
            cols = st.columns([5, 2])
            cols[0].write(f"🔹 {row['Produto']}")
            
            if saldo < 0:
                cols[1].markdown(f"🔴 **Faltando {abs(saldo):.0f} unidades**")
            else:
                cols[1].markdown(f"🟢 **Excesso {saldo:.0f} unidades**")
            
            st.markdown("""<hr style="height:1px;margin:0.5rem 0;background-color:#eee" />""", 
                       unsafe_allow_html=True)
## Seção de Lista de Compras
st.divider()
with st.container(border=True):
    st.subheader("📋 Lista de Compras Necessárias")
    
    df_quantidades = load_dataframe("Aux - Procedimentos")
    
    df_quantity_validation = df_analise.iloc[:, [0, 2]].merge(
        df_quantidades,
        left_on="Produto",
        right_on="PROCEDIMENTOS"
    ).drop(columns=["PROCEDIMENTOS"]).rename(columns={"QUANTIDADE_MINIMA": "Quantidade_Mínima"})
    
    df_quantity_validation["Validador"] = df_quantity_validation.iloc[:,1] - df_quantity_validation["Quantidade_Mínima"]
    df_quantity_validation["Compra?"] = df_quantity_validation["Validador"] < 0
    
    df_lista_compras = df_quantity_validation.loc[df_quantity_validation["Compra?"]].copy()
    df_lista_compras['Validador'] = df_lista_compras['Validador'] * (-1)
    lista_compra = df_lista_compras.iloc[:,[0,3]].to_dict(orient="records")

    if len(lista_compra) > 0:
        cols = st.columns([4, 3])
        cols[0].markdown("**Produto**", help="Item que precisa ser comprado")
        cols[1].markdown("**Fornecedor**", help="Fornecedor indicado")
        st.divider()
        
        for item in lista_compra:
            cols = st.columns([4, 3])
            produto = item.get('Produto', 'Nome não disponível')
            
            cols[0].write(f"🔹 {produto}")
            cols[1].write(procedimentos_fornecedores.get(produto, "Fornecedor não cadastrado"))
            st.markdown("""<hr style="height:1px;margin:0.5rem 0;background-color:#eee" />""", 
                       unsafe_allow_html=True)
        
        if st.button("📋 Copiar lista para área de transferência", 
                    help="Clique para copiar a lista completa",
                    type="primary"):
            texto_copia = "\n".join(
                [f"{item['Produto']} - {int(item['Validador'])} unidades - {procedimentos_fornecedores.get(item['Produto'], 'Sem fornecedor')}" 
                 for item in lista_compra]
            )
            try:
                pyperclip.copy(texto_copia)
                st.toast("✅ Lista copiada para a área de transferência!")
            except Exception as e:
                st.error(f"Erro ao copiar: {e}")
                with st.expander("Clique para ver a lista e copiar manualmente"):
                    st.code(texto_copia)
    else:
        st.success("🎉 Nenhum item necessário para compra no momento!")