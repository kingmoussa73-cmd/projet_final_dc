from fonction import *          # suppose que scrape_data() est dedans
import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime

# ────────────────────────────────────────────────
# Style global
# ────────────────────────────────────────────────
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

# ────────────────────────────────────────────────
# URLs & choix
# ────────────────────────────────────────────────
url_1 = 'https://dakar-auto.com/senegal/voitures-4'
url_2 = 'https://dakar-auto.com/senegal/motos-and-scooters-3'
url_3 = 'https://dakar-auto.com/senegal/location-de-voitures-19'

list_choix = ["", "Scraping BSoup", "download_web scraping", "Dashbord", "Evaluation"]

icons = {
    "Scraping BSoup": "image/sb.jpeg",
    "download_web scraping": "image/Dow.jpeg",
    "Dashbord": "image/Dash.jpeg",
    "Evaluation": "image/EV.jpeg",
}

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Mode")
    nb_page = st.selectbox("Pages à scraper", range(1, 2774), index=0)

    if 'choix' not in st.session_state:
        st.session_state.choix = list_choix[0]

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

# Bouton retour (hors accueil)
choix = st.session_state.choix
if choix != list_choix[0]:
    if st.button("← Retour à l'accueil", type="primary", use_container_width=True):
        st.session_state.choix = list_choix[0]
        st.rerun()

# ────────────────────────────────────────────────
# AFFICHAGE PRINCIPAL
# ────────────────────────────────────────────────
if choix == list_choix[0]:
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

    if action:
        with st.spinner("Scraping en cours..."):
            if action == "voiture":
                df = scrape_data(url_1, nb_page)
            elif action == "moto":
                df = scrape_data(url_2, nb_page)
            elif action == "location":
                df = scrape_data(url_3, nb_page)
            
            if df is not None and not df.empty:
                st.success(f"{len(df)} annonces récupérées")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Aucune donnée récupérée – vérifiez les URLs / le scraping")

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
        fichier = st.file_uploader(" ", type="csv", label_visibility="collapsed")
        if fichier:
            try:
                df = pd.read_csv(fichier)
                st.success(f"Fichier chargé — {len(df):,} lignes")
                st.dataframe(df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Erreur lecture : {e}")

    elif st.session_state.get("mode") == "prebuilt":
        st.markdown("### Fichiers disponibles")
        tab_voiture, tab_moto, tab_location = st.tabs(["Voitures", "Motos & Scooters", "Locations"])

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_FOLDER = os.path.join(BASE_DIR, "data")

        def afficher_fichier(fichier, titre):
            chemin = os.path.join(DATA_FOLDER, fichier)
            if os.path.exists(chemin):
                if st.button(f"Afficher {titre}", use_container_width=True):
                    try:
                        df = pd.read_csv(chemin)
                        st.session_state.df_affiche = df
                        st.session_state.titre_df = f"{titre} — {fichier}"
                    except Exception as e:
                        st.error(f"Erreur : {e}")
            else:
                st.info(f"Fichier {fichier} introuvable dans /data/")

        with tab_voiture:
            afficher_fichier("dakar_auto_sitemap.csv", "Voitures")   # adapte le nom réel

        # Ajoute les autres onglets de la même façon quand tu auras les noms exacts
        # with tab_moto:
        #     afficher_fichier("motos_dernier.csv", "Motos & Scooters")
        # with tab_location:
        #     afficher_fichier("locations.csv", "Locations")

        if "df_affiche" in st.session_state:
            st.markdown(f"## {st.session_state.titre_df}")
            st.dataframe(st.session_state.df_affiche, use_container_width=True, hide_index=True)
            if st.button("Effacer", type="primary"):
                for k in ["df_affiche", "titre_df"]:
                    st.session_state.pop(k, None)
                st.rerun()

elif choix == "Dashbord":
    st.title("Dashboard")

    tab1, tab2 = st.tabs(["Scraping récent", "Fichier CSV"])

    DATA_FOLDER = "data"   # adapte si différent

    def get_most_recent_csv(folder=DATA_FOLDER):
        if not os.path.exists(folder):
            return None, None
        csv_files = glob.glob(os.path.join(folder, "*.csv"))
        if not csv_files:
            return None, None
        most_recent = max(csv_files, key=os.path.getmtime)
        date_str = datetime.fromtimestamp(os.path.getmtime(most_recent)).strftime("%d/%m/%Y %H:%M")
        return most_recent, date_str

    with tab1:
        st.subheader("Dernier scraping enregistré")
        fichier, date = get_most_recent_csv()

        if fichier:
            st.info(f"Dernier fichier : **{os.path.basename(fichier)}**  \nDate : {date}")
            try:
                df = pd.read_csv(fichier, low_memory=False)
                st.success(f"{len(df):,} lignes chargées")

                # Aperçu rapide
                st.markdown("### Aperçu des 1 000 premières lignes")
                st.dataframe(df.head(1000), use_container_width=True)

                # Quelques stats / graphiques simples
                if 'prix' in df.columns:
                    st.markdown("### Distribution des prix")
                    fig_prix = df['prix'].dropna().plot(kind='hist', bins=40, title="Prix").figure
                    st.pyplot(fig_prix)

                if 'annee' in df.columns:
                    st.markdown("### Années des véhicules")
                    fig_annee = df['annee'].value_counts().sort_index().plot(kind='bar', title="Par année").figure
                    st.pyplot(fig_annee)

            except Exception as e:
                st.error(f"Impossible de lire le fichier :\n{e}")
        else:
            st.warning("Aucun fichier CSV trouvé dans le dossier data/")
            st.info("Lancez un scraping depuis l'onglet « Scraping BSoup » et sauvegardez le résultat.")

    with tab2:
        st.subheader("Choisir un autre fichier CSV")
        if os.path.exists(DATA_FOLDER):
            fichiers = sorted(glob.glob(os.path.join(DATA_FOLDER, "*.csv")))
            if fichiers:
                choix_fichier = st.selectbox("Fichier", [os.path.basename(f) for f in fichiers])
                if st.button("Charger et afficher", type="primary"):
                    try:
                        chemin = os.path.join(DATA_FOLDER, choix_fichier)
                        df = pd.read_csv(chemin, low_memory=False)
                        st.dataframe(df, use_container_width=True)
                    except Exception as e:
                        st.error(f"Erreur : {e}")
            else:
                st.info("Aucun .csv dans data/")
        else:
            st.error("Dossier data/ introuvable")

elif choix == "Evaluation":
    st.title("Accéder à mes formulaires")
    st.link_button("KoBoToolbox", "https://ee.kobotoolbox.org/x/CBgfDgVK", type="primary", use_container_width=True)
    st.link_button("Google Forms", "https://docs.google.com/forms/d/e/1FAIpQLSelIrqjlJ1YV5Z6P8tg6vz1FfREa1ce5keI6WX1NCD2pwe2HA/viewform?usp=dialog", type="primary", use_container_width=True)
