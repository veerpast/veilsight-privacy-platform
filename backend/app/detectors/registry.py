from __future__ import annotations

from app.detectors.base import FaceDetector
from app.detectors.haar import HaarFaceDetector
from app.detectors.mediapipe_detector import MediaPipeFaceDetector
from app.detectors.yolo_detector import YoloFaceDetector


class DetectorRegistry:
    def __init__(self) -> None:
        detectors: list[FaceDetector] = [
            HaarFaceDetector(),
            MediaPipeFaceDetector(),
            YoloFaceDetector(),
        ]
        self._detectors = {detector.key: detector for detector in detectors}

    def get(self, key: str) -> FaceDetector:
        try:
            detector = self._detectors[key]
        except KeyError as exc:
            raise ValueError(f"Unknown detector: {key}") from exc
        if not detector.available:
            raise RuntimeError(detector.unavailable_reason)
        return detector

    def status(self) -> list[dict[str, str | bool]]:
        return [
            {
                "key": detector.key,
                "label": detector.label,
                "available": detector.available,
                "reason": detector.unavailable_reason,
            }
            for detector in self._detectors.values()
        ]

    def available(self) -> list[FaceDetector]:
        return [detector for detector in self._detectors.values() if detector.available]

    def all(self) -> list[FaceDetector]:
        return list(self._detectors.values())
