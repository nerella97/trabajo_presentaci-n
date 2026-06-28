import streamlit as st

from components.code_window import code_window
from model import get_tiempo_verde


def render_control(modelo):
    st.markdown(
        '<div class="section-title">8. Control semafórico</div>',
        unsafe_allow_html=True
    )

    velocidad_actual = st.slider("Velocidad promedio actual (km/h)", 5, 60, 12)
    flujo_actual = st.slider("Flujo vehicular actual (veh/min)", 10, 100, 60)
    cola_actual = st.slider("Longitud de cola actual (m)", 0, 60, 25)

    nivel_congestion = modelo.predict([[
        velocidad_actual,
        flujo_actual,
        cola_actual
    ]])[0]

    tiempo_verde = get_tiempo_verde(nivel_congestion)

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown(
            f"""
<div class="result-box">
    <div class="result-sub">Resultado del sistema</div>
    <div class="result-main">{nivel_congestion}</div>
    <br>
    <div class="result-sub">Tiempo verde recomendado</div>
    <div class="result-main">{tiempo_verde} s</div>
    <br>
    <div class="metric-label">Orden enviada al controlador semafórico</div>
</div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
<div class="terminal">
&gt; Lectura de sensores recibida<br>
&gt; Radar Doppler: {velocidad_actual} km/h<br>
&gt; Espira inductiva: {flujo_actual} veh/min<br>
&gt; Cámara IA: {cola_actual} m<br><br>
&gt; Ejecutando modelo de decisión...<br>
&gt; Nivel de congestión: {nivel_congestion}<br>
&gt; Tiempo verde recomendado: {tiempo_verde} segundos<br>
&gt; Orden enviada al controlador semafórico.
</div>
            """,
            unsafe_allow_html=True
        )

    code_window(
        "control_semaforico.py",
        """if nivel_congestion == "ALTA":
    tiempo_verde = 40
elif nivel_congestion == "MEDIA":
    tiempo_verde = 30
else:
    tiempo_verde = 20"""
    )