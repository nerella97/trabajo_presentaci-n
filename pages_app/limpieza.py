import time
import html
import re

import streamlit as st
import streamlit.components.v1 as components


ALTURA_PANEL = 760


def pintar_codigo_python(codigo):
    lineas = []

    palabras_clave = [
        "import", "from", "as", "for", "in", "if", "else",
        "return", "print", "None", "True", "False", "display"
    ]

    funciones = [
        "DataFrame", "copy", "drop_duplicates", "to_numeric", "median",
        "fillna", "astype", "lower", "strip", "reset_index", "head"
    ]

    librerias = [
        "pandas", "pd", "sklearn", "DecisionTreeClassifier"
    ]

    variables = [
        "df_radar", "df_espira", "df_camara", "df_limpio",
        "df_entrenamiento_ia", "columnas_numericas", "columna", "mediana"
    ]

    for linea in codigo.split("\n"):
        linea_html = html.escape(linea)

        if linea.strip().startswith("#"):
            lineas.append(f'<span class="comment">{linea_html}</span>')
            continue

        linea_html = re.sub(
            r'(&quot;.*?&quot;)',
            r'<span class="string">\1</span>',
            linea_html
        )

        for palabra in palabras_clave:
            linea_html = re.sub(
                rf'\b{palabra}\b',
                f'<span class="keyword">{palabra}</span>',
                linea_html
            )

        for funcion in funciones:
            linea_html = re.sub(
                rf'\b{funcion}\b',
                f'<span class="func">{funcion}</span>',
                linea_html
            )

        for libreria in librerias:
            linea_html = re.sub(
                rf'\b{libreria}\b',
                f'<span class="keyword">{libreria}</span>',
                linea_html
            )

        for variable in variables:
            linea_html = re.sub(
                rf'\b{variable}\b',
                f'<span class="var">{variable}</span>',
                linea_html
            )

        lineas.append(linea_html)

    return "\n".join(lineas)


