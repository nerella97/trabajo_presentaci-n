import streamlit as st

from components.code_window import code_window


def render_consolidacion(data):
    st.markdown(
        '<div class="section-title">4. Consolidación de DataFrames</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Las variables seleccionadas se unen por `fecha_hora` para formar una sola base de entrenamiento."
    )

    st.dataframe(data["df_entrenamiento_ia"], use_container_width=True)

    code_window(
        "consolidacion.py",
        """df_entrenamiento_ia = (
    df_velocidad
    .merge(df_flujo, on="fecha_hora")
    .merge(df_cola, on="fecha_hora")
)

df_entrenamiento_ia["nivel_congestion"] = [
    "ALTA", "MEDIA", "ALTA", "ALTA"
]"""
    )

    st.success(
        "Resultado: una base única con variables físicas y etiqueta histórica de congestión."
    )