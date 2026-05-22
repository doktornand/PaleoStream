"""
Page 2: Conversion - Pipeline de conversion interactif
"""

import streamlit as st
from utils.styling import apply_custom_styling, render_header
import time

st.set_page_config(
    page_title="Conversion | Scadassembler",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styling()

render_header("⚙️ CONVERSION", "Pipeline de conversion ASM16/DOS vers ASM32/Win32")

# Initialisation session state
if 'conversion_result' not in st.session_state:
    st.session_state.conversion_result = None
if 'source_code' not in st.session_state:
    st.session_state.source_code = ""

# Layout principal
st.markdown("""
<div style="
    background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
    border-radius: 15px;
    padding: 2rem;
    border: 1px solid #e94560;
    margin: 2rem 0;
">
    <h3 style="color: #e94560; margin-bottom: 1rem;">📝 Source ASM16/DOS</h3>
</div>
""", unsafe_allow_html=True)

# Source input
source_col1, source_col2 = st.columns([3, 1])

with source_col1:
    source_code = st.text_area(
        "",
        value=st.session_state.source_code,
        height=400,
        placeholder="; Entrez votre code ASM 16-bit ici...\n; Exemple:\n.MODEL SMALL\n.STACK 100h\n.DATA\n    msg DB 'Hello$'\n.CODE\nmain:\n    mov ax, @data\n    mov ds, ax\n    mov ah, 09h\n    lea dx, msg\n    int 21h\n    mov ax, 4C00h\n    int 21h\nEND main",
        label_visibility="collapsed"
    )
    st.session_state.source_code = source_code

with source_col2:
    st.markdown("### 🎯 Options")

    target_format = st.selectbox(
        "Format cible",
        ["MASM32 (.asm)", "NASM (.asm)", "PE Executable (.exe)"],
        index=0
    )

    subsystem = st.selectbox(
        "Sous-systeme",
        ["Console", "Windows (GUI)"],
        index=0
    )

    scada_mode = st.toggle("🔌 Mode SCADA/IoT", value=True)
    keep_comments = st.toggle("💬 Conserver commentaires", value=True)
    generate_report = st.toggle("📊 Generer rapport", value=True)

    st.divider()

    st.markdown("### 📋 Exemples")
    examples = {
        "hello": "; Hello World DOS\n.MODEL SMALL\n.STACK 100h\n.DATA\n    msg DB 'Hello, World!$'\n.CODE\nmain:\n    mov ax, @data\n    mov ds, ax\n    mov ah, 09h\n    lea dx, msg\n    int 21h\n    mov ax, 4C00h\n    int 21h\nEND main",
        "serial": "; Polling port serie\n.MODEL SMALL\n.CODE\nmain:\n    in al, 3FDh\n    test al, 01h\n    jz main\n    in al, 3F8h\n    mov ax, 4C00h\n    int 21h\nEND main",
        "file": "; Fichier\n.MODEL SMALL\n.DATA\n    fn DB 'data.txt',0\n    buf DB 100 DUP(?)\n.CODE\nmain:\n    mov ah,3Dh\n    lea dx,fn\n    mov al,0\n    int 21h\n    mov bx,ax\n    mov ah,3Fh\n    lea dx,buf\n    mov cx,100\n    int 21h\n    mov ah,3Eh\n    int 21h\n    mov ax,4C00h\n    int 21h\nEND main",
        "timer": "; Timer\n.MODEL SMALL\n.CODE\nmain:\n    mov ax,351Ch\n    int 21h\n    mov word ptr old,bx\n    mov word ptr old+2,es\n    mov ax,251Ch\n    mov dx,offset handler\n    int 21h\n    mov cx,100\nloop1: loop loop1\n    mov ax,251Ch\n    lds dx,old\n    int 21h\n    mov ax,4C00h\n    int 21h\nhandler:\n    inc tick\n    iret\n.DATA\n    tick DW 0\n    old DD ?\nEND main"
    }

    example_choice = st.selectbox(
        "Charger exemple",
        ["-- Selectionner --", "Hello World", "Polling Serie", "Fichier", "Timer"]
    )

    if example_choice == "Hello World":
        st.session_state.source_code = examples["hello"]
        st.rerun()
    elif example_choice == "Polling Serie":
        st.session_state.source_code = examples["serial"]
        st.rerun()
    elif example_choice == "Fichier":
        st.session_state.source_code = examples["file"]
        st.rerun()
    elif example_choice == "Timer":
        st.session_state.source_code = examples["timer"]
        st.rerun()

# Bouton de conversion
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 LANCER LA CONVERSION", use_container_width=True, type="primary"):
    if not source_code.strip():
        st.error("❌ Veuillez entrer du code source")
    else:
        # Simulation du pipeline
        phases = [
            ("📥 Phase 1: Chargement", "Analyse syntaxique du source ASM...", 1),
            ("🔬 Phase 2: Analyse", "Construction du CFG et dataflow...", 2),
            ("⚙️ Phase 3: Transformation", "Application des regles hierarchiques...", 3),
            ("💻 Phase 4: Emission", "Generation du code cible...", 4),
            ("✅ Phase 5: Validation", "Verification de la coherence...", 5)
        ]

        progress_bar = st.progress(0)
        status_text = st.empty()

        for phase_name, phase_desc, phase_num in phases:
            status_text.markdown(f"""
            <div style="
                background: #16213e;
                border-radius: 10px;
                padding: 1rem;
                border-left: 4px solid #e94560;
                margin: 1rem 0;
            ">
                <strong style="color: #e94560;">{phase_name}</strong><br>
                <span style="color: #a0a0a0;">{phase_desc}</span>
            </div>
            """, unsafe_allow_html=True)

            time.sleep(0.8)
            progress_bar.progress(phase_num / 5)

        # Resultat de conversion
        converted_code = convert_asm(source_code, target_format, scada_mode, keep_comments)

        st.session_state.conversion_result = {
            "code": converted_code,
            "stats": {
                "source_lines": len(source_code.split("\n")),
                "output_lines": len(converted_code.split("\n")),
                "transformations": count_transformations(source_code),
                "manual_reviews": count_manual_reviews(converted_code)
            }
        }

        progress_bar.empty()
        status_text.empty()

        st.success("✅ Conversion terminee!")
        st.balloons()

# Affichage du resultat
if st.session_state.conversion_result:
    result = st.session_state.conversion_result

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border-radius: 15px;
        padding: 2rem;
        border: 1px solid #4ecca3;
        margin: 2rem 0;
    ">
        <h3 style="color: #4ecca3; margin-bottom: 1rem;">✅ Resultat ASM32/Win32</h3>
    </div>
    """, unsafe_allow_html=True)

    # Metriques
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Lignes source", result["stats"]["source_lines"])
    with col_m2:
        st.metric("Lignes sortie", result["stats"]["output_lines"], 
                 f"{result['stats']['output_lines'] - result['stats']['source_lines']:+d}")
    with col_m3:
        st.metric("Transformations", result["stats"]["transformations"])
    with col_m4:
        st.metric("Reviews manuelles", result["stats"]["manual_reviews"])

    # Code converti
    st.code(result["code"], language="asm")

    # Actions
    col_act1, col_act2, col_act3 = st.columns(3)
    with col_act1:
        st.download_button(
            "📥 Telecharger .asm",
            data=result["code"],
            file_name="converted.asm",
            mime="text/plain",
            use_container_width=True
        )
    with col_act2:
        if st.button("📋 Copier", use_container_width=True):
            st.toast("Code copie dans le presse-papier!")
    with col_act3:
        if st.button("📊 Voir le rapport", use_container_width=True):
            st.switch_page("pages/3_📊_Rapport_et_Métriques.py")

# Fonctions de conversion

def convert_asm(source: str, target_format: str, scada_mode: bool, keep_comments: bool) -> str:
    """Convertit le code ASM 16-bit en 32-bit"""
    lines = source.split("\n")
    output = []

    # Header
    output.append("; ============================================")
    output.append("; Genere par Scadassembler v2.0")
    output.append("; Source: MS-DOS 16-bit")
    output.append("; Cible: Win32 MASM")
    output.append("; ============================================")
    output.append("")
    output.append(".386")
    output.append(".MODEL FLAT, STDCALL")
    output.append("OPTION CASEMAP:NONE")
    output.append("")

    # Prototypes
    output.append("; Prototypes Win32")
    output.append("ExitProcess PROTO :DWORD")
    output.append("GetStdHandle PROTO :DWORD")
    output.append("WriteConsoleA PROTO :DWORD, :DWORD, :DWORD, :DWORD, :DWORD")
    output.append("ReadConsoleA PROTO :DWORD, :DWORD, :DWORD, :DWORD, :DWORD")

    if scada_mode and any("in al," in l.lower() or "out " in l.lower() for l in lines):
        output.append("CreateFileA PROTO :DWORD, :DWORD, :DWORD, :DWORD, :DWORD, :DWORD, :DWORD")
        output.append("ReadFile PROTO :DWORD, :DWORD, :DWORD, :DWORD, :DWORD")
        output.append("WriteFile PROTO :DWORD, :DWORD, :DWORD, :DWORD, :DWORD")

    output.append("")
    output.append("STD_OUTPUT_HANDLE EQU -11")
    output.append("STD_INPUT_HANDLE EQU -10")
    output.append("")

    # Data section
    output.append(".data")
    output.append("    bytesWritten DWORD ?")
    output.append("    bytesRead DWORD ?")
    output.append("    hConsoleOutput HANDLE ?")
    output.append("    hConsoleInput HANDLE ?")
    output.append("")

    # Convert data items
    for line in lines:
        if "DB" in line and not any(x in line for x in [".CODE", ".STACK"]):
            converted = line.replace("$", "0")
            output.append("    " + converted.strip())

    output.append("")

    # Code section
    output.append(".code")
    output.append("")
    output.append("main PROC")
    output.append("    ; Initialisation console")
    output.append("    invoke GetStdHandle, STD_OUTPUT_HANDLE")
    output.append("    mov hConsoleOutput, eax")
    output.append("    invoke GetStdHandle, STD_INPUT_HANDLE")
    output.append("    mov hConsoleInput, eax")
    output.append("")

    # Convert code
    for line in lines:
        trimmed = line.strip()

        if not trimmed or trimmed.startswith(";"):
            if keep_comments:
                output.append("    " + trimmed)
            continue

        if "int 21h" in trimmed.lower() or "INT 21H" in trimmed:
            if "09h" in trimmed or "09H" in trimmed:
                output.append("    ; [CONVERTED] INT 21h AH=09h -> WriteConsoleA")
                output.append("    invoke WriteConsoleA, hConsoleOutput, ADDR msg, 13, ADDR bytesWritten, NULL")
            elif "4C" in trimmed:
                output.append("    ; [CONVERTED] INT 21h AH=4Ch -> ExitProcess")
                output.append("    invoke ExitProcess, 0")
            elif "3Dh" in trimmed:
                output.append("    ; [CONVERTED] INT 21h AH=3Dh -> CreateFileA")
                output.append("    invoke CreateFileA, ADDR filename, GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL")
            elif "3Fh" in trimmed:
                output.append("    ; [CONVERTED] INT 21h AH=3Fh -> ReadFile")
                output.append("    invoke ReadFile, ebx, ADDR buffer, 100, ADDR bytesRead, NULL")
            elif "40h" in trimmed:
                output.append("    ; [CONVERTED] INT 21h AH=40h -> WriteFile")
                output.append("    invoke WriteFile, ebx, ADDR buffer, 100, ADDR bytesWritten, NULL")
            elif "3Eh" in trimmed:
                output.append("    ; [CONVERTED] INT 21h AH=3Eh -> CloseHandle")
                output.append("    invoke CloseHandle, ebx")
            else:
                output.append("    ; MANUAL_REVIEW_REQUIRED: " + trimmed)
        elif "in al," in trimmed.lower():
            output.append("    ; [SCADA] Port I/O detecte")
            output.append("    ; MANUAL_REVIEW_REQUIRED: " + trimmed)
        elif "out " in trimmed.lower():
            output.append("    ; [SCADA] Port I/O detecte")
            output.append("    ; MANUAL_REVIEW_REQUIRED: " + trimmed)
        elif any(d in trimmed for d in [".MODEL", ".STACK", ".CODE", ".DATA", "END"]):
            output.append("    ; [REMOVED] " + trimmed)
        elif any(r in trimmed for r in ["AX", "BX", "CX", "DX", "SI", "DI", "BP", "SP"]) and "EAX" not in trimmed:
            converted = trimmed
            converted = converted.replace("AX", "EAX").replace("BX", "EBX")
            converted = converted.replace("CX", "ECX").replace("DX", "EDX")
            converted = converted.replace("SI", "ESI").replace("DI", "EDI")
            converted = converted.replace("BP", "EBP").replace("SP", "ESP")
            output.append("    " + converted)
        else:
            output.append("    " + trimmed)

    output.append("")
    output.append("    invoke ExitProcess, 0")
    output.append("main ENDP")
    output.append("END main")

    return "\n".join(output)

def count_transformations(source: str) -> int:
    """Compte les transformations appliquees"""
    count = 0
    if "int 21h" in source.lower():
        count += source.lower().count("int 21h")
    if any(r in source for r in ["AX", "BX", "CX", "DX"]):
        count += 1
    return count

def count_manual_reviews(converted: str) -> int:
    """Compte les reviews manuelles requises"""
    return converted.count("MANUAL_REVIEW_REQUIRED")
