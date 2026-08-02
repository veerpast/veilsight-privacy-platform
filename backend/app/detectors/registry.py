from __future__ import annotations

from app.detectors.base import FaceDetector
from app.detectors.haar import HaarFaceDetector
from collections.abc import Callable


class DetectorRegistry:
    def __init__(self) -> None:
        # Optional runtimes are intentionally lazy: importing MediaPipe and
        # Ultralytics can take tens of seconds on a small Render instance.
        # Keeping them out of process startup makes /api/health reliable while
        # still loading the real detector when a request selects it.
        self._detectors: dict[str, FaceDetector | None] = {
            "haar": HaarFaceDetector(),
            "mediapipe": None,
            "yolo": None,
        }
        self._factories: dict[str, Callable[[], FaceDetector]] = {
            # Import heavyweight runtimes only when a request selects them.
            "mediapipe": lambda: __import__(
                "app.detectors.mediapipe_detector", fromlist=["MediaPipeFaceDetector"]
            ).MediaPipeFaceDetector(),
            "yolo": lambda: __import__(
                "app.detectors.yolo_detector", fromlist=["YoloFaceDetector"]
            ).YoloFaceDetector(),
        }

    def _load(self, key: str) -> FaceDetector:
        detector = self._detectors.get(key)
        if detector is None:
            factory = self._factories.get(key)
            if factory is None:
                raise ValueError(f"Unknown detector: {key}")
            detector = factory()
            self._detectors[key] = detector
        return detector

    def get(self, key: str) -> FaceDetector:
        try:
            detector = self._load(key)
        except KeyError as exc:
            raise ValueError(f"Unknown detector: {key}") from exc
        if not detector.available:
            raise RuntimeError(detector.unavailable_reason)
        return detector

    def status(self) -> list[dict[str, str | bool]]:
        labels = {"haar": "OpenCV Haar", "mediapipe": "MediaPipe", "yolo": "YOLO Face"}
        rows: list[dict[str, str | bool]] = []
        for key, detector in self._detectors.items():
            if detector is None:
                rows.append({
                    "key": key,
                    "label": labels[key],
                    "available": True,
                    "reason": "Ready on first use (lazy-loaded).",
                })
            else:
                rows.append({
                    "key": detector.key,
                    "label": detector.label,
                    "available": detector.available,
                    "reason": detector.unavailable_reason,
                })
        return rows

    def available(self) -> list[FaceDetector]:
        return [self._load(key) for key in self._detectors if self._load(key).available]

    def all(self) -> list[FaceDetector]:
        return [self._load(key) for key in self._detectors]
