---
name: json-tool
description: "Use this skill for validation-first JSON contract work: normalize candidate JSON when needed, validate against canonical schemas, and emit durable validation artifacts."
compatibility: "Best for JSON-first workflows with canonical JSON Schema contracts. The bundled execution surface in this repo is validation-first and centers on JSON Schema plus a local validator."
metadata:
  author: _404
  version: "0.1"
---

# JSON Tool

Use this skill when the task is primarily JSON contract validation work rather than ad hoc prose processing.

## Trigger

- Define or revise JSON contracts and validation envelopes.
- Normalize candidate JSON when the input is not already in contract shape.
- Validate JSON artifacts against canonical schemas.
- Emit durable validation reports and accepted-json artifacts.

## Rules

- `JSON Schema` is the canonical accepted-artifact authority.
- The bundled executable surface in this repo is `scripts/validate_json_contract.py`.
- Candidate extraction is optional and upstream of schema validation.
- Do not claim bundled `unify`, `derive`, `check`, `authorize`, or `render` execution unless those operators are explicitly added to this repo.

## Execution Shape

1. `assets/interface.json`
2. `assets/workflow.json`
3. `assets/sequence_dag.md`
4. `assets/operator_surface.json`
5. `references/stack.md`
6. `scripts/validate_json_contract.py`

## Output guidance

Choose the minimal operator path that matches the task:
- unstructured ingress: `extract -> validate`
- structured ingress: `validate`

When `scripts/validate_json_contract.py` is used for the validate step, pass output
paths when you need durable artifacts:
- `--report-out <path>` for the machine-readable validation report
- `--accepted-json-out <path>` for the accepted JSON artifact when validating a single file

Prefer JSON outputs first.
