import streamlit as st
import pandas as pd
import math
from pathlib import Path
from datetime import datetime

# Configuration de la page : titre et icône.
st.set_page_config(
    page_title="Tableau de bord du PIB",
    page_icon=":earth_americas:",
)

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# Titre et description de l'application

st.markdown(
    """
    # :earth_americas: Tableau de bord du PIB
    **Créé par RENE TOLNO**

    Explorez les données du PIB issues du [World Bank Open Data](https://data.worldbank.org/).  
    Vous pouvez sélectionner la plage d'années (déterminée automatiquement selon le fichier de données),  
    choisir les pays à afficher et personnaliser l'affichage.
    """
)

st.write("")
st.write("")

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
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
        st.caption("Les valeurs sont exprimées en indice (base 100 = valeur en {0}).".format(from_year))
    
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
            
            first_pib_b = first_pib / 1e9 if not pd.isna(first_pib) else float("nan")
            last_pib_b = last_pib / 1e9 if not pd.isna(last_pib) else float("nan")
            
            if pd.isna(first_pib_b) or first_pib_b == 0 or from_year == to_year:
                croissance = "n/a"
                delta_color = "off"
            else:
                croissance = f"{(last_pib_b / first_pib_b):,.2f}x"
                delta_color = "normal"
            
            st.metric(
                label=f"PIB de {country}",
                value=f"${last_pib_b:,.0f} Mds",
                delta=croissance,
                delta_color=delta_color
            )
    
    st.write("")
    # Calcul et affichage du CAGR (taux de croissance annuel moyen)
    st.subheader("Croissance annuelle moyenne (CAGR)")
    cols_cagr = st.columns(4)
    for i, country in enumerate(selected_countries):
        with cols_cagr[i % 4]:
            try:
                first_val = df_pib[(df_pib["Country Code"] == country) & (df_pib["Année"] == from_year)]["PIB"].iat[0]
                last_val = df_pib[(df_pib["Country Code"] == country) & (df_pib["Année"] == to_year)]["PIB"].iat[0]
            except IndexError:
                first_val = float("nan")
                last_val = float("nan")
            
            if pd.isna(first_val) or first_val == 0 or from_year == to_year:
                cagr = "n/a"
            else:
                cagr_value = (last_val / first_val) ** (1 / (to_year - from_year)) - 1
                cagr = f"{cagr_value * 100:.2f}%"
            
            st.metric(
                label=f"CAGR {country}",
                value=cagr
            )

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
        Vous pouvez :
        - Sélectionner la plage d'années (déduite automatiquement des données disponibles).
        - Choisir les pays à afficher.
        - Personnaliser l'affichage du graphique (type et mode : valeur absolue ou indice avec base 100).
        - Visualiser des indicateurs de performance, notamment le PIB en dollars et le taux de croissance annuel moyen (CAGR).

        **Notes** :  
        - Les montants sont affichés en dollars américains.  
        - Les valeurs du PIB sont converties en milliards pour une lecture simplifiée.
        """
    )
