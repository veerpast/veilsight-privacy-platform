from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from app.detectors.base import FaceDetector
from app.models import FaceBox


class YoloFaceDetector(FaceDetector):
    key = "yolo"
    label = "YOLO Face"

    def __init__(self) -> None:
        self._model = None
        self._reason = ""
        model_path = Path(os.getenv("VEILSIGHT_YOLO_MODEL", "models/yolov11n-face.pt"))
        try:
            from ultralytics import YOLO

            if not model_path.exists():
                self._reason = f"Model not found at {model_path}. See models/README.md."
                return
            self._model = YOLO(str(model_path))
        except Exception as exc:  # optional dependency or incompatible weight
            self._reason = f"YOLO Face is not configured ({type(exc).__name__}: {exc})."

    @property
    def available(self) -> bool:
        return self._model is not None

    @property
    def unavailable_reason(self) -> str:
        return self._reason

    def detect(self, image: np.ndarray, confidence: float) -> list[FaceBox]:
        if self._model is None:
            raise RuntimeError(self._reason)
        result = self._model.predict(image, conf=confidence, verbose=False)[0]
        faces: list[FaceBox] = []
        if result.boxes is None:
            return faces
        for xyxy, score in zip(result.boxes.xyxy.cpu().numpy(), result.boxes.conf.cpu().numpy()):
            x1, y1, x2, y2 = (int(value) for value in xyxy)
            faces.append(FaceBox(x1, y1, x2 - x1, y2 - y1, float(score)))
        return faces
