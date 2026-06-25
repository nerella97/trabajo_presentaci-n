import pandas as pd


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df_limpio = df.copy()
    numeric_cols = df_limpio.select_dtypes(include="number").columns

    for col in numeric_cols:
        df_limpio[col] = df_limpio[col].fillna(df_limpio[col].mean())

    return df_limpio


def get_all_data():
    df_radar_raw = pd.DataFrame({
        "fecha_hora": ["08:00", "08:05", "08:10", "08:15"],
        "velocidad_promedio": [12, 15, 11, None],
        "velocidad_maxima": [18, 20, 17, 19],
        "velocidad_minima": [8, 10, 7, 9],
        "estado_sensor": ["OK", "OK", "OK", "OK"]
    })

    df_espira_raw = pd.DataFrame({
        "fecha_hora": ["08:00", "08:05", "08:10", "08:15"],
        "flujo_vehicular": [60, 55, 58, 62],
        "ocupacion_carril": [85, 80, 88, None],
        "vehiculos_livianos": [45, 42, 44, 46],
        "estado_sensor": ["OK", "OK", "OK", "OK"]
    })

    df_camara_raw = pd.DataFrame({
        "fecha_hora": ["08:00", "08:05", "08:10", "08:15"],
        "longitud_cola": [25, 22, 24, 26],
        "vehiculos_detectados": [70, 65, 68, 72],
        "incidentes": [0, 0, 1, 0],
        "estado_sensor": ["OK", "OK", "OK", "OK"]
    })

    df_radar = limpiar_datos(df_radar_raw)
    df_espira = limpiar_datos(df_espira_raw)
    df_camara = limpiar_datos(df_camara_raw)

    df_velocidad = df_radar[["fecha_hora", "velocidad_promedio"]]
    df_flujo = df_espira[["fecha_hora", "flujo_vehicular"]]
    df_cola = df_camara[["fecha_hora", "longitud_cola"]]

    df_entrenamiento_ia = (
        df_velocidad
        .merge(df_flujo, on="fecha_hora")
        .merge(df_cola, on="fecha_hora")
    )

    df_entrenamiento_ia["nivel_congestion"] = [
        "ALTA", "MEDIA", "ALTA", "ALTA"
    ]

    return {
        "df_radar_raw": df_radar_raw,
        "df_espira_raw": df_espira_raw,
        "df_camara_raw": df_camara_raw,
        "df_radar": df_radar,
        "df_espira": df_espira,
        "df_camara": df_camara,
        "df_velocidad": df_velocidad,
        "df_flujo": df_flujo,
        "df_cola": df_cola,
        "df_entrenamiento_ia": df_entrenamiento_ia,
    }