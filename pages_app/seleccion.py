import streamlit as st

from components.code_window import code_window


def render_seleccion(data):
    st.markdown(
        '<div class="section-title">4. Selección de variables relevantes</div>',
        unsafe_allow_html=True
    )

    st.write(
        "El software toma solo las columnas que representan mejor el nivel de congestión: "
        "`velocidad_promedio`, `flujo_vehicular` y `longitud_cola`."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### df_velocidad")
        st.dataframe(data["df_velocidad"], use_container_width=True)

    with col2:
        st.markdown("### df_flujo")
        st.dataframe(data["df_flujo"], use_container_width=True)

    with col3:
        st.markdown("### df_cola")
        st.dataframe(data["df_cola"], use_container_width=True)

    code_window(
        "seleccion_variables.py",
        """df_velocidad = df_radar[
    ["fecha_hora", "velocidad_promedio"]
]

df_flujo = df_espira[
    ["fecha_hora", "flujo_vehicular"]
]

df_cola = df_camara[
    ["fecha_hora", "longitud_cola"]
]"""
    )

    st.info(
        "Esta etapa representa una decisión técnica: de todas las variables que entrega el sensor, "
        "se eligen solo las necesarias para la IA."
    )