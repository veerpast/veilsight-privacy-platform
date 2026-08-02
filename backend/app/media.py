from __future__ import annotations

import base64

import cv2
import numpy as np


MAX_IMAGE_BYTES = 15 * 1024 * 1024


def decode_image(data: bytes) -> np.ndarray:
    if not data:
        raise ValueError("The uploaded file is empty.")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("Images are limited to 15 MB.")
    image = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("This file is not a readable image.")
    return image


def encode_jpeg_data_url(image: np.ndarray, quality: int = 90) -> str:
    ok, encoded = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise RuntimeError("Could not encode the processed image.")
    payload = base64.b64encode(encoded.tobytes()).decode("ascii")
    return f"data:image/jpeg;base64,{payload}"
