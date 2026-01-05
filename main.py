# main.py
from fonction import *          # ta fonction scrape_data() doit être ici
import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime
import matplotlib.pyplot as plt

# ────────────────────────────────────────────────
# Style CSS
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
# Constantes
# ────────────────────────────────────────────────
URL_VOITURE   = 'https://dakar-auto.com/senegal/voitures-4'
URL_MOTO      = 'https://dakar-auto.com/senegal/motos-and-scooters-3'
URL_LOCATION  = 'https://dakar-auto.com/senegal/location-de-voitures-19'

OPTIONS       = ["", "Scraping BSoup", "download_web scraping", "Dashbord", "Evaluation"]

ICONS = {
    "Scraping BSoup"       : "image/sb.jpeg",
    "download_web scraping": "image/Dow.jpeg",
    "Dashbord"             : "image/Dash.jpeg",
    "Evaluation"           : "image/EV.jpeg",
}

DATA_FOLDER = "data"

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Mode")
    nb_pages = st.selectbox("Pages à scraper", range(1, 51), index=0)

    if 'choix' not in st.session_state:
        st.session_state.choix = ""

    for opt in OPTIONS[1:]:
        col1, col2 = st.columns([1, 4])
        with col1:
            try:
                st.image(ICONS[opt], width=36)
            except:
                st.image("image/default.jpeg", width=36)
        with col2:
            if st.button(opt, key=f"btn_{opt}", use_container_width=True):
                st.session_state.choix = opt
                st.rerun()

# Bouton retour (sauf accueil)
if st.session_state.choix != "":
    if st.button("← Retour à l'accueil", type="primary", use_container_width=True):
        st.session_state.choix = ""
        st.rerun()

# ────────────────────────────────────────────────
# Nettoyage prix (essentiel pour les graphs)
# ────────────────────────────────────────────────
def clean_prix(v):
    if pd.isna(v):
        return np.nan
    s = str(v).strip()
    # Supprimer unités et mots courants
    for w in ['F CFA', 'Fcfa', 'fcfa', 'CFA', 'Prix', ':', 'strong', 'FCFA', '€', '$', 'euro']:
        s = s.replace(w, '')
    # Nettoyer séparateurs
    s = s.replace('\xa0', '').replace(' ', '').replace('.', '').replace(',', '')
    # Garder uniquement chiffres
    s = ''.join(c for c in s if c.isdigit())
    try:
        return int(s) if s else np.nan
    except:
        return np.nan

# ────────────────────────────────────────────────
# AFFICHAGE PRINCIPAL
# ────────────────────────────────────────────────
choix = st.session_state.choix

# Debug rapide (à commenter plus tard si tu veux)
st.caption(f"DEBUG – Page actuelle : {choix or 'Accueil'}")

if choix == "":
    st.title("Bienvenue chez DAKAR MOBILITY HUB")
    st.image("image/1.jpeg", use_container_width=True)
    st.caption("Véhicules • Motos • Scooters • Locations – Dakar")
    st.markdown("Choisissez une option dans la barre latérale")

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
        with st.spinner(f"Scraping {action} en cours..."):
            try:
                if action == "voiture":
                    url = URL_VOITURE
                elif action == "moto":
                    url = URL_MOTO
                else:
                    url = URL_LOCATION

                df = scrape_data(url, nb_pages)   # ← ta fonction doit retourner un DataFrame

                if df is not None and not df.empty:
                    st.success(f"{len(df):,} lignes récupérées")

                    # Sauvegarde automatique
                    os.makedirs(DATA_FOLDER, exist_ok=True)
                    ts = datetime.now().strftime("%Y%m%d_%H%M")
                    filename = f"dakar_{action}_{ts}.csv"
                    path = os.path.join(DATA_FOLDER, filename)
                    df.to_csv(path, index=False, encoding='utf-8-sig')
                    st.info(f"Sauvegardé → {filename}")

                    st.dataframe(df.head(800), use_container_width=True)
                else:
                    st.warning("Aucune donnée retournée par scrape_data()")

            except Exception as e:
                st.error(f"Erreur scraping : {str(e)}")

