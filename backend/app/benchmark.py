from __future__ import annotations

import time

import numpy as np

from app.detectors.registry import DetectorRegistry
from app.models import DetectionRun, FaceBox


def run_detector(detector, image: np.ndarray, confidence: float) -> DetectionRun:
    started = time.perf_counter()
    faces = detector.detect(image, confidence)
    latency_ms = (time.perf_counter() - started) * 1000
    return DetectionRun(detector.label, tuple(faces), latency_ms)


def benchmark_detectors(
    registry: DetectorRegistry, image: np.ndarray, confidence: float
) -> list[dict]:
    runs: list[DetectionRun] = []
    for detector in registry.all():
        if not detector.available:
            runs.append(
                DetectionRun(
                    detector.label,
                    (),
                    0,
                    False,
                    detector.unavailable_reason,
                )
            )
            continue
        try:
            runs.append(run_detector(detector, image, confidence))
        except Exception as exc:
            runs.append(DetectionRun(detector.label, (), 0, False, str(exc)))

    consensus = _consensus_count(runs)
    rows = []
    for run in runs:
        row = run.to_dict()
        row["agreement"] = (
            round(1 - abs(len(run.faces) - consensus) / max(consensus, 1), 2)
            if run.available
            else 0
        )
        row["precision"] = None
        row["recall"] = None
        row["evaluation_note"] = "Needs labelled ground truth"
        rows.append(row)
    return rows


def intersection_over_union(first: FaceBox, second: FaceBox) -> float:
    x1, y1 = max(first.x, second.x), max(first.y, second.y)
    x2, y2 = min(first.x2, second.x2), min(first.y2, second.y2)
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    union = first.width * first.height + second.width * second.height - intersection
    return intersection / union if union else 0.0


def precision_recall(
    predictions: list[FaceBox], ground_truth: list[FaceBox], iou_threshold: float = 0.5
) -> tuple[float, float]:
    unmatched = set(range(len(ground_truth)))
    true_positives = 0
    for prediction in sorted(predictions, key=lambda box: box.confidence, reverse=True):
        candidates = [(intersection_over_union(prediction, ground_truth[index]), index) for index in unmatched]
        if not candidates:
            continue
        best_iou, best_index = max(candidates)
        if best_iou >= iou_threshold:
            true_positives += 1
            unmatched.remove(best_index)
    precision = true_positives / len(predictions) if predictions else 0.0
    recall = true_positives / len(ground_truth) if ground_truth else 0.0
    return precision, recall


def _consensus_count(runs: list[DetectionRun]) -> int:
    counts = sorted(len(run.faces) for run in runs if run.available)
    if not counts:
        return 0
    return counts[len(counts) // 2]
