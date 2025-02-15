import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configuration de la page : titre et icône.
st.set_page_config(
    page_title="Tableau de bord de la croissance du PIB mondial",
    page_icon=":earth_americas:",
)

# -------------------------------------------------------------------------
# Définition des fonctions utiles

@st.cache_data
def get_gdp_data():
    """
    Récupère les données du PIB à partir d'un fichier CSV et les transforme.

    Les colonnes d'années sont pivotées pour obtenir trois colonnes : 
    - Country Code
    - Année
    - PIB
    Les années disponibles sont déterminées dynamiquement en fonction du CSV.
    """
    DATA_FILENAME = Path(__file__).parent / "data/gdp_data.csv"
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    # Détermination dynamique des colonnes correspondant aux années
    year_columns = [col for col in raw_gdp_df.columns if col.isdigit()]
    MIN_YEAR = int(min(year_columns))
    MAX_YEAR = int(max(year_columns))

    # Transformation des données (pivot des colonnes d'années)
    gdp_df = raw_gdp_df.melt(
        id_vars=["Country Code"],
        value_vars=[str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        var_name="Année",
        value_name="PIB",
    )

    # Conversion de la colonne Année en entier
    gdp_df["Année"] = pd.to_numeric(gdp_df["Année"])

    return gdp_df

df_pib = get_gdp_data()

# -------------------------------------------------------------------------
# Titre et description de l'application

st.markdown(
    """
    # :earth_americas: Tableau de bord de la croissance du PIB mondial
    **Créé par RENE TOLNO**

    Plongez dans l'analyse des données du PIB grâce aux données ouvertes de la [Banque Mondiale](https://data.worldbank.org/). Cette application, conçue avec une approche basée sur la science des données, permet d'explorer et de visualiser les tendances économiques mondiales.

    Les principales Fonctionnalités :

    ✅ Sélection dynamique de la plage d’années selon les données disponibles.

    ✅ Choix des pays à comparer pour une analyse ciblée.

    ✅ Personnalisation avancée des graphiques : affichage en valeur absolue ou en indice (base 100).

    ✅ Indicateurs clés : PIB en milliards de dollars et taux de croissance annuel moyen (CAGR).

    Idéal pour les économistes, analystes et passionnés de data science souhaitant extraire des insights pertinents sur l’évolution économique mondiale. 🚀📊
    """
)

st.write("")

# -------------------------------------------------------------------------
# Sélection de la plage d'années et des pays

min_year_data = int(df_pib["Année"].min())
max_year_data = int(df_pib["Année"].max())

from_year, to_year = st.slider(
    "Sélectionnez la plage d'années :",
    min_value=min_year_data,
    max_value=max_year_data,
    value=(min_year_data, max_year_data)
)

countries = df_pib["Country Code"].unique()
selected_countries = st.multiselect(
    "Sélectionnez les pays à afficher :",
    options=list(countries),
    default=["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"]
)

st.write("")

# -------------------------------------------------------------------------
# Options supplémentaires pour le graphique

type_graphique = st.radio(
    "Choisissez le type de graphique :",
    options=["Ligne", "Barres"]
)

mode_affichage = st.radio(
    "Mode d'affichage du graphique :",
    options=["Valeur absolue", "Indice (base 100)"]
)

# Filtrage des données en fonction des sélections
df_filtre = df_pib[
    (df_pib["Country Code"].isin(selected_countries)) &
    (df_pib["Année"] >= from_year) &
    (df_pib["Année"] <= to_year)
]

# -------------------------------------------------------------------------
# Organisation de l'application en onglets

tabs = st.tabs(["Graphique", "Indicateurs", "Données brutes", "À propos"])

# Onglet Graphique
with tabs[0]:
    st.header("Évolution du PIB")
    
    # Création d'un tableau croisé : index = Année, colonnes = Country Code
    pivot_data = df_filtre.pivot(index="Année", columns="Country Code", values="PIB")
    
    # Transformation en indice si sélectionné
    if mode_affichage == "Indice (base 100)":
        pivot_data_index = pivot_data.copy()
        for country in pivot_data_index.columns:
            if from_year in pivot_data_index.index:
                base_val = pivot_data_index.loc[from_year, country]
                if base_val and not pd.isna(base_val) and base_val != 0:
                    pivot_data_index[country] = pivot_data_index[country] / base_val * 100
        pivot_data = pivot_data_index
        st.caption(f"Les valeurs sont exprimées en indice (base 100 = valeur en {from_year}).")
    
    # Affichage du graphique
    if type_graphique == "Ligne":
        st.line_chart(pivot_data)
    else:
        st.bar_chart(pivot_data)

# Onglet Indicateurs
with tabs[1]:
    st.header(f"Indicateurs pour l'année {to_year}")
    
    # Affichage du PIB (en milliards de dollars) et de la croissance totale
    st.subheader("PIB et croissance totale")
    cols = st.columns(4)
    for i, country in enumerate(selected_countries):
        with cols[i % 4]:
            try:
                first_pib = df_pib[(df_pib["Country Code"] == country) & (df_pib["Année"] == from_year)]["PIB"].iat[0]
                last_pib = df_pib[(df_pib["Country Code"] == country) & (df_pib["Année"] == to_year)]["PIB"].iat[0]
            except IndexError:
                first_pib = float("nan")
                last_pib = float("nan")
            
            first_pib_b = first
::contentReference[oaicite:1]{index=1}
 
