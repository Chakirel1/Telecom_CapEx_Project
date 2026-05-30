```markdown
# Architecture Technique

Cette section décrit les principes de conception logicielle mis en œuvre ainsi que le mécanisme de traitement des données de trafic.

## Séparation des Préoccupations (Separation of Concerns)

L'application découpe logiquement ses traitements en couches fonctionnelles distinctes pour isoler l'interface utilisateur de la logique métier lourde :

### 1. Couche Présentation UI (Presentation Layer)
Portée par le framework **Streamlit**, cette couche traduit les interactions de l'utilisateur (sélection de l'opérateur, filtres de saturation minimale, choix de la vue) en signaux réactifs. Elle orchestre l'affichage dynamique des composants :
* Les widgets métriques (KPIs) de performance du réseau.
* Les visualisations analytiques synchronisées avec la charte graphique de l'opérateur via **Plotly Express**.
* Le rendu de la carte géographique vectorielle via **Folium / Streamlit-Folium**.

### 2. Couche Métier / Algorithmique (Business Logic Layer)
Cette couche exécute l'ensemble des modélisations mathématiques et filtres logiques sur les structures de données en mémoire :
* **Moteur d'indexation temporelle :** Parsing et agrégation des dates par trimestres glissants à l'aide de **Pandas**.
* **Moteur d'évaluation de la saturation :** Segmentation dynamique et application de fonctions de coloration conditionnelle sur les stations de base franchissant le seuil critique d'exploitation.
* **Moteur de Modélisation Prédictive :** Intégration des paramètres de séries temporelles ARIMA générant la courbe de tendance centrale ainsi que le calcul des variations de la marge de sécurité (Intervalle de confiance à 95%).

---

## Schéma du Flux de Données

Le diagramme ci-dessous modélise le cycle de vie de la donnée de trafic, de sa lecture brute à sa restitution graphique finale sur l'interface :

```mermaid
graph TD
    A[data/trafic_data.csv] -->|Parsing des Dates via Pandas| B(Nettoyage & Extraction des Trimestres)
    B --> C{Sélection de la Vue dans l'UI}
    
    C -->|Vue Tableau de bord & Carte| D[Calcul des Saturation Moyennes et des KPIs]
    C -->|Vue Prévisions Trafic| E[Modélisation & Ingestion Courbe ARIMA]
    
    D --> F[Filtrage Matriciel par Opérateur & Technologie]
    E --> G[Calcul des Bornes de Sécurité Haute / Basse]
    
    F --> H[Rendu Map Folium & Donut Plots Régionaux]
    G --> I[Rendu Graphique Temporel Plotly avec Zone IC 95%]
    
    style A fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#fff
    style H fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#fff
    style I fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#fff
