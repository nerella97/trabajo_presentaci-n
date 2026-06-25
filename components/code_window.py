import streamlit as st


def code_window(title: str, code: str):
    st.markdown(
        f"""
<div class="code-window">
    <div class="code-header">{title}</div>
    <div class="code-body">{code}</div>
</div>
        """,
        unsafe_allow_html=True
    )