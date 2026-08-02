# Security notes

VeilSight is a local-first prototype for privacy engineering research. It is
not a hosted service and should not be exposed directly to the public internet.

The API includes upload-size checks, restrictive response headers, an explicit
CORS allow-list, temporary video workspaces, and no database/logging of source
media. Before production deployment, place it behind TLS and an authenticated
reverse proxy, add rate limiting and structured audit logs that exclude media,
scan dependencies, pin model artefacts by checksum, and run labelled
accuracy/privacy tests on representative consented data.

Report security issues privately rather than posting sample personal media in a
public issue.
