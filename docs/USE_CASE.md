# Applied use case: privacy-preserving space analytics

## Problem

Clinics, universities, and public-service teams often need to know whether a
reception area is becoming crowded or whether a queue needs another desk. The
obvious solution—send camera footage to a cloud dashboard—creates unnecessary
privacy, retention, and cross-border data risks.

## VeilSight's answer

The local pipeline detects visible faces, immediately anonymizes them, and
returns only a protected image/video plus aggregate signals:

- face-visible occupancy band (`low`, `moderate`, `high`);
- a conservative possible-queue signal;
- detector latency and agreement for quality assurance;
- privacy coverage and an explicit “no identity/tracking” interpretation.

These are decision-support signals, not identity or person-count claims. A
production deployment should calibrate thresholds with labelled, consented
data and a site-specific review process.

## Why this is a strong engineering project

It combines edge inference, model benchmarking, privacy-by-design, API
engineering, reproducible evaluation, and human review. The resulting demo can
answer a professor's “what problem does this solve?” question while giving a
recruiter concrete evidence of model trade-offs, failure handling, and data
governance.
