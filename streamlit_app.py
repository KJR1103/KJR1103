import streamlit as st
import pandas as pd
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Tableau de bord du PIB",
    page_icon=":earth_americas:",
)

@st.cache_data
def get_gdp_data() -> pd.DataFrame:
    """
    Charge et transforme les données du PIB à partir d'un fichier CSV.
    
    - Recherche les colonnes correspondant aux années.
    - Réalise un pivot pour obtenir trois colonnes : 'Country Code', 'Année' et 'PIB'.
    
    Returns:
        DataFrame contenant les données transformées.
    """
    try:
        data_file = Path(__file__).parent / "data/gdp_data.csv"
        df = pd.read_csv(data_file)
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier de données : {e}")
        return pd.DataFrame()

    # Identifier les colonnes correspondant aux années
    year_columns = [col for col in df.columns if col.isdigit()]
    if not year_columns:
        st.error("Aucune colonne d'années trouvée dans le fichier CSV.")
        return pd.DataFrame()

    min_year = int(min(year_columns))
    max_year = int(max(year_columns))

    # Transformation des données (pivot)
    gdp_df = df.melt(
        id_vars=["Country Code"],
        value_vars=[str(year) for year in range(min_year, max_year + 1)],
        var_name="Année",
        value_name="PIB",
    )
    # Conversion de la colonne 'Année' en entier
    gdp_df["Année"] = pd.to_numeric(gdp_df["Année"], errors="coerce")
    return gdp_df

# Chargement des données
df_pib = get_gdp_data()
if df_pib.empty:
    st.stop()

# ---------------------------
# Barre latérale : paramètres de l'analyse
# ---------------------------
st.sidebar.header("Paramètres de l'analyse")

min_year_data = int(df_pib["Année"].min())
max_year_data = int(df_pib["Année"].max())

from_year, to_year = st.sidebar.slider(
    "Sélectionnez la plage d'années :",
    min_value=min_year_data,
    max_value=max_year_data,
    value=(min_year_data, max_year_data)
)

countries = df_pib["Country Code"].unique()
default_countries = ["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"]
selected_countries = st.sidebar.multiselect(
    "Sélectionnez les pays à afficher :",
    options=list(countries),
    default=default_countries
)

chart_type = st.sidebar.radio("Type de graphique :", options=["Ligne", "Barres"])
display_mode = st.sidebar.radio("Mode d'affichage :", options=["Valeur absolue", "Indice (base 100)"])

# ---------------------------
# Titre et description principale
# ---------------------------
st.title(":earth_americas: Tableau de bord du PIB")
st.markdown(
    """
    **Créé par RENE TOLNO**

    Explorez les données du PIB issues du [World Bank Open Data](https://data.worldbank.org/).  
    Utilisez la barre latérale pour sélectionner la plage d'années, les pays et personnaliser l'affichage.
    """
)

# Filtrer les données en fonction des sélections
df_filtre = df_pib[
    (df_pib["Country Code"].isin(selected_countries)) &
    (df_pib["Année"] >= from_year) &
    (df_pib["Année"] <= to_year)
]

if df_filtre.empty:
    st.warning("Aucune donnée disponible pour les critères sélectionnés.")
    st.stop()

# ---------------------------
# Organisation en onglets
# ---------------------------
tabs = st.tabs(["Graphique", "Indicateurs", "Données brutes", "À propos"])

# Onglet Graphique
with tabs[0]:
    st.header("Évolution du PIB")
    
    # Création d'un tableau croisé pour le graphique
    pivot_data = df_filtre.pivot(index="Année", columns="Country Code", values="PIB")
    
    # Transformation en indice si sélectionné
    if display_mode == "Indice (base 100)":
        pivot_data_index = pivot_data.copy()
        for country in pivot_data_index.columns:
            if from_year in pivot_data_index.index:
                base_val = pivot_data_index.loc[from_year, country]
                if pd.notna(base_val) and base_val != 0:
                    pivot_data_index[country] = pivot_data_index[country] / base_val * 100
        pivot_data = pivot_data_index
        st.caption(f"Les valeurs sont exprimées en indice (base 100 = valeur en {from_year}).")
    
    # Affichage du graphique selon le type choisi
    if chart_type == "Ligne":
        st.line_chart(pivot_data)
    else:
        st.bar_chart(pivot_data)

