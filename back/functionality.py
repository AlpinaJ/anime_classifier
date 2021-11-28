from tensorflow import keras
import numpy as np


class Model:
    def __init__(self, model_path, classes_path):
        self.model = keras.models.load_model(model_path)
        self.class_names = []
        with open(classes_path) as file:
            for line in file.readlines():
                self.class_names.append(line[4:-1])

    def predict(self, img):
        to_predict = np.zeros((1, 128, 128, 3))
        to_predict[0] = img
        prediction = self.model.predict(to_predict)
        class_idx = np.argmax(prediction)
        return self.class_names[class_idx]
