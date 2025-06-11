import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("datanaf.csv")

df = load_data()

st.title("📊 Analyse des temps par Code NAF")
st.write("Entrez un **code NAF** pour afficher les clusters associés et les boxplots interactifs par temps.")

code_naf_input = st.text_input("Code NAF", value="0161Z")

temps_order = ["temps_code1", "temps_code3", "temps_code4", "temps_code5", "temps_code6"]

if code_naf_input:
    filtered = df[df["code_naf"] == code_naf_input]

    if filtered.empty:
        st.warning(f"Aucun résultat trouvé pour le code NAF : {code_naf_input}")
    else:
        st.success(f"Résultats pour le code NAF : {code_naf_input}")

        # Un seul cluster par temps_code (suppression doublons)
        filtered = filtered.drop_duplicates(subset="temps_code", keep="first")
        filtered["temps_code"] = pd.Categorical(filtered["temps_code"], categories=temps_order, ordered=True)
        filtered = filtered.sort_values("temps_code")

        # Affichage tableau simple
        tableau = filtered[["temps_code", "cluster", "mediane"]].rename(columns={
            "temps_code": "Temps",
            "cluster": "Cluster",
            "mediane": "Temps médian"
        })
        st.dataframe(tableau)

        st.write("### Boxplots interactifs combinés")

        fig = go.Figure()

        for _, row in filtered.iterrows():
            q1 = row["q1"]
            mediane = row["mediane"]
            q3 = row["q3"]
            cluster = row["cluster"]
            temps_code = row["temps_code"]

            iqr = q3 - q1
            lower_fence = max(q1 - 1.5 * iqr, 0)
            upper_fence = q3 + 1.5 * iqr

            # Simuler les valeurs pour forcer Plotly à afficher le boxplot voulu
            y_simulated = (
                [lower_fence]*10 +
                [q1]*20 +
                [mediane]*30 +
                [q3]*20 +
                [upper_fence]*10
            )

            fig.add_trace(go.Box(
                y=y_simulated,
                name=f"{temps_code} — Cluster {cluster}",
                boxpoints=False,
                marker_color="royalblue",
                hovertemplate=(
                    f"<b>{temps_code} — Cluster {cluster}</b><br>"
                    f"Lower Fence: {lower_fence:.2f}<br>"
                    f"Q1: {q1:.2f}<br>"
                    f"Médiane: {mediane:.2f}<br>"
                    f"Q3: {q3:.2f}<br>"
                    f"Upper Fence: {upper_fence:.2f}<br>"
                    "<extra></extra>"
                ),
                width=0.7  # largeur plus large
            ))

        fig.update_layout(
            height=600,  # plus grand
            margin=dict(l=50, r=50, t=50, b=50),
            yaxis_title="Temps",
            boxmode='group',
            legend=dict(
                title="Cliquez pour sélectionner/désélectionner",
                traceorder="normal",
                font=dict(size=12),
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )

        st.plotly_chart(fig, use_container_width=True)
