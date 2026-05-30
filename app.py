import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Dashboard Télécom Maroc",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stApp { background-color: #0f172a; }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    .metric-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #334155;
    }
    .stMetric label { font-size: 13px !important; color: #94a3b8 !important; }
    .stMetric [data-testid="metric-container"] { background: #1e293b; border-radius: 10px; padding: 14px; border: 1px solid #334155; }
    .stMetric [data-testid="stMetricValue"] { color: #ffffff !important; }
    h1, h2, h3 { color: #f8fafc; }
    .source-box { background: #1e293b; border-left: 4px solid #3b82f6; padding: 10px 14px; border-radius: 6px; font-size: 0.85rem; color: #94a3b8; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

try:
    trafic_historique = pd.read_csv("data/trafic_data.csv")
    trafic_historique['Date'] = pd.to_datetime(trafic_historique['Date'])
    trafic_historique['annee'] = trafic_historique['Date'].dt.year
    trafic_historique['trimestre'] = "T" + trafic_historique['Date'].dt.quarter.astype(str) + "-" + trafic_historique['annee'].astype(str)
    trafic_historique = trafic_historique.rename(columns={"Trafic_To": "volume_to"})
except FileNotFoundError:
    st.error("Fichier 'data/trafic_data.csv' introuvable.")
    st.stop()

previsions = pd.DataFrame({
    "trimestre": ["T1-2025","T2-2025","T3-2025","T4-2025","T1-2026","T2-2026","T3-2026","T4-2026"],
    "prevision_to": [918713, 981140, 1047496, 1118009, 1192916, 1272468, 1356927, 1446571],
    "borne_basse":  [849318, 866208, 884245,  901465,  917209,  931185,  943248,  953327],
    "borne_haute":  [993777, 1111321,1240888, 1386571, 1551500, 1738833, 1952033, 2195016],
})

parts_marche = pd.DataFrame({
    "operateur": ["Maroc Telecom", "Inwi", "Orange Maroc"],
    "part_marche_pct": [41.9, 33.9, 23.9],
    "revenus_MMAD": [14823, 5920, 4210]
})

antennes_data = {
    "mt": pd.DataFrame({
        "zone": ["Casablanca-Ain Diab","Casablanca-Hay Mohammadi","Casablanca-Bernoussi","Rabat-Hassan","Rabat-Agdal","Salé-Tabriquet","Marrakech-Guéliz","Marrakech-Médina","Agadir-Talborjt","Fès-Médina","Fès-Narjiss","Meknès-Hamria","Tanger-Centre","Tanger-Malabata","Tétouan-Centre","Oujda-Centre","Nador-Centre","Al Hoceima-Centre","Béni Mellal-Centre","Khouribga-Centre","Settat-Centre","Laâyoune-Centre","Dakhla-Centre","Guelmim-Centre"],
        "region": ["Grand Casablanca-Settat","Grand Casablanca-Settat","Grand Casablanca-Settat","Rabat-Salé-Kénitra","Rabat-Salé-Kénitra","Rabat-Salé-Kénitra","Marrakech-Safi","Marrakech-Safi","Souss-Massa","Fès-Meknès","Fès-Meknès","Fès-Meknès","Tanger-Tétouan-Al Hoceima","Tanger-Tétouan-Al Hoceima","Tanger-Tétouan-Al Hoceima","Oriental","Oriental","Tanger-Tétouan-Al Hoceima","Béni Mellal-Khénifra","Béni Mellal-Khénifra","Grand Casablanca-Settat","Laâyoune-Sakia El Hamra","Dakhla-Oued Ed-Dahab","Guelmim-Oued Noun"],
        "technologie": ["5G/4G+","4G+","4G","4G+","5G/4G+","4G","4G","4G","4G","4G","4G+","4G","5G/4G+","4G+","4G","4G","4G","4G","4G","4G","4G","4G","4G","3G/4G"],
        "capacite_gbps": [120,95,75,80,110,60,65,50,50,55,70,35,90,75,40,40,30,25,30,25,35,25,20,15],
        "saturation_pct": [87,79,65,74,68,55,81,62,52,68,59,72,58,54,45,45,38,35,60,48,52,38,30,28],
        "nb_antennes": [148,124,98,112,135,87,94,78,72,89,76,65,118,98,72,68,54,42,55,48,62,38,28,22],
        "lat": [33.601,33.561,33.602,34.020,33.994,34.037,31.641,31.626,30.420,34.062,34.023,33.893,35.771,35.784,35.570,34.688,35.174,35.248,32.336,32.883,33.000,27.160,23.683,28.987],
        "lon": [-7.680,-7.602,-7.536,-6.841,-6.860,-6.801,-8.010,-8.000,-9.598,-5.003,-5.042,-5.551,-5.799,-5.770,-5.368,-1.912,-2.928,-3.934,-6.361,-6.906,-7.619,-13.201,-15.960,-10.062]
    }),
    "inwi": pd.DataFrame({
        "zone": ["Casablanca-Maarif","Casablanca-Sidi Bernoussi","Casablanca-Ain Chock","Rabat-Agdal","Salé-Hay Salam","Kénitra-Centre","Marrakech-Médina","Marrakech-Menara","Agadir-Centre","Fès-Saiss","Meknès-Centre","Ifrane-Centre","Tanger-Dradeb","Tétouan-M'Diq","Chefchaouen-Centre","Oujda-Lazaret","Berkane-Centre","Nador-Corniche","Béni Mellal-Hay Isly","El Jadida-Centre","Safi-Centre","Laâyoune-Centre","Tiznit-Centre","Taroudant-Centre"],
        "region": ["Grand Casablanca-Settat","Grand Casablanca-Settat","Grand Casablanca-Settat","Rabat-Salé-Kénitra","Rabat-Salé-Kénitra","Rabat-Salé-Kénitra","Marrakech-Safi","Marrakech-Safi","Souss-Massa","Fès-Meknès","Fès-Meknès","Fès-Meknès","Tanger-Tétouan-Al Hoceima","Tanger-Tétouan-Al Hoceima","Tanger-Tétouan-Al Hoceima","Oriental","Oriental","Oriental","Béni Mellal-Khénifra","Grand Casablanca-Settat","Marrakech-Safi","Laâyoune-Sakia El Hamra","Souss-Massa","Souss-Massa"],
        "technologie": ["5G/4G+","4G+","4G","4G+","4G","4G","4G","4G+","4G","4G+","4G","4G","4G","4G+","4G","4G","4G","4G","4G","4G","4G","4G","4G","3G/4G"],
        "capacite_gbps": [100,80,65,70,55,50,55,65,40,60,45,25,60,50,30,35,28,32,30,45,38,25,22,18],
        "saturation_pct": [91,82,74,84,69,58,78,71,55,65,60,45,71,68,50,52,44,48,63,57,61,40,35,30],
        "nb_antennes": [124,102,88,98,75,68,82,90,65,78,62,38,88,74,52,58,44,50,48,62,55,32,30,24],
        "lat": [33.587,33.602,33.551,33.994,34.050,34.260,31.626,31.610,30.427,33.986,33.878,33.533,35.760,35.683,35.168,34.678,34.920,35.174,32.336,33.234,32.289,27.160,29.683,30.470],
        "lon": [-7.621,-7.536,-7.602,-6.860,-6.830,-6.594,-8.000,-8.020,-9.598,-4.983,-5.552,-5.105,-5.820,-5.310,-5.268,-1.923,-2.318,-2.928,-6.361,-8.506,-9.238,-13.201,-9.732,-8.876]
    }),
    "orange": pd.DataFrame({
        "zone": ["Casablanca-Anfa","Casablanca-Hay Hassani","Mohammedia-Centre","Rabat-Hay Riad","Rabat-Youssoufia","Salé-Hay Karima","Marrakech-Hivernage","Essaouira-Centre","Agadir-Hay Mohammadi","Fès-Bensouda","Meknès-Hamria","Khenifra-Centre","Tanger-Malabata","Tanger-Boukhalef","Tétouan-Centre","Oujda-Ville Nouvelle","Taourirt-Centre","Jerada-Centre","Béni Mellal-Hay Salam","Azilal-Centre","El Jadida-Centre","Laâyoune-Sakia","Boujdour-Centre","Tan-Tan-Centre"],
        "region": ["Grand Casablanca-Settat","Grand Casablanca-Settat","Grand Casablanca-Settat","Rabat-Salé-Kénitra","Rabat-Salé-Kénitra","Rabat-Salé-Kénitra","Marrakech-Safi","Marrakech-Safi","Souss-Massa","Fès-Meknès","Fès-Meknès","Béni Mellal-Khénifra","Tanger-Tétouan-Al Hoceima","Tanger-Tétouan-Al Hoceima","Tanger-Tétouan-Al Hoceima","Oriental","Oriental","Oriental","Béni Mellal-Khénifra","Béni Mellal-Khénifra","Grand Casablanca-Settat","Laâyoune-Sakia El Hamra","Laâyoune-Sakia El Hamra","Guelmim-Oued Noun"],
        "technologie": ["5G/4G+","4G+","4G","4G+","4G","4G","4G","4G","4G+","4G","4G","4G","5G/4G+","4G+","4G","4G","4G","3G/4G","4G","4G","4G","4G","3G/4G","3G/4G"],
        "capacite_gbps": [85,70,55,65,50,45,50,30,55,38,32,22,75,60,40,35,22,18,28,18,42,22,15,12],
        "saturation_pct": [79,68,55,63,52,48,71,42,58,48,44,38,54,50,45,42,34,28,55,38,49,35,25,22],
        "nb_antennes": [108,90,72,88,68,60,70,42,75,55,48,32,98,82,65,52,34,28,40,28,58,30,20,16],
        "lat": [33.594,33.547,33.686,33.988,33.976,34.044,31.633,31.508,30.420,34.040,33.893,32.933,35.784,35.727,35.570,34.680,34.408,34.315,32.340,31.963,33.234,27.152,26.124,28.438],
        "lon": [-7.650,-7.670,-7.383,-6.850,-6.870,-6.815,-8.008,-9.760,-9.598,-5.019,-5.551,-5.674,-5.770,-5.900,-5.368,-1.912,-2.885,-2.148,-6.354,-6.576,-8.506,-13.199,-14.486,-11.102]
    }),
}

penetration_regions = pd.DataFrame({
    "region": ["Grand Casablanca-Settat","Rabat-Salé-Kénitra","Tanger-Tétouan-Al Hoceima","Fès-Meknès","Marrakech-Safi","Oriental","Souss-Massa","Béni Mellal-Khénifra","Drâa-Tafilalet","Laâyoune-Sakia El Hamra","Guelmim-Oued Noun","Dakhla-Oued Ed-Dahab"],
    "taux_penetration_4g": [94.2, 91.8, 88.5, 85.3, 82.7, 79.4, 77.6, 71.2, 64.8, 72.3, 68.5, 65.1],
})

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Flag_of_Morocco.svg/120px-Flag_of_Morocco.svg.png", width=80)
    st.title("🇲🇦 Télécom Maroc")
    st.caption("Suivi CapEx & Surveillance Réseau")
    st.divider()

    operateur = st.selectbox(
        "Sélectionner l'opérateur",
        ["Maroc Telecom", "Inwi", "Orange Maroc"],
        index=0
    )
    op_key = {"Maroc Telecom": "mt", "Inwi": "inwi", "Orange Maroc": "orange"}[operateur]

    st.divider()
    st.markdown("### Navigation")
    vue = st.radio(
        "Navigation",
        [" Tableau de bord", "Carte des antennes", " Prévisions trafic"],
        label_visibility="collapsed"
    )

    st.divider()
    filtre_sat = st.slider("Seuil saturation minimum (%)", 0, 100, 0, 5)
    filtre_tech = st.multiselect("Technologies", ["5G/4G+","4G+","4G","3G/4G"], default=["5G/4G+","4G+","4G","3G/4G"])
    st.markdown('<div class="source-box">Données réelles : ANRT Maroc</div>', unsafe_allow_html=True)

df_ant = antennes_data[op_key].copy()
df_ant = df_ant[df_ant["saturation_pct"] >= filtre_sat]
df_ant = df_ant[df_ant["technologie"].isin(filtre_tech)]

total_antennes = {"mt": 4821, "inwi": 3914, "orange": 2756}[op_key]
sat_moy = df_ant["saturation_pct"].mean()
cap_totale = {"mt": 1820, "inwi": 1340, "orange": 890}[op_key]
antennes_critiques = len(df_ant[df_ant["saturation_pct"] >= 80])
op_info = parts_marche[parts_marche["operateur"] == operateur].iloc[0]

if vue == "Tableau de bord":
    st.markdown(f"##  {operateur} — Tableau de bord réseau")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Antennes actives", f"{total_antennes:,}")
    col2.metric("Part de marché", f"{op_info['part_marche_pct']}%")
    col3.metric("Capacité totale", f"{cap_totale} Gbps")
    col4.metric("Saturation moyenne", f"{sat_moy:.1f}%")
    col5.metric("Antennes critiques (>80%)", antennes_critiques)

    st.divider()
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("Statistiques par zone de couverture")
        df_display = df_ant[["zone","region","technologie","capacite_gbps","saturation_pct","nb_antennes"]].copy()
        df_display.columns = ["Zone","Région","Technologie","Capacité (Gbps)","Saturation (%)","Nb antennes"]
        
        def color_sat(val):
            if val >= 80: return "background-color: #7f1d1d; color: #fca5a5"
            elif val >= 65: return "background-color: #78350f; color: #fde68a"
            return "background-color: #064e3b; color: #a7f3d0"

        st.dataframe(
            df_display.style.map(color_sat, subset=["Saturation (%)"]),
            use_container_width=True, height=400
        )

    with col_b:
        st.subheader("Répartition des antennes")
        region_counts = df_ant.groupby("region")["nb_antennes"].sum().reset_index()
        fig_donut = px.pie(region_counts, values="nb_antennes", names="region", hole=0.55, template="plotly_dark")
        fig_donut.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0), height=200, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_donut, use_container_width=True)

        st.subheader("Technologies actives")
        tech_counts = df_ant.groupby("technologie")["nb_antennes"].sum().reset_index()
        fig_bar_tech = px.bar(tech_counts, x="technologie", y="nb_antennes", color="technologie", template="plotly_dark")
        fig_bar_tech.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0), height=180, xaxis_title="", yaxis_title="", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar_tech, use_container_width=True)

    st.divider()
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.subheader("Zones à forte saturation (Top 12)")
        top12 = df_ant.nlargest(12, "saturation_pct")
        fig_sat = go.Figure(go.Bar(
            x=top12["saturation_pct"], y=top12["zone"], orientation="h",
            marker_color=["#ef4444" if s>=80 else "#f59e0b" if s>=65 else "#10b981" for s in top12["saturation_pct"]],
            text=top12["saturation_pct"].astype(str)+"%", textposition="outside"
        ))
        fig_sat.add_vline(x=80, line_dash="dash", line_color="red")
        fig_sat.update_layout(height=350, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sat, use_container_width=True)

    with col_d:
        st.subheader("Indicateurs macro-financiers")
        fig_rev = px.bar(parts_marche, x="operateur", y="revenus_MMAD", color="operateur", text="revenus_MMAD", template="plotly_dark")
        fig_rev.update_traces(texttemplate="%{text:,} M MAD", textposition="outside")
        fig_rev.update_layout(showlegend=False, height=350, yaxis_title="Revenus (Millions MAD)", xaxis_title="", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rev, use_container_width=True)

elif vue == "Carte des antennes":
    st.markdown(f"## {operateur} — Carte des infrastructures")
    
    m = folium.Map(location=[31.7917, -7.0926], zoom_start=6, tiles="CartoDB dark_matter")

    for _, row in df_ant.iterrows():
        sat = row["saturation_pct"]
        color = "#ef4444" if sat >= 80 else "#f59e0b" if sat >= 65 else "#10b981"
        radius = 8 + (sat / 100) * 8

        popup_html = f"""
        <div style="font-family:Arial; min-width:180px; color:#000;">
            <b>{row['zone']}</b><br>
            Technologie: {row['technologie']}<br>
            Saturation: <span style="color:{color};font-weight:bold;">{sat}%</span><br>
            Antennes : {row['nb_antennes']}
        </div>"""

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)

    st_folium(m, width=None, height=500, returned_objects=[])

    st.divider()
    st.subheader("Taux de pénétration 4G par région")
    fig_pen = px.bar(penetration_regions.sort_values("taux_penetration_4g"), x="taux_penetration_4g", y="region", orientation="h", template="plotly_dark")
    fig_pen.update_layout(height=350, coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pen, use_container_width=True)

