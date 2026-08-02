from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class FaceBox:
    """A detector-independent face rectangle."""

    x: int
    y: int
    width: int
    height: int
    confidence: float = 1.0

    @property
    def x2(self) -> int:
        return self.x + self.width

    @property
    def y2(self) -> int:
        return self.y + self.height

    def clipped(self, image_width: int, image_height: int) -> "FaceBox":
        x1 = min(max(self.x, 0), image_width)
        y1 = min(max(self.y, 0), image_height)
        x2 = min(max(self.x2, x1), image_width)
        y2 = min(max(self.y2, y1), image_height)
        return FaceBox(x1, y1, x2 - x1, y2 - y1, self.confidence)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DetectionRun:
    detector: str
    faces: tuple[FaceBox, ...]
    latency_ms: float
    available: bool = True
    note: str = ""

    @property
    def fps(self) -> float:
        return 1000.0 / self.latency_ms if self.latency_ms > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "detector": self.detector,
            "faces": [face.to_dict() for face in self.faces],
            "face_count": len(self.faces),
            "latency_ms": round(self.latency_ms, 2),
            "fps": round(self.fps, 1),
            "available": self.available,
            "note": self.note,
        }