elif choix == "download_web scraping":
    st.subheader("Gestion des fichiers CSV")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Téléverser CSV local", use_container_width=True):
            st.session_state.mode_dl = "upload"
    with col2:
        if st.button("Voir fichiers existants", use_container_width=True):
            st.session_state.mode_dl = "liste"

    if st.session_state.get("mode_dl") == "upload":
        fichier = st.file_uploader(" ", type="csv", label_visibility="collapsed")
        if fichier is not None:
            try:
                df = pd.read_csv(fichier)
                st.success(f"Chargé – {len(df):,} lignes")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Erreur lecture : {e}")

    elif st.session_state.get("mode_dl") == "liste":
        fichiers = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
        if fichiers:
            sel = st.selectbox("Fichier", [os.path.basename(f) for f in fichiers])
            if st.button("Afficher"):
                try:
                    df = pd.read_csv(os.path.join(DATA_FOLDER, sel), low_memory=False)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(e)
        else:
            st.info("Aucun fichier CSV dans le dossier data/")

elif choix == "Dashbord":
    st.title("Dashboard")

    tab1, tab2 = st.tabs(["Dernier scraping", "Autre fichier"])

    def get_latest_file():
        fichiers = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
        if not fichiers:
            return None, None
        dernier = max(fichiers, key=os.path.getmtime)
        dt = datetime.fromtimestamp(os.path.getmtime(dernier))
        return dernier, dt.strftime("%d/%m/%Y %H:%M")

    with tab1:
        st.subheader("Dernier scraping")
        chemin, date_modif = get_latest_file()

        if chemin:
            st.info(f"Fichier : **{os.path.basename(chemin)}** | Modifié le {date_modif}")
            try:
                df = pd.read_csv(chemin, low_memory=False)

                # Nettoyage prix
                prix_col = next((c for c in df.columns if 'prix' in c.lower()), None)
                if prix_col:
                    df['prix_num'] = df[prix_col].apply(clean_prix)
                    n_valides = df['prix_num'].notna().sum()
                    st.info(f"Prix convertis : {n_valides:,} / {len(df):,} ({n_valides/len(df)*100:.1f}%)")

                st.markdown("### Aperçu")
                st.dataframe(df.head(1000), use_container_width=True)

                # Graphiques
                g1, g2 = st.columns(2)

                with g1:
                    if 'prix_num' in df.columns and df['prix_num'].notna().sum() >= 10:
                        st.markdown("**Distribution des prix**")
                        fig, ax = plt.subplots(figsize=(6,4))
                        df['prix_num'].dropna().plot.hist(bins=30, ax=ax, color='#3b82f6')
                        ax.set_title("Prix en FCFA")
                        ax.set_xlabel("Prix")
                        ax.set_ylabel("Nombre")
                        st.pyplot(fig)
                    else:
                        st.warning("Pas assez de prix numériques valides")

                with g2:
                    annee_col = next((c for c in df.columns if 'ann' in c.lower()), None)
                    if annee_col:
                        df['annee_num'] = pd.to_numeric(df[annee_col], errors='coerce')
                        counts = df['annee_num'].dropna().value_counts().sort_index()
                        if len(counts) >= 1:
                            st.markdown("**Années**")
                            fig2, ax2 = plt.subplots(figsize=(6,4))
                            counts.plot.bar(ax=ax2, color='#1e3a8a')
                            ax2.set_title("Répartition par année")
                            st.pyplot(fig2)

            except Exception as e:
                st.error(f"Erreur lecture : {e}")

        else:
            st.warning("Aucun fichier CSV trouvé dans data/")

    with tab2:
        st.subheader("Ouvrir un autre fichier")
        fichiers = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
        if fichiers:
            choix_f = st.selectbox("Fichier", [os.path.basename(f) for f in fichiers])
            if st.button("Charger"):
                try:
                    df = pd.read_csv(os.path.join(DATA_FOLDER, choix_f), low_memory=False)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(e)
        else:
            st.info("Aucun fichier disponible")

elif choix == "Evaluation":
    st.title("Formulaires")
    st.link_button("KoBoToolbox", "https://ee.kobotoolbox.org/x/CBgfDgVK", type="primary", use_container_width=True)
    st.link_button("Google Forms", "https://docs.google.com/forms/d/e/1FAIpQLSelIrqjlJ1YV5Z6P8tg6vz1FfREa1ce5keI6WX1NCD2pwe2HA/viewform?usp=dialog", type="primary", use_container_width=True)
