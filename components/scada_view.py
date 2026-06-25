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
            height: 740px;
            background:
                radial-gradient(circle at 20% 20%, rgba(30,240,178,0.08), transparent 25%),
                radial-gradient(circle at 80% 70%, rgba(0,180,255,0.08), transparent 25%),
                linear-gradient(145deg, #07111F, #0B1D2E);
            border: 1px solid rgba(125,255,240,0.28);
            border-radius: 24px;
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

        .legend {{
            position: absolute;
            left: 24px;
            bottom: 24px;
            background: rgba(2,10,18,0.82);
            border: 1px solid rgba(255,209,102,0.35);
            border-radius: 14px;
            padding: 12px 16px;
            color: #A9C8D8;
            font-size: 13px;
            z-index: 10;
        }}

        .legend strong {{
            color: #FFD166;
        }}

        .ia-box {{
            position: absolute;
            right: 24px;
            bottom: 24px;
            width: 315px;
            background: rgba(7,17,31,0.95);
            border: 1px solid rgba(255,209,102,0.65);
            border-radius: 18px;
            padding: 16px;
            box-shadow: 0 0 24px rgba(255,209,102,0.18);
            color: white;
            z-index: 10;
        }}

        .ia-title {{
            color: #7DFFF0;
            font-weight: 900;
            font-size: 14px;
            margin-bottom: 6px;
        }}

        .ia-alert {{
            color: #FFD166;
            font-size: 23px;
            font-weight: 950;
            margin-top: 4px;
        }}

        .ia-small {{
            color: #9EBBD0;
            font-size: 12px;
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

            <div class="legend">
                <strong>Regla:</strong> en ámbar los autos dejan de entrar 3 segundos antes del cambio a rojo; los que ya cruzaron siguen saliendo.
            </div>

            <div class="ia-box">
                <div class="ia-title">🧠 Procesamiento IA</div>
                <div id="phaseTitle" class="ia-alert">Congestión ALTA</div>
                <div class="ia-small">
                    Velocidad: {velocidad_live} km/h · Flujo: {flujo_live} veh/min · Cola: {cola_live} m
                </div>
            </div>
        </div>

<script>
    const canvas = document.getElementById("trafficCanvas");
    const ctx = canvas.getContext("2d");
    const statusText = document.getElementById("statusText");
    const phaseTitle = document.getElementById("phaseTitle");

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
       Ámbar más largo.
       Los autos dejan de entrar 3 segundos antes de que termine el ámbar.
       Eso permite liberar la intersección.
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
            statusText.textContent = "● Inicio: ambos sentidos detenidos";
            phaseTitle.textContent = "Semáforos en espera";
        }}
        else if (phase === "vertical") {{
            statusText.textContent = "● Vertical en verde · Horizontal en rojo";
            phaseTitle.textContent = "Paso vertical habilitado";
        }}
        else if (phase === "amber_vertical") {{
            statusText.textContent = "● Vertical en ámbar · Horizontal en rojo · despeje: " + amberRemaining + " s";
            phaseTitle.textContent = "Despeje vertical";
        }}
        else if (phase === "horizontal") {{
            statusText.textContent = "● Vertical en rojo · Horizontal en verde";
            phaseTitle.textContent = "Paso horizontal habilitado";
        }}
        else if (phase === "amber_horizontal") {{
            statusText.textContent = "● Vertical en rojo · Horizontal en ámbar · despeje: " + amberRemaining + " s";
            phaseTitle.textContent = "Despeje horizontal";
        }}
        else {{
            statusText.textContent = "● Fase segura: ambos sentidos en rojo";
            phaseTitle.textContent = "Fase de seguridad";
        }}
    }}

    const cars = [];

    const carW = 58;
    const carH = 26;

    /*
       Horizontal más lenta.
       Vertical mantiene buena fluidez.
    */
    const verticalSpeed = 0.070;
    const horizontalSpeed = 0.038;

    /*
       Más espacio para los autos horizontales.
       Vertical se mantiene con separación moderada.
    */
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
           Ambas pistas usan el mismo ancho real.
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

        for (const car of cars) {{
            if (car.dir === "up" && car.yPx === null) {{
                car.xPx = g.cx + car.xOffset;
                car.yPx = g.cy + 135 + car.initialIndex * verticalSpacing;
            }}

            if (car.dir === "left" && car.xPx === null) {{
                car.xPx = g.cx + 145 + car.initialIndex * horizontalSpacing;
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

        // Línea de pare vertical
        ctx.fillRect(roadV.x, g.stopY, roadV.width, 4);

        // Línea de pare horizontal
        ctx.fillRect(g.stopX, roadH.y, 4, roadH.height);

        ctx.shadowBlur = 0;

        ctx.strokeStyle = "rgba(255, 107, 107, 0.45)";
        ctx.lineWidth = 1;
        ctx.setLineDash([6, 6]);

        ctx.strokeRect(g.cx - 110, g.stopY, 220, h - g.stopY - 36);
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
        drawRoundedRect(x, y, 140, 30, 10, "rgba(2,10,18,0.92)", "rgba(125,255,240,0.45)");

        ctx.fillStyle = "#1EF0B2";
        ctx.beginPath();
        ctx.arc(x + 14, y + 15, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#EAF6FF";
        ctx.font = "12px Arial";
        ctx.fillText(text, x + 25, y + 19);
    }}

    function drawSensors(w, h, t) {{
        const g = getRoadGeometry(w, h);

        ctx.strokeStyle = "rgba(30,240,178,0.35)";
        ctx.lineWidth = 2;

        ctx.beginPath();
        ctx.arc(g.cx - 390, g.cy + 45, 38 + Math.sin(t / 300) * 8, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = "rgba(0,190,255,0.10)";
        ctx.beginPath();
        ctx.moveTo(g.cx + 520, g.cy - 115);
        ctx.lineTo(g.cx + 220, g.cy - 25);
        ctx.lineTo(g.cx + 220, g.cy + 45);
        ctx.lineTo(g.cx + 520, g.cy + 10);
        ctx.closePath();
        ctx.fill();

        drawRoundedRect(g.cx - 90, g.cy + 80, 74, 36, 10, "rgba(30,240,178,0.02)", "rgba(30,240,178,0.75)");

        drawSensorLabel(g.cx - 500, g.cy + 20, "Radar Doppler");
        drawSensorLabel(g.cx + 345, g.cy - 130, "Cámara IA");
        drawSensorLabel(g.cx - 120, g.cy + 50, "Espira inductiva");
    }}

    function drawCarBody(x, y, w, h, color) {{
        drawRoundedRect(x, y, w, h, 8, color, "rgba(10,14,18,0.75)");

        // Dos ventanas internas
        drawRoundedRect(x + 9, y + 6, 15, 6, 2, "rgba(32,39,46,0.92)", null);
        drawRoundedRect(x + w - 24, y + 6, 15, 6, 2, "rgba(32,39,46,0.92)", null);
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

        /*
           Para autos hacia arriba, adelante es menor yPx.
        */
        laneCars.sort((a, b) => a.yPx - b.yPx);

        for (let i = 0; i < laneCars.length; i++) {{
            const car = laneCars[i];

            const frontY = car.yPx - carW / 2;
            const rearY = car.yPx + carW / 2;

            /*
               El auto ya empezó a cruzar la línea de pare.
               Debe seguir hasta salir; nunca se debe quedar montado.
            */
            const alreadyEntered = frontY < g.stopY;

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

            /*
               Evita que se monten con el auto de adelante.
            */
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

        /*
           Para autos hacia la izquierda, adelante es menor xPx.
        */
        laneCars.sort((a, b) => a.xPx - b.xPx);

        for (let i = 0; i < laneCars.length; i++) {{
            const car = laneCars[i];

            const frontX = car.xPx - carW / 2;
            const rearX = car.xPx + carW / 2;

            /*
               Si ya cruzó la línea de pare, sigue saliendo.
               No se detiene en la intersección.
            */
            const alreadyEntered = frontX < g.stopX;

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

            /*
               Más separación horizontal para evitar que se monten.
            */
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

        /*
           Semáforo vertical: abajo.
           Semáforo horizontal: mantiene su X original, solo está más arriba.
        */
        const verticalLightX = g.cx + g.roadWidth / 2 - 85;
        const verticalLightY = g.cy + g.roadWidth / 2 - 15;

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

    components.html(scada_html, height=760, scrolling=False)