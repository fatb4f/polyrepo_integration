# Review Workspace Instructions

Use this file for the full review workflow. `AGENTS.md` and `.project.manifest.json`
are entrypoint and contract surfaces, not the full operator instructions.

## Scaffolding Structure

- `.project.manifest.json`
  Canonical project definitions, scaffold paths, and the project review contract.
- `.workspace/scripts/build_overrides.sh`
  Idempotent scaffold generator for `AGENTS.md` and the project-specific review
  schema/template files.
- `AGENTS.md`
  Thin repo entrypoint that points to the manifest, this instructions file, and
  the scaffold generator.
- `.workspace/templates/reviews/artifact_review.schema.json`
  Generic base review schema. This file is a hand-maintained source, not a
  manifest-generated artifact.
- `.workspace/templates/reviews/{project-profile,compatibility-schema,review-template}`
  Idempotent project-specific scaffold outputs generated from the manifest by
  `.workspace/scripts/build_overrides.sh`.

## Review Surface

Treat the uploaded archive and its extracted workspace as the primary review
surface.

Do not assume an installed `codex` runtime exists, and do not default to
runtime execution unless the required runtime is explicitly present and the task
asks for it.

Work in the same workspace where the archive is extracted.

## Priority Assets

Priority review assets are defined by `.project.manifest.json.priority_assets`.

Use these manifest keys:

- `entrypoint_files`
  Top-level files to read first.
- `workspace_dirs`
  Top-level shared scaffold directories to read recursively.
- `top_level_project_dirs`
  Top-level project-owned directories to read recursively.
- `extra_paths`
  Additional repo-relative paths when a project needs narrow exceptions.

## Output Rules

- do not generate full review artifacts in chat UI
- write review outputs directly to file in the internal `/mnt` workspace
- archive the generated review artifacts there
- in chat, return only the download link or file link plus a minimal status note
- prefer machine-readable output first, prose second
- use the review template and validate against the review schema before finalizing

## Review Rules

- keep findings severity-ordered
- separate verified execution from static review and recommendation
- do not overclaim coverage
- if something was not executed, say so explicitly
- if the runtime is unavailable, state that as an execution boundary, not as a failure

## Execution States

- `passed`
- `partial`
- `failed`
- `not_executed`
- `not_selected`

For approvals and collaboration:

- `partial` is correct when the surface is discovered but the deeper bidirectional path was not observed

## Default Review Posture

- bugs
- brittle assumptions
- documentary overclaim
- missing evidence
- schema or contract drift

Findings first. Summary second.

## Schema and Template Changes

- keep the generic base schema reusable
- keep the project profile project-specific
- preserve compatibility when practical
- after scaffold changes, rerun `./.workspace/scripts/build_overrides.sh`

Be concise and exact.
