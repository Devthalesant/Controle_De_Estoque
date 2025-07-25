from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import streamlit as st
from .mongo import *
from .get_data_from_sheets import *
from .treating_data_from_sheets import *
import pandas as pd 
import streamlit as st

def contagem_mais_recente():
    df_contagem_today, datas_formatadas = treating_counts_date()

    df_contagem_today = df_contagem_today.iloc[:,[0,2]]

    df_contagem_today = df_contagem_today.to_dict(orient='records')

    return df_contagem_today

