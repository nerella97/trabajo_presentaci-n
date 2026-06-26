import random
from datetime import datetime

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh


def generar_datos_radar():
    ejes = ["Horizontal", "Vertical"]
    carriles = {
        "Horizontal": ["H1", "H2"],
        "Vertical": ["V1", "V2"],
    }
    sentidos = {
        "Horizontal": ["Oeste → Este", "Este → Oeste"],
        "Vertical": ["Norte → Sur", "Sur → Norte"],
    }

    datos = []

    for eje in ejes:
        for i in range(5):
            carril = random.choice(carriles[eje])

            datos.append(
                {
                    "Hora": datetime.now().strftime("%H:%M:%S"),
                    "ID": f"RD-{random.randint(1000, 9999)}",
                    "Eje": eje,
                    "Carril": carril,
                    "Veloc. instantánea": random.randint(10, 70),
                    "Sentido": random.choice(sentidos[eje]),
                    "Unidad": "km/h",
                }
            )

    return pd.DataFrame(datos)


def generar_datos_espira():
    ejes = ["Horizontal", "Vertical"]
    carriles = {
        "Horizontal": ["H1", "H2"],
        "Vertical": ["V1", "V2"],
    }

    datos = []

    for eje in ejes:
        for i in range(5):
            carril = random.choice(carriles[eje])

            datos.append(
                {
                    "Hora": datetime.now().strftime("%H:%M:%S"),
                    "ID": f"EI-{random.randint(1000, 9999)}",
                    "Eje": eje,
                    "Carril": carril,
                    "Veh. detectado": random.choice(["Sí", "No"]),
                    "Tiempo ocupación": round(random.uniform(0.3, 3.5), 2),
                    "Inter. entre veh.": round(random.uniform(1.0, 8.0), 2),
                    "Unidad": "s",
                }
            )

    return pd.DataFrame(datos)


def generar_datos_camara():
    ejes = ["Horizontal", "Vertical"]
    carriles = {
        "Horizontal": ["H1", "H2"],
        "Vertical": ["V1", "V2"],
    }

    datos = []

    for eje in ejes:
        for i in range(5):
            carril = random.choice(carriles[eje])

            datos.append(
                {
                    "Hora": datetime.now().strftime("%H:%M:%S"),
                    "ID": f"CAM-{random.randint(1000, 9999)}",
                    "Eje": eje,
                    "Carril": carril,
                    "Veh. detectados": random.randint(3, 25),
                    "Veh. detenidos": random.randint(0, 18),
                    "Peatones": random.randint(0, 5),
                    "Ocupación": random.choice(["Baja", "Media", "Alta"]),
                }
            )

    return pd.DataFrame(datos)


def render_lectura(data=None):
    st_autorefresh(interval=2000, key="refresh_lectura_datos_crudos")

    st.markdown("## 1. Lectura de datos crudos")

    st.markdown(
        """
        En esta etapa se visualiza la entrada directa de datos desde los sensores hacia
        el sistema. Los valores todavía no han sido limpiados, seleccionados ni
        transformados. Por ello, cada sensor muestra diferentes tipos de señales crudas
        que luego serán procesadas en las siguientes etapas.
        """
    )

    df_radar = generar_datos_radar()
    df_espira = generar_datos_espira()
    df_camara = generar_datos_camara()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="sensor-window">
                <div class="sensor-title">📡 Radar Doppler</div>
                <div class="sensor-subtitle">Velocidad, carril y sentido detectado</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(df_radar, use_container_width=True, hide_index=True)

    with col2:
        st.markdown(
            """
            <div class="sensor-window">
                <div class="sensor-title">🧲 Espira inductiva</div>
                <div class="sensor-subtitle">Paso vehicular, ocupación e intervalo</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(df_espira, use_container_width=True, hide_index=True)

    with col3:
        st.markdown(
            """
            <div class="sensor-window">
                <div class="sensor-title">🎥 Cámara inteligente</div>
                <div class="sensor-subtitle">Vehículos, cola, peatones y ocupación visual</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(df_camara, use_container_width=True, hide_index=True)

    st.markdown(
        """
        Los datos mostrados corresponden a señales crudas. En las siguientes etapas,
        el sistema eliminará registros inválidos, seleccionará las variables útiles
        y calculará los indicadores principales del proyecto: velocidad promedio,
        flujo vehicular y longitud de cola.
        """
    )