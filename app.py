import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# Configuration de la page
st.set_page_config(page_title="Calcul Financier", layout="wide")

# Liste des utilisateurs
names = ["Primael Botcazou", "Alice Dupont"]
usernames = ["primael", "alice"]
passwords = ["motdepasse123", "monmdpsecret"]

# Hash des mots de passe
hashed_passwords = stauth.Hasher(passwords).generate()

# Création du dictionnaire des identifiants
credentials = {
    "usernames": {
        usernames[i]: {"name": names[i], "password": hashed_passwords[i]}
        for i in range(len(usernames))
    }
}

# Initialisation de l'authentificateur
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="cookie_calcul_financier",
    key="signature_key_123",
    cookie_expiry_days=0.1
)

# Login
name, authentication_status, username = authenticator.login("main", "Connexion")

# Authentification
if authentication_status:
    st.sidebar.success(f"Connecté : {name}")
    authenticator.logout("Déconnexion", "sidebar")
    st.title("📊 Tableau Financier Automatisé")

    # Paramètres
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
        "S", "C"
    ]

    df = pd.DataFrame(index=colonnes, columns=annees)

    st.subheader("🔢 Entrée des données")
    for annee in annees:
        with st.expander(f"Saisir les données pour {annee}"):
            for col in colonnes:
                safe_col = col.replace(" ", "_").replace("-", "_").lower()
                valeur = st.number_input(f"{col} ({annee})", step=1.0, format="%.2f", key=f"{annee}_{safe_col}")
                df.loc[col, annee] = valeur

    def calculs(df, taux_is):
        results = {}
        for annee in annees:
            try:
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
            except:
                continue

            CA = fact - pca_n + pca_n_1 + enc_n - enc_n_1
            prod_expl = CA + autre_prod
            VA = prod_expl - frais_gen
            EBE = VA - impots - charges_pers
            res_expl = EBE + rep_trans + autres_prod - dot_amort - autres_charges
            RCAI = res_expl + prod_fin - charg_fin

            # Intéressement
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

            part = 0.5 * (RCAI - 0.05 * c) * (s / VA) if VA != 0 else 0
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
                "RCAI": RCAI,
                "Intéressement": interet,
                "Participation": part,
                "IS": IS,
                "RCNET": RCNET,
                "B": B,
                "B1": B1,
            }
        return pd.DataFrame(results)

    st.subheader("📘 Résultats Calculés")
    resultats = calculs(df, taux_is)
    st.dataframe(resultats.style.format("{:.2f}"), use_container_width=True)

elif authentication_status is False:
    st.error("Nom d’utilisateur ou mot de passe incorrect")

elif authentication_status is None:
    st.warning("Veuillez vous connecter")
