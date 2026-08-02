from __future__ import annotations

import cv2
import numpy as np

from app.detectors.base import FaceDetector
from app.models import FaceBox


class HaarFaceDetector(FaceDetector):
    key = "haar"
    label = "OpenCV Haar"

    def __init__(self) -> None:
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self._cascade = cv2.CascadeClassifier(cascade_path)
        if self._cascade.empty():
            raise RuntimeError(f"Could not load Haar cascade from {cascade_path}")

    def detect(self, image: np.ndarray, confidence: float) -> list[FaceBox]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        # Haar does not expose calibrated probabilities. The UI names this
        # sensitivity for Haar and maps it to minNeighbors.
        min_neighbors = max(3, min(8, round(9 - confidence * 6)))
        minimum_face = max(36, round(min(image.shape[:2]) * 0.075))
        rects = self._cascade.detectMultiScale(
            gray,
            scaleFactor=1.08,
            minNeighbors=min_neighbors,
            minSize=(minimum_face, minimum_face),
        )
        return [FaceBox(int(x), int(y), int(w), int(h), 1.0) for x, y, w, h in rects]
