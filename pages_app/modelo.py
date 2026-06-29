import time
import html
import streamlit as st
import streamlit.components.v1 as components


ALTURA_PANEL = 760


def ventana_codigo_modelo():
    codigo_html = """
<span class="comment"># =====================================================</span>
<span class="comment"># ENTRENAMIENTO DEL MODELO DE IA</span>
<span class="comment"># =====================================================</span>

<span class="keyword">from</span> <span class="var">sklearn.tree</span> <span class="keyword">import</span> <span class="func">DecisionTreeClassifier</span>

<span class="var">X</span> = <span class="var">df_entrenamiento_ia</span>[
    [
        <span class="string">"velocidad_promedio"</span>,
        <span class="string">"flujo_vehicular"</span>,
        <span class="string">"longitud_cola"</span>
    ]
]

<span class="var">y</span> = <span class="var">df_entrenamiento_ia</span>[<span class="string">"nivel_congestion"</span>]

<span class="var">modelo_ia</span> = <span class="func">DecisionTreeClassifier</span>(
    <span class="param">max_depth</span>=<span class="number">4</span>,
    <span class="param">random_state</span>=<span class="number">42</span>
)

<span class="var">modelo_ia</span>.<span class="func">fit</span>(<span class="var">X</span>, <span class="var">y</span>)
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

            .comment {{ color: #6A9955; font-weight: 800; }}
            .var {{ color: #58A6FF; font-weight: 700; }}
            .string {{ color: #CE9178; }}
            .func {{ color: #DCDCAA; }}
            .param {{ color: #9CDCFE; }}
            .keyword {{ color: #C586C0; }}
            .number {{ color: #B5CEA8; }}
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
                <div class="file-name">modelo_entrenamiento.py</div>
            </div>
            <pre class="code-body">{codigo_html}</pre>
        </div>
    </body>
    </html>
    """

    components.html(html_code, height=ALTURA_PANEL + 5, scrolling=False)


def panel_espera_modelo():
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
                box-sizing: border-box;
                overflow: hidden;
            }}

            .output-header {{
                height: 34px;
                background: #101827;
                display: flex;
                align-items: center;
                padding: 0 12px;
                color: #A9C8D8;
                font-size: 12px;
                box-sizing: border-box;
            }}

            .output-body {{
                height: calc({ALTURA_PANEL}px - 34px);
                padding: 18px;
                box-sizing: border-box;
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
            <div class="output-header">visualización_entrenamiento_modelo</div>
            <div class="output-body">
                <div class="console">
                    <div>&gt;&gt;&gt; Esperando entrenamiento...</div>
                    <div class="muted">Presiona ▶ para construir el árbol de decisión.</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html_panel, height=ALTURA_PANEL + 5, scrolling=False)


def panel_ejecucion_modelo(mensajes, finalizado=False):
    lineas = ""
    for mensaje in mensajes:
        lineas += f"<div>{html.escape(mensaje)}</div>"

    visual_html = ""

    if finalizado:
        visual_html = """
        <div class="mini-console">
            <div>&gt;&gt;&gt; Cargando datos históricos</div>
            <div>&gt;&gt;&gt; Separando X e y</div>
            <div>&gt;&gt;&gt; Entrenando árbol de decisión</div>
            <div class="ok">&gt;&gt;&gt; Modelo entrenado correctamente</div>
        </div>

        <div class="tree-title">ÁRBOL DE DECISIÓN ENTRENADO</div>

        <div class="tree-zone">
            <svg class="tree-svg" viewBox="0 0 1000 560" preserveAspectRatio="xMidYMid meet">

                <defs>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="2.2" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>

                <!-- ================= RAMAS ORTOGONALES ================= -->

                <path class="branch b-l3" d="M250 192 V225 H120 V485" />
                <path class="branch b-l3" d="M250 225 H385 V270" />

                <path class="branch b-l4" d="M385 310 V345 H300 V470" />
                <path class="branch b-l4" d="M385 345 H470 V380" />

                <path class="branch b-leaf" d="M470 420 V445 H430 V470" />
                <path class="branch b-leaf" d="M470 445 H510 V470" />

                <path class="branch b-l3" d="M750 190 V225 H625 V270" />
                <path class="branch b-l3" d="M750 225 H875 V270" />

                <path class="branch b-leaf" d="M625 310 V445 H585 V470" />
                <path class="branch b-leaf" d="M625 445 H665 V470" />

                <path class="branch b-l4" d="M875 310 V345 H795 V380" />
                <path class="branch b-leaf" d="M875 345 H925 V470" />

                <path class="branch b-leaf" d="M795 420 V445 H760 V470" />
                <path class="branch b-leaf" d="M795 445 H830 V470" />

                <!-- ================= ETIQUETAS SÍ / NO ================= -->

                <rect class="tag n-l2" x="350" y="93" width="34" height="18" rx="6"/>
                <text class="tag-text n-l2" x="367" y="106">NO</text>

                <rect class="tag n-l2" x="655" y="93" width="34" height="18" rx="6"/>
                <text class="tag-text n-l2" x="672" y="106">SÍ</text>

                <rect class="tag n-l3" x="145" y="213" width="34" height="18" rx="6"/>
                <text class="tag-text n-l3" x="162" y="226">NO</text>

                <rect class="tag n-l3" x="320" y="213" width="34" height="18" rx="6"/>
                <text class="tag-text n-l3" x="337" y="226">SÍ</text>

                <rect class="tag n-l3" x="585" y="213" width="34" height="18" rx="6"/>
                <text class="tag-text n-l3" x="602" y="226">NO</text>

                <rect class="tag n-l3" x="825" y="213" width="34" height="18" rx="6"/>
                <text class="tag-text n-l3" x="842" y="226">SÍ</text>

                <rect class="tag n-l4" x="330" y="333" width="34" height="18" rx="6"/>
                <text class="tag-text n-l4" x="347" y="346">NO</text>

                <rect class="tag n-l4" x="430" y="333" width="34" height="18" rx="6"/>
                <text class="tag-text n-l4" x="447" y="346">SÍ</text>

                <rect class="tag n-l4" x="735" y="333" width="34" height="18" rx="6"/>
                <text class="tag-text n-l4" x="752" y="346">NO</text>

                <rect class="tag n-l4" x="845" y="333" width="34" height="18" rx="6"/>
                <text class="tag-text n-l4" x="862" y="346">SÍ</text>

                <!-- ================= NODOS ================= -->

                <rect class="node root n-root" x="455" y="32" width="90" height="42" rx="8"/>
                <text class="node-text n-root" x="500" y="57">cola ≤ 30</text>

                <!-- conexión raíz → nivel 2: se dibuja DESPUÉS del rect raíz para quedar encima de su glow -->
                <path class="branch b-l2" d="M500 74 V115" />
                <path class="branch b-l2" d="M250 115 H750" />
                <path class="branch b-l2" d="M250 115 V150" />
                <path class="branch b-l2" d="M750 115 V150" />

                <rect class="node n-l2" x="205" y="150" width="90" height="42" rx="8"/>
                <text class="node-text n-l2" x="250" y="175">flujo ≤ 54</text>

                <rect class="node n-l2" x="705" y="150" width="90" height="42" rx="8"/>
                <text class="node-text n-l2" x="750" y="175">vel ≤ 47</text>

                <rect class="node n-l3" x="340" y="270" width="90" height="42" rx="8"/>
                <text class="node-text n-l3" x="385" y="295">vel ≤ 62</text>

                <rect class="node n-l3" x="580" y="270" width="90" height="42" rx="8"/>
                <text class="node-text n-l3" x="625" y="295">flujo ≤ 70</text>

                <rect class="node n-l3" x="830" y="270" width="90" height="42" rx="8"/>
                <text class="node-text n-l3" x="875" y="295">cola ≤ 45</text>

                <rect class="node n-l4" x="425" y="380" width="90" height="42" rx="8"/>
                <text class="node-text n-l4" x="470" y="405">cola ≤ 18</text>

                <rect class="node n-l4" x="750" y="380" width="90" height="42" rx="8"/>
                <text class="node-text n-l4" x="795" y="405">vel ≤ 25</text>

                <!-- ================= HOJAS ALINEADAS ================= -->

                <rect class="leaf leaf-b n-leaf" x="103" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-b-text n-leaf" x="120" y="491">B</text>

                <rect class="leaf leaf-m n-leaf" x="283" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-m-text n-leaf" x="300" y="491">M</text>

                <rect class="leaf leaf-b n-leaf" x="413" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-b-text n-leaf" x="430" y="491">B</text>

                <rect class="leaf leaf-m n-leaf" x="493" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-m-text n-leaf" x="510" y="491">M</text>

                <rect class="leaf leaf-a n-leaf" x="568" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-a-text n-leaf" x="585" y="491">A</text>

                <rect class="leaf leaf-m n-leaf" x="648" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-m-text n-leaf" x="665" y="491">M</text>

                <rect class="leaf leaf-a n-leaf" x="743" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-a-text n-leaf" x="760" y="491">A</text>

                <rect class="leaf leaf-m n-leaf" x="813" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-m-text n-leaf" x="830" y="491">M</text>

                <rect class="leaf leaf-a n-leaf" x="908" y="470" width="34" height="30" rx="7"/>
                <text class="leaf-text leaf-a-text n-leaf" x="925" y="491">A</text>

                <!-- línea base inferior -->
                <line class="base-line n-leaf" x1="80" y1="512" x2="950" y2="512" />
            </svg>
        </div>

        <div class="status-bar">
            <span class="b-text">B = Baja</span>
            <span class="m-text">M = Media</span>
            <span class="a-text">A = Alta</span>
            <span class="trained">Modelo entrenado</span>
        </div>

        <div class="final-note">
            Modelo entrenado. Las reglas aprendidas se usarán en la siguiente etapa.
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

            .output-window {{
                width: 100%;
                height: {ALTURA_PANEL}px;
                background:
                    radial-gradient(circle at 50% 18%, rgba(0, 229, 255, 0.10), transparent 32%),
                    linear-gradient(180deg, #08111F 0%, #050B14 100%);
                border: 1px solid rgba(125, 255, 240, 0.24);
                box-sizing: border-box;
                overflow: hidden;
            }}

            .output-header {{
                height: 34px;
                background: #101827;
                display: flex;
                align-items: center;
                padding: 0 12px;
                color: #A9C8D8;
                font-size: 12px;
                box-sizing: border-box;
            }}

            .output-body {{
                height: calc({ALTURA_PANEL}px - 34px);
                padding: 10px;
                box-sizing: border-box;
                overflow-y: auto;
            }}

            .mini-console {{
                height: 58px;
                background: rgba(5, 10, 18, 0.82);
                border: 1px solid rgba(110, 231, 168, 0.26);
                border-radius: 9px;
                padding: 8px 10px;
                color: #CFE8D6;
                font-size: 10px;
                line-height: 1.25;
                box-sizing: border-box;
                margin-bottom: 6px;
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                column-gap: 12px;
            }}

            .mini-console .ok {{
                color: #6EE7A8;
                font-weight: 900;
            }}

            .tree-title {{
                color: #7DFFF0;
                font-size: 13px;
                font-weight: 900;
                letter-spacing: 0.4px;
                margin: 4px 0 6px 0;
                text-align: center;
            }}

            .tree-zone {{
                position: relative;
                width: 100%;
                height: 520px;
                border-radius: 12px;
                border: 1px solid rgba(125, 255, 240, 0.16);
                background:
                    linear-gradient(rgba(125,255,240,0.028) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(125,255,240,0.028) 1px, transparent 1px);
                background-size: 26px 26px;
                overflow: hidden;
            }}

            .tree-svg {{
                width: 100%;
                height: 100%;
                display: block;
            }}

            .branch {{
                fill: none;
                stroke: rgba(221, 235, 255, 0.82);
                stroke-width: 1.65;
                stroke-linecap: square;
                stroke-linejoin: miter;
                filter: url(#glow);
                opacity: 0;
                animation: growLine 0.55s ease-out forwards;
            }}

            .node {{
                fill: rgba(18, 32, 55, 0.96);
                stroke: rgba(125,255,240,0.60);
                stroke-width: 1.2;
                filter: url(#glow);
                opacity: 0;
                animation: appearNode 0.45s ease-out forwards;
            }}

            .root {{
                stroke: rgba(197, 134, 192, 0.95);
            }}

            .node-text {{
                fill: #EAF6FF;
                font-size: 11px;
                font-weight: 900;
                text-anchor: middle;
                dominant-baseline: middle;
                opacity: 0;
                animation: appearNode 0.45s ease-out forwards;
            }}

            .tag {{
                fill: rgba(16, 24, 39, 0.96);
                stroke: rgba(125,255,240,0.50);
                stroke-width: 1;
                opacity: 0;
                animation: appearNode 0.45s ease-out forwards;
            }}

            .tag-text {{
                fill: #9CDCFE;
                font-size: 9px;
                font-weight: 900;
                text-anchor: middle;
                dominant-baseline: middle;
                opacity: 0;
                animation: appearNode 0.45s ease-out forwards;
            }}

            .leaf {{
                fill: rgba(13, 27, 42, 0.98);
                stroke-width: 1.4;
                opacity: 0;
                animation: appearNode 0.45s ease-out forwards;
            }}

            .leaf-b {{ stroke: rgba(110,231,168,0.90); }}
            .leaf-m {{ stroke: rgba(255,208,77,0.90); }}
            .leaf-a {{ stroke: rgba(255,95,87,0.90); }}

            .leaf-text {{
                font-size: 13px;
                font-weight: 900;
                text-anchor: middle;
                dominant-baseline: middle;
                opacity: 0;
                animation: appearNode 0.45s ease-out forwards;
            }}

            .leaf-b-text {{ fill: #6EE7A8; }}
            .leaf-m-text {{ fill: #FFD04D; }}
            .leaf-a-text {{ fill: #FF5F57; }}

            .base-line {{
                stroke: rgba(125,255,240,0.25);
                stroke-width: 1;
                stroke-dasharray: 4 6;
                opacity: 0;
                animation: appearNode 0.45s ease-out forwards;
            }}

            .b-l2 {{ animation-delay: 0.35s; }}
            .b-l3 {{ animation-delay: 0.75s; }}
            .b-l4 {{ animation-delay: 1.15s; }}
            .b-leaf {{ animation-delay: 1.55s; }}

            .n-root {{ animation-delay: 0.15s; }}
            .n-l2 {{ animation-delay: 0.55s; }}
            .n-l3 {{ animation-delay: 0.95s; }}
            .n-l4 {{ animation-delay: 1.35s; }}
            .n-leaf {{ animation-delay: 1.75s; }}

            .b-text {{ color: #6EE7A8; font-weight: 900; }}
            .m-text {{ color: #FFD04D; font-weight: 900; }}
            .a-text {{ color: #FF5F57; font-weight: 900; }}

            .status-bar {{
                height: 36px;
                margin-top: 7px;
                border-radius: 9px;
                border: 1px solid rgba(125,255,240,0.18);
                background: rgba(13, 27, 42, 0.88);
                display: grid;
                grid-template-columns: 1fr 1fr 1fr 1.4fr;
                align-items: center;
                padding: 0 10px;
                box-sizing: border-box;
                color: #A9C8D8;
                font-size: 9.5px;
                gap: 8px;
            }}

            .trained {{
                color: #6EE7A8;
                font-weight: 900;
                text-align: right;
            }}

            .final-note {{
                margin-top: 7px;
                color: #DDEBFF;
                font-size: 10px;
                text-align: center;
                border-radius: 8px;
                padding: 7px;
                background: rgba(125,255,240,0.06);
                border: 1px solid rgba(125,255,240,0.14);
            }}

            @keyframes appearNode {{
                from {{
                    opacity: 0;
                    transform: translateY(-4px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            @keyframes growLine {{
                from {{
                    opacity: 0;
                    stroke-dasharray: 600;
                    stroke-dashoffset: 600;
                }}
                to {{
                    opacity: 1;
                    stroke-dasharray: 600;
                    stroke-dashoffset: 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="output-window">
            <div class="output-header">visualización_entrenamiento_modelo</div>
            <div class="output-body">
                {visual_html if finalizado else f'''
                <div class="mini-console">
                    {lineas}
                </div>
                '''}
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html_panel, height=ALTURA_PANEL + 5, scrolling=False)


def render_modelo(data=None, modelo=None, X=None, y=None):
    st.markdown(
        """
        <div style="margin-top:-20px; margin-bottom:10px;">
            <h2 style="margin:0; color:#EAF6FF;">5. Modelo de IA</h2>
            <p style="margin:6px 0 0 0; color:#A9C8D8; line-height:1.35;">
                Se entrena un árbol de decisión con datos históricos para aprender reglas
                asociadas al nivel de congestión vehicular.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_codigo, col_boton, col_ejecucion = st.columns(
        [0.465, 0.05, 0.485],
        gap="small"
    )

    with col_codigo:
        ventana_codigo_modelo()

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
            key="btn_ejecutar_modelo",
            help="Visualizar entrenamiento del modelo"
        )

    with col_ejecucion:
        salida = st.empty()

        if not ejecutar:
            with salida:
                panel_espera_modelo()
            return

        mensajes = []

        pasos = [
            (">>> Cargando datos históricos", 0.25),
            (">>> Separando X e y", 0.25),
            (">>> Entrenando árbol de decisión", 0.25),
            (">>> Generando estructura del árbol", 0.25),
            (">>> Modelo entrenado correctamente", 0.25),
        ]

        for mensaje, espera in pasos:
            mensajes.append(mensaje)
            with salida:
                panel_ejecucion_modelo(mensajes)
            time.sleep(espera)

        with salida:
            panel_ejecucion_modelo(mensajes, finalizado=True)