"""
Scadassembler v2.0 - Application Streamlit
Point d'entree principal
"""

import streamlit as st
from utils.styling import apply_custom_styling, render_header

# Configuration de la page
st.set_page_config(
    page_title="Scadassembler v2.0",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/doktornand/Scadassembler',
        'Report a bug': 'https://github.com/doktornand/Scadassembler/issues',
        'About': 'Scadassembler v2.0 - Convertisseur ASM16/DOS vers ASM32/Win32'
    }
)

# Application du styling custom
apply_custom_styling()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #e94560; font-size: 1.5rem;">🔧 Scadassembler</h2>
        <p style="color: #a0a0a0; font-size: 0.9rem;">v2.0 - Pipeline 5 phases</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📑 Navigation")
    st.page_link("app.py", label="🏠 Accueil", icon="🏠")
    st.page_link("pages/1_🔍_Analyseur_Binaire.py", label="🔍 Analyseur Binaire", icon="🔍")
    st.page_link("pages/2_⚙️_Conversion.py", label="⚙️ Conversion", icon="⚙️")
    st.page_link("pages/3_📊_Rapport_et_Métriques.py", label="📊 Rapport & Metriques", icon="📊")
    st.page_link("pages/4_📚_Documentation.py", label="📚 Documentation", icon="📚")

    st.divider()

    st.markdown("### ⚡ Quick Actions")

    if st.button("📁 Charger un exemple", use_container_width=True):
        st.session_state.load_example = True
        st.switch_page("pages/2_⚙️_Conversion.py")

    if st.button("📊 Voir un rapport demo", use_container_width=True):
        st.session_state.demo_report = True
        st.switch_page("pages/3_📊_Rapport_et_Métriques.py")

    st.divider()

    st.markdown("""
    <div style="font-size: 0.8rem; color: #a0a0a0; text-align: center;">
        <p>Pipeline 5 phases</p>
        <p>Parser MZ | Regles hierarchiques</p>
        <p>SCADA/IoT Ready</p>
    </div>
    """, unsafe_allow_html=True)

# Contenu principal
render_header(
    "SCADASSEMBLER v2.0",
    "Convertisseur ASM16/DOS vers ASM32/Win32 avec support SCADA/IoT"
)

