from __future__ import annotations

from collections.abc import Sequence

from app.models import FaceBox


def frame_insights(faces: Sequence[FaceBox], width: int, height: int) -> dict:
    """Return privacy-safe operational signals; never stores or identifies people."""
    count = len(faces)
    image_area = max(width * height, 1)
    covered = sum(face.width * face.height for face in faces) / image_area
    band = "low" if count <= 2 else "moderate" if count <= 6 else "high"
    centers = sorted(face.x + face.width / 2 for face in faces)
    queue_signal = "clear"
    if count >= 4 and centers and (centers[-1] - centers[0]) < width * 0.42:
        queue_signal = "possible queue"
    elif count >= 7:
        queue_signal = "review capacity"
    return {
        "occupancy_count": count,
        "occupancy_band": band,
        "face_area_ratio": round(covered, 4),
        "queue_signal": queue_signal,
        "privacy_coverage": 1.0 if count else 0.0,
        "interpretation": "Face-visible occupancy proxy; no identity, tracking, or biometric matching.",
    }
