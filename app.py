import random
import streamlit as st

from styles import load_styles
from data import get_all_data
from model import train_model
from components.scada_view import render_scada_panel
from pages_app.lectura import render_lectura
from pages_app.limpieza import render_limpieza
from pages_app.seleccion import render_seleccion
from pages_app.consolidacion import render_consolidacion
from pages_app.modelo import render_modelo
from pages_app.prediccion import render_prediccion
from pages_app.control import render_control


st.set_page_config(
    page_title="Simulación HMI/SCADA - Semáforos Inteligentes",
    page_icon="🚦",
    layout="wide"
)

load_styles()

data = get_all_data()
modelo, X, y = train_model(data["df_entrenamiento_ia"])

st.sidebar.markdown("## 🚦 Simulación")
st.sidebar.markdown("### HMI / SCADA académico")

etapa = st.sidebar.radio(
    "Navegar por etapas",
    [
        "1. Lectura de datos crudos",
        "2. Limpieza de datos",
        "3. Selección de variables",
        "4. Consolidación de DataFrames",
        "5. Modelo IA",
        "6. Predicción en tiempo real",
        "7. Control semafórico",
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Sensores considerados**")
st.sidebar.markdown("- Radar Doppler")
st.sidebar.markdown("- Espira inductiva")
st.sidebar.markdown("- Cámara de visión artificial")

st.markdown(
    '<div class="main-title">Simulación HMI / SCADA - Semáforos Inteligentes</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Representación académica de sensores, variables físicas, procesamiento de datos e intervención semafórica.</div>',
    unsafe_allow_html=True
)

velocidad_live = random.randint(10, 20)
flujo_live = random.randint(52, 68)
cola_live = random.randint(20, 30)

render_scada_panel(velocidad_live, flujo_live, cola_live)

st.markdown("---")

if etapa == "1. Lectura de datos crudos":
    render_lectura(data)

elif etapa == "2. Limpieza de datos":
    render_limpieza(data)

elif etapa == "3. Selección de variables":
    render_seleccion(data)

elif etapa == "4. Consolidación de DataFrames":
    render_consolidacion(data)

elif etapa == "5. Modelo IA":
    render_modelo(X, y)

elif etapa == "6. Predicción en tiempo real":
    render_prediccion(modelo)

elif etapa == "7. Control semafórico":
    render_control(modelo)