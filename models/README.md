# Optional local models

VeilSight works immediately with OpenCV Haar. Model weights are intentionally not committed because they are large and may have different licence terms.

## MediaPipe

Install the full detector stack in the same environment as the API:

```bash
make setup-full
```

The adapter uses MediaPipe's local face detector. The included
`blaze_face_short_range.tflite` asset is loaded locally; no media is sent to Google.
The implementation prefers the current Tasks API and falls back to the 0.10.x
Solutions API for compatibility.

On some macOS/Apple Silicon combinations the MediaPipe wheel cannot create its
OpenGL service even when CPU inference is requested. VeilSight reports that
detector as unavailable instead of taking down the API; run the same setup in a
Linux container/CI runner for a production MediaPipe benchmark, or keep Haar
and YOLO enabled locally.

## YOLO Face

1. Choose a face-specific Ultralytics-compatible model from a source you trust.
2. Review its training data, licence, and limitations.
3. Place the weight at `models/yolov11n-face.pt`, or set `VEILSIGHT_YOLO_MODEL` to another local path. The repository's setup uses the nano YOLO11 face weight from the community `yolo-face` release; review its licence and provenance before commercial use.
4. Install `ultralytics` in the API environment (included in `make setup-full`).

```bash
pip install ultralytics
```

VeilSight does not automatically download an arbitrary community weight. That friction is intentional: a portfolio should be able to explain where its model came from.
