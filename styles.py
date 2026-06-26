import streamlit as st


def load_styles():
    st.markdown(
        """
<style>
    /* =========================
       FONDO GENERAL
    ========================= */

    html, body, .stApp {
        background: #07111F !important;
        color: #EAF6FF !important;
        overflow-x: hidden !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main {
        background: #07111F !important;
        overflow-x: hidden !important;
    }

    /* =========================
       HEADER SUPERIOR VISIBLE
    ========================= */

    header[data-testid="stHeader"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        height: 56px !important;
        background: linear-gradient(90deg, #06101D, #0B1F33) !important;
        border-bottom: 1px solid rgba(125, 255, 240, 0.22) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.24) !important;
        z-index: 999999 !important;
    }

    header[data-testid="stHeader"]::before {
        content: "Simulación HMI / SCADA - Semáforos Inteligentes";
        position: fixed;
        top: 12px;
        left: 50%;
        transform: translateX(-50%);

        width: max-content;
        max-width: calc(100vw - 160px);

        color: #EAF6FF;
        font-size: 24px;
        font-weight: 950;
        letter-spacing: 0.2px;
        line-height: 1.2;
        z-index: 999999;
        text-align: center;

        pointer-events: none;
        text-shadow: 0 0 12px rgba(125, 255, 240, 0.12);
    }

    /* No ocultar controles del header */
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] svg,
    button[data-testid="stBaseButton-headerNoPadding"],
    button[kind="headerNoPadding"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #7DFFF0 !important;
        fill: #7DFFF0 !important;
        z-index: 1000000 !important;
    }

    /* Ocultar solo decoración inferior/superior innecesaria */
    div[data-testid="stDecoration"],
    footer {
        display: none !important;
    }

    /* =========================
       CONTENIDO PRINCIPAL PEGADO A LA IZQUIERDA
    ========================= */

    [data-testid="stMain"] {
        margin-left: 0 !important;
        padding-left: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        padding-left: 0 !important;
        overflow-x: hidden !important;
    }

    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-top: 4.1rem !important;
        padding-bottom: 1rem !important;

        padding-left: 0.15rem !important;
        padding-right: 0.45rem !important;

        margin-left: 0 !important;
        margin-right: 0 !important;

        max-width: 100% !important;
        width: 100% !important;

        box-sizing: border-box !important;
        overflow-x: hidden !important;
    }

    main .block-container {
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding-left: 0.15rem !important;
    }

    iframe {
        width: 100% !important;
        max-width: 100% !important;
    }

    /* =========================
       SIDEBAR NATIVO
       NO FORZADO, PARA QUE EL BOTÓN FUNCIONE
    ========================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06101D, #0B1F33) !important;
        border-right: 1px solid rgba(80, 255, 220, 0.25) !important;
        z-index: 999998 !important;
    }

    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #06101D, #0B1F33) !important;
        padding-top: 0.25rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }

    section[data-testid="stSidebarContent"] {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
        background: transparent !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.25rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
    }

    section[data-testid="stSidebar"] * {
        color: #EAF6FF !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #7DFFF0 !important;
        font-weight: 900 !important;
    }

    section[data-testid="stSidebar"] p {
        color: #BFD7E8 !important;
    }

    section[data-testid="stSidebar"] label {
        font-weight: 800 !important;
        font-size: 14px !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        color: #EAF6FF !important;
        font-weight: 850 !important;
        padding: 5px 0px !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        color: #7DFFF0 !important;
    }

    section[data-testid="stSidebar"] svg {
        color: #7DFFF0 !important;
        fill: #7DFFF0 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(125, 255, 240, 0.22) !important;
    }

    /* =========================
       TEXTOS GENERALES
    ========================= */

    h1, h2, h3, h4, h5, h6 {
        color: #EAF6FF !important;
    }

    p, span, label {
        color: #A9C8D8;
    }

    /* El título ahora está en el header */
    .main-title {
        display: block !important;
        text-align: right;
        padding-right:40px;
    }

    .subtitle {
        display: none !important;
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #7DFFF0;
        margin-top: 10px;
        margin-bottom: 16px;
    }

    /* =========================
       TARJETAS
    ========================= */

    .card {
        background: linear-gradient(145deg, #0B1E32, #0D2B3A);
        border: 1px solid rgba(125, 255, 240, 0.28);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 0 24px rgba(30, 200, 165, 0.10);
        min-height: 135px;
    }

    .card-title {
        color: #7DFFF0;
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .metric-big {
        font-size: 34px;
        color: #FFFFFF;
        font-weight: 900;
        line-height: 1.1;
    }

    .metric-label {
        color: #A9C8D8;
        font-size: 13px;
    }

    .ok {
        color: #1EF0B2;
        font-weight: 800;
    }

    .warning {
        color: #FFD166;
        font-weight: 800;
    }

    .danger {
        color: #FF6B6B;
        font-weight: 800;
    }

    /* =========================
       BLOQUES TIPO TERMINAL / CÓDIGO
    ========================= */

    .terminal {
        background: #020A12;
        color: #7DFFF0;
        border: 1px solid rgba(125, 255, 240, 0.35);
        border-radius: 16px;
        padding: 18px;
        font-family: Consolas, monospace;
        font-size: 14px;
        min-height: 210px;
        box-shadow: inset 0 0 20px rgba(30, 200, 165, 0.08);
    }

    .code-window {
        background: #08101A;
        border: 1px solid rgba(125, 255, 240, 0.25);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 0 22px rgba(30, 200, 165, 0.10);
        margin-bottom: 18px;
    }

    .code-header {
        background: #0D1B2A;
        padding: 10px 14px;
        color: #A9C8D8;
        font-family: Consolas, monospace;
        font-size: 13px;
        border-bottom: 1px solid rgba(125, 255, 240, 0.15);
    }

    .code-body {
        padding: 16px;
        font-family: Consolas, monospace;
        font-size: 14px;
        color: #EAF6FF;
        white-space: pre-wrap;
        line-height: 1.45;
    }

    .selected-var {
        background: rgba(30, 240, 178, 0.13);
        border-left: 4px solid #1EF0B2;
        color: #FFFFFF;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-weight: 800;
    }

    .discarded-var {
        color: #718A9A;
        padding: 8px 12px;
        margin-bottom: 8px;
        border-left: 4px solid rgba(113, 138, 154, 0.25);
    }

    .result-box {
        background: radial-gradient(circle at top left, #123F3A, #07111F 70%);
        border: 2px solid #1EF0B2;
        border-radius: 22px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 0 34px rgba(30, 240, 178, 0.22);
    }

    .result-main {
        font-size: 48px;
        font-weight: 950;
        color: #FFFFFF;
    }

    .result-sub {
        font-size: 20px;
        font-weight: 800;
        color: #7DFFF0;
    }

    /* =========================
       RESPONSIVE
    ========================= */

    @media (max-width: 900px) {
        header[data-testid="stHeader"]::before {
            font-size: 18px;
            left: 54px;
            top: 16px;
        }

        .block-container,
        [data-testid="stMainBlockContainer"] {
            padding-left: 0.15rem !important;
            padding-right: 0.25rem !important;
        }
    }

    .sensor-window {
    background: linear-gradient(180deg, #0D1B2E 0%, #08111F 100%);
    border: 1px solid rgba(82, 190, 255, 0.35);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: 0 0 18px rgba(0, 180, 255, 0.12);
}

.sensor-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #EAF6FF;
    margin-bottom: 4px;
}

.sensor-subtitle {
    font-size: 0.78rem;
    color: #8FB8D8;
}

</style>
        """,
        unsafe_allow_html=True
    )
    