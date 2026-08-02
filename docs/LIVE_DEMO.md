# Live demo guide

## Start

From the repository root:

```bash
make setup-full       # first run only
./scripts/start_demo.sh
```

Open `http://127.0.0.1:5173`. The API health page is at
`http://127.0.0.1:8000/api/health`.

## Five-minute walkthrough

1. Start on **Privacy Studio** and explain that the use case is privacy-safe
   occupancy and queue analytics for a clinic, campus, or public-service desk.
2. Upload a consented image, choose **YOLO Face**, and run the analysis.
3. Compare the original and protected outputs. Point out that source media is
   processed locally and not stored.
4. Show the operational insight cards: occupancy proxy, queue signal, and
   privacy coverage. Clarify that this is not identity recognition or a true
   person count.
5. Open **Benchmarks** and compare Haar, MediaPipe, and YOLO latency and face
   counts. Agreement is a diagnostic; labelled data is required for accuracy.
6. Open **About** or the README to explain the threat model and limitations.

## Interview explanation

The backend is FastAPI. A detector registry normalizes OpenCV, MediaPipe, and
YOLO outputs into `FaceBox` objects. An anonymization layer applies blur,
pixelation, or a solid mask. The video pipeline uses temporary files and drops
audio. The React/Vite frontend is a thin client over these API boundaries.

The engineering contribution is the privacy-by-design evaluation loop: detect,
protect, measure latency/agreement, and return only aggregate operational
signals. It avoids face recognition, embeddings, identity labels, and tracking.
