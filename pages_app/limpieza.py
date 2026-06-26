import random
from datetime import datetime

import pandas as pd
import streamlit as st


def generar_datos_crudos_para_limpieza():
    datos = [
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Sensor": "Radar Doppler",
            "Eje": "Horizontal",
            "Dato": "Vel. inst.",
            "Valor": random.randint(10, 70),
            "Unidad": "km/h",
        },
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Sensor": "Radar Doppler",
            "Eje": "Vertical",
            "Dato": "Vel. inst.",
            "Valor": random.choice([random.randint(10, 70), -8, 160, None]),
            "Unidad": "km/h",
        },
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Sensor": "Espira inductiva",
            "Eje": "Horizontal",
            "Dato": "Tiempo ocup.",
            "Valor": round(random.uniform(0.2, 3.5), 2),
            "Unidad": "s",
        },
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Sensor": "Espira inductiva",
            "Eje": "Vertical",
            "Dato": "Tiempo ocup.",
            "Valor": random.choice([round(random.uniform(0.2, 3.5), 2), -1.2, None]),
            "Unidad": "s",
        },
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Sensor": "Cámara inteligente",
            "Eje": "Horizontal",
            "Dato": "Veh. detectados",
            "Valor": random.randint(3, 25),
            "Unidad": "veh.",
        },
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Sensor": "Cámara inteligente",
            "Eje": "Vertical",
            "Dato": "Veh. detenidos",
            "Valor": random.choice([random.randint(0, 18), -4, None]),
            "Unidad": "veh.",
        },
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Sensor": "Cámara inteligente",
            "Eje": "Vertical",
            "Dato": "Peatones",
            "Valor": random.randint(0, 5),
            "Unidad": "peat.",
        },
    ]

    # Duplicado intencional para simular error común de adquisición
    datos.append(datos[0].copy())

    return pd.DataFrame(datos)


def limpiar_datos(df):
    df_limpio = df.copy()

    registros_iniciales = len(df_limpio)

    # 1. Eliminar duplicados
    df_limpio = df_limpio.drop_duplicates()

    # 2. Eliminar registros sin valor
    df_limpio = df_limpio.dropna(subset=["Valor"])

    # 3. Convertir a número
    df_limpio["Valor"] = pd.to_numeric(df_limpio["Valor"], errors="coerce")
    df_limpio = df_limpio.dropna(subset=["Valor"])

    # 4. Aplicar reglas de validación por tipo de dato
    condiciones_validas = (
        ((df_limpio["Dato"] == "Vel. inst.") & (df_limpio["Valor"].between(0, 100)))
        | ((df_limpio["Dato"] == "Tiempo ocup.") & (df_limpio["Valor"].between(0, 10)))
        | ((df_limpio["Dato"] == "Veh. detectados") & (df_limpio["Valor"].between(0, 60)))
        | ((df_limpio["Dato"] == "Veh. detenidos") & (df_limpio["Valor"].between(0, 40)))
        | ((df_limpio["Dato"] == "Peatones") & (df_limpio["Valor"].between(0, 20)))
    )

    df_limpio = df_limpio[condiciones_validas]

    registros_finales = len(df_limpio)
    registros_eliminados = registros_iniciales - registros_finales

    resumen = {
        "Registros iniciales": registros_iniciales,
        "Registros válidos": registros_finales,
        "Registros eliminados": registros_eliminados,
        "Duplicados / vacíos / fuera de rango": registros_eliminados,
    }

    return df_limpio, resumen


def render_limpieza(data=None):
    st.markdown("## 2. Limpieza de datos")

    st.markdown(
        """
        En esta etapa se simula el procesamiento inicial de las señales crudas recibidas
        desde los sensores. Los datos pueden contener registros duplicados, valores vacíos
        o mediciones fuera de rango. Antes de seleccionar variables para el modelo, el
        sistema debe limpiar estos registros.
        """
    )

    st.markdown("### Celda de código simulada")

    codigo_limpieza = """
# Limpieza de datos crudos del sistema SCADA

df_limpio = df_crudo.copy()

# 1. Eliminar registros duplicados
df_limpio = df_limpio.drop_duplicates()

# 2. Eliminar valores vacíos
df_limpio = df_limpio.dropna(subset=["Valor"])

# 3. Convertir valores a formato numérico
df_limpio["Valor"] = pd.to_numeric(df_limpio["Valor"], errors="coerce")

# 4. Validar rangos aceptables
# Velocidad: 0 a 100 km/h
# Tiempo de ocupación: 0 a 10 s
# Vehículos detectados: 0 a 60 veh.
# Vehículos detenidos: 0 a 40 veh.
# Peatones: 0 a 20 peat.

df_limpio = df_limpio[condiciones_validas]
"""

    st.code(codigo_limpieza, language="python")

    ejecutar = st.button("▶ Ejecutar limpieza de datos", use_container_width=True)

    if ejecutar:
        df_crudo = generar_datos_crudos_para_limpieza()
        df_limpio, resumen = limpiar_datos(df_crudo)

        st.markdown("### Datos crudos recibidos")

        st.dataframe(
            df_crudo,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Resultado después de la limpieza")

        st.dataframe(
            df_limpio,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Resumen del proceso")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Registros iniciales",
                resumen["Registros iniciales"],
            )

        with col2:
            st.metric(
                "Registros válidos",
                resumen["Registros válidos"],
            )

        with col3:
            st.metric(
                "Registros eliminados",
                resumen["Registros eliminados"],
            )

        st.success(
            "Limpieza ejecutada correctamente. Los datos duplicados, vacíos o fuera de rango fueron retirados."
        )

        st.markdown(
            """
            Después de esta etapa, los datos quedan preparados para la selección de
            variables relevantes. Todavía no se calcula el nivel de congestión; únicamente
            se depuran las señales crudas para que el modelo no trabaje con datos erróneos.
            """
        )

    else:
        st.info("Presiona el botón para ejecutar la limpieza de datos crudos.")