"""
Page 3: Rapport et Metriques - Visualisation avancee
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.styling import apply_custom_styling, render_header
from utils.report_generator import create_complexity_gauge, create_register_heatmap

st.set_page_config(
    page_title="Rapport | Scadassembler",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styling()

render_header("📊 RAPPORT & METRIQUES", "Visualisation et analyse des conversions")

# Demo data ou session state
if 'demo_report' not in st.session_state:
    st.session_state.demo_report = {
        "summary": {
            "status": "SUCCESS",
            "duration_ms": 1245,
            "phases_completed": 5,
            "total_phases": 5
        },
        "metrics": {
            "source_lines": 45,
            "output_lines": 78,
            "transformations_applied": 12,
            "manual_reviews_required": 2,
            "warnings": 3
        },
        "complexity": {
            "score": 4,
            "level": "MEDIUM",
            "auto_convertible": True,
            "requires_review": True
        },
        "register_usage": {
            "AX": 12, "BX": 5, "CX": 8, "DX": 15,
            "SI": 3, "DI": 2, "BP": 7, "SP": 9
        },
        "phases": {
            "load": {"status": "COMPLETED", "details": "Format MZ detecte, 2 segments"},
            "analyze": {"status": "COMPLETED", "details": "3 fonctions, 12 interruptions"},
            "transform": {"status": "COMPLETED", "details": "8 regles CRITICAL, 4 HIGH"},
            "emit": {"status": "COMPLETED", "details": "MASM32 genere, 78 lignes"},
            "validate": {"status": "COMPLETED", "details": "5 checks passes, 2 warnings"}
        },
        "transformations": [
            {"type": "register_expansion", "rule": "arch_x86_16_to_32", "count": 8},
            {"type": "interrupt_replacement", "rule": "int_21h_file_ops", "count": 4},
            {"type": "memory_model", "rule": "seg_model_conversion", "count": 1},
            {"type": "segment_elimination", "rule": "arch_segment_elimination", "count": 3},
            {"type": "iot_bridge", "rule": "domain_scada_iot", "count": 2}
        ]
    }

report = st.session_state.demo_report

# Metriques principales
st.markdown("### 📈 Metriques de Conversion")

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

with col_m1:
    st.markdown(f"""
    <div style="background: #16213e; border-radius: 10px; padding: 1rem; text-align: center; border: 1px solid #4ecca3;">
        <div style="font-size: 2rem; color: #4ecca3; font-weight: bold;">{report['metrics']['source_lines']}</div>
        <div style="color: #a0a0a0; font-size: 0.85rem;">Lignes source</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div style="background: #16213e; border-radius: 10px; padding: 1rem; text-align: center; border: 1px solid #e94560;">
        <div style="font-size: 2rem; color: #e94560; font-weight: bold;">{report['metrics']['output_lines']}</div>
        <div style="color: #a0a0a0; font-size: 0.85rem;">Lignes sortie</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
    <div style="background: #16213e; border-radius: 10px; padding: 1rem; text-align: center; border: 1px solid #f4d03f;">
        <div style="font-size: 2rem; color: #f4d03f; font-weight: bold;">{report['metrics']['transformations_applied']}</div>
        <div style="color: #a0a0a0; font-size: 0.85rem;">Transformations</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
    <div style="background: #16213e; border-radius: 10px; padding: 1rem; text-align: center; border: 1px solid #e94560;">
        <div style="font-size: 2rem; color: #e94560; font-weight: bold;">{report['metrics']['manual_reviews_required']}</div>
        <div style="color: #a0a0a0; font-size: 0.85rem;">Reviews manuelles</div>
    </div>
    """, unsafe_allow_html=True)

with col_m5:
    st.markdown(f"""
    <div style="background: #16213e; border-radius: 10px; padding: 1rem; text-align: center; border: 1px solid #a0a0a0;">
        <div style="font-size: 2rem; color: #a0a0a0; font-weight: bold;">{report['summary']['duration_ms']}ms</div>
        <div style="color: #a0a0a0; font-size: 0.85rem;">Duree</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Layout: Gauche (complexite + phases), Droite (visualisations)
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### 🎯 Complexite")

    complexity = report['complexity']

    # Jauge de complexite
    fig_gauge = create_complexity_gauge(complexity['score'])
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown(f"""
    <div style="background: #16213e; border-radius: 10px; padding: 1rem; margin-top: 1rem;">
        <h4 style="color: #e94560;">Niveau: {complexity['level']}</h4>
        <p style="color: #a0a0a0;">Auto-convertible: {'✅ Oui' if complexity['auto_convertible'] else '❌ Non'}</p>
        <p style="color: #a0a0a0;">Review requise: {'✅ Oui' if complexity['requires_review'] else '❌ Non'}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 Phases Executees")

    for phase_name, phase_data in report['phases'].items():
        status_color = "#4ecca3" if phase_data['status'] == "COMPLETED" else "#e94560"
        st.markdown(f"""
        <div style="
            background: {status_color}10;
            border-left: 4px solid {status_color};
            border-radius: 5px;
            padding: 0.75rem;
            margin: 0.5rem 0;
        ">
            <strong style="color: {status_color};">✓ {phase_name.upper()}</strong><br>
            <span style="color: #a0a0a0; font-size: 0.85rem;">{phase_data['details']}</span>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 🔄 Distribution des Transformations")

    # Bar chart des transformations
    trans_df = pd.DataFrame(report['transformations'])
    fig_bar = px.bar(
        trans_df,
        x='type',
        y='count',
        color='rule',
        title="Transformations par categorie",
        color_discrete_sequence=px.colors.sequential.Reds
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': '#eeeeee'},
        xaxis={'gridcolor': '#0f3460'},
        yaxis={'gridcolor': '#0f3460'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 🔄 Heatmap Registres 16→32 bit")

    # Heatmap des registres
    fig_heatmap = create_register_heatmap(report['register_usage'])
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Sankey diagram
    st.markdown("### 🕸️ Flux de Transformations")

    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=["Source DOS", "Registres", "Interruptions", "Segments", "IoT", "Win32 API", "MASM Code"],
            color=["#e94560", "#e94560", "#e94560", "#e94560", "#e94560", "#4ecca3", "#4ecca3"]
        ),
        link=dict(
            source=[0, 0, 0, 0, 1, 2, 3, 4],
            target=[1, 2, 3, 4, 5, 5, 6, 5],
            value=[8, 4, 3, 2, 8, 4, 3, 2],
            color=["rgba(233, 69, 96, 0.4)"] * 8
        )
    )])

    fig_sankey.update_layout(
        title_text="Flux de conversion",
        font_size=12,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_sankey, use_container_width=True)

