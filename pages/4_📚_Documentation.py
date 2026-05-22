"""
Page 4: Documentation - Documentation integree
"""

import streamlit as st
from utils.styling import apply_custom_styling, render_header

st.set_page_config(
    page_title="Documentation | Scadassembler",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styling()

render_header("📚 DOCUMENTATION", "Guide complet de Scadassembler v2.0")

# Tabs pour differentes sections de documentation
tab_arch, tab_mz, tab_rules, tab_api = st.tabs([
    "🏗️ Architecture", "📦 Format MZ", "📐 Regles", "🔌 API"
])

with tab_arch:
    st.markdown("""
    <div style="background: #16213e; border-radius: 10px; padding: 2rem;">
        <h3 style="color: #e94560;">Pipeline de Conversion (5 Phases)</h3>

        <div style="margin: 2rem 0;">
            <div style="display: flex; align-items: center; margin: 1rem 0;">
                <div style="background: #e94560; color: white; padding: 0.5rem 1rem; border-radius: 5px; min-width: 150px; text-align: center;">
                    <strong>Phase 1</strong>
                </div>
                <div style="margin-left: 1rem; flex: 1;">
                    <h4 style="color: #eeeeee; margin: 0;">Chargement</h4>
                    <p style="color: #a0a0a0; margin: 0;">Detection du format (.COM/.EXE/.ASM), parsing binaire ou source</p>
                </div>
            </div>

            <div style="display: flex; align-items: center; margin: 1rem 0;">
                <div style="background: #e94560; color: white; padding: 0.5rem 1rem; border-radius: 5px; min-width: 150px; text-align: center;">
                    <strong>Phase 2</strong>
                </div>
                <div style="margin-left: 1rem; flex: 1;">
                    <h4 style="color: #eeeeee; margin: 0;">Analyse</h4>
                    <p style="color: #a0a0a0; margin: 0;">Construction du CFG, analyse dataflow, detection patterns SCADA/IoT</p>
                </div>
            </div>

            <div style="display: flex; align-items: center; margin: 1rem 0;">
                <div style="background: #e94560; color: white; padding: 0.5rem 1rem; border-radius: 5px; min-width: 150px; text-align: center;">
                    <strong>Phase 3</strong>
                </div>
                <div style="margin-left: 1rem; flex: 1;">
                    <h4 style="color: #eeeeee; margin: 0;">Transformation</h4>
                    <p style="color: #a0a0a0; margin: 0;">Application des regles hierarchiques JSON avec resolution de conflits</p>
                </div>
            </div>

            <div style="display: flex; align-items: center; margin: 1rem 0;">
                <div style="background: #e94560; color: white; padding: 0.5rem 1rem; border-radius: 5px; min-width: 150px; text-align: center;">
                    <strong>Phase 4</strong>
                </div>
                <div style="margin-left: 1rem; flex: 1;">
                    <h4 style="color: #eeeeee; margin: 0;">Emission</h4>
                    <p style="color: #a0a0a0; margin: 0;">Generation MASM32, NASM ou binaire PE selon le backend choisi</p>
                </div>
            </div>

            <div style="display: flex; align-items: center; margin: 1rem 0;">
                <div style="background: #e94560; color: white; padding: 0.5rem 1rem; border-radius: 5px; min-width: 150px; text-align: center;">
                    <strong>Phase 5</strong>
                </div>
                <div style="margin-left: 1rem; flex: 1;">
                    <h4 style="color: #eeeeee; margin: 0;">Validation</h4>
                    <p style="color: #a0a0a0; margin: 0;">Verification point d'entree, modele FLAT, prototypes Win32</p>
                </div>
            </div>
        </div>

        <h4 style="color: #e94560;">Structure des Modules</h4>
        <pre style="background: #0d1117; padding: 1rem; border-radius: 5px; overflow-x: auto;">
src/
├── loader/           # Parsers binaires
│   ├── mz_parser.py      # Parser complet format MZ
│   ├── com_parser.py     # Parser format COM
│   ├── pe_builder.py     # Generateur PE
│   └── binary_utils.py   # Utilitaires binaires
├── core/             # Pipeline et moteur
│   ├── converter.py      # Pipeline principal
│   ├── rule_engine.py    # Moteur de regles hierarchiques
│   ├── cfg_builder.py    # Construction du CFG
│   └── dataflow_analyzer.py
├── backends/         # Generateurs de code
│   ├── masm_backend.py   # Emission MASM32
│   ├── nasm_backend.py   # Emission NASM
│   └── pe_backend.py     # Emission binaire PE
└── plugins/          # Plugins specialises
    ├── bcd_emulator.py       # Emulation instructions BCD
    ├── farcall_resolver.py   # Resolution far calls
    ├── iot_bridge.py         # Bridge IoT moderne
    └── interrupt_dispatcher.py
        </pre>
    </div>
    """, unsafe_allow_html=True)

with tab_mz:
    st.markdown("""
    <div style="background: #16213e; border-radius: 10px; padding: 2rem;">
        <h3 style="color: #e94560;">Format MZ (MS-DOS Executable)</h3>

        <p style="color: #a0a0a0;">Le format MZ est le format executable standard de MS-DOS, nomme d'apres Mark Zbikowski.</p>

        <h4 style="color: #e94560;">Structure du Fichier</h4>

        <pre style="background: #0d1117; padding: 1rem; border-radius: 5px; overflow-x: auto;">
Offset  Size  Description
------  ----  -----------
  0      2    Magic "MZ" ou "ZM"
  2      2    Last page bytes (e_cblp)
  4      2    Pages in file (e_cp)
  6      2    Relocation count (e_crlc)
  8      2    Header paragraphs (e_cparhdr) * 16 = header size
  10     2    Min allocation (e_minalloc)
  12     2    Max allocation (e_maxalloc)
  14     2    Initial SS (e_ss) - relatif
  16     2    Initial SP (e_sp)
  18     2    Checksum (e_csum)
  20     2    Initial IP (e_ip)
  22     2    Initial CS (e_cs) - relatif
  24     2    Relocation offset (e_lfarlc)
  26     2    Overlay number (e_ovno)
  28     8    Reserved
  36     2    OEM ID
  38     2    OEM Info
  40     20   Reserved
  60     4    PE Header offset (e_lfanew)
        </pre>

        <h4 style="color: #e94560;">Calculs Importants</h4>

        <div style="background: #0f3460; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
            <p style="color: #eeeeee;"><strong>Taille du programme:</strong></p>
            <code style="color: #4ecca3;">program_size = pages * 512 - (last_page ? 512 - last_page : 0) - header_paras * 16</code>

            <p style="color: #eeeeee; margin-top: 1rem;"><strong>Point d'entree:</strong></p>
            <code style="color: #4ecca3;">physical = (loading_segment + CS) * 16 + IP</code>

            <p style="color: #eeeeee; margin-top: 1rem;"><strong>Conversion relocation:</strong></p>
            <code style="color: #4ecca3;">PE_RVA = segment * 16 + offset</code>
        </div>

        <h4 style="color: #e94560;">Mapping Segments → Sections PE</h4>

        <table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
            <tr style="background: #0f3460;">
                <th style="padding: 0.5rem; text-align: left; color: #e94560;">Segment DOS</th>
                <th style="padding: 0.5rem; text-align: left; color: #e94560;">Section PE</th>
                <th style="padding: 0.5rem; text-align: left; color: #e94560;">Caracteristiques</th>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">CODE</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">.text</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>CODE | EXECUTE | READ</code></td>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">DATA</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">.data</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>INITIALIZED_DATA | READ | WRITE</code></td>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">BSS</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">.bss</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>UNINITIALIZED_DATA | READ | WRITE</code></td>
            </tr>
            <tr>
                <td style="padding: 0.5rem;">STACK</td>
                <td style="padding: 0.5rem;">(integre)</td>
                <td style="padding: 0.5rem;"><code>SizeOfStackReserve/Commit</code></td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with tab_rules:
    st.markdown("""
    <div style="background: #16213e; border-radius: 10px; padding: 2rem;">
        <h3 style="color: #e94560;">Systeme de Regles Hierarchiques</h3>

        <p style="color: #a0a0a0;">Le moteur de regles utilise une cascade hierarchique avec 11 categories et resolution de conflits par priorite.</p>

        <h4 style="color: #e94560;">Ordre de Cascade</h4>

        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;">
            <span style="background: #e94560; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">architecture_rules (CRITICAL)</span>
            <span style="background: #e94560; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">format_rules (CRITICAL)</span>
            <span style="background: #ff6b6b; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">domain_rules (HIGH)</span>
            <span style="background: #ff6b6b; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">pattern_rules (HIGH)</span>
            <span style="background: #f4d03f; color: black; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">instruction_rules (MEDIUM)</span>
            <span style="background: #f4d03f; color: black; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">interrupt_rules (MEDIUM)</span>
            <span style="background: #f4d03f; color: black; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">register_rules (MEDIUM)</span>
            <span style="background: #f4d03f; color: black; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">segment_rules (MEDIUM)</span>
            <span style="background: #4ecca3; color: black; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">directive_rules (LOW)</span>
            <span style="background: #4ecca3; color: black; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">macro_rules (LOW)</span>
            <span style="background: #a0a0a0; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">fallback_rules (INFO)</span>
        </div>

        <h4 style="color: #e94560;">Schema d'une Regle</h4>

        <pre style="background: #0d1117; padding: 1rem; border-radius: 5px; overflow-x: auto;">
{
  "id": "arch_x86_16_to_32",
  "name": "Passage 16-bit vers 32-bit",
  "condition": {
    "source_arch": "x86_16",
    "target_arch": "x86_32"
  },
  "transformations": {
    "register_expansion": {
      "AX": "EAX", "BX": "EBX", "CX": "ECX", "DX": "EDX",
      "SI": "ESI", "DI": "EDI", "BP": "EBP", "SP": "ESP"
    },
    "stack_operations": {
      "PUSHF": "PUSHFD",
      "POPF": "POPFD"
    },
    "memory_model": {
      "source": ".MODEL SMALL",
      "target": ".MODEL FLAT, STDCALL"
    }
  }
}
        </pre>

        <h4 style="color: #e94560;">Types de Conditions</h4>

        <table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
            <tr style="background: #0f3460;">
                <th style="padding: 0.5rem; text-align: left; color: #e94560;">Type</th>
                <th style="padding: 0.5rem; text-align: left; color: #e94560;">Syntaxe</th>
                <th style="padding: 0.5rem; text-align: left; color: #e94560;">Exemple</th>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">Egalite</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>"field": "value"</code></td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>"source_arch": "x86_16"</code></td>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">Alternatives</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>"field": "a | b | c"</code></td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>"instruction": "CALLF | JMPF"</code></td>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">Liste</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>"field": ["a", "b"]</code></td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>"instructions": ["AAA", "DAA"]</code></td>
            </tr>
            <tr>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;">Comparateurs</td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>"field": {"gt": 10}</code></td>
                <td style="padding: 0.5rem; border-bottom: 1px solid #0f3460;"><code>"score": {"gt": 8}</code></td>
            </tr>
            <tr>
                <td style="padding: 0.5rem;">Regex</td>
                <td style="padding: 0.5rem;"><code>"field": {"regex": "^pattern"}</code></td>
                <td style="padding: 0.5rem;"><code>"directive": {"regex": "^\\.(8086|186)$"}</code></td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with tab_api:
    st.markdown("""
    <div style="background: #16213e; border-radius: 10px; padding: 2rem;">
        <h3 style="color: #e94560;">API et Integration</h3>

        <h4 style="color: #e94560;">Utilisation Programmatique</h4>

        <pre style="background: #0d1117; padding: 1rem; border-radius: 5px; overflow-x: auto;">
from core.mz_parser import MZParser
from core.rule_engine import HierarchicalRuleEngine
from core.converter import ScadassemblerConverter

# Parser un fichier MZ
parser = MZParser()
result = parser.parse(file_bytes)

# Evaluer les regles
engine = HierarchicalRuleEngine("config/hierarchical_rules.json")
context = {
    "source_arch": "x86_16",
    "target_arch": "x86_32",
    "source_format": "MZ",
    "target_format": "PE",
    "domain": "SCADA"
}
transformations = engine.evaluate(context)

# Convertir completement
converter = ScadassemblerConverter({
    "target_format": "MASM",
    "scada_mode": True
})
result = converter.convert("input.exe", "output.asm")
        </pre>

        <h4 style="color: #e94560;">Export CodeCartographer</h4>

        <pre style="background: #0d1117; padding: 1rem; border-radius: 5px; overflow-x: auto;">
# Generer un export pour analyse corpus
corpus_data = {
    "format": "MZ",
    "architecture": {"source": "x86_16", "target": "x86_32"},
    "metrics": {
        "file_size": result["metadata"]["file_size"],
        "relocation_count": len(result["relocation_table"]),
        "segment_count": len(result["segments"])
    },
    "instruction_distribution": parser.export_for_corpus_analysis()["instructionDistribution"],
    "api_surface": result.get("apiSurface", []),
    "migration_metadata": {
        "auto_convertible": complexity["score"] <= 3,
        "manual_reviews": len(recommendations)
    }
}
        </pre>

        <h4 style="color: #e94560;">Plugins Disponibles</h4>

        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 1rem 0;">
            <div style="background: #0f3460; padding: 1rem; border-radius: 5px;">
                <h5 style="color: #e94560;">BCDEmulator</h5>
                <p style="color: #a0a0a0; font-size: 0.85rem;">Emulation des instructions BCD (AAA, AAS, AAM, AAD, DAA, DAS)</p>
            </div>
            <div style="background: #0f3460; padding: 1rem; border-radius: 5px;">
                <h5 style="color: #e94560;">FarCallResolver</h5>
                <p style="color: #a0a0a0; font-size: 0.85rem;">Resolution des far calls avec tables de dispatch</p>
            </div>
            <div style="background: #0f3460; padding: 1rem; border-radius: 5px;">
                <h5 style="color: #e94560;">IoTBridge</h5>
                <p style="color: #a0a0a0; font-size: 0.85rem;">Bridge ports serie/parallele et timers vers Win32</p>
            </div>
            <div style="background: #0f3460; padding: 1rem; border-radius: 5px;">
                <h5 style="color: #e94560;">InterruptDispatcher</h5>
                <p style="color: #a0a0a0; font-size: 0.85rem;">Dispatch des interruptions DOS vers APIs Win32</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