# Hero section
st.markdown("""
<div style="
    background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
    border-radius: 15px;
    padding: 2rem;
    border: 1px solid #e94560;
    margin: 2rem 0;
">
    <h3 style="color: #e94560; margin-bottom: 1rem;">🚀 Pipeline de Conversion (5 Phases)</h3>
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
        <div style="
            background: #1a1a2e;
            border-radius: 10px;
            padding: 1rem;
            flex: 1;
            min-width: 150px;
            border: 1px solid #e94560;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📥</div>
            <div style="color: #e94560; font-weight: bold;">Chargement</div>
            <div style="color: #a0a0a0; font-size: 0.8rem;">Parse MZ/COM/ASM</div>
        </div>
        <div style="color: #e94560; font-size: 2rem; display: flex; align-items: center;">→</div>
        <div style="
            background: #1a1a2e;
            border-radius: 10px;
            padding: 1rem;
            flex: 1;
            min-width: 150px;
            border: 1px solid #e94560;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔬</div>
            <div style="color: #e94560; font-weight: bold;">Analyse</div>
            <div style="color: #a0a0a0; font-size: 0.8rem;">CFG + Dataflow</div>
        </div>
        <div style="color: #e94560; font-size: 2rem; display: flex; align-items: center;">→</div>
        <div style="
            background: #1a1a2e;
            border-radius: 10px;
            padding: 1rem;
            flex: 1;
            min-width: 150px;
            border: 1px solid #e94560;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚙️</div>
            <div style="color: #e94560; font-weight: bold;">Transformation</div>
            <div style="color: #a0a0a0; font-size: 0.8rem;">Regles hierarchiques</div>
        </div>
        <div style="color: #e94560; font-size: 2rem; display: flex; align-items: center;">→</div>
        <div style="
            background: #1a1a2e;
            border-radius: 10px;
            padding: 1rem;
            flex: 1;
            min-width: 150px;
            border: 1px solid #e94560;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💻</div>
            <div style="color: #e94560; font-weight: bold;">Emission</div>
            <div style="color: #a0a0a0; font-size: 0.8rem;">MASM/NASM/PE</div>
        </div>
        <div style="color: #e94560; font-size: 2rem; display: flex; align-items: center;">→</div>
        <div style="
            background: #1a1a2e;
            border-radius: 10px;
            padding: 1rem;
            flex: 1;
            min-width: 150px;
            border: 1px solid #e94560;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
            <div style="color: #e94560; font-weight: bold;">Validation</div>
            <div style="color: #a0a0a0; font-size: 0.8rem;">Verification PE</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Features grid
st.markdown("### 🎯 Fonctionnalites Cles")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        background: #16213e;
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #0f3460;
        height: 100%;
    ">
        <h4 style="color: #e94560;">📦 Parser MZ Complet</h4>
        <ul style="color: #a0a0a0; font-size: 0.9rem;">
            <li>Header DOS (28+ champs)</li>
            <li>Table de relocation</li>
            <li>Detection PE/NE/LE/LX</li>
            <li>Analyse segments</li>
            <li>Heuristique code/data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: #16213e;
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #0f3460;
        height: 100%;
    ">
        <h4 style="color: #e94560;">📐 Regles Hierarchiques</h4>
        <ul style="color: #a0a0a0; font-size: 0.9rem;">
            <li>11 categories en cascade</li>
            <li>Resolution de conflits</li>
            <li>Priorites CRITICAL→INFO</li>
            <li>Conditions complexes</li>
            <li>Substitutions variables</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background: #16213e;
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #0f3460;
        height: 100%;
    ">
        <h4 style="color: #e94560;">🔌 Plugins SCADA/IoT</h4>
        <ul style="color: #a0a0a0; font-size: 0.9rem;">
            <li>Emulation BCD (AAA, DAA...)</li>
            <li>Resolution far calls</li>
            <li>Bridge ports serie</li>
            <li>Dispatch interruptions</li>
            <li>Timers multimedia</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Formats supportes
st.markdown("### 📁 Formats Supportes")

col_fmt1, col_fmt2, col_fmt3, col_fmt4 = st.columns(4)

with col_fmt1:
    st.metric(".COM", "64K max", "Format plat")
with col_fmt2:
    st.metric(".EXE (MZ)", "Relocatable", "Segments multiples")
with col_fmt3:
    st.metric(".ASM", "Source", "Direct")
with col_fmt4:
    st.metric("Sortie", "MASM/NASM/PE", "Win32")

# Call to action
st.markdown("""
<div style="
    background: linear-gradient(90deg, #e94560 0%, #ff6b6b 100%);
    border-radius: 15px;
    padding: 2rem;
    text-align: center;
    margin: 2rem 0;
">
    <h3 style="color: white; margin-bottom: 1rem;">🚀 Commencer la Conversion</h3>
    <p style="color: white; opacity: 0.9;">
        Chargez un fichier binaire DOS ou un source ASM pour demarrer le pipeline de conversion.
    </p>
</div>
""", unsafe_allow_html=True)

col_cta1, col_cta2 = st.columns(2)
with col_cta1:
    if st.button("🔍 Analyser un Binaire", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🔍_Analyseur_Binaire.py")
with col_cta2:
    if st.button("⚙️ Convertir un Source", use_container_width=True, type="primary"):
        st.switch_page("pages/2_⚙️_Conversion.py")

# Footer info
st.divider()
st.markdown("""
<div style="text-align: center; color: #a0a0a0; font-size: 0.85rem;">
    <p>Scadassembler v2.0 | Pipeline 5 phases | Parser MZ | Regles hierarchiques | SCADA/IoT Ready</p>
    <p>Compatible avec <a href="#" style="color: #e94560;">CodeCartographer</a> pour analyse de corpus</p>
</div>
""", unsafe_allow_html=True)
