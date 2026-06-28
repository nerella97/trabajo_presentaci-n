import streamlit as st

from components.code_window import code_window


def render_modelo(X, y):
    st.markdown(
        '<div class="section-title">6. Entrenamiento del modelo IA</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Variables de entrada X")
        st.dataframe(X, use_container_width=True)

    with col2:
        st.markdown("### Variable de salida y")
        st.dataframe(y, use_container_width=True)

    code_window(
        "modelo_ia.py",
        """X = df_entrenamiento_ia[
    ["velocidad_promedio", "flujo_vehicular", "longitud_cola"]
]

y = df_entrenamiento_ia["nivel_congestion"]

modelo_congestion = DecisionTreeClassifier(random_state=42)
modelo_congestion.fit(X, y)"""
    )

    st.info(
        "El árbol de decisión aprende la relación entre las variables físicas y el nivel de congestión."
    )