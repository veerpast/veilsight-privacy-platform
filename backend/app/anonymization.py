from __future__ import annotations

import cv2
import numpy as np

from app.models import FaceBox


METHODS = {"blur", "pixelate", "solid"}


def anonymize_faces(
    image: np.ndarray,
    faces: list[FaceBox] | tuple[FaceBox, ...],
    method: str = "blur",
    intensity: float = 0.72,
) -> np.ndarray:
    """Return a copy with every supplied face region protected."""
    if method not in METHODS:
        raise ValueError(f"Unknown anonymization method: {method}")
    intensity = float(min(max(intensity, 0.05), 1.0))
    output = image.copy()
    image_height, image_width = output.shape[:2]

    for face in faces:
        box = face.clipped(image_width, image_height)
        if box.width < 2 or box.height < 2:
            continue
        region = output[box.y : box.y2, box.x : box.x2]

        if method == "blur":
            base = max(7, round(min(box.width, box.height) * (0.08 + intensity * 0.3)))
            kernel = base if base % 2 == 1 else base + 1
            protected = cv2.GaussianBlur(region, (kernel, kernel), 0)
        elif method == "pixelate":
            blocks = max(3, round(18 - intensity * 14))
            tiny = cv2.resize(region, (blocks, blocks), interpolation=cv2.INTER_LINEAR)
            protected = cv2.resize(tiny, (box.width, box.height), interpolation=cv2.INTER_NEAREST)
        else:
            protected = np.full_like(region, (15, 35, 59))

        output[box.y : box.y2, box.x : box.x2] = protected

    return output
