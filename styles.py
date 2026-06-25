import streamlit as st


def load_styles():
    st.markdown(
        """
<style>
    .stApp {
        background: #07111F;
        color: #EAF6FF;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06101D, #0B1F33);
        border-right: 1px solid rgba(80, 255, 220, 0.18);
    }

    .main-title {
        font-size: 34px;
        font-weight: 900;
        color: #EAF6FF;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 16px;
        color: #9EBBD0;
        margin-bottom: 22px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #7DFFF0;
        margin-top: 10px;
        margin-bottom: 16px;
    }

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
</style>
        """,
        unsafe_allow_html=True
    )