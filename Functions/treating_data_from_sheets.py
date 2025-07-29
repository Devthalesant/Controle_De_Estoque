from .get_data_from_sheets import *
import pandas as pd

#handling stocks output

def merging_stocks_outputs_and_counts(df_contagens_final,datas_formatadas):
    df_baixas = load_dataframe("Aux - Baixas Compiladas")

    # Tratando as datas
    df_baixas['Data'] = pd.to_datetime(df_baixas['Data'])
    df_baixas['Data'] = df_baixas['Data'].dt.strftime('%d/%m/%Y')

    # Pegando somente as baixas que estão no período de contagnes 
    df_baixas = df_baixas.loc[df_baixas['Data'].isin(datas_formatadas)]

    # Agrupando por produto
    df_baixas_gp_produto = df_baixas.groupby('Produto').agg({'Quantidade' : 'sum'}).reset_index()

    # Merge do df das 2 últimas contagens com as baixas do período
    df_analise = pd.merge(df_contagens_final,df_baixas_gp_produto,
                        how='left',
                        on="Produto")


    # tRATANDO Nan
    df_analise = df_analise.fillna(0)

    # Renomeando a coluna 
    df_analise = df_analise.rename(columns={'Quantidade' : 'Baixas_do_período'})

    # Criando a coluna de Estoque previsto 
    # estou pegando por index as colunas pois o nome varia com as datas
    df_analise["Estoque_Previsto"] = df_analise.iloc[:, 1] - df_analise['Baixas_do_período']

    # Criando a coluna que mostra as diferenças do estoque
    # estou pegando por index as colunas pois o nome varia com as datas
    df_analise["Diferenças"] = df_analise.iloc[:,2] - df_analise['Estoque_Previsto']

    return df_analise