import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

ESTADOS_SENSOR = ["Activo", "Activo", "Activo", "Activo", "Standby", "Error"]
WINDOW = 15


def _ts(offset_minutes: int = 0) -> str:
    return (datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=offset_minutes)).strftime(
        "%Y-%m-%d %H:%M"
    )


# ── Radar ──────────────────────────────────────────────────────────────────────

def _fila_radar(item: int) -> dict:
    ejes = ["Horizontal", "Vertical"]
    carriles = {"Horizontal": ["H1", "H2"], "Vertical": ["V1", "V2"]}
    sentidos = {
        "Horizontal": ["Oeste → Este", "Este → Oeste"],
        "Vertical": ["Norte → Sur", "Sur → Norte"],
    }
    eje = ejes[item % 2]
    carril = carriles[eje][item % 2]
    v_prom = random.randint(30, 65)
    return {
        "item": item,
        "fecha_hora": _ts(),
        "id_sensor": f"RD-{random.randint(1000, 9999)}",
        "sensor": "Radar Doppler",
        "eje": eje,
        "carril": carril,
        "sentido": random.choice(sentidos[eje]),
        "velocidad_promedio": v_prom,
        "velocidad_maxima": v_prom + random.randint(5, 20),
        "velocidad_minima": max(10, v_prom - random.randint(5, 20)),
        "distancia_deteccion": round(random.uniform(10.0, 50.0), 1),
        "unidad_velocidad": "km/h",
        "estado_sensor": random.choice(ESTADOS_SENSOR),
    }


def _init_radar() -> pd.DataFrame:
    return pd.DataFrame([_fila_radar(i + 1) for i in range(WINDOW)])


# ── Espira ─────────────────────────────────────────────────────────────────────

def _fila_espira(item: int) -> dict:
    ejes = ["Horizontal", "Vertical"]
    carriles = {"Horizontal": ["H1", "H2"], "Vertical": ["V1", "V2"]}
    eje = ejes[item % 2]
    carril = carriles[eje][item % 2]
    ocupacion = round(random.uniform(5.0, 95.0), 1)
    tiempo_ocup = (
        round(0.5 + (ocupacion / 100) * 4.5, 2)
        if ocupacion > 60
        else round(random.uniform(0.3, 2.5), 2)
    )
    flujo = random.randint(5, 40)
    livianos = int(flujo * random.uniform(0.6, 0.85))
    pesados = flujo - livianos
    return {
        "item": item,
        "fecha_hora": _ts(),
        "id_sensor": f"EI-{random.randint(1000, 9999)}",
        "sensor": "Espira Inductiva",
        "eje": eje,
        "carril": carril,
        "vehiculo_detectado": "Sí" if random.random() > 0.15 else "No",
        "flujo_vehicular": flujo,
        "ocupacion_carril": ocupacion,
        "vehiculos_livianos": livianos,
        "vehiculos_pesados": pesados,
        "tiempo_ocupacion": tiempo_ocup,
        "intervalo_entre_vehiculos": round(random.uniform(1.0, 8.0), 2),
        "unidad_flujo": "veh/min",
        "estado_sensor": random.choice(ESTADOS_SENSOR),
    }


def _init_espira() -> pd.DataFrame:
    return pd.DataFrame([_fila_espira(i + 1) for i in range(WINDOW)])


# ── Cámara ─────────────────────────────────────────────────────────────────────

def _fila_camara(item: int) -> dict:
    ejes = ["Horizontal", "Vertical"]
    zonas = {"Horizontal": ["Zona-H1", "Zona-H2"], "Vertical": ["Zona-V1", "Zona-V2"]}
    incidentes_posibles = [
        "Ninguno", "Ninguno", "Ninguno",
        "Frenada brusca", "Vehículo detenido", "Peatón en calzada",
    ]
    eje = ejes[item % 2]
    zona = zonas[eje][item % 2]
    ocupacion_visual = random.choice(["Baja", "Media", "Alta"])
    incidente = random.choice(incidentes_posibles)
    veh_detectados = random.randint(3, 25)
    if ocupacion_visual == "Alta":
        veh_detenidos = random.randint(int(veh_detectados * 0.4), veh_detectados)
    elif ocupacion_visual == "Media":
        veh_detenidos = random.randint(1, int(veh_detectados * 0.4))
    else:
        veh_detenidos = random.randint(0, 3)
    if incidente != "Ninguno":
        longitud_cola = random.randint(30, 120)
    else:
        longitud_cola = random.randint(0, 30) if ocupacion_visual == "Alta" else random.randint(0, 10)
    return {
        "item": item,
        "fecha_hora": _ts(),
        "id_sensor": f"CAM-{random.randint(1000, 9999)}",
        "sensor": "Cámara Inteligente",
        "eje": eje,
        "zona_deteccion": zona,
        "vehiculos_detectados": veh_detectados,
        "vehiculos_detenidos": veh_detenidos,
        "longitud_cola": longitud_cola,
        "peatones_detectados": random.randint(0, 8),
        "incidentes": incidente,
        "ocupacion_visual": ocupacion_visual,
        "nivel_visibilidad": random.choice(["Buena", "Buena", "Buena", "Regular", "Reducida"]),
        "unidad_cola": "m",
        "estado_sensor": random.choice(ESTADOS_SENSOR),
    }


