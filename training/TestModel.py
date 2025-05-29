import numpy as np
import csv
from tensorflow.keras.models import load_model
from training.FormatData import FormatData

class TestModel:
    def __init__(self, modelPath):
        self.modelGesture = load_model(modelPath)
        self.formatData = FormatData()

    def read_csv(self, filepath):
        coords = []
        with open(filepath, newline='') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader, start=1):
                if len(row) != 63:
                    raise ValueError(f"Fila {i}: longitud {len(row)} encontrada, se esperaban 63 columnas.")
                coords.append([float(x) for x in row])
        if len(coords) != 30:
            raise ValueError(f"Se esperaban 30 filas, pero el archivo tiene {len(coords)}.")
        return coords

    def test_model_LSTM(self, coords_list):
        arr = np.array(coords_list)          # shape (30, 63)
        seq = arr[None, ...]                # shape (1, 30, 63)
        prob = float(self.modelGesture.predict(seq, verbose=0)[0, 0])
        print(f"Probabilidad de gesto: {prob:.3f}")

if __name__ == '__main__':
    model_path = ''
    test_model = TestModel(model_path)

    # Read the CSV file
    coords_list = test_model.read_csv('')

    # Test the model with the read coordinates
    test_model.test_model_LSTM(coords_list)
