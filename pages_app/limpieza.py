import streamlit as st
import pandas as pd
import time
import html


def render_limpieza(data=None):

    st.markdown(
        """
        <div class="section-card">
            <h2>🧹 Limpieza de datos</h2>
            <p>
                En esta etapa se simula el proceso de limpieza de datos provenientes de los sensores del sistema
                SCADA: radar Doppler, espiras inductivas y cámaras de tráfico.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Vista tipo notebook")

    codigo_limpieza = """
import pandas as pd

# Copia del conjunto de datos original
df_limpio = df_entrenamiento_ia.copy()

# 1. Eliminar registros duplicados
df_limpio = df_limpio.drop_duplicates()

# 2. Corregir valores nulos
df_limpio["velocidad_promedio"] = df_limpio["velocidad_promedio"].fillna(
    df_limpio["velocidad_promedio"].mean()
)

df_limpio["flujo_vehicular"] = df_limpio["flujo_vehicular"].fillna(
    df_limpio["flujo_vehicular"].median()
)

df_limpio["longitud_cola"] = df_limpio["longitud_cola"].fillna(
    df_limpio["longitud_cola"].median()
)

# 3. Eliminar valores negativos no válidos
df_limpio = df_limpio[df_limpio["velocidad_promedio"] >= 0]
df_limpio = df_limpio[df_limpio["flujo_vehicular"] >= 0]
df_limpio = df_limpio[df_limpio["longitud_cola"] >= 0]

# 4. Normalizar texto de la variable objetivo
df_limpio["nivel_congestion"] = (
    df_limpio["nivel_congestion"]
    .astype(str)
    .str.lower()
    .str.strip()
)

# 5. Reiniciar índice
df_limpio = df_limpio.reset_index(drop=True)

print("Limpieza completada correctamente")
print(df_limpio.head())
"""

    st.markdown(
        f"""
        <div class="notebook-box">
            <div class="notebook-header">
                <span class="circle red"></span>
                <span class="circle yellow"></span>
                <span class="circle green"></span>
                <span class="notebook-title">limpieza_datos.ipynb</span>
            </div>
            <pre><code>{codigo_limpieza}</code></pre>
        </div>
        """,
        unsafe_allow_html=True
    )

    if data is None:
        st.warning("No se recibieron datos desde app.py.")
        return

    df_original = data.get("df_entrenamiento_ia")

    if df_original is None:
        st.error("No se encontró el DataFrame df_entrenamiento_ia dentro de data.py.")
        return

    st.markdown("### Datos antes de la limpieza")
    st.dataframe(df_original, use_container_width=True)

    ejecutar = st.button("▶ Ejecutar limpieza de datos", use_container_width=True)

    if ejecutar:
        progress = st.progress(0)
        estado = st.empty()

        estado.info("Iniciando proceso de limpieza...")
        time.sleep(0.5)
        progress.progress(20)

        df_limpio = df_original.copy()

        estado.info("Eliminando registros duplicados...")
        time.sleep(0.5)
        df_limpio = df_limpio.drop_duplicates()
        progress.progress(40)

        estado.info("Corrigiendo valores nulos...")
        time.sleep(0.5)

        columnas_numericas = [
            "velocidad_promedio",
            "flujo_vehicular",
            "longitud_cola"
        ]

        for columna in columnas_numericas:
            if columna in df_limpio.columns:
                df_limpio[columna] = pd.to_numeric(
                    df_limpio[columna],
                    errors="coerce"
                )
                df_limpio[columna] = df_limpio[columna].fillna(
                    df_limpio[columna].median()
                )

        progress.progress(60)

        estado.info("Eliminando valores negativos no válidos...")
        time.sleep(0.5)

        for columna in columnas_numericas:
            if columna in df_limpio.columns:
                df_limpio = df_limpio[df_limpio[columna] >= 0]

        progress.progress(80)

        estado.info("Normalizando variable de congestión...")
        time.sleep(0.5)

        if "nivel_congestion" in df_limpio.columns:
            df_limpio["nivel_congestion"] = (
                df_limpio["nivel_congestion"]
                .astype(str)
                .str.lower()
                .str.strip()
            )

        df_limpio = df_limpio.reset_index(drop=True)

        progress.progress(100)
        estado.success("Limpieza completada correctamente.")

        st.session_state["df_limpio"] = df_limpio

        st.markdown("### Resultado de la ejecución")

        st.markdown(
            """
            <div class="terminal-box">
                <p>>>> Ejecutando celda...</p>
                <p>Importando librerías...</p>
                <p>Copiando datos originales...</p>
                <p>Eliminando duplicados...</p>
                <p>Corrigiendo valores nulos...</p>
                <p>Validando magnitudes físicas...</p>
                <p>Normalizando variable objetivo...</p>
                <p class="success-text">Limpieza completada correctamente.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Registros originales",
                len(df_original)
            )

        with col2:
            st.metric(
                "Registros limpios",
                len(df_limpio)
            )

        with col3:
            eliminados = len(df_original) - len(df_limpio)
            st.metric(
                "Registros eliminados",
                eliminados
            )

        st.markdown("### Datos después de la limpieza")
        st.dataframe(df_limpio, use_container_width=True)

        st.markdown(
            """
            <div class="comment-box">
                <h4>Comentario del proceso</h4>
                <p>
                    La limpieza permitió preparar los datos antes de entrenar el modelo de inteligencia artificial.
                    Se eliminaron duplicados, se corrigieron valores nulos y se descartaron valores negativos que no
                    tienen sentido físico dentro del sistema de tráfico. Con esto, las variables de velocidad, flujo
                    vehicular y longitud de cola quedan listas para ser usadas en la etapa de selección de variables.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            """
            <div class="comment-box">
                <h4>Indicaciones</h4>
                <p>
                    Presiona el botón de ejecución para simular el procesamiento de datos como si se estuviera
                    ejecutando una celda de Google Colab. El sistema mostrará el avance, la consola de ejecución
                    y el resultado final de la limpieza.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )