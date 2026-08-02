# Contributing

Thank you for taking the time to look closely at VeilSight.

Before opening a change, please ask one practical question: does this make the system easier to verify, safer for the people in the media, or more honest about its limitations?

## Local checks

1. Keep detector-specific code inside `backend/app/detectors/`.
2. Return the shared `FaceBox` type; do not leak vendor objects across the pipeline.
3. Add a deterministic test for privacy or evaluation changes.
4. Run `make test`.
5. Never add private media, downloaded model weights, or benchmark claims without provenance.

Small, clearly explained pull requests are easier to review than broad rewrites.