elif vue == " Prévisions trafic":
    st.markdown("##  Algorithme prédictif entraîné sur l'historique ANRT")
    
    fig_main = go.Figure()

    fig_main.add_trace(go.Scatter(
        x=trafic_historique["trimestre"], y=trafic_historique["volume_to"]/1000,
        mode="lines+markers", name="Historique Réel",
        line=dict(color="#10b981", width=3),
        marker=dict(size=6)
    ))

    fig_main.add_trace(go.Scatter(
        x=previsions["trimestre"], y=previsions["prevision_to"]/1000,
        mode="lines+markers", name="Prédiction Modèle",
        line=dict(color="#ef4444", width=3, dash="dash"),
        marker=dict(size=6)
    ))

    fig_main.add_trace(go.Scatter(
        x=list(previsions["trimestre"]) + list(previsions["trimestre"])[::-1],
        y=list(previsions["borne_haute"]/1000) + list(previsions["borne_basse"]/1000)[::-1],
        fill="toself", fillcolor="rgba(239,68,68,0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Marge de sécurité (IC 95%)"
    ))

    fig_main.update_layout(
        xaxis=dict(tickangle=90, title="Trimestres", gridcolor="#334155"),
        yaxis=dict(title="Volume Global (Milliers de To)", gridcolor="#334155"),
        height=550,
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="v", yanchor="top", y=0.99, xanchor="right", x=0.99),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_main, use_container_width=True)

    st.divider()
    col_e, col_f = st.columns(2)
    
    with col_e:
        st.subheader("Évolution de la croissance annuelle")
        annuel = trafic_historique.groupby("annee")["volume_to"].sum().reset_index()
        annuel["croissance_pct"] = annuel["volume_to"].pct_change() * 100
        fig_growth = px.bar(annuel.dropna(), x="annee", y="croissance_pct", template="plotly_dark", text="croissance_pct")
        fig_growth.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_growth.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Année", yaxis_title="Croissance (%)")
        st.plotly_chart(fig_growth, use_container_width=True)

    with col_f:
        st.subheader("Valeurs numériques des prévisions")
        prev_display = previsions.copy()
        prev_display["prevision_to"] = prev_display["prevision_to"].apply(lambda x: f"{x:,.0f} To")
        prev_display["borne_basse"] = prev_display["borne_basse"].apply(lambda x: f"{x:,.0f} To")
        prev_display["borne_haute"] = prev_display["borne_haute"].apply(lambda x: f"{x:,.0f} To")
        prev_display.columns = ["Trimestre","Prévision","Borne basse (95%)","Borne haute (95%)"]
        st.dataframe(prev_display, use_container_width=True, height=300)
