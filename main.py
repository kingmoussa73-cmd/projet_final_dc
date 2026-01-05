from fonction import *
import streamlit as st
import pandas as pd
import numpy as np
import os

# Style global (boutons + tableau)
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(45deg, #1e3a8a, #3b82f6) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        border: none !important;
        transition: 0.3s !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        background: linear-gradient(45deg, #3b82f6, #60a5fa) !important;
    }
    .dataframe thead th {
        background-color: #1e3a8a !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# URLs
url_1 = 'https://dakar-auto.com/senegal/voitures-4'
url_2 = 'https://dakar-auto.com/senegal/motos-and-scooters-3'
url_3 = 'https://dakar-auto.com/senegal/location-de-voitures-19'

# Liste des options
list_choix = ["", "Scraping BSoup", "download_web scraping", "Dashbord", "Evaluation"]

# Icônes (ajuste les noms si besoin)
icons = {
    "Scraping BSoup": "image/sb.jpeg",
    "download_web scraping": "image/Dow.jpeg",
    "Dashbord": "image/Dash.jpeg",
    "Evaluation": "image/EV.jpeg",
}

# SIDEBAR
with st.sidebar:
    st.markdown("### Mode")
    nb_page = st.selectbox("Pages à scraper", range(1, 2774))

    # Initialisation persistante du choix
    if 'choix' not in st.session_state:
        st.session_state.choix = list_choix[0]

    # Boutons avec icônes
    for opt in list_choix[1:]:
        col1, col2 = st.columns([1, 4])
        with col1:
            try:
                st.image(icons[opt], width=36)
            except:
                st.image("image/default.jpeg", width=36)
        with col2:
            if st.button(opt, key=f"btn_{opt}", use_container_width=True):
                st.session_state.choix = opt
                st.rerun()

# PAGE PRINCIPALE
choix = st.session_state.choix

# Bouton "Retour à l'accueil" (visible seulement hors accueil)
if choix != list_choix[0]:
    if st.button("← Retour à l'accueil", type="primary", use_container_width=True):
        st.session_state.choix = list_choix[0]
        st.rerun()

# AFFICHAGE SELON CHOIX
if choix == list_choix[0]:
    # Page d'accueil
    st.title("Bienvenue chez DAKAR MOBILITY HUB")
    st.image("image/1.jpeg", use_container_width=True)
    st.caption("Véhicules • Motos • Scooters • Locations – Dakar")
    st.markdown("Sélectionnez une option dans la barre latérale")

elif choix == "Scraping BSoup":
    st.markdown("<h1>Scraping des données avec BeautifulSoup</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    action = None

    with col1:
        if st.button("Voiture", use_container_width=True):
            action = "voiture"
    with col2:
        if st.button("Moto", use_container_width=True):
            action = "moto"
    with col3:
        if st.button("Location Véhicule", use_container_width=True):
            action = "location"

    if action == "voiture":
        with st.spinner("Scraping en cours..."):
            df1 = scrape_data(url_1, nb_page)
            st.dataframe(df1, use_container_width=True)
    elif action == "moto":
        with st.spinner("Scraping en cours..."):
            df2 = scrape_data(url_2, nb_page)
            st.dataframe(df2, use_container_width=True)
    elif action == "location":
        with st.spinner("Scraping en cours..."):
            df3 = scrape_data(url_3, nb_page)
            st.dataframe(df3, use_container_width=True)

elif choix == "download_web scraping":
    st.subheader("Gestion des fichiers CSV")
    st.markdown("Chargez un fichier local ou visualisez les données pré-enregistrées.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Téléverser un fichier CSV local", use_container_width=True):
            st.session_state.mode = "upload"
    with col2:
        if st.button("Charger un fichier pré-enregistré", use_container_width=True):
            st.session_state.mode = "prebuilt"

    if st.session_state.get("mode") == "upload":
        st.info("Sélectionnez un fichier CSV depuis votre ordinateur.")
        fichier = st.file_uploader(" ", type="csv", label_visibility="collapsed")
        if fichier is not None:
            with st.spinner("Lecture..."):
                try:
                    df = pd.read_csv(fichier)
                    st.success(f"Fichier chargé — {len(df):,} lignes")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Erreur : {str(e)}")

    elif st.session_state.get("mode") == "prebuilt":
        st.markdown("### Fichiers disponibles")
        tab_voiture, tab_moto, tab_location = st.tabs(["Voitures", "Motos & Scooters", "Locations"])

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_FOLDER = os.path.join(BASE_DIR, "data")

        with tab_voiture:
            if st.button("Afficher Voitures", use_container_width=True, key="btn_voit"):
                with st.spinner("Chargement..."):
                    try:
                        df = pd.read_csv(os.path.join(DATA_FOLDER, "dakar_auto_sitemap.csv"))
                        st.session_state.df_affiche = df
                        st.session_state.titre_df = "Voitures - dakar_auto_sitemap.csv"
                    except Exception as e:
                        st.error(f"Erreur : {str(e)}")

        # ... (même logique pour tab_moto et tab_location – copie/colle si besoin)

        if "df_affiche" in st.session_state:
            st.markdown(f"## {st.session_state.titre_df}")
            st.dataframe(st.session_state.df_affiche, use_container_width=True, hide_index=True)
            if st.button("Effacer", type="primary"):
                del st.session_state.df_affiche
                del st.session_state.titre_df
                st.rerun()

elif choix == "Dashbord":
    import os
    import glob
    
    csv_files = glob.glob("*.csv") + glob.glob("data/*.csv") + glob.glob("output/*.csv")
    if csv_files:
        most_recent = max(csv_files, key=os.path.getmtime)
        st.info(f"Dernier CSV détecté : {most_recent}")
        st.info(f"Date : {os.path.getmtime(most_recent)} → {os.path.getctime(most_recent)}")
    else:
        st.error("AUCUN fichier CSV trouvé dans le dossier courant ou data/")
        st.title("Dashboard")
        tab1, tab2 = st.tabs(["Scraping récent", "Fichier CSV"])
        # ... ton code dashboard ici (histogramme, etc.)

elif choix == "Evaluation":
    st.title("Accéder à mes formulaires")
    st.link_button("KoBoToolbox", "https://ee.kobotoolbox.org/x/CBgfDgVK", type="primary", use_container_width=True)
    st.link_button("Google Forms", "https://docs.google.com/forms/d/e/1FAIpQLSelIrqjlJ1YV5Z6P8tg6vz1FfREa1ce5keI6WX1NCD2pwe2HA/viewform?usp=dialog", type="primary", use_container_width=True)

