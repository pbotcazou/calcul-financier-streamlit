import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

st.set_page_config(page_title="Calcul Financier", layout="wide")

# Création des identifiants
names = ["Primael Botcazou", "Alice Dupont"]
usernames = ["primael", "alice"]
# Mots de passe hashés (motdepasse123, monmdpsecret)
hashed_passwords = [
    "$2b$12$HxhCtuUGqYvCBvDD/z5H9O4dC5b6/v5mTmcZAp9t3V9hvx2TxC9VW",
    "$2b$12$7w9M6DK1xGgnR8GUfN81Ze7qHmrHPYPzIMR2p4OtfozD2oy2ZqWiG"
]

credentials = {
    "usernames": {
        usernames[0]: {"name": names[0], "password": hashed_passwords[0]},
        usernames[1]: {"name": names[1], "password": hashed_passwords[1]},
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "cookie_calcul_financier",
    "signature_key_123",
    cookie_expiry_days=0.1
)

name, authentication_status, username = authenticator.login("main", "Connexion")


if authentication_status:
    
    st.write(f"Bienvenue {name} !")
    st.title("📊 Tableau Financier Automatisé")

    # Sidebar - paramètres
    st.sidebar.header("Paramètres")
    taux_is = st.sidebar.radio("Taux d'IS", [0.25, 0.15])

    annees = ["2023", "2024"]
    colonnes = [
        "Facturation", "PCA N", "PCA N-1", "Encours N", "Encours N-1", "Autre produit", "Frais généraux",
        "Impôts", "Charges personnel", "Salaires Bruts",
        "Reprises et transferts", "Autres produits", "Dotations amortissements", "Autres charges",
        "Produits financiers", "Charges financières",
        "Résultat exceptionnel", "Réintégrations fiscales", "Deductions fiscales",
        "Participation Année N", "Participation Année N-1",
        "Réductions IS",
        "S",
        "C"
    ]

    df = pd.DataFrame(index=colonnes, columns=annees)

    st.subheader("🔢 Entrée des données")
    for annee in annees:
        with st.expander(f"Saisir les données pour {annee}"):
            for col in colonnes:
                safe_col = col.replace(" ", "_").replace("-", "_minus_").lower()
                valeur = st.number_input(f"{col} ({annee})", step=1.0, format="%.2f", key=f"input_{annee}_{safe_col}")
                df.loc[col, annee] = valeur

    def calculs(df, taux_is):
        results = {}
        for annee in annees:
            fact = float(df.loc["Facturation", annee])
            pca_n = float(df.loc["PCA N", annee])
            pca_n_1 = float(df.loc["PCA N-1", annee])
            enc_n = float(df.loc["Encours N", annee])
            enc_n_1 = float(df.loc["Encours N-1", annee])
            autre_prod = float(df.loc["Autre produit", annee])
            frais_gen = float(df.loc["Frais généraux", annee])
            impots = float(df.loc["Impôts", annee])
            charges_pers = float(df.loc["Charges personnel", annee])
            salaires = float(df.loc["Salaires Bruts", annee])
            rep_trans = float(df.loc["Reprises et transferts", annee])
            autres_prod = float(df.loc["Autres produits", annee])
            dot_amort = float(df.loc["Dotations amortissements", annee])
            autres_charges = float(df.loc["Autres charges", annee])
            prod_fin = float(df.loc["Produits financiers", annee])
            charg_fin = float(df.loc["Charges financières", annee])
            res_excep = float(df.loc["Résultat exceptionnel", annee])
            reinteg_fisc = float(df.loc["Réintégrations fiscales", annee])
            deduc_fisc = float(df.loc["Deductions fiscales", annee])
            partN = float(df.loc["Participation Année N", annee])
            partN_1 = float(df.loc["Participation Année N-1", annee])
            reduc_is = float(df.loc["Réductions IS", annee])
            s = float(df.loc["S", annee])
            c = float(df.loc["C", annee])

            CA = fact - pca_n + pca_n_1 + enc_n - enc_n_1
            prod_expl = CA + autre_prod
            VA = prod_expl - frais_gen
            EBE = VA - impots - charges_pers
            res_expl = EBE + rep_trans + autres_prod - dot_amort - autres_charges
            RCAI = res_expl + prod_fin - charg_fin

            if EBE < 0.08 * CA:
                interet = 0
            elif EBE < 0.12 * CA:
                interet = 0.03 * EBE
            elif EBE < 0.16 * CA:
                interet = 0.04 * EBE
            elif EBE < 0.20 * CA:
                interet = 0.05 * EBE
            else:
                interet = 0.06 * EBE

            if VA != 0:
                part = 0.5 * (RCAI - 0.05 * c) * (s / VA)
            else:
                part = 0

            IS = taux_is * RCAI - reduc_is
            RCNET = RCAI + res_excep - interet - part - IS
            B = RCAI + res_excep + reinteg_fisc - deduc_fisc + partN - partN_1 - interet
            B1 = RCAI - IS

            results[annee] = {
                "CA": CA,
                "Produits d'exploitation": prod_expl,
                "VA": VA,
                "EBE": EBE,
                "Résultat d'exploitation": res_expl,
                "Résultat courant (RCAI)": RCAI,
                "Intéressement": interet,
                "Participation": part,
                "IS": IS,
                "RCNET": RCNET,
                "Résultat fiscal (B)": B,
                "B1 = RCAI - IS": B1
            }

        return pd.DataFrame(results)

    st.subheader("📘 Résultats Calculés")
    resultats = calculs(df, taux_is)
    st.dataframe(resultats.style.format("{:.2f}"), height=600, use_container_width=True)

    # Bouton de déconnexion dans la sidebar
    authenticator.logout("Déconnexion", "sidebar")

elif authentication_status == False:
    st.error("Nom d’utilisateur ou mot de passe incorrect")

elif authentication_status is None:
    st.warning("Veuillez vous connecter")
