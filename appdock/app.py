import streamlit as st
import pandas as pd
import pyodbc
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# ------------------ CONFIG ------------------

SERVER = 'masterdatabase-apl.database.windows.net'
DATABASE = 'masterdata'
USERNAME = 'PowerBI'
PASSWORD = os.getenv('MDP_SQLServer_masterdata')  # Variable d'environnement
DRIVER = "ODBC Driver 17 for SQL Server"

connection_url = URL.create(
    "mssql+pyodbc",
    username=USERNAME,
    password=PASSWORD,
    host=SERVER,
    database=DATABASE,
    query={"driver": DRIVER, "Encrypt": "yes", "TrustServerCertificate": "yes"}
)

engine = create_engine(connection_url)

# ------------------ Helper ------------------

def format_value(val):
    if pd.isna(val) or val in ["None", "none", "", None]:
        return f'<span style="color:red;">❌ Aucun renseignement</span>'
    return str(val)

def format_currency(val):
    if pd.isna(val) or val in ["None", "none", "", None]:
        return f'<span style="color:red;">❌ Aucun renseignement</span>'
    # Format français : espace pour milliers, virgule pour décimales
    return f'{val:,.2f} €'.replace(",", " ").replace(".", ",")

def format_boolean_icon(val):
    if str(val).strip().lower() in ["true", "1", "oui", "yes"]:
        return '<span style="color:green; font-size:20px;">🟩 ✅</span>'
    return '<span style="color:red; font-size:20px;">⬛ ❌</span>'


def display_customer(customer_row):
    with st.container():
        # Titre avec nom + dossier CEGID
        st.markdown(f"### 👤 {customer_row['name']} ({customer_row['syd_n_de_dossier_cegid']})")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Code NAF**: {format_value(customer_row['syd_naf'])}", unsafe_allow_html=True)
            st.markdown(f"**Forme juridique**: {format_value(customer_row['syd_forme_juridique_sirene'])}", unsafe_allow_html=True)
            st.markdown(f"**CA**: {format_currency(customer_row['syd_ca'])}", unsafe_allow_html=True)
            st.markdown(f"**Salariés**: {format_value(customer_row['syd_total_salaries'])}", unsafe_allow_html=True)

            account_id = customer_row.get("accountid")
            if account_id and pd.notna(account_id):
                account_id = account_id.lower()
                url = f'https://apl.crm4.dynamics.com/main.aspx?appid=32ab0bd5-76c4-eb11-bacc-0022489cbd7e&forceUCI=1&pagetype=entityrecord&etn=account&id={account_id}'
                st.markdown(f'''
                    <a href="{url}" target="_blank">
                        <button style="background-color:GreenYellow; padding:5px; border:none; border-radius:5px; cursor:pointer;">
                            🔗 Lien CRM
                        </button>
                    </a>
                ''', unsafe_allow_html=True)

        with col2:
            st.markdown(f"**Activité**: {format_value(customer_row['syd_activite'])}", unsafe_allow_html=True)
            st.markdown(f"**Première signature**: {format_value(customer_row['syd_premiere_date_de_signature'])}", unsafe_allow_html=True)
            st.markdown(f"**Caisse**: {format_boolean_icon(customer_row['syd_caisse'])}", unsafe_allow_html=True)
            st.markdown(
                f"**Factures**: Fournisseurs: {format_value(customer_row['syd_nbre_annuel_de_factures_fournisseurs'])}, "
                f"Clients: {format_value(customer_row['syd_nb_facture_client'])}, "
                f"Banque: {format_value(customer_row['syd_nbre_annuel_lignes_releves_compte'])}",
                unsafe_allow_html=True
            )

# ------------------ APP ------------------

st.title("🔍 Recherche Client par Numéro CEGID")


st.markdown("""
<style>
/* Cibler tous les inputs de type text (y compris st.text_input) */
input[type="text"] {
    border: 3px solid #4CAF50 !important;  /* bordure verte */
    border-radius: 10px !important;
    padding: 10px !important;
    font-size: 18px !important;
    background-color: #f0fff0 !important;
    outline: none !important;
    color: #000 !important;
    box-sizing: border-box;
}

/* Sur focus */
input[type="text"]:focus {
    border-color: #2E7D32 !important;
    box-shadow: 0 0 8px #81C784 !important;
    background-color: #e6ffe6 !important;
}
</style>
""", unsafe_allow_html=True)

client_code = st.text_input("Entrez le numéro de dossier CEGID du client :", "")



if client_code:
    query = text("""
        SELECT
            a.name,
            a.syd_n_de_dossier_cegid,
            a.syd_naf,
            a.syd_forme_juridique_sirene,
            a.syd_activite,
            a.syd_premiere_date_de_signature,
            a.syd_total_salaries,
            a.accountid,
            a.syd_nbre_annuel_de_factures_fournisseurs,
            a.syd_nb_facture_client,
            a.syd_nbre_annuel_lignes_releves_compte,
            a.syd_caisse,
            a.syd_ca
        FROM CrmAccounts AS a
        WHERE a.syd_n_de_dossier_cegid = :code
    """)

    try:
        with engine.connect() as connection:
            df = pd.read_sql(query, con=connection, params={"code": client_code})

        if df.empty:
            st.warning("⚠️ Aucun client trouvé avec ce numéro.")
        else:
            data = df.iloc[0].to_dict()  # transforme en dict pour plus facile à manipuler
            display_customer(data)

    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des données : {e}")

