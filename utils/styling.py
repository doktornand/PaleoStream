"""
Styling - CSS custom et theming pour Streamlit
"""

import streamlit as st

def apply_custom_styling():
    """Injecte le CSS custom cyberpunk/SCADA"""

    css = """
    <style>
    /* Global */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Header */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 2px solid #e94560;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        color: #e94560 !important;
        font-size: 3rem !important;
        text-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
        letter-spacing: 3px;
    }

    .main-header p {
        color: #a0a0a0;
        font-size: 1.2rem;
    }

    /* Cards */
    .stMetric {
        background: #0f3460;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e94560;
        box-shadow: 0 0 10px rgba(233, 69, 96, 0.2);
    }

    .stMetric > div {
        color: #eeeeee !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 0 15px rgba(233, 69, 96, 0.4) !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(233, 69, 96, 0.6) !important;
        transform: translateY(-2px) !important;
    }

    /* Code blocks */
    .stCodeBlock {
        background: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }

    .stCodeBlock code {
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        font-size: 13px !important;
    }

    /* Dataframes */
    .stDataFrame {
        background: #16213e;
        border-radius: 10px;
        border: 1px solid #0f3460;
    }

    .stDataFrame th {
        background: #0f3460 !important;
        color: #e94560 !important;
        font-weight: bold !important;
    }

    .stDataFrame td {
        color: #eeeeee !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #16213e !important;
        border-right: 2px solid #e94560;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #eeeeee !important;
    }

    /* Progress */
    .stProgress > div > div {
        background: linear-gradient(90deg, #e94560, #ff6b6b) !important;
    }

    /* Alerts */
    .stAlert {
        border-radius: 10px !important;
        border-left: 4px solid !important;
    }

    .stAlert[data-baseweb="notification"][kind="error"] {
        background: rgba(233, 69, 96, 0.1) !important;
        border-color: #e94560 !important;
    }

    .stAlert[data-baseweb="notification"][kind="success"] {
        background: rgba(78, 204, 163, 0.1) !important;
        border-color: #4ecca3 !important;
    }

    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: rgba(244, 208, 63, 0.1) !important;
        border-color: #f4d03f !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #16213e !important;
        border-radius: 10px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #a0a0a0 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #e94560 !important;
        border-bottom-color: #e94560 !important;
    }

    /* Selectbox, text input */
    .stSelectbox > div > div, .stTextInput > div > div {
        background: #0f3460 !important;
        border-color: #16213e !important;
        color: #eeeeee !important;
    }

    /* File uploader */
    .stFileUploader > div {
        background: #16213e !important;
        border: 2px dashed #e94560 !important;
        border-radius: 10px !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #0f3460 !important;
        color: #e94560 !important;
        border-radius: 8px !important;
    }

    /* Badges */
    .badge-scada {
        display: inline-block;
        background: #0f3460;
        color: #e94560;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        border: 1px solid #e94560;
        margin: 2px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }

    ::-webkit-scrollbar-thumb {
        background: #e94560;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #ff6b6b;
    }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

def render_header(title: str, subtitle: str = ""):
    """Rendu du header principal"""
    st.markdown(f"""
    <div class="main-header">
        <h1>{title}</h1>
        {f"<p>{subtitle}</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def render_badge(text: str, color: str = "#e94560"):
    """Rendu d'un badge style"""
    st.markdown(f"""
    <span class="badge-scada" style="border-color: {color}; color: {color};">
        {text}
    </span>
    """, unsafe_allow_html=True)

def render_metric_card(label: str, value: str, delta: str = None, color: str = "#e94560"):
    """Rendu d'une metrique stylee"""
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"""
        <div style="
            background: {color}20;
            border: 1px solid {color};
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        ">
            <div style="font-size: 2rem; color: {color}; font-weight: bold;">{value}</div>
            <div style="font-size: 0.8rem; color: #a0a0a0;">{label}</div>
        </div>
        """, unsafe_allow_html=True)
