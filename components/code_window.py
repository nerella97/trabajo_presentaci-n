import html
import re
import streamlit.components.v1 as components


_KEYWORDS = [
    "if", "elif", "else", "for", "in", "return", "import", "from",
    "as", "None", "True", "False", "and", "or", "not", "def", "class",
    "with", "while", "try", "except", "finally", "pass", "raise",
    "print", "display",
]


def _highlight(codigo: str) -> str:
    lineas = []
    for linea in codigo.split("\n"):
        esc = html.escape(linea)
        if linea.strip().startswith("#"):
            lineas.append(f'<span class="comment">{esc}</span>')
            continue
        esc = re.sub(
            r'(&quot;[^&]*?&quot;)',
            r'<span class="string">\1</span>',
            esc,
        )
        for kw in _KEYWORDS:
            esc = re.sub(rf'\b{kw}\b', f'<span class="keyword">{kw}</span>', esc)
        esc = re.sub(
            r'\b([A-Za-z_]\w*)\s*(?=\()',
            r'<span class="func">\1</span>',
            esc,
        )
        esc = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="number">\1</span>', esc)
        lineas.append(esc)
    return "\n".join(lineas)


def code_window(title: str, code: str):
    n_lines = code.count("\n") + 1
    altura = max(120, 34 + n_lines * 20 + 28)
    codigo_html = _highlight(code)

    html_code = f"""<!DOCTYPE html>
<html>
<head>
<style>
  html, body {{ margin:0; padding:0; background:transparent; overflow:hidden; }}
  .colab-window {{
    width:100%; height:{altura}px;
    background:#0B1020;
    border:1px solid rgba(125,255,240,0.24);
    box-shadow:0 18px 42px rgba(0,0,0,0.35);
    font-family:Consolas,Monaco,"Courier New",monospace;
    box-sizing:border-box; overflow:hidden;
  }}
  .colab-header {{
    height:34px; background:#101827;
    display:flex; align-items:center; padding:0 12px;
    border-bottom:1px solid rgba(255,255,255,0.08); box-sizing:border-box;
  }}
  .dots {{ display:flex; gap:8px; align-items:center; }}
  .dot {{ width:13px; height:13px; border-radius:50%; display:inline-block; }}
  .red {{ background:#ff5f57; }}
  .yellow {{ background:#ffbd2e; }}
  .green {{ background:#28c840; }}
  .file-name {{ flex:1; text-align:center; color:#A9C8D8; font-size:12px; letter-spacing:0.2px; }}
  .code-body {{
    margin:0; height:calc({altura}px - 34px);
    padding:14px 16px;
    background:#0B1020; color:#DDEBFF;
    font-size:13px; line-height:1.32;
    white-space:pre-wrap; overflow:auto; box-sizing:border-box;
  }}
  .comment {{ color:#6A9955; font-weight:800; }}
  .var     {{ color:#58A6FF; }}
  .string  {{ color:#CE9178; }}
  .func    {{ color:#DCDCAA; }}
  .param   {{ color:#9CDCFE; }}
  .keyword {{ color:#C586C0; }}
  .number  {{ color:#B5CEA8; }}
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
      <div class="file-name">{html.escape(title)}</div>
    </div>
    <pre class="code-body">{codigo_html}</pre>
  </div>
</body>
</html>"""

    components.html(html_code, height=altura + 5, scrolling=False)
