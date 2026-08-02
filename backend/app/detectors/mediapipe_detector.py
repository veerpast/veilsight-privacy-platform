from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from app.detectors.base import FaceDetector
from app.models import FaceBox


class MediaPipeFaceDetector(FaceDetector):
    """MediaPipe Tasks face detector, forced to CPU for portable server runs.

    MediaPipe 1.x removed the old ``mp.solutions`` namespace.  The Tasks API
    also avoids silently requesting Metal/GPU acceleration on machines where
    the graph service is not available (a common macOS crash mode).
    """

    key = "mediapipe"
    label = "MediaPipe"

    def __init__(self) -> None:
        self._detector = None
        self._reason = ""
        self._legacy = False
        default_model = Path(__file__).resolve().parents[3] / "models" / "blaze_face_short_range.tflite"
        model_path = Path(os.getenv("VEILSIGHT_MEDIAPIPE_MODEL", str(default_model)))
        try:
            import mediapipe as mp
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision

            if not model_path.exists():
                self._reason = f"Model not found at {model_path}. See models/README.md."
                return
            options = vision.FaceDetectorOptions(
                base_options=python.BaseOptions(
                    model_asset_path=str(model_path),
                    delegate=python.BaseOptions.Delegate.CPU,
                ),
                min_detection_confidence=0.25,
                running_mode=vision.RunningMode.IMAGE,
            )
            self._mp = mp
            self._detector = vision.FaceDetector.create_from_options(options)
        except Exception as exc:  # optional dependency or model setup
            # 0.10.x still ships the Solutions API. Keep it as a compatibility
            # fallback so a student can run the project on older wheels.
            try:
                import mediapipe as mp
                self._detector = mp.solutions.face_detection.FaceDetection(
                    model_selection=0,
                    min_detection_confidence=0.25,
                )
                self._mp = mp
                self._legacy = True
                return
            except Exception as legacy_exc:
                self._reason = f"MediaPipe is not configured ({type(legacy_exc).__name__}: {legacy_exc})."

    @property
    def available(self) -> bool:
        return self._detector is not None

    @property
    def unavailable_reason(self) -> str:
        return self._reason

    def detect(self, image: np.ndarray, confidence: float) -> list[FaceBox]:
        if self._detector is None:
            raise RuntimeError(self._reason)

        import cv2

        height, width = image.shape[:2]
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if getattr(self, "_legacy", False):
            result = self._detector.process(rgb)
            faces: list[FaceBox] = []
            for detection in result.detections or []:
                score = float(detection.score[0])
                if score < confidence:
                    continue
                box = detection.location_data.relative_bounding_box
                faces.append(FaceBox(round(box.xmin * width), round(box.ymin * height), round(box.width * width), round(box.height * height), score).clipped(width, height))
            return faces

        result = self._detector.detect(self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=rgb))
        faces: list[FaceBox] = []
        for detection in result.detections:
            score = float(detection.categories[0].score) if detection.categories else 0.0
            if score < confidence:
                continue
            box = detection.bounding_box
            faces.append(FaceBox(box.origin_x, box.origin_y, box.width, box.height, score).clipped(width, height))
        return faces

    def __del__(self) -> None:
        detector = getattr(self, "_detector", None)
        if detector is not None:
            try:
                detector.close()
            except Exception:
                pass