# Onglet Indicateurs
with tabs[1]:
    st.header(f"Indicateurs pour la période {from_year} - {to_year}")
    
    # Affichage du PIB en milliards de dollars
    st.subheader("PIB (en milliards de dollars)")
    cols = st.columns(min(4, len(selected_countries)))
    for idx, country in enumerate(selected_countries):
        with cols[idx % 4]:
            try:
                first_pib = df_pib[(df_pib["Country Code"] == country) & (df_pib["Année"] == from_year)]["PIB"].iat[0]
                last_pib = df_pib[(df_pib["Country Code"] == country) & (df_pib["Année"] == to_year)]["PIB"].iat[0]
            except IndexError:
                first_pib, last_pib = None, None
            
            first_pib_b = first_pib / 1e9 if first_pib not in [None, 0] and pd.notna(first_pib) else None
            last_pib_b = last_pib / 1e9 if last_pib not in [None, 0] and pd.notna(last_pib) else None
            
            if first_pib_b is None or first_pib_b == 0 or from_year == to_year:
                croissance = "n/a"
                delta_color = "off"
            else:
                croissance = f"{(last_pib_b / first_pib_b):,.2f}x"
                delta_color = "normal"
            
            if last_pib_b is not None:
                st.metric(
                    label=f"PIB {country}",
                    value=f"${last_pib_b:,.0f} Mds",
                    delta=croissance,
                    delta_color=delta_color
                )
            else:
                st.metric(label=f"PIB {country}", value="n/a", delta="n/a")
    
    st.write("")
    st.subheader("Croissance annuelle moyenne (CAGR)")
    cols_cagr = st.columns(min(4, len(selected_countries)))
    for idx, country in enumerate(selected_countries):
        with cols_cagr[idx % 4]:
            try:
                first_val = df_pib[(df_pib["Country Code"] == country) & (df_pib["Année"] == from_year)]["PIB"].iat[0]
                last_val = df_pib[(df_pib["Country Code"] == country) & (df_pib["Année"] == to_year)]["PIB"].iat[0]
            except IndexError:
                first_val, last_val = None, None

            if first_val is None or first_val == 0 or from_year == to_year:
                cagr = "n/a"
            else:
                try:
                    cagr_value = (last_val / first_val) ** (1 / (to_year - from_year)) - 1
                    cagr = f"{cagr_value * 100:.2f}%"
                except Exception:
                    cagr = "n/a"
            
            st.metric(label=f"CAGR {country}", value=cagr)

# Onglet Données brutes
with tabs[2]:
    st.header("Données brutes")
    st.dataframe(df_filtre)
    csv = df_filtre.to_csv(index=False).encode("utf-8")
    st.download_button("Télécharger les données", data=csv, file_name="donnees_pib.csv", mime="text/csv")

# Onglet À propos
with tabs[3]:
    st.header("À propos")
    st.markdown(
        """
        **Tableau de bord du PIB**  
        Créé par **RENE TOLNO**

        Cette application permet d'explorer les données du PIB issues du [World Bank Open Data](https://data.worldbank.org/).  
        Utilisez la barre latérale pour sélectionner la plage d'années, les pays et personnaliser l'affichage.

        **Fonctionnalités** :
        - Sélection dynamique de la plage d'années basée sur les données.
        - Choix des pays à afficher.
        - Visualisation en graphique linéaire ou en barres.
        - Affichage en valeurs absolues ou en indice (base 100).
        - Indicateurs financiers tels que le PIB en milliards de dollars et le CAGR.
        - Téléchargement des données brutes.
        
        **Remarques** :
        - Les montants sont affichés en dollars américains et convertis en milliards pour une lecture simplifiée.
        """
    )
