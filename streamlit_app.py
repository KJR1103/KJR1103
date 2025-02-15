import streamlit as st
import pandas as pd
import math
from pathlib import Path
from datetime import datetime

# Configuration de la page : titre et icône.
st.set_page_config(
    page_title="Tableau de bord de la croissance du PIB mondial",
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

    # Exclusion des années 2023, 2024 et 2025
    year_columns = [col for col in year_columns if int(col) < 2023]

    # Transformation des données (pivot des colonnes d'années)
    gdp_df = raw_gdp_df.melt(
        id_vars=["Country Code", "Country Name"],
        value_vars=year_columns,
        var_name="Année",
        value_name="PIB",
    )

    # Conversion de la colonne Année en entier
    gdp_df["Année"] = pd.to_numeric(gdp_df["Année"])

    # Ajouter les continents pour chaque pays (données fictives à ajuster selon la source)
    continent_map = {
# Dictionnaire complet avec tous les pays et leurs continents
country_dict = {
    # Afrique
    "DZA": {"name": "Algeria", "continent": "Afrique"},
    "AGO": {"name": "Angola", "continent": "Afrique"},
    "BEN": {"name": "Benin", "continent": "Afrique"},
    "BWA": {"name": "Botswana", "continent": "Afrique"},
    "BFA": {"name": "Burkina Faso", "continent": "Afrique"},
    "BDI": {"name": "Burundi", "continent": "Afrique"},
    "CPV": {"name": "Cabo Verde", "continent": "Afrique"},
    "CMR": {"name": "Cameroon", "continent": "Afrique"},
    "CAF": {"name": "Central African Republic", "continent": "Afrique"},
    "TCD": {"name": "Chad", "continent": "Afrique"},
    "COM": {"name": "Comoros", "continent": "Afrique"},
    "COG": {"name": "Congo", "continent": "Afrique"},
    "COD": {"name": "Congo (Democratic Republic)", "continent": "Afrique"},
    "CIV": {"name": "Côte d'Ivoire", "continent": "Afrique"},
    "DJI": {"name": "Djibouti", "continent": "Afrique"},
    "EGY": {"name": "Egypt", "continent": "Afrique"},
    "GNQ": {"name": "Equatorial Guinea", "continent": "Afrique"},
    "ERI": {"name": "Eritrea", "continent": "Afrique"},
    "SWZ": {"name": "Eswatini", "continent": "Afrique"},
    "ETH": {"name": "Ethiopia", "continent": "Afrique"},
    "GAB": {"name": "Gabon", "continent": "Afrique"},
    "GMB": {"name": "Gambia", "continent": "Afrique"},
    "GHA": {"name": "Ghana", "continent": "Afrique"},
    "GIN": {"name": "Guinea", "continent": "Afrique"},
    "GNB": {"name": "Guinea-Bissau", "continent": "Afrique"},
    "KEN": {"name": "Kenya", "continent": "Afrique"},
    "LSO": {"name": "Lesotho", "continent": "Afrique"},
    "LBR": {"name": "Liberia", "continent": "Afrique"},
    "LBY": {"name": "Libya", "continent": "Afrique"},
    "MDG": {"name": "Madagascar", "continent": "Afrique"},
    "MWI": {"name": "Malawi", "continent": "Afrique"},
    "MLI": {"name": "Mali", "continent": "Afrique"},
    "MRT": {"name": "Mauritania", "continent": "Afrique"},
    "MUS": {"name": "Mauritius", "continent": "Afrique"},
    "MAR": {"name": "Morocco", "continent": "Afrique"},
    "MOZ": {"name": "Mozambique", "continent": "Afrique"},
    "NAM": {"name": "Namibia", "continent": "Afrique"},
    "NER": {"name": "Niger", "continent": "Afrique"},
    "NGA": {"name": "Nigeria", "continent": "Afrique"},
    "RWA": {"name": "Rwanda", "continent": "Afrique"},
    "STP": {"name": "Sao Tome and Principe", "continent": "Afrique"},
    "SEN": {"name": "Senegal", "continent": "Afrique"},
    "SYC": {"name": "Seychelles", "continent": "Afrique"},
    "SLE": {"name": "Sierra Leone", "continent": "Afrique"},
    "SOM": {"name": "Somalia", "continent": "Afrique"},
    "ZAF": {"name": "South Africa", "continent": "Afrique"},
    "SSD": {"name": "South Sudan", "continent": "Afrique"},
    "SDN": {"name": "Sudan", "continent": "Afrique"},
    "TZA": {"name": "Tanzania", "continent": "Afrique"},
    "TGO": {"name": "Togo", "continent": "Afrique"},
    "TUN": {"name": "Tunisia", "continent": "Afrique"},
    "UGA": {"name": "Uganda", "continent": "Afrique"},
    "ZMB": {"name": "Zambia", "continent": "Afrique"},
    "ZWE": {"name": "Zimbabwe", "continent": "Afrique"},

    # Amérique du Nord
    "USA": {"name": "United States", "continent": "Amérique du Nord"},
    "CAN": {"name": "Canada", "continent": "Amérique du Nord"},
    "MEX": {"name": "Mexico", "continent": "Amérique du Nord"},
    "BLZ": {"name": "Belize", "continent": "Amérique du Nord"},
    "CRI": {"name": "Costa Rica", "continent": "Amérique du Nord"},
    "SLV": {"name": "El Salvador", "continent": "Amérique du Nord"},
    "GTM": {"name": "Guatemala", "continent": "Amérique du Nord"},
    "HND": {"name": "Honduras", "continent": "Amérique du Nord"},
    "NIC": {"name": "Nicaragua", "continent": "Amérique du Nord"},
    "PAN": {"name": "Panama", "continent": "Amérique du Nord"},

    # Amérique du Sud
    "ARG": {"name": "Argentina", "continent": "Amérique du Sud"},
    "BOL": {"name": "Bolivia", "continent": "Amérique du Sud"},
    "BRA": {"name": "Brazil", "continent": "Amérique du Sud"},
    "CHL": {"name": "Chile", "continent": "Amérique du Sud"},
    "COL": {"name": "Colombia", "continent": "Amérique du Sud"},
    "ECU": {"name": "Ecuador", "continent": "Amérique du Sud"},
    "GUY": {"name": "Guyana", "continent": "Amérique du Sud"},
    "PRY": {"name": "Paraguay", "continent": "Amérique du Sud"},
    "PER": {"name": "Peru", "continent": "Amérique du Sud"},
    "SUR": {"name": "Suriname", "continent": "Amérique du Sud"},
    "URY": {"name": "Uruguay", "continent": "Amérique du Sud"},
    "VEN": {"name": "Venezuela", "continent": "Amérique du Sud"},

    # Asie
    "AFG": {"name": "Afghanistan", "continent": "Asie"},
    "ARM": {"name": "Armenia", "continent": "Asie"},
    "AZE": {"name": "Azerbaijan", "continent": "Asie"},
    "BHR": {"name": "Bahrain", "continent": "Asie"},
    "BGD": {"name": "Bangladesh", "continent": "Asie"},
    "BTN": {"name": "Bhutan", "continent": "Asie"},
    "BRN": {"name": "Brunei", "continent": "Asie"},
    "KHM": {"name": "Cambodia", "continent": "Asie"},
    "CHN": {"name": "China", "continent": "Asie"},
    "GEO": {"name": "Georgia", "continent": "Asie"},
    "IND": {"name": "India", "continent": "Asie"},
    "IDN": {"name": "Indonesia", "continent": "Asie"},
    "IRN": {"name": "Iran", "continent": "Asie"},
    "IRQ": {"name": "Iraq", "continent": "Asie"},
    "ISR": {"name": "Israel", "continent": "Asie"},
    "JPN": {"name": "Japan", "continent": "Asie"},
    "JOR": {"name": "Jordan", "continent": "Asie"},
    "KAZ": {"name": "Kazakhstan", "continent": "Asie"},
    "KWT": {"name": "Kuwait", "continent": "Asie"},
    "KGZ": {"name": "Kyrgyzstan", "continent": "Asie"},
    "LAO": {"name": "Laos", "continent": "Asie"},
    "LBN": {"name": "Lebanon", "continent": "Asie"},
    "MYS": {"name": "Malaysia", "continent": "Asie"},
    "MDV": {"name": "Maldives", "continent": "Asie"},
    "MNG": {"name": "Mongolia", "continent": "Asie"},
    "MMR": {"name": "Myanmar", "continent": "Asie"},
    "NPL": {"name": "Nepal", "continent": "Asie"},
    "PRK": {"name": "North Korea", "continent": "Asie"},
    "OMN": {"name": "Oman", "continent": "Asie"},
    "PAK": {"name": "Pakistan", "continent": "Asie"},
    "PHL": {"name": "Philippines", "continent": "Asie"},
    "QAT": {"name": "Qatar", "continent": "Asie"},
    "SAU": {"name": "Saudi Arabia", "continent": "Asie"},
    "SGP": {"name": "Singapore", "continent": "Asie"},
    "KOR": {"name": "South Korea", "continent": "Asie"},
    "LKA": {"name": "Sri Lanka", "continent": "Asie"},
    "SYR": {"name": "Syria", "continent": "Asie"},
    "TWN": {"name": "Taiwan", "continent": "Asie"},
    "TJK": {"name": "Tajikistan", "continent": "Asie"},
    "THA": {"name": "Thailand", "continent": "Asie"},
    "TLS": {"name": "Timor-Leste", "continent": "Asie"},
    "TKM": {"name": "Turkmenistan", "continent": "Asie"},
    "ARE": {"name": "United Arab Emirates", "continent": "Asie"},
    "UZB": {"name": "Uzbekistan", "continent": "Asie"},
    "VNM": {"name": "Vietnam", "continent": "Asie"},
    "YEM": {"name": "Yemen", "continent": "Asie"},

    # Europe
    "ALB": {"name": "Albania", "continent": "Europe"},
    "AND": {"name": "Andorra", "continent": "Europe"},
    "AUT": {"name": "Austria", "continent": "Europe"},
    "BLR": {"name": "Belarus", "continent": "Europe"},
    "BEL": {"name": "Belgium", "continent": "Europe"},
    "BIH": {"name": "Bosnia and Herzegovina", "continent": "Europe"},
    "BGR": {"name": "Bulgaria", "continent": "Europe"},
    "HRV": {"name": "Croatia", "continent": "Europe"},
    "CYP": {"name": "Cyprus", "continent": "Europe"},
    "CZE": {"name": "Czech Republic", "continent": "Europe"},
    "DNK": {"name": "Denmark", "continent": "Europe"},
    "EST": {"name": "Estonia", "continent": "Europe"},
    "FIN": {"name": "Finland", "continent": "Europe"},
    "FRA": {"name": "France", "continent": "Europe"},
    "DEU": {"name": "Germany", "continent": "Europe"},
    "GRC": {"name": "Greece", "continent": "Europe"},
    "HUN": {"name": "Hungary", "continent": "Europe"},
    "ISL": {"name": "Iceland", "continent": "Europe"},
    "IRL": {"name": "Ireland", "continent": "Europe"},
    "ITA": {"name": "Italy", "continent": "Europe"},
    "LVA": {"name": "Latvia", "continent": "Europe"},
    "LIE": {"name": "Liechtenstein", "continent": "Europe"},
    "LTU": {"name": "Lithuania", "continent": "Europe"},
    "LUX": {"name": "Luxembourg", "continent": "Europe"},
    "MLT": {"name": "Malta", "continent": "Europe"},
    "MDA": {"name": "Moldova", "continent": "Europe"},
    "MCO": {"name": "Monaco", "continent": "Europe"},
    "MNE": {"name": "Montenegro", "continent": "Europe"},
    "NLD": {"name": "Netherlands", "continent": "Europe"},
    "MKD": {"name": "North Macedonia", "continent": "Europe"},
    "NOR": {"name": "Norway", "continent": "Europe"},
    "POL": {"name": "Poland", "continent": "Europe"},
    "PRT": {"name": "Portugal", "continent": "Europe"},
    "ROU": {"name": "Romania", "continent": "Europe"},
    "RUS": {"name": "Russia", "continent": "Europe"},
    "SMR": {"name": "San Marino", "continent": "Europe"},
    "SRB": {"name": "Serbia", "continent": "Europe"},
    "SVK": {"name": "Slovakia", "continent": "Europe"},
    "SVN": {"name": "Slovenia", "continent": "Europe"},
    "ESP": {"name": "Spain", "continent": "Europe"},
    "SWE": {"name": "Sweden", "continent": "Europe"},
    "CHE": {"name": "Switzerland", "continent": "Europe"},
    "TUR": {"name": "Turkey", "continent": "Europe"},
    "UKR": {"name": "Ukraine", "continent": "Europe"},
    "GBR": {"name": "United Kingdom", "continent": "Europe"},
    "VAT": {"name": "Vatican City", "continent": "Europe"},

    # Océanie
    "AUS": {"name": "Australia", "continent": "Océanie"},
    "FJI": {"name": "Fiji", "continent": "Océanie"},
    "KIR": {"name": "Kiribati", "continent": "Océanie"},
    "MHL": {"name": "Marshall Islands", "continent": "Océanie"},
    "FSM": {"name": "Micronesia", "continent": "Océanie"},
    "NRU": {"name": "Nauru", "continent": "Océanie"},
    "NZL": {"name": "New Zealand", "continent": "Océanie"},
    "PLW": {"name": "Palau", "continent": "Océanie"},
    "PNG": {"name": "Papua New Guinea", "continent": "Océanie"},
    "WSM": {"name": "Samoa", "continent": "Océanie"},
    "SLB": {"name": "Solomon Islands", "continent": "Océanie"},
    "TON": {"name": "Tonga", "continent": "Océanie"},
    "TUV": {"name": "Tuvalu", "continent": "Océanie"},
    "VUT": {"name": "Vanuatu", "continent": "Océanie"},
}

# Affichage de tous les pays avec leurs codes et continents
for code, info in country_dict.items():
    print(f"{code}: {info['name']} - {info['continent']}")

        # Ajoutez ici tous les autres pays et leurs continents
    }
    gdp_df["Continent"] = gdp_df["Country Code"].map(continent_map)

    return gdp_df

df_pib = get_gdp_data()

# -----------------------------------------------------------------------------
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

**Copyright 2025** - Données de la Banque Mondiale
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

# Liste des pays et noms pour l'affichage dans le sélecteur
countries_dict = {country: name for country, name in zip(df_pib["Country Code"].unique(), df_pib["Country Name"].unique())}
countries = list(countries_dict.keys())

selected_countries = st.multiselect(
    "Sélectionnez les pays à afficher :",
    options=countries,
    default=countries[:6],  # Par défaut, affiche les 6 premiers pays
    format_func=lambda country: f"{country} - {countries_dict[country]}"  # Afficher le nom du pays avec son code
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

    # Classement par pays pour chaque année
    st.subheader("Classement des pays par PIB (tous les pays)")
    for year in range(from_year, to_year + 1):
        ranking_df = df_pib[df_pib["Année"] == year].sort_values("PIB", ascending=False)
        st.subheader(f"Classement des pays pour l'année {year}")
        st.dataframe(ranking_df[["Country Code", "Country Name", "PIB"]].head(10))  # Afficher le top 10 des pays

    # Classement par continent pour chaque année
    st.subheader(f"Classement par continent en {to_year}")
    continent_rank = df_pib[df_pib["Année"] == to_year].groupby("Continent")["PIB"].sum().sort_values(ascending=False)
    st.dataframe(continent_rank)

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

        **Tous doits reservés** - Données de la Banque Mondiale
        """
    )
