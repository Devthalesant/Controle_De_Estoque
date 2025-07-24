import streamlit as st

st.set_page_config(layout="wide")

# --- PAGE SETUP ---
visualizar_page = st.Page(
    "views/Stock_control_view.py",
    title="Controle de Estoque",
    icon=":material/thumb_up:",
    default=True,
)

entradas_page = st.Page(
    "views/entries_into_stock.py",
    title="Entradas",
    icon=":material/thumb_up:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Visualização - Estoque 💉": [visualizar_page],
        "Entradas - Estoque 📦": [entradas_page]
    }
)

# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")


# --- RUN NAVIGATION ---
pg.run()