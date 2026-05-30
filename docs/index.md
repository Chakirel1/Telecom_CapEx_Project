# Dashboard Télécom Maroc — Suivi CapEx & Trafic

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![MkDocs](https://img.shields.io/badge/MkDocs-Material-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-ff4b4b.svg)
![ANRT](https://img.shields.io/badge/Donn%C3%A9es-ANRT%20Officielles-orange.svg)

Bienvenue sur la documentation technique officielle de l'Analyseur de Trafic de Données Télécom Maroc. Cette application a été conçue pour centraliser, cartographier et anticiper les dynamiques de consommation de données mobiles afin d'optimiser les décisions d'investissements en capital (CapEx).

## Contextualisation

Le marché marocain des télécommunications fait face à une explosion du trafic de données mobiles (croissance annuelle moyenne de +51.2% sur la période 2017-2024). Pour les opérateurs du Royaume (Maroc Telecom, Inwi, Orange Maroc), maintenir une excellente qualité de service nécessite une visibilité granulaire de la charge des infrastructures afin d'allouer stratégiquement les dépenses d'extension réseau (CapEx) vers les zones prioritaires.

## Objectifs Principaux

* **Analyse d'Infrastructure Multiplexée :** Consolider les parts de marché, les volumes d'abonnés et la capacité de transit agrégée par opérateur.
* **Supervison Géospatiale de la Saturation :** Identifier instantanément à l'aide d'une cartographie interactive les cellules réseau à risque ou en état de saturation critique (seuil $\ge 80\%$).
* **Planification Prédictive :** Anticiper l'évolution de la charge globale du réseau à l'horizon 2026-2027 via une modélisation ARIMA pour planifier les vagues de déploiement d'antennes 4G+/5G.

## Architecture du Code Source

Voici l'organisation structurelle de l'arborescence actuelle de ton projet sur l'environnement de développement :

```text
Telecom_CapEx_Project/
├── .streamlit/
│   └── config.toml          # Configuration graphique native du serveur Streamlit
├── data/
│   └── trafic_data.csv      # Historique officiel du trafic Data (Source: ANRT 2017-2024)
├── docs/
│   ├── index.md             # Page d'accueil de la présente documentation
│   ├── guide.md             # Guide pas à pas d'installation et déploiement
│   └── technical_reference.md # Spécifications d'architecture de l'application
├── notebooks/               # Notebooks Jupyter d'expérimentation et d'évaluation du modèle ARIMA
├── src/                     # Modules applicatifs et scripts de traitement secondaires
├── app.py                   # Point d'entrée principal de l'interface Streamlit (Dashboard)
├── mkdocs.yml               # Fichier de configuration du site de documentation
└── requirements.txt         # Liste stricte des dépendances Python requises
