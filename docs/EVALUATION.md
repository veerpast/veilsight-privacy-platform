# Evaluation plan

## Measurements

- **Precision / recall:** IoU ≥ 0.5 matching against labelled face boxes.
- **Latency:** detector wall-clock time per image or frame.
- **Throughput:** `1000 / latency_ms`, reported as an indicative FPS.
- **Agreement:** similarity between a detector's face count and the median available detector count. This is not accuracy.
- **Coverage:** slices for lighting, pose, scale, occlusion and image quality.

## Dataset protocol

Create train-free evaluation subsets with documented consent and licences. Do not tune thresholds on the final test subset. Report sample count, hardware, versions, warm-up policy, input resolution, confidence threshold and error bars.

Suggested slice sheet:

| Slice | Minimum examples | Question |
|---|---:|---|
| Frontal daylight | 100 | Clean-condition ceiling |
| Profile / 3⁄4 pose | 100 | Pose robustness |
| Low light | 100 | Sensor and illumination failure |
| Partial occlusion | 100 | Masks, hands, glasses |
| Small faces | 100 | Distance and group scenes |

## Error analysis

Save only consented evaluation crops. Review false negatives before false positives because a missed face is a privacy failure. Include representative errors in the final report rather than only aggregate metrics.
