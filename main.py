from fonction import *  # suppose que scrape_data() est définie ici
import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime
import matplotlib.pyplot as plt

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
    nb_page = st.selectbox("Pages à scraper", range(1, 51), index=0)  # limité pour éviter abus

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
# Fonction nettoyage prix
# ────────────────────────────────────────────────
def clean_prix(value):
    if pd.isna(value):
        return np.nan
    s = str(value).strip()
    for mot in ['F CFA', 'Fcfa', 'fcfa', 'CFA', 'Prix', ':', 'strong', 'FCFA', 'Fcfa', '€', '$', '€uro', 'FCFA']:
        s = s.replace(mot, '')
    s = s.replace('\xa0', '').replace(' ', '').replace('.', '').replace(',', '')
    s = ''.join(c for c in s if c.isdigit())
    try:
        return int(s) if s else np.nan
    except:
        return np.nan

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
            try:
                if action == "voiture":
                    df = scrape_data(url_1, nb_page)
                elif action == "moto":
                    df = scrape_data(url_2, nb_page)
                elif action == "location":
                    df = scrape_data(url_3, nb_page)

                if df is not None and not df.empty:
                    st.success(f"{len(df):,} annonces récupérées")
                    # Option : sauvegarde automatique
                    os.makedirs("data", exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%Hh%M")
                    chemin = f"data/dakar_{action}_{timestamp}.csv"
                    df.to_csv(chemin, index=False, encoding='utf-8-sig')
                    st.info(f"Données sauvegardées → {chemin}")
                    st.dataframe(df.head(1000), use_container_width=True)
                else:
                    st.warning("Aucune donnée récupérée")
                    
            except Exception as e:
                st.error(f"Erreur pendant le scraping : {str(e)}")

elif choix == "download_web scraping":
    st.subheader("Gestion des fichiers CSV")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Téléverser un fichier CSV local", use_container_width=True):
            st.session_state.mode = "upload"
    with col2:
        if st.button("Charger un fichier pré-enregistré", use_container_width=True):
            st.session_state.mode = "prebuilt"

    if st.session_state.get("mode") == "upload":
        fichier = st.file_uploader(" ", type="csv", label_visibility="collapsed")
        if fichier is not None:
            try:
                df = pd.read_csv(fichier)
                st.success(f"Fichier chargé — {len(df):,} lignes")
                st.dataframe(df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Erreur lecture : {e}")

    elif st.session_state.get("mode") == "prebuilt":
        st.markdown("### Fichiers disponibles")
        DATA_FOLDER = "data"
        fichiers = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))

        if fichiers:
            selected = st.selectbox("Choisir un fichier", [os.path.basename(f) for f in fichiers])
            if st.button("Afficher", type="primary"):
                try:
                    df = pd.read_csv(os.path.join(DATA_FOLDER, selected), low_memory=False)
                    st.session_state.df_show = df
                    st.session_state.show_title = selected
                except Exception as e:
                    st.error(f"Erreur : {e}")
        else:
            st.info("Aucun fichier CSV dans le dossier data/")

        if "df_show" in st.session_state:
            st.markdown(f"## {st.session_state.show_title}")
            st.dataframe(st.session_state.df_show, use_container_width=True)
            if st.button("Effacer affichage", type="secondary"):
                for k in ["df_show", "show_title"]:
                    st.session_state.pop(k, None)
                st.rerun()

elif choix == "Dashbord":
    st.title("Dashboard")
    tab1, tab2 = st.tabs(["Scraping récent", "Choisir un fichier"])

    DATA_FOLDER = "data"

    def get_latest_csv(folder=DATA_FOLDER):
        if not os.path.exists(folder):
            return None, None
        csvs = glob.glob(os.path.join(folder, "*.csv"))
        if not csvs:
            return None, None
        latest = max(csvs, key=os.path.getmtime)
        dt = datetime.fromtimestamp(os.path.getmtime(latest))
        return latest, dt.strftime("%d/%m/%Y %H:%M")

    with tab1:
        st.subheader("Dernier scraping")
        fichier, date_modif = get_latest_csv()

        if fichier:
            st.info(f"Fichier : **{os.path.basename(fichier)}**   |   Modifié le {date_modif}")
            try:
                df = pd.read_csv(fichier, low_memory=False)

                # Nettoyage prix
                if 'prix' in df.columns:
                    df['prix_numeric'] = df['prix'].apply(clean_prix)
                    valides = df['prix_numeric'].notna().sum()
                    st.info(f"Prix convertis en nombre : {valides:,} / {len(df):,} ({valides/len(df)*100:.1f}%)")

                st.markdown("### Aperçu")
                st.dataframe(df.head(1000), use_container_width=True)

                # Graphiques
                col_g1, col_g2 = st.columns(2)

                with col_g1:
                    if 'prix_numeric' in df.columns and df['prix_numeric'].notna().sum() >= 5:
                        st.markdown("**Distribution des prix**")
                        fig, ax = plt.subplots(figsize=(6,4))
                        df['prix_numeric'].dropna().plot.hist(bins=35, ax=ax, color='#3b82f6')
                        ax.set_title("Prix en FCFA")
                        ax.set_xlabel("Prix")
                        ax.set_ylabel("Nombre d'annonces")
                        st.pyplot(fig)
                    else:
                        st.warning("Pas assez de prix numériques valides pour un histogramme")

                with col_g2:
                    if 'annee' in df.columns or 'année' in df.columns:
                        col_annee = 'annee' if 'annee' in df.columns else 'année'
                        df['annee_num'] = pd.to_numeric(df[col_annee], errors='coerce')
                        annees = df['annee_num'].dropna().value_counts().sort_index()
                        if len(annees) > 0:
                            st.markdown("**Années des véhicules**")
                            fig2, ax2 = plt.subplots(figsize=(6,4))
                            annees.plot.bar(ax=ax2, color='#1e3a8a')
                            ax2.set_title("Répartition par année")
                            st.pyplot(fig2)

            except Exception as e:
                st.error(f"Erreur lecture fichier : {str(e)}")
        else:
            st.warning("Aucun fichier CSV trouvé dans data/")
            st.info("Faites un scraping et laissez-le se sauvegarder automatiquement.")

    with tab2:
        st.subheader("Ouvrir un autre fichier")
        csv_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
        if csv_files:
            choix_f = st.selectbox("Fichier", [os.path.basename(f) for f in csv_files])
            if st.button("Charger & afficher", type="primary"):
                try:
                    df = pd.read_csv(os.path.join(DATA_FOLDER, choix_f), low_memory=False)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Erreur : {e}")
        else:
            st.info("Aucun fichier .csv disponible dans data/")

elif choix == "Evaluation":
    st.title("Accéder à mes formulaires")
    st.link_button("KoBoToolbox", "https://ee.kobotoolbox.org/x/CBgfDgVK", type="primary", use_container_width=True)
    st.link_button("Google Forms", "https://docs.google.com/forms/d/e/1FAIpQLSelIrqjlJ1YV5Z6P8tg6vz1FfREa1ce5keI6WX1NCD2pwe2HA/viewform?usp=dialog", type="primary", use_container_width=True)
