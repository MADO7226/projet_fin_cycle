import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Configuration de la page
st.set_page_config(
    page_title="Système de Suivi et Prévision Sanitaire - Drépanocytose",
    page_icon="https://api.iconify.design/lucide:activity.svg?color=%232563eb",
    layout="wide"
)

# Chargement automatique du modèle joblib
@st.cache_resource
def load_prediction_model():
    model_files = [f for f in os.listdir() if f.endswith('.joblib')]
    if model_files:
        return joblib.load(model_files[0])
    return None

model = load_prediction_model()

# Gestion de la base de données locale (pour la consultation de l'historique)
DATA_FILE = "data_collecte.csv"
colonnes_base = [
    "horodateur", "age", "genre", "poids_kg", "taille_m", "groupe_sanguin", 
    "drepano", "profil", "decouverte", "crises", "suivi", 
    "contrainte_acces", "difficulte_principale", "accessibilite", "localite"
]

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=colonnes_base)

# Menu de navigation latéral avec de vraies icônes (via HTML/SVG ou libellés propres)
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
        <h2 style="margin: 0; font-size: 1.25rem;">Navigation</h2>
    </div>
    """, 
    unsafe_allow_html=True
)

choix = st.sidebar.radio("Sections", [
    "Collecte en temps réel",
    "Analyse & Visualisation des cas",
    "Outil de prévision"
], label_visibility="collapsed")

# -------------------------------------------------------------
# 1. COLLECTE DES DONNÉES EN TEMPS RÉEL (FORMULAIRE + HISTORIQUE)
# -------------------------------------------------------------
if choix == "Collecte en temps réel":
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>
            <h1 style="margin: 0; font-size: 1.8rem;">Collecte et Historique des Données</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("Renseignez le formulaire ci-dessous pour enregistrer un nouveau cas, ou consultez l'historique complet.")

    # Formulaire de saisie
    with st.form("form_collecte"):
        st.subheader("Nouveau cas patient")
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("1. Âge (en années)", min_value=0, max_value=120, value=25, key="c_age")
            genre = st.selectbox("2. Genre", ["Femme", "Homme"], key="c_genre")
            poids_kg = st.number_input("3. Poids (kg)", min_value=0.0, max_value=200.0, value=60.0, key="c_poids")
            taille_m = st.number_input("4. Taille (m)", min_value=0.0, max_value=2.5, value=1.70, key="c_taille")
            groupe_sanguin = st.selectbox("5. Groupe sanguin", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], key="c_groupe")
            drepano = st.selectbox("6. Atteint(e) de drépanocytose ?", ["Oui", "Non"], key="c_drepano")
            profil = st.selectbox("7. Type de drépanocytose", ["AS", "SS", "SC", "Sβ-thalassémie", "N'ayant pas / Autre"], key="c_profil")
            decouverte = st.selectbox("8. Mode de découverte", ["Analyse de sang", "Dépistage médical", "À la suite de crises ou de symptômes", "Antécédents familiaux", "N'ayant","Autre",], key="c_decouverte")

        with col2:
            crises = st.selectbox("9. Fréquence des crises", ["Jamais", "Rarement", "Parfois", "Souvent", "Très souvent"], key="c_crises")
            suivi = st.selectbox("10. Suivi régulier", ["Oui", "Non"], key="c_suivi")
            contrainte_acces = st.selectbox("11. Contrainte d'accès aux soins", ["Oui", "Non"], key="c_contrainte")
            difficulte_principale = st.selectbox("12. Principale difficulté", ["Coût des soins", "Distance", "Transport", "Manque de médicaments", "Manque de spécialistes", "Autre"], key="c_difficulte")
            accessibilite = st.selectbox("13. Accessibilité des soins", ["Oui", "Non", "Moyennement"], key="c_accessibilite")
            localite = st.selectbox("14. Localité", ["urbain", "rurale"], key="c_localite")

        valider = st.form_submit_button("Enregistrer le cas")

        if valider:
            from datetime import datetime
            horodateur = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            nouvelle_ligne = pd.DataFrame({
                "horodateur": [horodateur],
                "age": [age], "genre": [genre], "poids_kg": [poids_kg],
                "taille_m": [taille_m], "groupe_sanguin": [groupe_sanguin], 
                "drepano": [drepano], "profil": [profil], "decouverte": [decouverte], 
                "crises": [crises], "suivi": [suivi], "contrainte_acces": [contrainte_acces], 
                "difficulte_principale": [difficulte_principale], "accessibilite": [accessibilite], 
                "localite": [localite]
            })
            
            df = pd.concat([df, nouvelle_ligne], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Donnée collectée et enregistrée avec succès dans l'historique !")

    st.markdown("---")
    st.subheader("Historique des Données Collectées")

    if st.button("🗑️ Réinitialiser (vider) tout l'historique"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        df = pd.DataFrame(columns=colonnes_base)
        st.success("L'historique a été réinitialisé avec succès !")
        st.rerun()

    if df.empty:
        st.info("Aucune donnée n'a encore été enregistrée.")
    else:
        st.write(f"Nombre total d'enregistrements dans l'historique : **{len(df)}**")
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger l'historique en CSV",
            data=csv_data,
            file_name="historique_drepanocytose.csv",
            mime="text/csv",
        )

# -------------------------------------------------------------
# 2. ANALYSE ET VISUALISATION DES CAS DE MALADIE
# -------------------------------------------------------------
elif choix == "Analyse & Visualisation des cas":
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
            <h1 style="margin: 0; font-size: 1.8rem;">Analyse et Visualisation</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("Analyse des cas de drépanocytose en fonction des critères démographiques et cliniques.")

    if df.empty:
        st.info("Aucune donnée disponible pour l'instant.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total des cas enregistrés", len(df))
        col2.metric("Localités représentées", df["localite"].nunique() if "localite" in df.columns else 0)
        col3.metric("Moyenne de poids (kg)", f"{df['poids_kg'].mean():.1f} kg" if "poids_kg" in df.columns and not df['poids_kg'].isnull().all() else "N/A")

        st.markdown("---")

        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Répartition par Localité")
            if "localite" in df.columns:
                st.bar_chart(df["localite"].value_counts())

        with c2:
            st.subheader("Répartition par Genre")
            if "genre" in df.columns:
                st.bar_chart(df["genre"].value_counts())

        if "difficulte_principale" in df.columns:
            st.subheader("Principales difficultés d'accès aux soins")
            st.bar_chart(df["difficulte_principale"].value_counts())

# -------------------------------------------------------------
# 3. OUTIL DE PRÉVISION (MODÈLE JOBLIB)
# -------------------------------------------------------------
elif choix == "Outil de prévision":
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#9333ea" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.2 1.2L3 12l5.9 1.9a2 2 0 0 1 1.2 1.2L12 21l1.9-5.8a2 2 0 0 1 1.2-1.2L21 12l-5.9-1.9a2 2 0 0 1-1.2-1.2Z"/></svg>
            <h1 style="margin: 0; font-size: 1.8rem;">Outil de Prévision de la Maladie</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("Renseignez l'ensemble des caractéristiques cliniques du patient pour lancer la prévision via le modèle.")

    if model is None:
        st.error("Aucun fichier `.joblib` n'a été trouvé dans le dossier de l'application.")
    else:
        st.success("Modèle de prévision chargé avec succès !")

        with st.form("form_prediction"):
            st.write("Veuillez renseigner les variables d'entrée exactes attendues par votre modèle :")
            
            col1, col2 = st.columns(2)
            with col1:
                p_age = st.number_input("1. Âge (en années)", min_value=0, max_value=120, value=25, key="p_age")
                p_genre = st.selectbox("2. Genre", ["Femme", "Homme"], key="p_genre")
                p_poids = st.number_input("3. Poids (kg)", min_value=0.0, max_value=200.0, value=60.0, key="p_poids")
                p_taille = st.number_input("4. Taille (m)", min_value=0.0, max_value=2.5, value=1.70, key="p_taille")
                p_groupe = st.selectbox("5. Groupe sanguin", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], key="p_groupe")
                p_drepano = st.selectbox("6. Atteint(e) de drépanocytose ?", ["Oui", "Non"], key="p_drepano")
                p_profil = st.selectbox("7. Type de drépanocytose", ["AS", "SS", "SC", "Sβ-thalassémie", "N'ayant pas / Autre"], key="p_profil")
                p_decouverte = st.selectbox("8. Mode de découverte", ["Analyse de sang", "Dépistage médical", "À la suite de crises ou de symptômes", "Antécédents familiaux", "Autre"], key="p_decouverte")
            
            with col2:
                p_crises = st.selectbox("9. Fréquence des crises", ["Jamais", "Rarement", "Parfois", "Souvent", "Très souvent"], key="p_crises")
                p_suivi = st.selectbox("10. Suivi régulier", ["Oui", "Non"], key="p_suivi")
                p_contrainte = st.selectbox("11. Contrainte d'accès aux soins", ["Oui", "Non"], key="p_contrainte")
                p_difficulte = st.selectbox("12. Principale difficulté", ["Coût des soins", "Distance", "Transport", "Manque de médicaments", "Manque de spécialistes", "Autre"], key="p_difficulte")
                p_accessibilite = st.selectbox("13. Accessibilité des soins", ["Oui", "Non", "Moyennement"], key="p_accessibilite")
                p_localite = st.selectbox("14. Localité", ["urbain", "rurale"], key="p_localite")
            
            predict_btn = st.form_submit_button("Lancer la prévision de la maladie")

            if predict_btn:
                if p_drepano == "Non" and p_crises == "Jamais" and p_profil in ["AS", "N'ayant pas / Autre"]:
                    st.markdown("---")
                    st.subheader("Résultat de la prévision")
                    st.info("ℹ️ **Information : Selon les informations renseignées, l'individu n'est pas atteint de la drépanocytose.**")
                else:
                    input_data = pd.DataFrame([[
                        p_age, p_genre, p_poids, p_taille, p_groupe, 
                        p_drepano, p_profil, p_decouverte, p_crises, p_suivi,
                        p_contrainte, p_difficulte, p_accessibilite, p_localite
                    ]], columns=[
                        'age', 'genre', 'poids_kg', 'taille_m', 'groupe_sanguin', 
                        'drepano', 'profil', 'decouverte', 'crises', 'suivi',
                        'contrainte_acces', 'difficulte_principale', 'accessibilite', 'localite'
                    ])
                    
                    try:
                        prediction = model.predict(input_data)
                        valeur_predite = prediction[0]
                        
                        st.markdown("---")
                        st.subheader("Résultat de la prévision")
                        
                        if valeur_predite in [1, 1.0, True, "Oui", "Positif"]:
                            st.error("⚠️ **Résultat : Le modèle prédit que l'individu présente un profil compatible avec la drépanocytose.**")
                            st.write("Avis : Il est recommandé de consulter un médecin pour un bilan sanguin de confirmation.")
                        else:
                            st.info("ℹ️ **Information : L'individu n'est pas atteint de la maladie de la drépanocytose.**")
                            
                    except Exception as e:
                        st.error(f"Erreur lors de l'exécution du modèle : {e}")