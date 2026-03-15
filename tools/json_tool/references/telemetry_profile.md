# Telemetry Profile

Current next-layer telemetry governance packet:
- `authority://telemetry_profile/llmops.telemetry.profile.v1.json`
- `authority://telemetry_profile/event-envelope.v1.json`
- `authority://telemetry_profile/otel-mapping.v1.json`
- `authority://telemetry_profile/llm-semantics.v1.json`

Availability:
- external authority, not bundled into this repo by default

Current authority split:
- CloudEvents for raw envelope only
- OTel/OTLP for transport and correlation
- OTel GenAI and OpenInference as semantic mapping vocabularies
- internal JSON Schema contracts remain canonical accepted-artifact authority
