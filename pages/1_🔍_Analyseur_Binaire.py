"""
Page 1: Analyseur Binaire - Upload et analyse de fichiers DOS
"""

import streamlit as st
import struct
from utils.styling import apply_custom_styling, render_header, render_badge
from utils.hex_viewer import hex_dump, hex_dump_bytes
from core.mz_parser import MZParser
from core.com_parser import COMParser

st.set_page_config(
    page_title="Analyseur Binaire | Scadassembler",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styling()

render_header("🔍 ANALYSEUR BINAIRE", "Parseur MZ/COM avec visualisation hexadecimale interactive")

# Upload section
st.markdown("""
<div style="
    background: #16213e;
    border-radius: 10px;
    padding: 2rem;
    border: 2px dashed #e94560;
    text-align: center;
    margin: 2rem 0;
">
    <h3 style="color: #e94560;">📁 Deposez votre fichier DOS</h3>
    <p style="color: #a0a0a0;">Formats supportes: .COM, .EXE (MZ), .ASM</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=['com', 'exe', 'asm'], label_visibility="collapsed")

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_ext = uploaded_file.name.split('.')[-1].lower()

    # Detection du format
    magic = file_bytes[0:2].decode('ascii', errors='replace')

    st.success(f"✅ Fichier charge: **{uploaded_file.name}** ({len(file_bytes)} bytes)

    # Badges de format
    col_badges = st.columns(4)
    with col_badges[0]:
        if magic in ('MZ', 'ZM'):
            render_badge("FORMAT: MZ (.EXE)", "#e94560")
        elif file_ext == 'com':
            render_badge("FORMAT: COM", "#4ecca3")
        elif file_ext == 'asm':
            render_badge("FORMAT: ASM SOURCE", "#f4d03f")
    with col_badges[1]:
        render_badge(f"TAILLE: {len(file_bytes)} bytes", "#a0a0a0")
    with col_badges[2]:
        render_badge(f"MAGIC: {magic}", "#a0a0a0")
    with col_badges[3]:
        render_badge(f"EXTENSION: .{file_ext.upper()}", "#a0a0a0")

    st.divider()

    # Tabs pour differentes vues
    tab_hex, tab_header, tab_analysis, tab_export = st.tabs([
        "🗂️ Hex Dump", "📋 Header", "🔬 Analyse", "📤 Export"
    ])

    with tab_hex:
        st.subheader("Visualisation Hexadecimale")

        col_hex1, col_hex2 = st.columns([3, 1])

        with col_hex1:
            # Hex dump interactif
            hex_data = hex_dump(file_bytes, length=min(len(file_bytes), 512))

            # Coloration par type
            def color_type(val):
                colors = {
                    "CODE": "background-color: rgba(233, 69, 96, 0.2); color: #e94560;",
                    "DATA": "background-color: rgba(78, 204, 163, 0.2); color: #4ecca3;",
                    "ASCII": "background-color: rgba(244, 208, 63, 0.2); color: #f4d03f;",
                    "ZERO": "background-color: rgba(160, 160, 160, 0.2); color: #a0a0a0;",
                    "RELOC": "background-color: rgba(142, 68, 173, 0.2); color: #8e44ad;"
                }
                return colors.get(val, "")

            styled_df = hex_data.style.map(color_type, subset=["type"])
            st.dataframe(styled_df, use_container_width=True, height=500)

        with col_hex2:
            st.markdown("### 🎨 Legende")
            st.markdown("""
            <div style="font-size: 0.85rem;">
                <div style="margin: 5px 0;"><span style="background: rgba(233, 69, 96, 0.3); padding: 2px 8px; border-radius: 4px;">CODE</span> Probable code</div>
                <div style="margin: 5px 0;"><span style="background: rgba(78, 204, 163, 0.3); padding: 2px 8px; border-radius: 4px;">DATA</span> Donnees</div>
                <div style="margin: 5px 0;"><span style="background: rgba(244, 208, 63, 0.3); padding: 2px 8px; border-radius: 4px;">ASCII</span> Texte ASCII</div>
                <div style="margin: 5px 0;"><span style="background: rgba(160, 160, 160, 0.3); padding: 2px 8px; border-radius: 4px;">ZERO</span> Zeros</div>
            </div>
            """, unsafe_allow_html=True)

            st.divider()

            st.markdown("### 📊 Stats")
            type_counts = hex_data['type'].value_counts().to_dict()
            for t, c in type_counts.items():
                st.markdown(f"- **{t}**: {c} lignes")

    with tab_header:
        st.subheader("Structure du Fichier")

        if magic in ('MZ', 'ZM'):
            try:
                parser = MZParser()
                result = parser.parse(file_bytes)

                col_h1, col_h2 = st.columns(2)

                with col_h1:
                    st.markdown("#### 📋 Header MZ")
                    header_data = result['header']

                    header_df = {
                        "Champ": [
                            "Magic", "Last Page Bytes", "Pages", "Relocations",
                            "Header Paras", "Min Alloc", "Max Alloc",
                            "Initial SS", "Initial SP", "Checksum",
                            "Initial IP", "Initial CS", "Relocation Offset", "Overlay"
                        ],
                        "Valeur": [
                            header_data['magic'],
                            f"0x{header_data['last_page_bytes']:04X} ({header_data['last_page_bytes']})",
                            f"0x{header_data['pages_in_file']:04X} ({header_data['pages_in_file']})",
                            f"0x{header_data['relocation_count']:04X} ({header_data['relocation_count']})",
                            f"0x{header_data['header_paragraphs']:04X} ({header_data['header_paragraphs']} para = {header_data['header_size']} bytes)",
                            f"0x{header_data['min_alloc']:04X} ({header_data['min_alloc'] * 16} bytes)",
                            f"0x{header_data['max_alloc']:04X} ({header_data['max_alloc'] * 16} bytes)",
                            f"0x{header_data['initial_ss']:04X} (relatif)",
                            f"0x{header_data['initial_sp']:04X}",
                            f"0x{header_data['checksum']:04X}",
                            f"0x{header_data['initial_ip']:04X}",
                            f"0x{header_data['initial_cs']:04X} (relatif)",
                            f"0x{header_data['relocation_offset']:04X}",
                            f"0x{header_data['overlay_number']:04X}"
                        ]
                    }
                    st.dataframe(
                        {"Champ": header_df["Champ"], "Valeur": header_df["Valeur"]},
                        use_container_width=True,
                        hide_index=True
                    )

                with col_h2:
                    st.markdown("#### 🎯 Points d'entree")

                    ep = result['entry_point']
                    st.metric("Entry Point", f"{ep['cs']:04X}:{ep['ip']:04X}")
                    st.metric("Offset fichier", f"0x{ep['file_offset']:04X}")

                    stack = result['stack']
                    st.metric("Stack", f"{stack['ss']:04X}:{stack['sp']:04X}")

                    st.divider()

                    st.markdown("#### 📐 Segments")
                    for seg in result['segments']:
                        with st.expander(f"{seg['name']} ({seg['type']})"):
                            st.write(f"Base relative: 0x{seg['relative_base']:04X}")
                            st.write(f"But: {seg['purpose']}")
                            if 'relocation_count' in seg:
                                st.write(f"Relocations: {seg['relocation_count']}")

                # Relocation table
                if result['relocation_table']:
                    st.markdown("#### 🔄 Table de Relocation")
                    reloc_df = {
                        "Index": [r['index'] for r in result['relocation_table']],
                        "Offset": [f"0x{r['offset']:04X}" for r in result['relocation_table']],
                        "Segment": [f"0x{r['segment']:04X}" for r in result['relocation_table']],
                        "Adresse fichier": [f"0x{r['file_address']:04X}" for r in result['relocation_table']]
                    }
                    st.dataframe(reloc_df, use_container_width=True, height=200)

                # Extended format
                if result['is_extended']:
                    st.warning(f"⚠️ Format etendu detecte: {result['extended_header']['type']}")
            except Exception as e:
                st.error(f"Erreur parsing MZ: {e}")

        elif file_ext == 'com':
            try:
                parser = COMParser()
                result = parser.parse(file_bytes)

                st.markdown("#### 📋 Format COM")
                st.metric("Taille", f"{result['file_size']} bytes")
                st.metric("Entry Point", "CS:0100h")

                st.markdown("#### 🗺️ Layout Memoire")
                layout = result['memory_layout']
                for name, info in layout.items():
                    st.write(f"**{name.upper()}**: 0x{info['start']:04X} - 0x{info['end']:04X} ({info['size']} bytes)")

                if result['interrupts']:
                    st.markdown(f"#### ⚡ Interruptions detectees: {len(result['interrupts'])}")
                    for intr in result['interrupts'][:10]:
                        st.write(f"- INT 0x{intr['number']:02X} a offset 0x{intr['offset']:04X}")
            except Exception as e:
                st.error(f"Erreur parsing COM: {e}")

        else:
            st.info("Format ASM source - pas de header binaire a analyser")

    with tab_analysis:
        st.subheader("Analyse Avancee")

        if magic in ('MZ', 'ZM'):
            try:
                parser = MZParser()
                result = parser.parse(file_bytes)

                # Complexity assessment
                report = parser.generate_migration_report()

                col_a1, col_a2, col_a3 = st.columns(3)

                with col_a1:
                    complexity = report['complexity']
                    color = "#4ecca3" if complexity['level'] == 'LOW' else "#f4d03f" if complexity['level'] == 'MEDIUM' else "#e94560"
                    st.markdown(f"""
                    <div style="
                        background: {color}20;
                        border: 2px solid {color};
                        border-radius: 10px;
                        padding: 1rem;
                        text-align: center;
                    ">
                        <div style="font-size: 2rem; color: {color}; font-weight: bold;">{complexity['score']}/10</div>
                        <div style="color: #a0a0a0; font-size: 0.9rem;">Complexite: {complexity['level']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_a2:
                    difficulty = report['conversion_difficulty']
                    st.markdown(f"""
                    <div style="
                        background: #16213e;
                        border: 1px solid #0f3460;
                        border-radius: 10px;
                        padding: 1rem;
                    ">
                        <h4 style="color: #e94560;">Difficulte</h4>
                        <p style="color: #a0a0a0;">Auto-convertible: {'✅' if difficulty['auto_convertible'] else '❌'}</p>
                        <p style="color: #a0a0a0;">Review requise: {'✅' if difficulty['requires_review'] else '❌'}</p>
                        <p style="color: #a0a0a0;">Rewrite necessaire: {'⚠️' if difficulty['requires_rewrite'] else '❌'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col_a3:
                    work = report['estimated_manual_work']
                    st.markdown(f"""
                    <div style="
                        background: #16213e;
                        border: 1px solid #0f3460;
                        border-radius: 10px;
                        padding: 1rem;
                    ">
                        <h4 style="color: #e94560;">Estimation</h4>
                        <p style="color: #a0a0a0; font-size: 1.5rem;">{work['estimated_hours']}h</p>
                        <p style="color: #a0a0a0;">Confiance: {work['confidence']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Recommendations
                if report['recommendations']:
                    st.markdown("#### 💡 Recommandations")
                    for rec in report['recommendations']:
                        priority_color = {"CRITICAL": "#e94560", "HIGH": "#ff6b6b", "MEDIUM": "#f4d03f", "LOW": "#4ecca3"}.get(rec['priority'], "#a0a0a0")
                        st.markdown(f"""
                        <div style="
                            background: {priority_color}10;
                            border-left: 4px solid {priority_color};
                            border-radius: 5px;
                            padding: 0.75rem;
                            margin: 0.5rem 0;
                        ">
                            <strong style="color: {priority_color};">[{rec['priority']}] {rec['category']}</strong><br>
                            <span style="color: #eeeeee;">{rec['message']}</span><br>
                            <span style="color: #a0a0a0; font-size: 0.85rem;">→ {rec['action']}</span>
                        </div>
                        """, unsafe_allow_html=True)

                # Zones visualization
                st.markdown("#### 🗺️ Zones Code/Data")
                zones = result['zones']

                import plotly.graph_objects as go

                fig = go.Figure()

                for zone in zones:
                    color = "#e94560" if zone['type'] == 'code' else "#4ecca3"
                    fig.add_trace(go.Bar(
                        x=[zone['offset'] + zone['size'] / 2],
                        y=[zone['size']],
                        width=[zone['size']],
                        marker_color=color,
                        opacity=0.7,
                        name=f"{zone['type'].upper()} @ 0x{zone['offset']:04X}",
                        hovertemplate=f"Type: {zone['type']}<br>Offset: 0x{zone['offset']:04X}<br>Taille: {zone['size']} bytes<extra></extra>"
                    ))

                fig.update_layout(
                    title="Distribution des Zones",
                    xaxis_title="Offset dans le fichier",
                    yaxis_title="Taille (bytes)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': '#eeeeee'},
                    showlegend=False,
                    barmode='overlay'
                )

                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Erreur analyse: {e}")

    with tab_export:
        st.subheader("Export pour CodeCartographer")

        if magic in ('MZ', 'ZM'):
            try:
                parser = MZParser()
                result = parser.parse(file_bytes)

                corpus_data = {
                    "format": "MZ",
                    "header": result['header'],
                    "metrics": {
                        "file_size": result['metadata']['file_size'],
                        "program_size": result['header']['calculated_program_size'],
                        "relocation_count": len(result['relocation_table']),
                        "segment_count": len(result['segments']),
                        "zone_count": len(result['zones'])
                    },
                    "complexity": result.get('complexity', {}),
                    "api_surface": [
                        {"type": "INT", "number": f"{i['number']:02X}", "offset": i['offset']}
                        for i in result.get('apiSurface', [])
                    ]
                }

                corpus_json = str(corpus_data).replace("'", '"')

                st.download_button(
                    "📥 Telecharger JSON Corpus",
                    data=str(corpus_data).replace("'", '"'),
                    file_name=f"{uploaded_file.name}_corpus.json",
                    mime="application/json",
                    use_container_width=True
                )

                with st.expander("Voir le JSON"):
                    st.code(str(corpus_data), language="json")

            except Exception as e:
                st.error(f"Erreur export: {e}")
        else:
            st.info("Export corpus disponible pour les formats binaires MZ/COM")

else:
    # Etat vide
    st.markdown("""
    <div style="
        background: #16213e;
        border-radius: 10px;
        padding: 3rem;
        text-align: center;
        border: 1px solid #0f3460;
        margin: 2rem 0;
    ">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📂</div>
        <h3 style="color: #a0a0a0;">Aucun fichier charge</h3>
        <p style="color: #a0a0a0;">Utilisez le uploader ci-dessus ou deposez un fichier directement</p>
    </div>
    """, unsafe_allow_html=True)

    # Demo info
    st.markdown("### 📖 Formats supportes")

    demo_col1, demo_col2, demo_col3 = st.columns(3)

    with demo_col1:
        st.markdown("""
        <div style="background: #16213e; border-radius: 10px; padding: 1rem;">
            <h4 style="color: #e94560;">.COM</h4>
            <p style="color: #a0a0a0; font-size: 0.85rem;">
                Format plat 64K<br>
                CS=DS=ES=SS<br>
                IP=0100h fixe<br>
                Pas de relocation
            </p>
        </div>
        """, unsafe_allow_html=True)

    with demo_col2:
        st.markdown("""
        <div style="background: #16213e; border-radius: 10px; padding: 1rem;">
            <h4 style="color: #e94560;">.EXE (MZ)</h4>
            <p style="color: #a0a0a0; font-size: 0.85rem;">
                Header 28+ bytes<br>
                Table de relocation<br>
                Segments multiples<br>
                Entry point variable
            </p>
        </div>
        """, unsafe_allow_html=True)

    with demo_col3:
        st.markdown("""
        <div style="background: #16213e; border-radius: 10px; padding: 1rem;">
            <h4 style="color: #e94560;">.ASM</h4>
            <p style="color: #a0a0a0; font-size: 0.85rem;">
                Source texte<br>
                Directives MASM/TASM<br>
                Macros et structures<br>
                Conversion directe
            </p>
        </div>
        """, unsafe_allow_html=True)
