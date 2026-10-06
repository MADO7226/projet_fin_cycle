import streamlit as st
import pandas as pd
import joblib
import sklearn

# Configuration de la page
st.set_page_config(
    page_title="Prédiction & Dépistage Drépanocytose",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Assistant d'Orientation - Drépanocytose")
st.write(
    "Cette application utilise un modèle prédictif pour évaluer la probabilité "
    "de présence déclarée de la drépanocytose en fonction du profil du participant."
)

# 1. Chargement du modèle exporté
@st.cache_resource
def load_model():
    return joblib.load("meilleur_modele_drepano.joblib")

try:
    model = load_model()
    st.success("Modèle prédictif chargé avec succès !")
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle : {e}")
    st.info("Assurez-vous que le fichier 'meilleur_modele_drepano.joblib' est bien présent dans le même dossier que ce script.")
    st.stop()

# 2. Formulaire utilisateur
st.header("Profil du participant")

age = st.selectbox("Quel est votre âge ?", ["Moins de 18 ans", "18–25 ans", "26–35 ans", "Plus de 35 ans"])
sexe = st.selectbox("Quel est votre sexe ?", ["Femme", "Homme"])
poids_kg = st.number_input("Quel est votre poids (en kg) ?", min_value=10.0, max_value=200.0, value=60.0, step=1.0)
taille_m = st.number_input("Quelle est votre taille (en mètres) ?", min_value=1.0, max_value=2.3, value=1.70, step=0.01)
groupe_sanguin = st.selectbox("Quel est votre groupe sanguin ?", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
localite = st.selectbox("Localité ?", ["Urbain", "Rural"])
difficulte_acces = st.selectbox("Avez-vous des difficultés pour accéder aux soins ?", ["Oui", "Non"])
difficulte_principale = st.selectbox("Si oui, quelle est la principale difficulté ?", ["Transport", "Coût des soins", "Autre", "Aucune"])
accessibilite = st.selectbox("Les soins sont-ils facilement accessibles près de chez vous ?", ["Oui", "Non", "Moyennement"])

# 3. Prédiction
if st.button("Lancer l'évaluation", type="primary"):
    # Création du DataFrame avec la même structure que l'entraînement
    input_data = pd.DataFrame([{
        "age": age,
        "sexe": sexe,
        "poids_kg": poids_kg,
        "taille_m": taille_m,
        "groupe_sanguin": groupe_sanguin,
        "localite": localite,
        "difficulte_acces": difficulte_acces,
        "difficulte_principale": difficulte_principale,
        "accessibilite": accessibilite
    }])

    # Calcul de la prédiction et des probabilités
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    st.subheader("Résultat de l'analyse")
    if prediction == 1:
        st.warning(f"⚠️ Profil à risque élevé de drépanocytose (Probabilité : {probabilities[1]*100:.1f}%)")
        st.write("Il est fortement recommandé de réaliser un test de dépistage clinique (électrophorèse de l'hémoglobine) pour confirmation.")
    else:
        st.success(f"✅ Profil à faible risque (Probabilité : {probabilities[0]*100:.1f}%)")
        st.write("Les caractéristiques saisies indiquent une faible probabilité de présence constatée.")


