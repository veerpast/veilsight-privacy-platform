# Four-minute walkthrough script

## 0:00 — The problem

“Most face-detection tutorials stop when a rectangle appears. I wanted to ask the next question: what should happen to the person inside that rectangle?”

Show the repository and open Privacy Studio.

## 0:25 — The human workflow

Upload a consented image. Change the detector and protection method. Explain that Haar is the zero-setup baseline while MediaPipe and YOLO are explicit optional integrations.

Run the analysis and compare original with protected output. Point out the solid-mask option and the warning that blur is not a guarantee of anonymity.

## 1:20 — Engineering structure

Show `backend/app/detectors/`. Explain the shared `FaceBox` boundary and why it prevents vendor-specific model objects from leaking across the codebase.

Show the anonymization function and one clipping/non-mutation test.

## 2:05 — Benchmark honesty

Run the benchmark. Explain latency, FPS and agreement. Then say: “You’ll notice precision and recall are not magically populated. Those require labelled ground truth, and the project refuses to manufacture them.”

Show the IoU matching test and evaluation document.

## 2:50 — Privacy design

Open the About screen. Explain stateless image processing, temporary video cleanup, media-free browser reports, and the explicit threats that remain.

## 3:25 — What I would research next

Discuss low-light and occlusion slices, temporal tracking without unprotected frames, and ONNX/hardware benchmarking.

## 3:50 — Close

“VeilSight is not a claim that face anonymization is solved. It is an example of how I approach AI engineering: build the useful system, measure it honestly, and make the limitations visible.”
