import streamlit as st

from components.code_window import code_window


def render_limpieza(data):
    st.markdown(
        '<div class="section-title">2. Limpieza de datos</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Antes de seleccionar variables para la IA, se revisan datos vacíos. "
        "En esta simulación, los valores numéricos faltantes se reemplazan por el promedio de su columna."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Datos crudos")
        st.dataframe(data["df_radar_raw"], use_container_width=True)
        st.dataframe(data["df_espira_raw"], use_container_width=True)
        st.dataframe(data["df_camara_raw"], use_container_width=True)

    with col2:
        st.markdown("### Datos limpios")
        st.dataframe(data["df_radar"], use_container_width=True)
        st.dataframe(data["df_espira"], use_container_width=True)
        st.dataframe(data["df_camara"], use_container_width=True)

    code_window(
        "limpieza_datos.py",
        """def limpiar_datos(df):
    df_limpio = df.copy()
    numeric_cols = df_limpio.select_dtypes(include="number").columns

    for col in numeric_cols:
        df_limpio[col] = df_limpio[col].fillna(df_limpio[col].mean())

    return df_limpio

df_radar = limpiar_datos(df_radar_raw)
df_espira = limpiar_datos(df_espira_raw)
df_camara = limpiar_datos(df_camara_raw)"""
    )

    st.success("La limpieza evita que el modelo reciba valores vacíos.")