st.divider()

# Export section
st.markdown("### 📤 Export pour CodeCartographer")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    corpus_json = """{
  "format": "MZ",
  "architecture": {"source": "x86_16", "target": "x86_32"},
  "metrics": {
    "file_size": 16384,
    "program_size": 8192,
    "relocation_count": 12,
    "segment_count": 3,
    "zone_count": 5
  },
  "transformations": [
    {"type": "register_expansion", "count": 8},
    {"type": "interrupt_replacement", "count": 4}
  ],
  "complexity": {"score": 4, "level": "MEDIUM"}
}"""

    st.download_button(
        "📥 Exporter JSON Corpus",
        data=corpus_json,
        file_name="scadassembler_corpus.json",
        mime="application/json",
        use_container_width=True
    )

with col_exp2:
    st.markdown("""
    <div style="background: #16213e; border-radius: 10px; padding: 1rem;">
        <h4 style="color: #e94560;">Integration CodeCartographer</h4>
        <p style="color: #a0a0a0; font-size: 0.85rem;">
            L'export JSON contient les metadonnees structurees pour analyse linguistique:
        </p>
        <ul style="color: #a0a0a0; font-size: 0.85rem;">
            <li>Distribution des instructions</li>
            <li>Surface API (interruptions)</li>
            <li>Patterns de migration</li>
            <li>Complexite et convertibilite</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
