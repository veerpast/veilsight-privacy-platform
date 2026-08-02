# Architecture decisions

## Detector boundary

Every detector converts vendor output into `FaceBox`. This keeps model installation, confidence conventions and tensor libraries out of anonymization and evaluation code.

## Local-first API

The browser talks to a local FastAPI service. An image returns two data URLs and metrics. Video returns a generated MP4, then its temporary work directory is deleted by a response background task.

## Honest benchmark semantics

Runtime measurements need no labels. Accuracy does. The application therefore distinguishes detector agreement from precision/recall instead of presenting agreement as a substitute for correctness.

## Why React instead of a notebook UI

The notebook remains useful for exploratory analysis. React provides clearer state, responsive comparison, accessibility, file workflows and a recruiter-friendly product surface. The Python pipeline remains independently testable.
