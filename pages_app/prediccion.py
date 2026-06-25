import streamlit as st

from components.code_window import code_window


def render_prediccion(modelo):
    st.markdown(
        '<div class="section-title">6. Predicción en tiempo real</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        velocidad_actual = st.slider("Velocidad actual (km/h)", 5, 60, 12)

    with col2:
        flujo_actual = st.slider("Flujo actual (veh/min)", 10, 100, 60)

    with col3:
        cola_actual = st.slider("Longitud de cola actual (m)", 0, 60, 25)

    prediccion = modelo.predict([[
        velocidad_actual,
        flujo_actual,
        cola_actual
    ]])[0]

    code_window(
        "prediccion.py",
        """nivel_congestion = modelo_congestion.predict([[
    velocidad_actual,
    flujo_actual,
    cola_actual
]])[0]"""
    )

    st.markdown(
        f"""
<div class="result-box">
    <div class="result-sub">Nivel de congestión predicho</div>
    <div class="result-main">{prediccion}</div>
</div>
        """,
        unsafe_allow_html=True
    )