from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from app.models import FaceBox


class FaceDetector(ABC):
    key: str
    label: str

    @property
    def available(self) -> bool:
        return True

    @property
    def unavailable_reason(self) -> str:
        return ""

    @abstractmethod
    def detect(self, image: np.ndarray, confidence: float) -> list[FaceBox]:
        raise NotImplementedError
