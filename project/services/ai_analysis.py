"""AI image preprocessing and CNN-style inference module."""
import os
from typing import Dict, Tuple

import cv2
import numpy as np
import tensorflow as tf

from config import Config

DISEASE_LABELS = [
    "bacterial dermatitis",
    "fungal infection",
    "viral rash",
    "protozoan skin lesion",
]


class SkinDiseaseAnalyzer:
    """Encapsulates OpenCV preprocessing and TensorFlow model inference."""

    def __init__(self, model_path: str = None):
        self.model_path = model_path or Config.MODEL_PATH
        self.model = self._load_or_create_model()

    def _load_or_create_model(self):
        if os.path.exists(self.model_path):
            return tf.keras.models.load_model(self.model_path)

        # Lightweight CNN skeleton for demo/development usage.
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Input(shape=(128, 128, 3)),
                tf.keras.layers.Conv2D(16, 3, activation="relu"),
                tf.keras.layers.MaxPooling2D(),
                tf.keras.layers.Conv2D(32, 3, activation="relu"),
                tf.keras.layers.MaxPooling2D(),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(len(DISEASE_LABELS), activation="softmax"),
            ]
        )
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        return model

    @staticmethod
    def preprocess_image(file_path: str) -> np.ndarray:
        """OpenCV-based preprocessing pipeline."""
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError("Invalid or unreadable image file.")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.GaussianBlur(image, (3, 3), 0)
        image = cv2.resize(image, (128, 128))
        image = image.astype(np.float32) / 255.0
        tensor = np.expand_dims(image, axis=0)
        return tensor

    def predict(self, file_path: str) -> Tuple[str, float, Dict[str, float]]:
        """Run inference and return predicted disease, confidence, and probabilities."""
        tensor = self.preprocess_image(file_path)

        # Untrained fallback: combine model output with simple color heuristic.
        preds = self.model.predict(tensor, verbose=0)[0]
        if float(np.max(preds)) < 0.4:
            redness = float(np.mean(tensor[:, :, :, 0]))
            if redness > 0.55:
                preds = np.array([0.45, 0.2, 0.25, 0.1])
            else:
                preds = np.array([0.2, 0.5, 0.2, 0.1])

        best_idx = int(np.argmax(preds))
        probs = {label: float(prob) for label, prob in zip(DISEASE_LABELS, preds)}
        return DISEASE_LABELS[best_idx], float(preds[best_idx]), probs
