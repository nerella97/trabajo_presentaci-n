from sklearn.tree import DecisionTreeClassifier


def train_model(df_entrenamiento_ia):
    X = df_entrenamiento_ia[
        ["velocidad_promedio", "flujo_vehicular", "longitud_cola"]
    ]

    y = df_entrenamiento_ia["nivel_congestion"]

    modelo = DecisionTreeClassifier(random_state=42)
    modelo.fit(X, y)

    return modelo, X, y


def get_tiempo_verde(nivel_congestion: str) -> int:
    if nivel_congestion == "ALTA":
        return 40
    if nivel_congestion == "MEDIA":
        return 30
    return 20