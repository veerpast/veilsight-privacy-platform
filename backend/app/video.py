from __future__ import annotations

import shutil
from pathlib import Path

import cv2

from app.anonymization import anonymize_faces
from app.benchmark import run_detector


def anonymize_video(
    source: Path,
    destination: Path,
    detector,
    method: str,
    confidence: float,
    intensity: float,
) -> dict[str, float | int]:
    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise ValueError("OpenCV could not open this video.")

    fps = capture.get(cv2.CAP_PROP_FPS) or 24.0
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if width <= 0 or height <= 0:
        capture.release()
        raise ValueError("The video has invalid dimensions.")

    writer = cv2.VideoWriter(
        str(destination),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not writer.isOpened():
        capture.release()
        raise RuntimeError("This OpenCV build cannot create an MP4 file.")

    processed = 0
    total_faces = 0
    total_latency = 0.0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            run = run_detector(detector, frame, confidence)
            writer.write(anonymize_faces(frame, run.faces, method, intensity))
            processed += 1
            total_faces += len(run.faces)
            total_latency += run.latency_ms
    finally:
        capture.release()
        writer.release()

    if processed == 0:
        destination.unlink(missing_ok=True)
        raise ValueError("The video did not contain readable frames.")

    return {
        "frames": processed,
        "source_frames": frame_count,
        "face_detections": total_faces,
        "average_faces_per_frame": round(total_faces / processed, 2),
        "average_detection_ms": round(total_latency / processed, 2),
        "source_fps": round(fps, 2),
    }


def remove_work_directory(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)
