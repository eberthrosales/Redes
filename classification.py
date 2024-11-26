import joblib

MODEL_PATH = "model/device_classifier.pkl"

def load_model():
    """Carga el modelo de clasificación preentrenado."""
    return joblib.load(MODEL_PATH)

def classify_devices(devices):
    """Clasifica dispositivos basándose en sus características."""
    model = load_model()
    data = []
    for device in devices:
        features = [
            len(device['mac']),  # Longitud de la MAC
            hash(device['vendor']) % 10,  # Fabricante reducido a un hash
            hash(device['os']) % 10  # Sistema operativo reducido a un hash
        ]
        category = model.predict([features])[0]
        data.append({
            'IP': device['ip'],
            'MAC': device['mac'],
            'Fabricante': device['vendor'],
            'Sistema Operativo': device['os'],
            'Host': device['host'],
            'Categoría': category
        })
    return data
