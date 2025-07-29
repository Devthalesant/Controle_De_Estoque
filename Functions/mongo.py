from pymongo.mongo_client import MongoClient, UpdateOne
from pymongo.server_api import ServerApi
import pandas as pd
import streamlit as st

#para funcionar: base = df.to_dict(orient='records')

uri = st.secrets.mongo_credentials.uri


def subir_dados_mongodb(database_name, collection_name, dados):
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]
    
    if not dados:
        return None
    
    # Extrai a data do primeiro documento (assumindo que todos são da mesma data)
    data_estoque = dados[0]['metadata']['data_estoque']
    
    # 1. Primeiro remove contagens existentes da mesma data
    collection.delete_many({"metadata.data_estoque": data_estoque})
    
    # 2. Depois insere os novos dados
    insert_result = collection.insert_many(dados)
    
    return insert_result

def pegar_dados_mongodb(database_name,collection_name, query=None):
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    # Use empty query if none is provided
    if query is None:
        query = {}

    # Apply the query to filter documents
    filtered_documents = collection.find(query)

    data = list(filtered_documents)
    df = pd.DataFrame(data).drop(columns=['_id'], errors='ignore')

    return df

def deletar_todos_documentos(database_name, collection_name, query=None):
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    # Delete all documents if no query is specified
    if query is None:
        result = collection.delete_many({})
    else:
        result = collection.delete_many(query)

    client.close()


def atualizar_estoque(data, produtos_quantidades):
    client = MongoClient(uri)
    db = client["controle_de_estoque"]
    collection = db["contagens_diarias"]
    
    for produto, quantidade in produtos_quantidades.items():
        # Busca se já existe registro do produto naquela data
        filtro = {
            "metadata.data_estoque": data,
            "estoque.procedimento": produto
        }
        
        # Atualiza ou insere o novo valor
        collection.update_one(
            filtro,
            {"$inc": {"estoque.$.quantidade": quantidade}},  # Incrementa a quantidade
            upsert=True  # Cria novo registro se não existir
        )