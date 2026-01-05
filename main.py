from fonction import *
import streamlit as st 
import pandas as pd
import numpy as np


st.markdown("""
<style>
    /* Boutons dégradés */
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

    /* DataFrame headers */
    .dataframe thead th {
        background-color: #1e3a8a !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

url_1 = 'https://dakar-auto.com/senegal/voitures-4' 
url_2= 'https://dakar-auto.com/senegal/motos-and-scooters-3'
url_3= 'https://dakar-auto.com/senegal/location-de-voitures-19'


if choix == list_choix[0]:
    st.markdown("# Bienvenue dans l'application ")

    # Affichage de l'image depuis le dossier image/
    try:
        # Chemin relatif simple (marche le mieux sur Streamlit Cloud)
        st.image("image/1.jpg", use_container_width=True)
        # Ou avec caption et ajustement
        # st.image("1.jpg", caption="Marché automobile vibrant à Dakar", use_container_width=True)
    except Exception as e:
        st.warning(f"Impossible d'afficher l'image : {e}\nVérifie que 'image/accueil_voitures.jpg' existe dans le repo GitHub.")

    st.markdown("### Veuillez sélectionner une option")

# MENU DE CHOIX

if choix == list_choix[0]:
    st.markdown("# Bienvenue dans l'application ")
    st.markdown("### Veuillez sélectionner une option")
    
elif choix == list_choix[1]:  # "Scraping BSoup"
    st.markdown("<h1>Scraping des données avec BeautifulSoup</h1>", unsafe_allow_html=True)
    
    # Les colonnes ne sont créées QUE si on est dans ce mode
    col1, col2, col3 = st.columns(3)

    # Variable d'action (très bien vu)
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

    # Affichage des résultats (en dehors des colonnes → bonne pratique)
    if action == "voiture":
        with st.spinner("Scraping en cours..."):
            df1 = scrape_data(url_1, nb_page)          # ← assure-toi que url_1 est défini
            st.dataframe(df1, use_container_width=True)

    elif action == "moto":
        with st.spinner("Scraping en cours..."):
            df2 = scrape_data(url_2, nb_page)
            st.dataframe(df2, use_container_width=True)

    elif action == "location":
        with st.spinner("Scraping en cours..."):
            df3 = scrape_data(url_3, nb_page)
            st.dataframe(df3, use_container_width=True)
            

elif choix == list_choix[2]:
    st.subheader("Gestion des fichiers CSV")
    st.markdown("Chargez un fichier local ou visualisez les données pré-enregistrées.")

    # ─── Deux boutons principaux en haut ────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        if st.button(" Téléverser un fichier CSV local", use_container_width=True):
            st.session_state.mode = "upload"

    with col2:
        if st.button(" Charger un fichier pré-enregistré", use_container_width=True):
            st.session_state.mode = "prebuilt"

    # ─── Contenu conditionnel selon le mode choisi ──────────────────────────────
    if st.session_state.get("mode") == "upload":
        st.info("Sélectionnez un fichier CSV depuis votre ordinateur.")
        fichier = st.file_uploader(" ", type="csv", label_visibility="collapsed")

        if fichier is not None:
            with st.spinner("Lecture du fichier en cours..."):
                try:
                    df = pd.read_csv(fichier)
                    st.success(f"Fichier chargé avec succès — {len(df):,} lignes, {len(df.columns)} colonnes")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Erreur lors de la lecture : {str(e)}")

    elif st.session_state.get("mode") == "prebuilt":
        st.markdown("### Fichiers disponibles")
    
        # Onglets pour une navigation très propre
        tab_voiture, tab_moto, tab_location = st.tabs([" Voitures", " Motos & Scooters", " Locations"])
    
        # ────────────────────────────────────────────────
        # IMPORTANT : Chemin RELATIF → fonctionne local + cloud
        # Les fichiers doivent être dans le dossier data/ à la racine du repo GitHub
        # ────────────────────────────────────────────────
        import os
    
        # Option la plus robuste (recommandée)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_FOLDER = os.path.join(BASE_DIR, "data")
    
        # Ou version ultra-simple (suffit dans 95 % des cas sur Streamlit)
        # DATA_FOLDER = "data"
    
        with tab_voiture:
            if st.button("Afficher les données Voitures", use_container_width=True, key="btn_voit"):
                with st.spinner("Chargement..."):
                    try:
                        file_path = os.path.join(DATA_FOLDER, "dakar_auto_sitemap.csv")
                        df = pd.read_csv(file_path)
                        st.session_state.df_affiche = df
                        st.session_state.titre_df = "Voitures - dakar_auto_sitemap.csv"
                    except FileNotFoundError:
                        st.error(f"Fichier non trouvé : {file_path}\nVérifie que le fichier est bien dans le dossier data/ sur GitHub.")
                    except Exception as e:
                        st.error(f"Erreur lors du chargement : {str(e)}")
    
        with tab_moto:
            if st.button("Afficher les données Motos", use_container_width=True, key="btn_moto"):
                with st.spinner("Chargement..."):
                    try:
                        file_path = os.path.join(DATA_FOLDER, "dakar_motos_scooters.csv")
                        df = pd.read_csv(file_path)
                        st.session_state.df_affiche = df
                        st.session_state.titre_df = "Motos & Scooters - dakar_motos_scooters.csv"
                    except FileNotFoundError:
                        st.error(f"Fichier non trouvé : {file_path}\nVérifie que le fichier est bien dans le dossier data/ sur GitHub.")
                    except Exception as e:
                        st.error(f"Erreur lors du chargement : {str(e)}")
    
        with tab_location:
            if st.button("Afficher les données Locations", use_container_width=True, key="btn_loc"):
                with st.spinner("Chargement..."):
                    try:
                        file_path = os.path.join(DATA_FOLDER, "dakar_location_voitures.csv")
                        df = pd.read_csv(file_path)
                        st.session_state.df_affiche = df
                        st.session_state.titre_df = "Locations - dakar_location_voitures.csv"
                    except FileNotFoundError:
                        st.error(f"Fichier non trouvé : {file_path}\nVérifie que le fichier est bien dans le dossier data/ sur GitHub.")
                    except Exception as e:
                        st.error(f"Erreur lors du chargement : {str(e)}")
    
        # Affichage unique du dataframe sélectionné
        if "df_affiche" in st.session_state:
            st.markdown(f"## {st.session_state.titre_df}")
            st.dataframe(
                st.session_state.df_affiche,
                use_container_width=True,
                hide_index=True,
                column_config={
                    col: st.column_config.TextColumn(col, width="medium")
                    for col in st.session_state.df_affiche.columns[:5]  # exemple
                }
            )
    
            if st.button("Effacer l'affichage", type="primary"):
                if "df_affiche" in st.session_state:
                    del st.session_state.df_affiche
                if "titre_df" in st.session_state:
                    del st.session_state.titre_df
                st.rerun()
            
elif choix == list_choix[3]:
    st.title("Dashboard")

    tab1, tab2 = st.tabs(["Scraping récent", "Fichier CSV"])

    # ───────────────────────────────────────────────
    # Tab 1 : Scraping récent
    # ───────────────────────────────────────────────
    with tab1:
        st.subheader("Histogramme des prix – Scraping récent")

        categorie = st.radio(
            "Quelle catégorie voulez-vous visualiser ?",
            options=["Voiture", "Moto", "Location Véhicule"],
            horizontal=True,
            key="dashboard_categorie_scrap"
        )

        if st.button(f"Scraper 1 page → Afficher histogramme ({categorie})", type="primary"):
            with st.spinner("Scraping en cours..."):
                try:
                    url_mapping = {
                        "Voiture": url_1,
                        "Moto": url_2,
                        "Location Véhicule": url_3
                    }

                    url = url_mapping.get(categorie)
                    if not url or not isinstance(url, str) or not url.strip():
                        st.error("URL non définie ou invalide pour cette catégorie")
                        st.stop()

                    df = scrape_data(url, 1)

                    if df is None or df.empty:
                        st.error("Aucune donnée récupérée")
                        st.stop()

                    # Recherche colonne prix
                    prix_col = next(
                        (col for col in df.columns if any(m in col.lower() for m in ["prix", "price", "montant", "coût", "€", "euro"])),
                        None
                    )

                    if not prix_col:
                        st.warning("Aucune colonne contenant 'prix' n'a été détectée")
                        st.write("Colonnes disponibles :", list(df.columns))
                    else:
                        # Fonction de nettoyage renforcée
                        def clean_price(x):
                            if pd.isna(x):
                                return np.nan
                            
                            # Gestion tuple/liste → on prend le premier élément
                            if isinstance(x, (tuple, list)):
                                if len(x) == 0:
                                    return np.nan
                                x = x[0]
                            
                            # Conversion en chaîne et nettoyage
                            x = str(x).strip()
                            x = x.replace('\xa0', '') \
                                 .replace(' ', '') \
                                 .replace('FCFA', '') \
                                 .replace('CFA', '') \
                                 .replace('€', '') \
                                 .replace('$', '')
                            
                            # Gestion virgule/point selon format probable
                            if ',' in x and '.' not in x[-3:]:
                                x = x.replace(',', '.')           # 1 234,56 → 1234.56
                            else:
                                x = x.replace(',', '')            # 1,234.56 → 1234.56
                            
                            # Garder uniquement chiffres + . + -
                            x = ''.join(c for c in x if c.isdigit() or c in '.-')
                            
                            try:
                                return float(x)
                            except (ValueError, TypeError):
                                return np.nan

                        # Application
                        df['prix_nettoye'] = df[prix_col].apply(clean_price)
                        prix_valides = df['prix_nettoye'].dropna()

                        if prix_valides.empty:
                            st.warning("Aucune valeur numérique valide après nettoyage")
                            st.write("Exemples bruts :", df[prix_col].head(10).tolist())
                        else:
                            st.success(f"{len(prix_valides)} prix affichés")

                            # Histogramme
                            st.subheader(f"Histogramme des prix – {categorie}")
                            hist, bins = np.histogram(prix_valides, bins=15)

                            # Labels d'intervalles bien formatés
                            interval_labels = [
                                f"{int(bins[i]):,} – {int(bins[i+1]):,}".replace(',', ' ')
                                for i in range(len(bins)-1)
                            ]

                            hist_df = pd.DataFrame({
                                'Intervalle': interval_labels,
                                'Nombre': hist
                            }).set_index('Intervalle')

                            st.bar_chart(hist_df, use_container_width=True, color="#1f77b4")

                            # Métriques avec formatage propre (espace comme séparateur)
                            cols = st.columns(3)
                            cols[0].metric("Prix moyen", f"{prix_valides.mean():,.0f} FCFA".replace(',', ' '))
                            cols[1].metric("Prix min",   f"{prix_valides.min():,.0f} FCFA".replace(',', ' '))
                            cols[2].metric("Prix max",   f"{prix_valides.max():,.0f} FCFA".replace(',', ' '))

                            st.subheader("Aperçu des données")
                            st.dataframe(df.head(10), use_container_width=True)

                except Exception as e:
                    st.error(f"Erreur pendant le scraping ou le traitement :\n{str(e)}")

    # ───────────────────────────────────────────────
    # Tab 2 : Fichier CSV (même logique de nettoyage)
    # ───────────────────────────────────────────────
    with tab2:
        st.subheader("Histogramme des prix – Fichier CSV")

        fichier = st.file_uploader("Choisissez un fichier CSV", type="csv")

        if fichier is not None:
            try:
                df = pd.read_csv(fichier)

                prix_col = next(
                    (col for col in df.columns if any(m in col.lower() for m in ["prix", "price", "montant", "coût", "FCFA"])),
                    None
                )

                if not prix_col:
                    st.warning("Aucune colonne contenant 'prix' n'a été trouvée")
                else:
                    # Même fonction clean_price (vous pouvez la définir une seule fois en haut du fichier)
                    df['prix_nettoye'] = df[prix_col].apply(clean_price)
                    prix_valides = df['prix_nettoye'].dropna()

                    if prix_valides.empty:
                        st.warning("Aucune valeur numérique valide après nettoyage")
                    else:
                        st.success(f"{len(prix_valides)} prix trouvés")

                        # Histogramme
                        st.subheader("Histogramme des prix")
                        hist, bins = np.histogram(prix_valides, bins=15)

                        interval_labels = [
                            f"{int(bins[i]):,} – {int(bins[i+1]):,}".replace(',', ' ')
                            for i in range(len(bins)-1)
                        ]

                        hist_df = pd.DataFrame({
                            'Intervalle': interval_labels,
                            'Nombre': hist
                        }).set_index('Intervalle')

                        st.bar_chart(hist_df, use_container_width=True, color="#2ca02c")

                        # Métriques formatées
                        cols = st.columns(3)
                        cols[0].metric("Prix moyen", f"{prix_valides.mean():,.0f} FCFA".replace(',', ' '))
                        cols[1].metric("Prix min",   f"{prix_valides.min():,.0f} FCFA".replace(',', ' '))
                        cols[2].metric("Prix max",   f"{prix_valides.max():,.0f} FCFA".replace(',', ' '))

                        st.subheader("Aperçu")
                        st.dataframe(df.head(10), use_container_width=True)

            except Exception as e:
                st.error(f"Erreur lors de la lecture du fichier :\n{str(e)}")
    
elif choix == list_choix[4]:

    st.title("Accéder à mes formulaires")

    st.link_button(
        "KoBoToolbox  Mes formulaires",
        "https://ee.kobotoolbox.org/x/CBgfDgVK",
        type="primary",
        use_container_width=True,
        icon=":material/folder_open:"
    )

    st.link_button(
        "Google Forms  Mes formulaires",
        "https://docs.google.com/forms/u/0/",
        type="primary",
        use_container_width=True,
        icon=":material/folder_open:"

)


