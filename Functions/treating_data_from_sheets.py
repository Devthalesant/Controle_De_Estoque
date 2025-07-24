from get_data_from_sheets import *
import pandas as pd


######################################################################################### 
#Treating the counts

def treating_counts_date():
    df_contagens = load_dataframe("Aux - Contagem - Respostas")

    # Ordenar por data
    df_contagens = df_contagens.sort_values('Timestamp', ascending=False)

    # Pegar as 2 últimas datas em que tivemos contagem
    ultimas_duas_datas = df_contagens['Timestamp'].head(2)

    # Pega a data mais recente (a primeira após ordenar)
    ultima_data = df_contagens['Timestamp'].iloc[0]
    penultima_data = df_contagens['Timestamp'].iloc[1]

    # Formatando as datas
    ultima_data = pd.to_datetime(ultima_data).date()
    penultima_data = pd.to_datetime(penultima_data).date()

    # Gera todas as datas no intervalo (de penúltima até um dia antes da última)
    datas_intervalo = pd.date_range(
        start=penultima_data,
        end=ultima_data - pd.Timedelta(days=1),  # Exclui a última data
        freq='D'  # Frequência diária
    ).date.tolist()  # Converte para lista de datas

    # formatando as daras da lista  - List comprehension
    datas_formatadas = [data.strftime('%d/%m/%Y') for data in datas_intervalo]

    # Filtrando o DataFrame para apenas essas 2 linhas
    df_contagens_filtrado = df_contagens[df_contagens['Timestamp'].isin(ultimas_duas_datas)]

    # Agora fazemos a transformação (melt) para ter produtos como linhas
    df_contagens_transformado = df_contagens_filtrado.melt(
        id_vars=['Timestamp', 'Email Address'], 
        var_name='Produto', 
        value_name='Quantidade'
    )

    # Tranformando as datas
    df_contagens_transformado['Timestamp'] = pd.to_datetime(df_contagens_transformado['Timestamp'])
    df_contagens_transformado['Timestamp'] = df_contagens_transformado['Timestamp'].dt.strftime('%d/%m/%Y')

    # Pivotamos para ter as datas como colunas
    df_contagens_final = df_contagens_transformado.pivot(
        index='Produto', 
        columns='Timestamp', 
        values='Quantidade'
    ).reset_index()

    # Remove o nome do eixo das colunas
    df_contagens_final.columns.name = None  


    # Resultado final
    return df_contagens_final, datas_formatadas

######################################################################################### 
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