def ventana_codigo(codigo):
    codigo_html = pintar_codigo_python(codigo)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
                overflow: hidden;
            }}

            .editor-window {{
                width: 100%;
                height: {ALTURA_PANEL}px;
                background: #0B1020;
                border: 1px solid rgba(125, 255, 240, 0.24);
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.42);
                font-family: Consolas, Monaco, "Courier New", monospace;
                box-sizing: border-box;
                overflow: hidden;
            }}

            .editor-header {{
                height: 34px;
                background: #101827;
                display: flex;
                align-items: center;
                padding: 0 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                box-sizing: border-box;
            }}

            .dots {{
                display: flex;
                gap: 8px;
                align-items: center;
            }}

            .dot {{
                width: 14px;
                height: 14px;
                border-radius: 50%;
                display: inline-block;
            }}

            .red {{ background: #ff5f57; }}
            .yellow {{ background: #ffbd2e; }}
            .green {{ background: #28c840; }}

            .file-name {{
                flex: 1;
                text-align: center;
                color: #A9C8D8;
                font-size: 12px;
                letter-spacing: 0.2px;
            }}

            .editor-body {{
                margin: 0;
                height: calc({ALTURA_PANEL}px - 34px);
                padding: 16px 18px 22px 18px;
                background: #0B1020;
                color: #DDEBFF;
                font-size: 13px;
                line-height: 1.32;
                white-space: pre;
                overflow: auto;
                box-sizing: border-box;
            }}

            .comment {{ color: #6A9955; font-weight: 600; }}
            .keyword {{ color: #C586C0; }}
            .func    {{ color: #DCDCAA; }}
            .var     {{ color: #58A6FF; }}
            .string  {{ color: #CE9178; }}
            .param   {{ color: #9CDCFE; }}
            .number  {{ color: #B5CEA8; }}
        </style>
    </head>
    <body>
        <div class="editor-window">
            <div class="editor-header">
                <div class="dots">
                    <span class="dot red"></span>
                    <span class="dot yellow"></span>
                    <span class="dot green"></span>
                </div>
                <div class="file-name">bases_sensores.py</div>
            </div>
            <pre class="editor-body"><code>{codigo_html}</code></pre>
        </div>
    </body>
    </html>
    """

    components.html(
        html_code,
        height=ALTURA_PANEL + 5,
        scrolling=False
    )


def panel_espera():
    html_panel = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
                overflow: hidden;
                font-family: Consolas, Monaco, "Courier New", monospace;
            }}

            .execution-window {{
                width: 100%;
                height: {ALTURA_PANEL}px;
                background: #08111F;
                border: 1px solid rgba(125, 255, 240, 0.24);
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.35);
                box-sizing: border-box;
                overflow: hidden;
            }}

            .execution-header {{
                height: 34px;
                background: #101827;
                display: flex;
                align-items: center;
                padding: 0 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                color: #A9C8D8;
                font-size: 12px;
                box-sizing: border-box;
            }}

            .execution-body {{
                height: calc({ALTURA_PANEL}px - 34px);
                padding: 16px;
                box-sizing: border-box;
                overflow-y: auto;
            }}

            .console {{
                background: #050A12;
                border: 1px solid rgba(110, 231, 168, 0.28);
                border-radius: 10px;
                padding: 4px 12px;
                color: #CFE8D6;
                font-size: 13px;
                line-height: 1.2;
                margin-bottom: 8px;
                white-space: normal;
            }}

            .muted {{ color: #8FAFC2; }}
        </style>
    </head>
    <body>
        <div class="execution-window">
            <div class="execution-header">salida_ejecucion</div>
            <div class="execution-body">
                <div class="console">
                    <div>&gt;&gt;&gt; Esperando ejecución...</div>
                    <div class="muted">Presiona el botón ▶ para ejecutar la celda.</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(
        html_panel,
        height=ALTURA_PANEL + 5,
        scrolling=False
    )


def panel_ejecucion(mensajes, df_radar=None, df_espira=None, df_camara=None, finalizado=False):
    lineas = ""

    for mensaje in mensajes:
        lineas += f"<div>{html.escape(mensaje)}</div>"

    if finalizado:
        lineas += '<div class="success">✔ Código ejecutado correctamente.</div>'

    tablas_html = ""

    if finalizado and df_radar is not None and df_espira is not None and df_camara is not None:
        tabla_radar = df_radar.to_html(index=False, classes="sensor-table")
        tabla_espira = df_espira.to_html(index=False, classes="sensor-table")
        tabla_camara = df_camara.to_html(index=False, classes="sensor-table")

        tablas_html = f"""
        <div class="tables-title">Tablas generadas</div>

        <div class="sensor-block">
            <div class="sensor-name">DataFrame 1: Radar Doppler</div>
            {tabla_radar}
        </div>

        <div class="sensor-block">
            <div class="sensor-name">DataFrame 2: Espira Inductiva</div>
            {tabla_espira}
        </div>

        <div class="sensor-block">
            <div class="sensor-name">DataFrame 3: Cámara de Visión Artificial</div>
            {tabla_camara}
        </div>
        """

    html_panel = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
                overflow: hidden;
                font-family: Consolas, Monaco, "Courier New", monospace;
                color: #EAF6FF;
            }}

            .execution-window {{
                width: 100%;
                height: {ALTURA_PANEL}px;
                background: #08111F;
                border: 1px solid rgba(125, 255, 240, 0.24);
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.35);
                box-sizing: border-box;
                overflow: hidden;
            }}

            .execution-header {{
                height: 34px;
                background: #101827;
                display: flex;
                align-items: center;
                padding: 0 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                color: #A9C8D8;
                font-size: 12px;
                box-sizing: border-box;
            }}

            .execution-body {{
                height: calc({ALTURA_PANEL}px - 34px);
                padding: 14px;
                box-sizing: border-box;
                overflow-y: auto;
            }}

            .console {{
                background: #050A12;
                border: 1px solid rgba(110, 231, 168, 0.28);
                border-radius: 10px;
                padding: 14px;
                color: #CFE8D6;
                font-size: 13px;
                line-height: 1.5;
                margin-bottom: 16px;
                white-space: pre-wrap;
            }}

            .success {{
                color: #6EE7A8;
                font-weight: 800;
                margin-top: 6px;
            }}

            .tables-title {{
                color: #7DFFF0;
                font-size: 14px;
                font-weight: 800;
                margin: 10px 0 12px 0;
            }}

            .sensor-block {{ margin-bottom: 18px; }}

            .sensor-name {{
                font-size: 13px;
                font-weight: 800;
                color: #BFEFFF;
                margin-bottom: 8px;
            }}

            table.sensor-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
                background: #0D1B2A;
                color: #EAF6FF;
                border-radius: 8px;
                overflow: hidden;
            }}

            table.sensor-table th {{
                background: #12304A;
                color: #7DFFF0;
                padding: 8px;
                border: 1px solid rgba(255,255,255,0.08);
                text-align: left;
                font-weight: 800;
                white-space: nowrap;
            }}

            table.sensor-table td {{
                padding: 8px;
                border: 1px solid rgba(255,255,255,0.08);
                color: #DDEBFF;
                white-space: nowrap;
            }}

            table.sensor-table tr:nth-child(even) {{ background: #0A1624; }}
        </style>
    </head>
    <body>
        <div class="execution-window">
            <div class="execution-header">salida_ejecucion</div>
            <div class="execution-body">
                <div class="console"><div> Ejecutando celda...</div>{lineas}</div>
                {tablas_html}
            </div>
        </div>
    </body>
    </html>
    """

    components.html(
        html_panel,
        height=ALTURA_PANEL + 5,
        scrolling=False
    )


def render_limpieza(data=None):

    if data is None:
        st.warning("No se recibieron datos desde app.py.")
        return

    df_radar = data.get("df_radar")
    df_espira = data.get("df_espira")
    df_camara = data.get("df_camara")

    if df_radar is None or df_espira is None or df_camara is None:
        st.error("No se encontraron df_radar, df_espira o df_camara dentro de data.py.")
        st.write("Claves disponibles en data:")
        st.write(list(data.keys()))
        return

    st.markdown("### Visualización de datos")

    codigo_sensores = """import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# =====================================================
# VISUALIZACIÓN DE DATAFRAMES HISTÓRICOS DE SENSORES
# =====================================================

# DataFrame del Radar Doppler
display(df_radar)

# DataFrame de la Espira Inductiva
display(df_espira)

# DataFrame de la Cámara de Visión Artificial
display(df_camara)
"""

    col_codigo, col_boton, col_ejecucion = st.columns(
        [0.465, 0.05, 0.485],
        gap="small"
    )

    with col_codigo:
        ventana_codigo(codigo_sensores)

    with col_boton:
        st.markdown(
            """
            <style>
                div[data-testid="column"] {
                    overflow: visible !important;
                }

                div[data-testid="column"] > div {
                    overflow: visible !important;
                }

                div[data-testid="stVerticalBlock"] {
                    overflow: visible !important;
                }

                div[data-testid="stButton"] {
                    display: flex !important;
                    justify-content: center !important;
                    align-items: center !important;
                    overflow: visible !important;
                    position: relative !important;
                    z-index: 9999 !important;
                }

                div[data-testid="stButton"] button,
                button[kind="secondary"],
                button[data-testid="baseButton-secondary"] {
                    width: 90px !important;
                    height: 90px !important;
                    min-width: 90px !important;
                    max-width: 90px !important;
                    min-height: 90px !important;
                    max-height:910px !important;

                    border-radius: 50% !important;
                    padding: 0 !important;
                    margin: 0 auto !important;

                    font-size: 452px !important;
                    font-weight: 900 !important;
                    line-height: 1 !important;

                    background-color: #111314 !important;
                    color: #7DFFF0 !important;
                    border: 4px solid rgba(125, 255, 240, 0.9) !important;
                    box-shadow: 0 0 14px rgba(125, 255, 240, 0.18) !important;

                    position: relative !important;
                    left: 50% !important;
                    transform: translateX(-50%) !important;
                    z-index: 99999 !important;
                }

                div[data-testid="stButton"] button:hover,
                button[kind="secondary"]:hover,
                button[data-testid="baseButton-secondary"]:hover {
                    background-color: #172033 !important;
                    color: #FFFFFF !important;
                    border: 4px solid rgba(125, 255, 240, 1) !important;
                    box-shadow: 0 0 22px rgba(125, 255, 240, 0.28) !important;
                    transform: translateX(-50%) scale(1.06) !important;
                }

                div[data-testid="stButton"] button p,
                button[kind="secondary"] p,
                button[data-testid="baseButton-secondary"] p {
                    font-size: 52px !important;
                    line-height: 1 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        espacio_superior = max((ALTURA_PANEL // 2) - 65, 0)

        st.markdown(
            f"<div style='height: {espacio_superior}px;'></div>",
            unsafe_allow_html=True
        )

        ejecutar = st.button(
            "▶",
            key="btn_ejecutar_sensores",
            help="Ejecutar celda"
        )

    with col_ejecucion:
        salida = st.empty()

        if not ejecutar:
            with salida:
                panel_espera()
            return

        try:
            mensajes = []

            pasos = [
                (">>> import pandas as pd", 0.3),
                (">>> from sklearn.tree import DecisionTreeClassifier", 0.3),
                ("[1/3] display(df_radar)", 0.4),
                ("[2/3] display(df_espira)", 0.4),
                ("[3/3] display(df_camara)", 0.4),
            ]

            for mensaje, espera in pasos:
                mensajes.append(mensaje)
                with salida:
                    panel_ejecucion(mensajes)
                time.sleep(espera)

            with salida:
                panel_ejecucion(
                    mensajes,
                    df_radar=df_radar,
                    df_espira=df_espira,
                    df_camara=df_camara,
                    finalizado=True
                )

        except Exception as e:
            st.error("Ocurrió un error durante la ejecución del código.")
            st.exception(e)
