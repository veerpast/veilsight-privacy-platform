from __future__ import annotations

import tempfile
import os
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.responses import FileResponse

from app.anonymization import METHODS, anonymize_faces
from app.analytics import frame_insights
from app.benchmark import benchmark_detectors, run_detector
from app.detectors import DetectorRegistry
from app.media import decode_image, encode_jpeg_data_url
from app.video import anonymize_video, remove_work_directory

app = FastAPI(
    title="VeilSight API",
    version="0.1.0",
    description="Local-first face detection, anonymization, and honest benchmarking.",
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        max_bytes = int(os.getenv("VEILSIGHT_MAX_UPLOAD_BYTES", str(25 * 1024 * 1024)))
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > max_bytes:
            return JSONResponse({"detail": "Upload exceeds the configured 25 MB limit."}, status_code=413)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("VEILSIGHT_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["X-VeilSight-Metrics"],
)

registry = DetectorRegistry()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "storage": "none", "detectors": registry.status()}


@app.get("/api/detectors")
def detectors() -> dict:
    return {"detectors": registry.status(), "anonymization_methods": sorted(METHODS)}


@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    detector: str = Form("haar"),
    anonymization: str = Form("blur"),
    confidence: float = Form(0.55),
    intensity: float = Form(0.72),
) -> dict:
    try:
        image = decode_image(await file.read())
        selected = registry.get(detector)
        run = run_detector(selected, image, confidence)
        protected = anonymize_faces(image, run.faces, anonymization, intensity)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "original": encode_jpeg_data_url(image),
        "protected": encode_jpeg_data_url(protected),
        "run": run.to_dict(),
        "privacy": {
            "stored": False,
            "faces_anonymized": len(run.faces),
            "method": anonymization,
        },
        "insights": frame_insights(run.faces, image.shape[1], image.shape[0]),
    }


@app.post("/api/benchmark")
async def benchmark(file: UploadFile = File(...), confidence: float = Form(0.55)) -> dict:
    try:
        image = decode_image(await file.read())
        rows = benchmark_detectors(registry, image, confidence)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"rows": rows, "stored": False}


@app.post("/api/analyze/video", response_class=FileResponse)
async def analyze_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    detector: str = Form("haar"),
    anonymization: str = Form("blur"),
    confidence: float = Form(0.55),
    intensity: float = Form(0.72),
):
    import json

    work_dir = Path(tempfile.mkdtemp(prefix="veilsight-"))
    suffix = Path(file.filename or "input.mp4").suffix.lower()
    if suffix not in {".mp4", ".mov", ".avi", ".m4v"}:
        remove_work_directory(work_dir)
        raise HTTPException(status_code=400, detail="Use MP4, MOV, AVI or M4V video.")
    source, destination = work_dir / f"input{suffix}", work_dir / "protected.mp4"
    size = 0
    try:
        with source.open("wb") as stream:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > 200 * 1024 * 1024:
                    raise ValueError("Videos are limited to 200 MB.")
                stream.write(chunk)
        selected = registry.get(detector)
        metrics = anonymize_video(source, destination, selected, anonymization, confidence, intensity)
    except (ValueError, RuntimeError) as exc:
        remove_work_directory(work_dir)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    background_tasks.add_task(remove_work_directory, work_dir)
    return FileResponse(
        destination,
        media_type="video/mp4",
        filename="veilsight-protected.mp4",
        headers={"X-VeilSight-Metrics": json.dumps(metrics, separators=(",", ":"))},
        background=background_tasks,
    )
