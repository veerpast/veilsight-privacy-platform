# Privacy and threat model

## Promise

VeilSight is designed to process media for one request and then forget it.

- Image bytes remain in memory for the duration of the request.
- Video input and output use a randomly named temporary directory.
- Protected video exports intentionally contain no audio track.
- That directory is removed after the response completes.
- The API has no database and emits no source images to application logs.
- Browser reports contain metrics only.

## What anonymization does not hide

A protected face does not remove voice, tattoos, clothing, gait, location, filenames, EXIF metadata in the original file, or other people’s knowledge. Blur and pixelation may preserve enough structure for re-identification. A missed detection leaves a face exposed.

## Threats considered

| Threat | Current response | Residual risk |
|---|---|---|
| Accidental server retention | Stateless image path; temporary video cleanup | Process crash may leave an OS temp file until cleanup |
| Face missed by detector | Compare detectors; visible review | No detector has perfect recall |
| Blur reversal | Solid-mask option and warning | Context can still identify a person |
| Model silently unavailable | Status endpoint and disabled UI option | User must configure optional models |
| Misleading benchmark | Unlabelled runs do not claim precision/recall | Small labelled datasets can still mislead |

## Production hardening still needed

Use encrypted temporary storage, strict request limits, authentication, dependency scanning, structured audit events without media, metadata stripping, a retention test, and a human review step before publication.
