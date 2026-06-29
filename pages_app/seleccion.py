import time
import html
import streamlit as st
import streamlit.components.v1 as components


ALTURA_PANEL = 760


def ventana_codigo_seleccion():
    codigo_html = """
<span class="comment"># =====================================================</span>
<span class="comment"># SELECCIÓN DE VARIABLES PARA LA IA</span>
<span class="comment"># =====================================================</span>

<span class="var">df_velocidad</span> = <span class="var">df_radar</span>[
    [<span class="string">"fecha_hora"</span>, <span class="string">"velocidad_promedio"</span>]
]

<span class="var">df_flujo</span> = <span class="var">df_espira</span>[
    [<span class="string">"fecha_hora"</span>, <span class="string">"flujo_vehicular"</span>]
]

<span class="var">df_cola</span> = <span class="var">df_camara</span>[
    [<span class="string">"fecha_hora"</span>, <span class="string">"longitud_cola"</span>]
]

<span class="var">df_variables_ia</span> = (
    <span class="var">df_velocidad</span>
    .<span class="func">merge</span>(<span class="var">df_flujo</span>, <span class="param">on</span>=<span class="string">"fecha_hora"</span>)
    .<span class="func">merge</span>(<span class="var">df_cola</span>, <span class="param">on</span>=<span class="string">"fecha_hora"</span>)
)

<span class="var">df_variables_ia</span>
"""

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

            .colab-window {{
                width: 100%;
                height: {ALTURA_PANEL}px;
                background: #0B1020;
                border: 1px solid rgba(125, 255, 240, 0.24);
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.35);
                font-family: Consolas, Monaco, "Courier New", monospace;
                box-sizing: border-box;
                overflow: hidden;
            }}

            .colab-header {{
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
                width: 13px;
                height: 13px;
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

            .code-body {{
                margin: 0;
                height: calc({ALTURA_PANEL}px - 34px);
                padding: 14px 16px;
                background: #0B1020;
                color: #DDEBFF;
                font-size: 13px;
                line-height: 1.32;
                white-space: pre-wrap;
                overflow: auto;
                box-sizing: border-box;
            }}

            .comment {{
                color: #6A9955;
                font-weight: 800;
            }}

            .var {{
                color: #58A6FF;
            }}

            .string {{
                color: #CE9178;
            }}

            .func {{
                color: #DCDCAA;
            }}

            .param {{
                color: #9CDCFE;
            }}

            .keyword {{
                color: #C586C0;
            }}

            .number {{
                color: #B5CEA8;
            }}
        </style>
    </head>
    <body>
        <div class="colab-window">
            <div class="colab-header">
                <div class="dots">
                    <span class="dot red"></span>
                    <span class="dot yellow"></span>
                    <span class="dot green"></span>
                </div>
                <div class="file-name">seleccion_variables.ipynb</div>
            </div>
            <pre class="code-body">{codigo_html}</pre>
        </div>
    </body>
    </html>
    """

    components.html(html_code, height=ALTURA_PANEL + 5, scrolling=False)


def panel_espera_seleccion():
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

            .output-window {{
                width: 100%;
                height: {ALTURA_PANEL}px;
                background: #08111F;
                border: 1px solid rgba(125, 255, 240, 0.24);
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.35);
                box-sizing: border-box;
                overflow: hidden;
            }}

            .output-header {{
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

            .output-body {{
                height: calc({ALTURA_PANEL}px - 34px);
                padding: 14px;
                box-sizing: border-box;
                overflow-y: auto;
            }}

            .console {{
                background: #050A12;
                border: 1px solid rgba(110, 231, 168, 0.28);
                border-radius: 10px;
                padding: 16px;
                color: #CFE8D6;
                font-size: 13px;
                line-height: 1.35;
            }}

            .muted {{
                color: #8FAFC2;
                margin-top: 6px;
            }}
        </style>
    </head>
    <body>
        <div class="output-window">
            <div class="output-header">salida_ejecucion</div>
            <div class="output-body">
                <div class="console">
                    <div>&gt;&gt;&gt; Esperando ejecución...</div>
                    <div class="muted">Presiona el botón ▶ para ejecutar la celda.</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html_panel, height=ALTURA_PANEL + 5, scrolling=False)


def panel_ejecucion_seleccion(mensajes, df_variables_ia=None, finalizado=False):
    lineas = ""

    for mensaje in mensajes:
        lineas += f"<div>{html.escape(mensaje)}</div>"

    if finalizado:
        lineas += '<div class="success">✔ Código ejecutado correctamente.</div>'

    tabla_html = ""

    if finalizado and df_variables_ia is not None:
        tabla_html = f"""
        <div class="tables-title">Variables seleccionadas para el modelo IA</div>
        {df_variables_ia.to_html(index=False, classes="sensor-table")}
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

            .output-window {{
                width: 100%;
                height: {ALTURA_PANEL}px;
                background: #08111F;
                border: 1px solid rgba(125, 255, 240, 0.24);
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.35);
                box-sizing: border-box;
                overflow: hidden;
            }}

            .output-header {{
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

            .output-body {{
                height: calc({ALTURA_PANEL}px - 34px);
                padding: 14px;
                box-sizing: border-box;
                overflow-y: auto;
            }}

            .console {{
                background: #050A12;
                border: 1px solid rgba(110, 231, 168, 0.28);
                border-radius: 10px;
                padding: 16px;
                color: #CFE8D6;
                font-size: 13px;
                line-height: 1.35;
                margin-bottom: 14px;
            }}

            .console div {{
                margin: 0;
                padding: 0;
            }}

            .success {{
                color: #6EE7A8;
                font-weight: 800;
                margin-top: 8px !important;
            }}

            .tables-title {{
                color: #7DFFF0;
                font-size: 14px;
                font-weight: 800;
                margin: 10px 0 12px 0;
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

            table.sensor-table tr:nth-child(even) {{
                background: #0A1624;
            }}
        </style>
    </head>
    <body>
        <div class="output-window">
            <div class="output-header">salida_ejecucion</div>
            <div class="output-body">
                <div class="console">
                    <div>&gt;&gt;&gt; Ejecutando celda...</div>
                    {lineas}
                </div>
                {tabla_html}
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html_panel, height=ALTURA_PANEL + 5, scrolling=False)


def render_seleccion(data=None):
    st.markdown(
        """
        <div style="margin-top:-20px; margin-bottom:10px;">
            <h2 style="margin:0; color:#EAF6FF;">3. Selección y consolidación de variables</h2>
            <p style="margin:6px 0 0 0; color:#A9C8D8; line-height:1.35;">
                Se seleccionan las variables principales de cada sensor y se consolidan
                en un único DataFrame mediante merge, generando la base que usará el modelo de IA.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if data is None:
        st.warning("No se recibieron datos desde app.py.")
        return

    df_radar = data.get("df_radar")
    df_espira = data.get("df_espira")
    df_camara = data.get("df_camara")

    if df_radar is None or df_espira is None or df_camara is None:
        st.error("No se encontraron df_radar, df_espira o df_camara dentro de data.py.")
        return

    col_codigo, col_boton, col_ejecucion = st.columns(
        [0.465, 0.05, 0.485],
        gap="small"
    )

    with col_codigo:
        ventana_codigo_seleccion()

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
                    max-height: 90px !important;

                    border-radius: 50% !important;
                    padding: 0 !important;
                    margin: 0 auto !important;

                    font-size: 52px !important;
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
            key="btn_ejecutar_seleccion",
            help="Ejecutar selección de variables"
        )

    with col_ejecucion:
        salida = st.empty()

        if not ejecutar:
            with salida:
                panel_espera_seleccion()
            return

        try:
            mensajes = []

            df_velocidad = df_radar[["fecha_hora", "velocidad_promedio"]]
            df_flujo = df_espira[["fecha_hora", "flujo_vehicular"]]
            df_cola = df_camara[["fecha_hora", "longitud_cola"]]

            df_variables_ia = (
                df_velocidad
                .merge(df_flujo, on="fecha_hora")
                .merge(df_cola, on="fecha_hora")
            )

            pasos = [
                (">>> Leyendo datos del radar Doppler", 0.25),
                (">>> Seleccionando velocidad_promedio", 0.25),
                (">>> Leyendo datos de la espira inductiva", 0.25),
                (">>> Seleccionando flujo_vehicular", 0.25),
                (">>> Leyendo datos de cámara", 0.25),
                (">>> Seleccionando longitud_cola", 0.25),
                (">>> Uniendo variables mediante fecha_hora", 0.25),
                (">>> Generando base de variables para IA", 0.25),
            ]

            for mensaje, espera in pasos:
                mensajes.append(mensaje)
                with salida:
                    panel_ejecucion_seleccion(mensajes)
                time.sleep(espera)

            with salida:
                panel_ejecucion_seleccion(
                    mensajes,
                    df_variables_ia=df_variables_ia,
                    finalizado=True
                )

        except Exception as e:
            st.error("Ocurrió un error durante la selección de variables.")
            st.exception(e)