def _init_camara() -> pd.DataFrame:
    return pd.DataFrame([_fila_camara(i + 1) for i in range(WINDOW)])


# ── Render ─────────────────────────────────────────────────────────────────────

def render_lectura(data=None):
    st_autorefresh(interval=2500, key="refresh_lectura_datos_crudos")

    # ── Inicialización de session_state ────────────────────────────────────────
    if "df_radar_live" not in st.session_state:
        st.session_state["df_radar_live"] = _init_radar()
        st.session_state["radar_next_item"] = WINDOW + 1

    if "df_espira_live" not in st.session_state:
        st.session_state["df_espira_live"] = _init_espira()
        st.session_state["espira_next_item"] = WINDOW + 1

    if "df_camara_live" not in st.session_state:
        st.session_state["df_camara_live"] = _init_camara()
        st.session_state["camara_next_item"] = WINDOW + 1

    # ── Agregar 1 nueva fila por sensor en cada refresco ──────────────────────
    nueva_radar = pd.DataFrame([_fila_radar(st.session_state["radar_next_item"])])
    st.session_state["df_radar_live"] = (
        pd.concat([st.session_state["df_radar_live"], nueva_radar], ignore_index=True)
        .tail(WINDOW)
        .reset_index(drop=True)
    )
    st.session_state["radar_next_item"] += 1

    nueva_espira = pd.DataFrame([_fila_espira(st.session_state["espira_next_item"])])
    st.session_state["df_espira_live"] = (
        pd.concat([st.session_state["df_espira_live"], nueva_espira], ignore_index=True)
        .tail(WINDOW)
        .reset_index(drop=True)
    )
    st.session_state["espira_next_item"] += 1

    nueva_camara = pd.DataFrame([_fila_camara(st.session_state["camara_next_item"])])
    st.session_state["df_camara_live"] = (
        pd.concat([st.session_state["df_camara_live"], nueva_camara], ignore_index=True)
        .tail(WINDOW)
        .reset_index(drop=True)
    )
    st.session_state["camara_next_item"] += 1

    # ── Encabezado ─────────────────────────────────────────────────────────────
    st.markdown("## 2. Lectura de datos crudos")

    st.markdown(
        """
        En esta etapa se visualiza la entrada directa de datos desde los sensores hacia
        el sistema. Los valores todavía no han sido limpiados, seleccionados ni
        transformados. Cada actualización incorpora una nueva lectura al final de la tabla
        y conserva solo las últimas 15 observaciones, como una ventana móvil de monitoreo.
        Para fines demostrativos, las lecturas se generan automáticamente a partir del
        escenario SCADA.
        """
    )

    df_radar = st.session_state["df_radar_live"]
    df_espira = st.session_state["df_espira_live"]
    df_camara = st.session_state["df_camara_live"]

    radar_total = st.session_state["radar_next_item"] - 1
    espira_total = st.session_state["espira_next_item"] - 1
    camara_total = st.session_state["camara_next_item"] - 1
    total_lecturas = radar_total + espira_total + camara_total

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Lecturas radar", radar_total)
    col_m2.metric("Lecturas espira", espira_total)
    col_m3.metric("Lecturas cámara", camara_total)
    col_m4.metric("Total lecturas", total_lecturas)

    st.caption(
        "Las tablas muestran una ventana móvil con las últimas 15 lecturas por sensor. "
        "El conteo superior corresponde al total de lecturas acumuladas durante la sesión."
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="sensor-window">
            <div class="sensor-title">📡 Radar Doppler</div>
            <div class="sensor-subtitle">Velocidad promedio, máxima, mínima, sentido y distancia de detección</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(df_radar, width="stretch", hide_index=True, height=350)

    st.markdown("---")

    st.markdown(
        """
        <div class="sensor-window">
            <div class="sensor-title">🧲 Espira Inductiva</div>
            <div class="sensor-subtitle">Flujo vehicular, ocupación de carril, clasificación y tiempos</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(df_espira, width="stretch", hide_index=True, height=350)

    st.markdown("---")

    st.markdown(
        """
        <div class="sensor-window">
            <div class="sensor-title">🎥 Cámara Inteligente</div>
            <div class="sensor-subtitle">Vehículos, cola, peatones, incidentes y visibilidad</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(df_camara, width="stretch", hide_index=True, height=350)

    st.markdown(
        """
        Los datos mostrados corresponden a señales crudas recibidas desde los sensores del
        sistema SCADA. En las siguientes etapas, el sistema eliminará registros inválidos,
        seleccionará las variables útiles y calculará los indicadores principales:
        velocidad promedio, flujo vehicular y longitud de cola.
        """
    )
