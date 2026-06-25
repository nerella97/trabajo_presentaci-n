import streamlit as st

from components.code_window import code_window


def render_lectura(data):
    st.markdown(
        '<div class="section-title">1. Lectura de datos crudos del sensor</div>',
        unsafe_allow_html=True
    )

    st.write(
        "En campo, cada equipo no entrega una sola variable. "
        "Cada sensor puede entregar varias columnas o señales. "
        "Luego el software decide cuáles son útiles para el modelo."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
<div class="card">
    <div class="card-title">📡 Radar Doppler</div>
    <div class="selected-var">velocidad_promedio</div>
    <div class="discarded-var">velocidad_maxima</div>
    <div class="discarded-var">velocidad_minima</div>
    <div class="discarded-var">estado_sensor</div>
</div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
<div class="card">
    <div class="card-title">🧲 Espira inductiva</div>
    <div class="selected-var">flujo_vehicular</div>
    <div class="discarded-var">ocupacion_carril</div>
    <div class="discarded-var">vehiculos_livianos</div>
    <div class="discarded-var">estado_sensor</div>
</div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
<div class="card">
    <div class="card-title">🎥 Cámara IA</div>
    <div class="selected-var">longitud_cola</div>
    <div class="discarded-var">vehiculos_detectados</div>
    <div class="discarded-var">incidentes</div>
    <div class="discarded-var">estado_sensor</div>
</div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Bases crudas recibidas")

    tab1, tab2, tab3 = st.tabs(["df_radar_raw", "df_espira_raw", "df_camara_raw"])

    with tab1:
        st.dataframe(data["df_radar_raw"], use_container_width=True)

    with tab2:
        st.dataframe(data["df_espira_raw"], use_container_width=True)

    with tab3:
        st.dataframe(data["df_camara_raw"], use_container_width=True)

    code_window(
        "lectura_datos.py",
        """df_radar = pd.DataFrame(...)
df_espira = pd.DataFrame(...)
df_camara = pd.DataFrame(...)"""
    )