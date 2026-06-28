import streamlit as st
import pandas as pd
import time


def render_limpieza(data=None):

    st.markdown(
        """
        <div class="section-card">
            <h2>🧹 Limpieza de datos</h2>
            <p>
                En esta etapa se simula la limpieza de datos obtenidos desde los sensores del sistema
                SCADA: radar Doppler, espiras inductivas y cámaras de tráfico. El proceso genera un
                nuevo DataFrame limpio para continuar con la selección de variables y el modelo de IA.
            </p>
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

    st.markdown("### Simulación tipo notebook")

    st.markdown(
        """
        <div class="notebook-box">
            <div class="notebook-header">
                <span class="circle red"></span>
                <span class="circle yellow"></span>
                <span class="circle green"></span>
                <span class="notebook-title">limpieza_datos.ipynb</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    codigo_limpieza = '''
import pandas as pd

df_limpio = df_entrenamiento_ia.copy()

df_limpio = df_limpio.drop_duplicates()

columnas_numericas = [
    "velocidad_promedio",
    "flujo_vehicular",
    "longitud_cola"
]

for columna in columnas_numericas:
    df_limpio[columna] = pd.to_numeric(
        df_limpio[columna],
        errors="coerce"
    )

for columna in columnas_numericas:
    mediana = df_limpio[columna].median()
    df_limpio[columna] = df_limpio[columna].fillna(mediana)

for columna in columnas_numericas:
    df_limpio = df_limpio[df_limpio[columna] >= 0]

df_limpio["nivel_congestion"] = (
    df_limpio["nivel_congestion"]
    .astype(str)
    .str.lower()
    .str.strip()
)

df_limpio = df_limpio.reset_index(drop=True)

print("Limpieza completada correctamente")
print(df_limpio.head())
'''

    st.code(codigo_limpieza, language="python")

    ejecutar = st.button("▶ Ejecutar limpieza de datos", use_container_width=True)

    if ejecutar:
        progress = st.progress(0)
        estado = st.empty()

        estado.info("Iniciando proceso de limpieza...")
        time.sleep(0.4)
        progress.progress(15)

        df_limpio = df_original.copy()
        registros_originales = len(df_limpio)

        estado.info("Copiando DataFrame original...")
        time.sleep(0.4)
        progress.progress(25)

        estado.info("Eliminando registros duplicados...")
        time.sleep(0.4)
        df_limpio = df_limpio.drop_duplicates()
        progress.progress(40)

        columnas_numericas = [
            "velocidad_promedio",
            "flujo_vehicular",
            "longitud_cola"
        ]

        estado.info("Convirtiendo variables numéricas...")
        time.sleep(0.4)

        for columna in columnas_numericas:
            if columna in df_limpio.columns:
                df_limpio[columna] = pd.to_numeric(
                    df_limpio[columna],
                    errors="coerce"
                )

        progress.progress(55)

        estado.info("Corrigiendo valores nulos...")
        time.sleep(0.4)

        for columna in columnas_numericas:
            if columna in df_limpio.columns:
                mediana = df_limpio[columna].median()
                df_limpio[columna] = df_limpio[columna].fillna(mediana)

        progress.progress(70)

        estado.info("Eliminando valores negativos no válidos...")
        time.sleep(0.4)

        for columna in columnas_numericas:
            if columna in df_limpio.columns:
                df_limpio = df_limpio[df_limpio[columna] >= 0]

        progress.progress(85)

        estado.info("Normalizando variable objetivo...")
        time.sleep(0.4)

        if "nivel_congestion" in df_limpio.columns:
            df_limpio["nivel_congestion"] = (
                df_limpio["nivel_congestion"]
                .astype(str)
                .str.lower()
                .str.strip()
            )

        df_limpio = df_limpio.reset_index(drop=True)

        registros_limpios = len(df_limpio)
        registros_eliminados = registros_originales - registros_limpios

        st.session_state["df_limpio"] = df_limpio

        progress.progress(100)
        estado.success("Limpieza completada correctamente.")

        st.markdown("### Consola de ejecución")

        st.markdown(
            """
            <div class="terminal-box">
                <p>>>> Ejecutando celda...</p>
                <p>Importando librerías...</p>
                <p>Copiando DataFrame original...</p>
                <p>Eliminando registros duplicados...</p>
                <p>Convirtiendo variables numéricas...</p>
                <p>Corrigiendo valores nulos...</p>
                <p>Eliminando valores negativos no válidos...</p>
                <p>Normalizando variable objetivo...</p>
                <p class="success-text">Limpieza completada correctamente.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Registros originales", registros_originales)

        with col2:
            st.metric("Registros limpios", registros_limpios)

        with col3:
            st.metric("Registros eliminados", registros_eliminados)

        st.markdown("### Nuevo DataFrame generado")

        st.dataframe(
            df_limpio,
            use_container_width=True,
            hide_index=True
        )

        st.markdown(
            """
            <div class="comment-box">
                <h4>Comentario del proceso</h4>
                <p>
                    Al ejecutar la limpieza se genera un nuevo DataFrame llamado <b>df_limpio</b>.
                    Este conjunto de datos ya no contiene registros duplicados, valores nulos en las
                    variables principales ni valores negativos que no tienen sentido físico. De esta
                    manera, las variables de velocidad promedio, flujo vehicular y longitud de cola
                    quedan preparadas para la siguiente etapa del sistema.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )