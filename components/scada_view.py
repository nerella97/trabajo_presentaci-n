import streamlit.components.v1 as components


def render_scada_panel(velocidad_live: int, flujo_live: int, cola_live: int):
    scada_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            background: transparent;
            font-family: Arial, sans-serif;
        }}

        .scada-wrap {{
            position: relative;
            width: 100%;
            max-width: 100%;
            height: 1000px;
            margin: 0 auto;
            box-sizing: border-box;
            
            background:
                radial-gradient(circle at 20% 20%, rgba(30,240,178,0.08), transparent 25%),
                radial-gradient(circle at 80% 70%, rgba(0,180,255,0.08), transparent 25%),
                linear-gradient(145deg, #07111F, #0B1D2E);
            border-left: 1px solid rgba(125,255,240,0.28);
            border-right: 1px solid rgba(125,255,240,0.28);
            border-bottom: 1px solid rgba(125,255,240,0.28);
            border-top: none;
            border-radius: 0 0 24px 24px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(30,200,165,0.12);
        }}

        .topbar {{
            position: absolute;
            left: 0;
            right: 0;
            top: 0;
            height: 46px;
            background: rgba(2,10,18,0.88);
            border-bottom: 1px solid rgba(125,255,240,0.18);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            color: #7DFFF0;
            font-weight: 900;
            z-index: 10;
            box-sizing: border-box;
        }}

        .status {{
            color: #FFD166;
            font-size: 13px;
            font-weight: 800;
        }}

        canvas {{
            position: absolute;
            left: 0;
            top: 46px;
            width: 100%;
            height: calc(100% - 46px);
        }}

        .metric-strip {{
            position: absolute;
            left: 24px;
            right: 24px;
            bottom: 20px;
            height: 44px;
            background: rgba(2,10,18,0.72);
            border: 1px solid rgba(125,255,240,0.22);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 34px;
            color: #A9C8D8;
            font-size: 13px;
            z-index: 10;
            backdrop-filter: blur(4px);
        }}

        .metric-strip span {{
            color: #7DFFF0;
            font-weight: 900;
        }}
    </style>
    </head>

    <body>
        <div class="scada-wrap">
            <div class="topbar">
                <div>HMI / SCADA - MONITOREO DE INTERSECCIÓN</div>
                <div id="statusText" class="status">● Inicializando simulación</div>
            </div>

            <canvas id="trafficCanvas"></canvas>

            <div class="metric-strip">
                <div>Velocidad: <span>{velocidad_live} km/h</span></div>
                <div>Flujo: <span>{flujo_live} veh/min</span></div>
                <div>Cola: <span>{cola_live} m</span></div>
            </div>
        </div>

<script>
    const canvas = document.getElementById("trafficCanvas");
    const ctx = canvas.getContext("2d");
    const statusText = document.getElementById("statusText");

    function resizeCanvas() {{
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
    }}

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    const colors = ["#4CC9F0", "#FFD166", "#EF476F", "#06D6A0", "#EAF6FF", "#9B5DE5"];

    let phase = "start";
    let phaseStart = performance.now();
    let cycleState = "start";

    const startDuration = 3000;
    const greenDuration = 10000;

    /*
       Ámbar de seguridad.
       Los autos dejan de entrar 3 segundos antes de pasar a rojo.
    */
    const amberDuration = 5200;
    const amberStopBeforeEnd = 3000;
    const allRedDuration = 1300;

    function updatePhase(now) {{
        const elapsed = now - phaseStart;

        if (cycleState === "start" && elapsed > startDuration) {{
            cycleState = "vertical";
            phase = "vertical";
            phaseStart = now;
        }}
        else if (cycleState === "vertical" && elapsed > greenDuration) {{
            cycleState = "amber_vertical";
            phase = "amber_vertical";
            phaseStart = now;
        }}
        else if (cycleState === "amber_vertical" && elapsed > amberDuration) {{
            cycleState = "allred_to_horizontal";
            phase = "allred";
            phaseStart = now;
        }}
        else if (cycleState === "allred_to_horizontal" && elapsed > allRedDuration) {{
            cycleState = "horizontal";
            phase = "horizontal";
            phaseStart = now;
        }}
        else if (cycleState === "horizontal" && elapsed > greenDuration) {{
            cycleState = "amber_horizontal";
            phase = "amber_horizontal";
            phaseStart = now;
        }}
        else if (cycleState === "amber_horizontal" && elapsed > amberDuration) {{
            cycleState = "allred_to_vertical";
            phase = "allred";
            phaseStart = now;
        }}
        else if (cycleState === "allred_to_vertical" && elapsed > allRedDuration) {{
            cycleState = "vertical";
            phase = "vertical";
            phaseStart = now;
        }}

        const elapsedInPhase = now - phaseStart;
        const amberRemaining = Math.max(0, Math.ceil((amberDuration - elapsedInPhase) / 1000));

        if (phase === "start") {{
            statusText.textContent = "● Inicio de simulación";
        }}
        else if (phase === "vertical") {{
            statusText.textContent = "● Vertical en verde · Horizontal en rojo";
        }}
        else if (phase === "amber_vertical") {{
            statusText.textContent = "● Vertical en ámbar · despeje: " + amberRemaining + " s";
        }}
        else if (phase === "horizontal") {{
            statusText.textContent = "● Horizontal en verde · Vertical en rojo";
        }}
        else if (phase === "amber_horizontal") {{
            statusText.textContent = "● Horizontal en ámbar · despeje: " + amberRemaining + " s";
        }}
        else {{
            statusText.textContent = "● Fase segura · ambos sentidos en rojo";
        }}
    }}

    const cars = [];

    const carW = 58;
    const carH = 26;

    const verticalSpeed = 0.070;
    const horizontalSpeed = 0.038;

    const verticalSpacing = 96;
    const horizontalSpacing = 94;

    function addVerticalLane(xOffset, laneIndex) {{
        for (let i = 0; i < 20; i++) {{
            cars.push({{
                dir: "up",
                lane: laneIndex,
                xOffset: xOffset,
                xPx: null,
                yPx: null,
                speed: verticalSpeed,
                color: colors[(i + laneIndex) % colors.length],
                initialIndex: i
            }});
        }}
    }}

    function addHorizontalLane(yOffset, laneIndex) {{
        for (let i = 0; i < 30; i++) {{
            cars.push({{
                dir: "left",
                lane: laneIndex,
                xPx: null,
                yPx: null,
                yOffset: yOffset,
                speed: horizontalSpeed,
                color: colors[(i + laneIndex + 2) % colors.length],
                initialIndex: i
            }});
        }}
    }}

    addVerticalLane(-24, 0);
    addVerticalLane(24, 1);

    addHorizontalLane(-20, 0);
    addHorizontalLane(20, 1);

    function getRoadGeometry(w, h) {{
        const cx = w / 2;
        const cy = h / 2;

        /*
           Ambas pistas tienen el mismo ancho real en píxeles.
        */
        const roadWidth = Math.min(w, h) * 0.31;

        return {{
            cx,
            cy,
            roadWidth,
            roadV: {{
                x: cx - roadWidth / 2,
                y: 0,
                width: roadWidth,
                height: h
            }},
            roadH: {{
                x: 0,
                y: cy - roadWidth / 2,
                width: w,
                height: roadWidth
            }},
            stopY: cy + roadWidth / 2 + 14,
            stopX: cx + roadWidth / 2 + 14,
            intersectionLeft: cx - roadWidth / 2,
            intersectionRight: cx + roadWidth / 2,
            intersectionTop: cy - roadWidth / 2,
            intersectionBottom: cy + roadWidth / 2
        }};
    }}

    function initializeCarsIfNeeded(w, h) {{
        const g = getRoadGeometry(w, h);

        /*
           Los autos iniciales nacen detrás de la línea de pare.
           Así no se escapan carros de ambas pistas al inicio.
        */
        const verticalStartY = g.stopY + carW + 45;
        const horizontalStartX = g.stopX + carW + 45;

        for (const car of cars) {{
            if (car.dir === "up" && car.yPx === null) {{
                car.xPx = g.cx + car.xOffset;
                car.yPx = verticalStartY + car.initialIndex * verticalSpacing;
            }}

            if (car.dir === "left" && car.xPx === null) {{
                car.xPx = horizontalStartX + car.initialIndex * horizontalSpacing;
                car.yPx = g.cy + car.yOffset;
            }}
        }}
    }}

    function drawRoundedRect(x, y, w, h, r, fill, stroke) {{
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.lineTo(x + w - r, y);
        ctx.quadraticCurveTo(x + w, y, x + w, y + r);
        ctx.lineTo(x + w, y + h - r);
        ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
        ctx.lineTo(x + r, y + h);
        ctx.quadraticCurveTo(x, y + h, x, y + h - r);
        ctx.lineTo(x, y + r);
        ctx.quadraticCurveTo(x, y, x + r, y);
        ctx.closePath();

        ctx.fillStyle = fill;
        ctx.fill();

        if (stroke) {{
            ctx.strokeStyle = stroke;
            ctx.lineWidth = 1.5;
            ctx.stroke();
        }}
    }}

    function drawRoads(w, h) {{
        const g = getRoadGeometry(w, h);
        const roadV = g.roadV;
        const roadH = g.roadH;

        ctx.fillStyle = "#253A4D";
        ctx.fillRect(roadV.x, roadV.y, roadV.width, roadV.height);
        ctx.fillRect(roadH.x, roadH.y, roadH.width, roadH.height);

        ctx.fillStyle = "#2D455A";
        ctx.fillRect(roadV.x, roadH.y, roadV.width, roadH.height);

        ctx.strokeStyle = "rgba(255,255,255,0.45)";
        ctx.lineWidth = 2;
        ctx.setLineDash([18, 18]);

        ctx.beginPath();
        ctx.moveTo(g.cx, 0);
        ctx.lineTo(g.cx, h);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, g.cy);
        ctx.lineTo(w, g.cy);
        ctx.stroke();

        ctx.setLineDash([]);

        ctx.fillStyle = "rgba(255, 107, 107, 0.95)";
        ctx.shadowColor = "rgba(255,107,107,0.75)";
        ctx.shadowBlur = 12;

        ctx.fillRect(roadV.x, g.stopY, roadV.width, 4);
        ctx.fillRect(g.stopX, roadH.y, 4, roadH.height);

        ctx.shadowBlur = 0;

        ctx.strokeStyle = "rgba(255, 107, 107, 0.45)";
        ctx.lineWidth = 1;
        ctx.setLineDash([6, 6]);

        ctx.strokeRect(g.cx - 110, g.stopY, 220, h - g.stopY - 92);
        ctx.strokeRect(g.stopX, g.cy - 44, w - g.stopX - 120, 88);

        ctx.setLineDash([]);

        ctx.fillStyle = "rgba(255,255,255,0.55)";
        ctx.font = "30px Arial";
        ctx.fillText("↑", g.cx - 12, g.cy + 145);
        ctx.fillText("←", g.cx + 360, g.cy + 10);

        ctx.fillStyle = "#FFB3B3";
        ctx.font = "12px Arial";
        ctx.fillText("Cola vertical: {cola_live} m", g.cx + 115, g.cy + 148);
        ctx.fillText("Cola horizontal: flujo alto", g.cx + 325, roadH.y - 8);
    }}

    function drawTrafficLight(x, y, active) {{
        drawRoundedRect(x, y, 32, 100, 12, "#020A12", "rgba(255,255,255,0.25)");

        function light(cx, cy, color, glow) {{
            ctx.beginPath();
            ctx.arc(cx, cy, 8, 0, Math.PI * 2);
            ctx.fillStyle = color;

            if (glow) {{
                ctx.shadowColor = color;
                ctx.shadowBlur = 14;
            }}

            ctx.fill();
            ctx.shadowBlur = 0;
        }}

        light(x + 16, y + 18, active === "red" ? "#FF4D4D" : "#333", active === "red");
        light(x + 16, y + 50, active === "amber" ? "#FFD166" : "#333", active === "amber");
        light(x + 16, y + 82, active === "green" ? "#1EF0B2" : "#333", active === "green");
    }}

    function drawSensorLabel(x, y, text) {{
        drawRoundedRect(x, y, 130, 28, 10, "rgba(2,10,18,0.90)", "rgba(125,255,240,0.42)");

        ctx.fillStyle = "#1EF0B2";
        ctx.beginPath();
        ctx.arc(x + 13, y + 14, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#EAF6FF";
        ctx.font = "11px Arial";
        ctx.fillText(text, x + 24, y + 18);
    }}

    function drawCameraIcon(x, y) {{
        drawRoundedRect(x, y, 34, 22, 5, "rgba(0,190,255,0.22)", "rgba(125,255,240,0.80)");
        ctx.beginPath();
        ctx.arc(x + 17, y + 11, 5, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(125,255,240,0.75)";
        ctx.fill();
        ctx.beginPath();
        ctx.moveTo(x + 34, y + 7);
        ctx.lineTo(x + 48, y + 2);
        ctx.lineTo(x + 48, y + 20);
        ctx.lineTo(x + 34, y + 15);
        ctx.closePath();
        ctx.fillStyle = "rgba(0,190,255,0.16)";
        ctx.fill();
    }}

    function drawRadarIcon(x, y, t) {{
        ctx.strokeStyle = "rgba(30,240,178,0.38)";
        ctx.lineWidth = 2;

        for (let i = 0; i < 3; i++) {{
            ctx.beginPath();
            ctx.arc(x, y, 18 + i * 12 + Math.sin(t / 300) * 2, -0.8, 0.8);
            ctx.stroke();
        }}

        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = "#1EF0B2";
        ctx.fill();
    }}

    function drawLoopSensor(x, y, w, h) {{
        ctx.strokeStyle = "rgba(30,240,178,0.78)";
        ctx.lineWidth = 2;
        ctx.setLineDash([7, 5]);
        ctx.strokeRect(x, y, w, h);
        ctx.setLineDash([]);

        ctx.strokeStyle = "rgba(30,240,178,0.30)";
        ctx.lineWidth = 1;
        ctx.strokeRect(x + 7, y + 7, w - 14, h - 14);
    }}

    function drawCameraCone(points) {{
        ctx.fillStyle = "rgba(0,190,255,0.08)";
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {{
            ctx.lineTo(points[i].x, points[i].y);
        }}
        ctx.closePath();
        ctx.fill();

        ctx.strokeStyle = "rgba(0,190,255,0.24)";
        ctx.lineWidth = 1;
        ctx.stroke();
    }}

    function drawSensors(w, h, t) {{
        const g = getRoadGeometry(w, h);

        /*
           Configuración representativa:
           - 2 cámaras: una para cada eje de circulación.
           - 2 radares: uno por aproximación principal.
           - 2 espiras: una por eje para conteo/flujo.
        */

        // Cámara para eje horizontal
        drawCameraCone([
                   {{x: g.cx + 430, y: g.cy - 150}},   // Ápice (punta de la cámara)
    {{x: g.cx + 200, y: g.cy - 50}},     // Esquina sup. izq.
    {{x: g.cx + 200, y: g.cy + 80}},     // Esquina inf. izq.
    {{x: g.cx + 668, y: g.cy + 80}},    // Esquina inf. der. (más a la derecha)
    {{x: g.cx + 668, y: g.cy - 50}}     // Esquina sup. der. (más a la derecha)
        ]);
        
        drawCameraIcon(g.cx + 405, g.cy - 165);
        drawSensorLabel(g.cx + 345, g.cy - 198, "Cámara eje H");

        
        // Cámara para eje vertical
// Ubicada en la esquina inferior izquierda, apuntando hacia la cola vertical y la intersección
drawCameraCone([
    {{x: g.cx - 360, y: g.cy + 260}},   // Ápice (cámara)
    {{x: g.cx - 70, y: g.stopY + 20}},  // Esquina sup. izq. del rectángulo
    {{x: g.cx + 75, y: g.stopY + 20}},  // Esquina sup. der. del rectángulo
    {{x: g.cx + 75, y: g.cy + 400}},    // Esquina inf. der. (aumenté Y)
    {{x: g.cx - 70, y: g.cy + 400}}     // Esquina inf. izq. (aumenté Y)
]);

drawCameraIcon(g.cx - 380, g.cy + 250);
drawSensorLabel(g.cx - 430, g.cy + 292, "Cámara eje V");

        // Radar horizontal
        drawRadarIcon(g.cx + 360, g.cy + 92, t);
        drawSensorLabel(g.cx + 285, g.cy + 112, "Radar eje H");

        // Radar vertical
        drawRadarIcon(g.cx - 115, g.cy + 235, t);
        drawSensorLabel(g.cx - 190, g.cy + 255, "Radar eje V");

        // Espira horizontal dentro de la pista
        drawLoopSensor(g.stopX + 50, g.cy - 34, 78, 68);
        drawSensorLabel(g.stopX + 32, g.cy + 47, "Espira eje H");

        // Espira vertical dentro de la pista
        drawLoopSensor(g.cx - 37, g.stopY + 50, 74, 68);
        drawSensorLabel(g.cx - 70, g.stopY + 128, "Espira eje V");
    }}

    function drawCarBody(x, y, w, h, color) {{
    /*
       Diseño mejorado del vehículo visto desde arriba.
       Mantiene el mismo tamaño para no romper la simulación.
    */

    // Sombra suave debajo del auto
    ctx.save();
    ctx.shadowColor = "rgba(0, 0, 0, 0.38)";
    ctx.shadowBlur = 8;
    ctx.shadowOffsetX = 2;
    ctx.shadowOffsetY = 3;

    // Carrocería principal
    drawRoundedRect(
        x,
        y,
        w,
        h,
        9,
        color,
        "rgba(5, 10, 16, 0.85)"
    );

    ctx.restore();

    // Parte central superior del auto, para dar sensación de volumen
    drawRoundedRect(
        x + 8,
        y + 4,
        w - 16,
        h - 8,
        7,
        "rgba(255, 255, 255, 0.10)",
        null
    );

    // Cabina central oscura
    drawRoundedRect(
        x + w * 0.34,
        y + 4,
        w * 0.32,
        h - 8,
        5,
        "rgba(18, 28, 38, 0.92)",
        "rgba(255, 255, 255, 0.18)"
    );

    // Parabrisas delantero
    drawRoundedRect(
        x + w * 0.18,
        y + 6,
        w * 0.18,
        h - 12,
        4,
        "rgba(32, 48, 60, 0.92)",
        null
    );

    // Luneta trasera
    drawRoundedRect(
        x + w * 0.64,
        y + 6,
        w * 0.18,
        h - 12,
        4,
        "rgba(32, 48, 60, 0.92)",
        null
    );

    // Línea decorativa central
    ctx.strokeStyle = "rgba(255, 255, 255, 0.20)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x + w * 0.50, y + 5);
    ctx.lineTo(x + w * 0.50, y + h - 5);
    ctx.stroke();

    // Ruedas superiores
    drawRoundedRect(
        x + 8,
        y - 2,
        10,
        4,
        2,
        "rgba(5, 8, 12, 0.95)",
        null
    );

    drawRoundedRect(
        x + w - 18,
        y - 2,
        10,
        4,
        2,
        "rgba(5, 8, 12, 0.95)",
        null
    );

    // Ruedas inferiores
    drawRoundedRect(
        x + 8,
        y + h - 2,
        10,
        4,
        2,
        "rgba(5, 8, 12, 0.95)",
        null
    );

    drawRoundedRect(
        x + w - 18,
        y + h - 2,
        10,
        4,
        2,
        "rgba(5, 8, 12, 0.95)",
        null
    );

    // Luces delanteras
    drawRoundedRect(
        x + 2,
        y + 6,
        4,
        5,
        2,
        "rgba(255, 245, 190, 0.95)",
        null
    );

    drawRoundedRect(
        x + 2,
        y + h - 11,
        4,
        5,
        2,
        "rgba(255, 245, 190, 0.95)",
        null
    );

    // Luces traseras
    drawRoundedRect(
        x + w - 6,
        y + 6,
        4,
        5,
        2,
        "rgba(255, 70, 80, 0.95)",
        null
    );

    drawRoundedRect(
        x + w - 6,
        y + h - 11,
        4,
        5,
        2,
        "rgba(255, 70, 80, 0.95)",
        null
    );
}}

    function drawCar(car) {{
        ctx.save();

        if (car.dir === "up") {{
            ctx.translate(car.xPx, car.yPx);
            ctx.rotate(-Math.PI / 2);
            drawCarBody(-carW / 2, -carH / 2, carW, carH, car.color);
        }}
        else {{
            drawCarBody(car.xPx - carW / 2, car.yPx - carH / 2, carW, carH, car.color);
        }}

        ctx.restore();
    }}

    function isVerticalClearingAllowed() {{
        const elapsedInPhase = performance.now() - phaseStart;

        if (phase === "vertical") {{
            return true;
        }}

        if (phase === "amber_vertical") {{
            return elapsedInPhase < amberDuration - amberStopBeforeEnd;
        }}

        return false;
    }}

    function isHorizontalClearingAllowed() {{
        const elapsedInPhase = performance.now() - phaseStart;

        if (phase === "horizontal") {{
            return true;
        }}

        if (phase === "amber_horizontal") {{
            return elapsedInPhase < amberDuration - amberStopBeforeEnd;
        }}

        return false;
    }}

    function respawnCars(w, h) {{
        const g = getRoadGeometry(w, h);

        for (let lane = 0; lane < 2; lane++) {{
            const verticalLane = cars.filter(c => c.dir === "up" && c.lane === lane);
            const horizontalLane = cars.filter(c => c.dir === "left" && c.lane === lane);

            for (const car of verticalLane) {{
                if (car.yPx < -120) {{
                    const maxY = Math.max(...verticalLane.map(c => c.yPx));
                    car.yPx = Math.max(h + 80, maxY + verticalSpacing);
                    car.xPx = g.cx + car.xOffset;
                }}
            }}

            for (const car of horizontalLane) {{
                if (car.xPx < -120) {{
                    const maxX = Math.max(...horizontalLane.map(c => c.xPx));
                    car.xPx = Math.max(w + 80, maxX + horizontalSpacing);
                    car.yPx = g.cy + car.yOffset;
                }}
            }}
        }}
    }}

    function updateLaneVertical(laneCars, dt, g) {{
        const canEnterIntersection = isVerticalClearingAllowed();

        laneCars.sort((a, b) => a.yPx - b.yPx);

        for (let i = 0; i < laneCars.length; i++) {{
            const car = laneCars[i];

            const frontY = car.yPx - carW / 2;
            const rearY = car.yPx + carW / 2;

            /*
               El auto solo se considera liberado cuando todo el vehículo
               cruzó la línea de pare. Así no se escapan autos al inicio.
            */
            const alreadyEntered = rearY < g.stopY;

            let desiredY;

            if (canEnterIntersection || alreadyEntered) {{
                desiredY = car.yPx - car.speed * dt;
            }}
            else {{
                desiredY = Math.max(
                    car.yPx - car.speed * dt,
                    g.stopY + carW / 2 + 8
                );
            }}

            if (i > 0) {{
                const carAhead = laneCars[i - 1];
                const minimumY = carAhead.yPx + verticalSpacing;

                if (desiredY < minimumY) {{
                    desiredY = minimumY;
                }}
            }}

            car.yPx = desiredY;
        }}
    }}

    function updateLaneHorizontal(laneCars, dt, g) {{
        const canEnterIntersection = isHorizontalClearingAllowed();

        laneCars.sort((a, b) => a.xPx - b.xPx);

        for (let i = 0; i < laneCars.length; i++) {{
            const car = laneCars[i];

            const frontX = car.xPx - carW / 2;
            const rearX = car.xPx + carW / 2;

            /*
               Igual que en vertical: solo sigue libre si todo el auto
               cruzó la línea. Esto evita superposición al inicio.
            */
            const alreadyEntered = rearX < g.stopX;

            let desiredX;

            if (canEnterIntersection || alreadyEntered) {{
                desiredX = car.xPx - car.speed * dt;
            }}
            else {{
                desiredX = Math.max(
                    car.xPx - car.speed * dt,
                    g.stopX + carW / 2 + 8
                );
            }}

            if (i > 0) {{
                const carAhead = laneCars[i - 1];
                const minimumX = carAhead.xPx + horizontalSpacing;

                if (desiredX < minimumX) {{
                    desiredX = minimumX;
                }}
            }}

            car.xPx = desiredX;
        }}
    }}

    function updateCars(dt, w, h) {{
        const g = getRoadGeometry(w, h);

        for (let lane = 0; lane < 2; lane++) {{
            const verticalLane = cars.filter(c => c.dir === "up" && c.lane === lane);
            const horizontalLane = cars.filter(c => c.dir === "left" && c.lane === lane);

            updateLaneVertical(verticalLane, dt, g);
            updateLaneHorizontal(horizontalLane, dt, g);
        }}

        respawnCars(w, h);
    }}

    let last = performance.now();

    function animate(now) {{
        const dt = Math.min(now - last, 40);
        last = now;

        updatePhase(now);

        const w = canvas.width;
        const h = canvas.height;

        initializeCarsIfNeeded(w, h);

        ctx.clearRect(0, 0, w, h);

        drawRoads(w, h);
        updateCars(dt, w, h);

        for (const car of cars) {{
            drawCar(car);
        }}

        drawSensors(w, h, now);

        const g = getRoadGeometry(w, h);

        const verticalLightX = g.cx + g.roadWidth / 2 - 85;
        const verticalLightY = g.cy + g.roadWidth / 2 - 15;

        /*
           Semáforo horizontal: mantiene su ubicación lateral original,
           solo está elevado para no interferir con la pista.
        */
        const horizontalLightX = g.cx + g.roadWidth / 2 + 20;
        const horizontalLightY = g.cy - g.roadWidth / 2 - 105;

        if (phase === "vertical") {{
            drawTrafficLight(verticalLightX, verticalLightY, "green");
            drawTrafficLight(horizontalLightX, horizontalLightY, "red");
        }}
        else if (phase === "amber_vertical") {{
            drawTrafficLight(verticalLightX, verticalLightY, "amber");
            drawTrafficLight(horizontalLightX, horizontalLightY, "red");
        }}
        else if (phase === "horizontal") {{
            drawTrafficLight(verticalLightX, verticalLightY, "red");
            drawTrafficLight(horizontalLightX, horizontalLightY, "green");
        }}
        else if (phase === "amber_horizontal") {{
            drawTrafficLight(verticalLightX, verticalLightY, "red");
            drawTrafficLight(horizontalLightX, horizontalLightY, "amber");
        }}
        else {{
            drawTrafficLight(verticalLightX, verticalLightY, "red");
            drawTrafficLight(horizontalLightX, horizontalLightY, "red");
        }}

        requestAnimationFrame(animate);
    }}

    requestAnimationFrame(animate);
</script>
    </body>
    </html>
    """

    components.html(scada_html, height=1050, scrolling=False)