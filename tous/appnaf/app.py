import streamlit as st

def main():
    st.set_page_config(
        page_title="APL Métrage Dashboard",
        page_icon=":chart_with_upwards_trend:",
        layout="wide"
    )

    # Bannière avec titre à gauche et encadré à droite
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background-color: #f0f0f0; border-radius: 8px;">
            <h1 style="margin: 0;">📏 Métrage des nouveaux clients</h1>
            <div style="background-color: rgb(111, 243, 148); padding: 1rem 1.5rem; border-radius: 8px; border: 1px solid #ccc;">
                <strong>🔍 Complétez les champs ci-dessous pour voir le tarif correspondant :</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Veuillez saisir vos temps (en heures) :")

    # Champs de saisie
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    with col1:
        temps1 = st.number_input("Temps 1", min_value=0.0, value=0.0, step=0.1)
    with col2:
        temps3 = st.number_input("Temps 3", min_value=0.0, value=0.0, step=0.1)
    with col3:
        temps5 = st.number_input("Temps 5", min_value=0.0, value=0.0, step=0.1)
    with col4:
        temps4 = st.number_input("Temps 4", min_value=0.0, value=0.0, step=0.1)
    with col5:
        temps6 = st.number_input("Temps 6", min_value=0.0, value=0.0, step=0.1)

    # Calculs
    prix1 = temps1 * (0.1 * 225 + 0.3 * 135 + 0.6 * 110)
    prix3 = temps3 * (0.4 * 225 + 0.6 * 135)
    prix5 = temps5 * 110
    prix4 = temps4 * 136  # à adapter
    prix6 = temps6 * 138  # à adapter

    prix_total = prix1 + prix3 + prix5 + prix4 + prix6

    # Affichage du prix
    st.markdown("---")
    st.subheader(f"💰 Prix total : {prix_total:.2f} €")

    with st.expander("📋 Détail du calcul"):
        st.markdown(f"- Temps 1 : {prix1:.2f} €")
        st.markdown(f"- Temps 3 : {prix3:.2f} €")
        st.markdown(f"- Temps 5 : {prix5:.2f} €")
        st.markdown(f"- Temps 4 : {prix4:.2f} €")
        st.markdown(f"- Temps 6 : {prix6:.2f} €")


if __name__ == "__main__":
    main()
