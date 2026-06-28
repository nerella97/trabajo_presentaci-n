import pandas as pd


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df_limpio = df.copy()
    numeric_cols = df_limpio.select_dtypes(include="number").columns

    for col in numeric_cols:
        df_limpio[col] = df_limpio[col].fillna(df_limpio[col].mean())

    return df_limpio


def get_all_data():
    horas = [
        "08:00", "08:05", "08:10", "08:15", "08:20",
        "08:25", "08:30", "08:35", "08:40", "08:45",
        "08:50", "08:55", "09:00", "09:05", "09:10",
    ]

    # df_radar: incluye velocidad_promedio (variable clave) y columnas adicionales
    # velocidad_maxima de la fila 6 es None para demostrar imputación en limpieza
    df_radar_raw = pd.DataFrame({
        "fecha_hora":        horas,
        "id_sensor":         [f"RD-{1000 + i}" for i in range(15)],
        "velocidad_promedio":[12, 35, 50, 14, 28, 45, 11, 32, 48, 13, 25, 52, 10, 38, 55],
        "velocidad_maxima":  [18, 45, 65, 20, 38, 58, None, 42, 60, 19, 35, 68, 15, 50, 70],
        "velocidad_minima":  [ 8, 28, 40,  9, 20, 35,   7, 24, 38,  8, 18, 42,  6, 30, 45],
        "unidad":            ["km/h"] * 15,
        "estado_sensor":     ["OK"] * 15,
    })

    # df_espira: incluye flujo_vehicular (variable clave) y columnas adicionales
    # ocupacion_carril de la fila 10 es None para demostrar imputación en limpieza
    df_espira_raw = pd.DataFrame({
        "fecha_hora":        horas,
        "id_sensor":         [f"EI-{1000 + i}" for i in range(15)],
        "flujo_vehicular":   [62, 38, 18, 65, 42, 20, 68, 35, 15, 60, 45, 12, 70, 30, 10],
        "ocupacion_carril":  [88, 55, 30, 90, 60, 28, 92, 52, 25, 85, None, 22, 94, 48, 18],
        "vehiculos_livianos":[48, 28, 14, 50, 32, 15, 52, 27, 11, 46, 34,  9, 54, 23,  8],
        "vehiculos_pesados": [14, 10,  4, 15, 10,  5, 16,  8,  4, 14, 11,  3, 16,  7,  2],
        "unidad":            ["veh/min"] * 15,
        "estado_sensor":     ["OK"] * 15,
    })

    # df_camara: incluye longitud_cola (variable clave) y columnas adicionales
    # peatones_detectados de la fila 8 es None para demostrar imputación en limpieza
    df_camara_raw = pd.DataFrame({
        "fecha_hora":           horas,
        "id_sensor":            [f"CAM-{1000 + i}" for i in range(15)],
        "longitud_cola":        [28, 14, 5, 32, 16, 6, 35, 12, 4, 25, 18, 3, 40, 10, 2],
        "vehiculos_detectados": [72, 52, 28, 76, 56, 30, 80, 48, 24, 68, 60, 20, 85, 42, 18],
        "vehiculos_detenidos":  [35, 18,  5, 40, 20,  6, 42, 15,  4, 30, 22,  3, 48, 12,  2],
        "peatones_detectados":  [ 3,  2,  1,  4,  3,  1,  5,  2, None, 3,  2,  0,  6,  2,  1],
        "incidentes":           [ 0,  0,  0,  1,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0],
        "unidad":               ["m"] * 15,
        "estado_sensor":        ["OK"] * 15,
    })

    df_radar  = limpiar_datos(df_radar_raw)
    df_espira = limpiar_datos(df_espira_raw)
    df_camara = limpiar_datos(df_camara_raw)

    df_velocidad = df_radar[["fecha_hora", "velocidad_promedio"]]
    df_flujo     = df_espira[["fecha_hora", "flujo_vehicular"]]
    df_cola      = df_camara[["fecha_hora", "longitud_cola"]]

    df_entrenamiento_ia = (
        df_velocidad
        .merge(df_flujo, on="fecha_hora")
        .merge(df_cola, on="fecha_hora")
    )

    # 5 registros ALTA · 5 MEDIA · 5 BAJA — balanceado para el árbol de decisión
    df_entrenamiento_ia["nivel_congestion"] = [
        "ALTA",  "MEDIA", "BAJA",
        "ALTA",  "MEDIA", "BAJA",
        "ALTA",  "MEDIA", "BAJA",
        "ALTA",  "MEDIA", "BAJA",
        "ALTA",  "MEDIA", "BAJA",
    ]

    return {
        "df_radar_raw":       df_radar_raw,
        "df_espira_raw":      df_espira_raw,
        "df_camara_raw":      df_camara_raw,
        "df_radar":           df_radar,
        "df_espira":          df_espira,
        "df_camara":          df_camara,
        "df_velocidad":       df_velocidad,
        "df_flujo":           df_flujo,
        "df_cola":            df_cola,
        "df_entrenamiento_ia": df_entrenamiento_ia,
    }
