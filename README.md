# Tableau de bord du PIB

Ce projet est une application **Streamlit** permettant d'explorer les données du PIB issues du [World Bank Open Data](https://data.worldbank.org/).  
L'application offre une interface interactive pour visualiser l'évolution du PIB pour différents pays sur une plage d'années sélectionnée.

## Fonctionnalités

- **Visualisation interactive**  
  - Graphique en ligne ou en barres pour visualiser l'évolution du PIB.
  - Option d'affichage en valeur absolue ou en indice (base 100).

- **Indicateurs financiers**  
  - Affichage du PIB en milliards de dollars.
  - Calcul du taux de croissance annuel moyen (CAGR).

- **Navigation intuitive**  
  - Contrôles accessibles via la barre latérale.
  - Onglets dédiés pour le graphique, les indicateurs, les données brutes et les informations sur l'application.

- **Téléchargement des données**  
  - Possibilité de télécharger les données brutes filtrées au format CSV.

## Installation

### Prérequis

- Python 3.7 ou supérieur
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

### Installation des dépendances

Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/VOTRE_UTILISATEUR/tableau-de-bord-pib.git
cd tableau-de-bord-pib
pip install -r requirements.txt
