# Review Workspace Instructions

Use this file for the full review workflow. `AGENTS.md` and `.project.manifest.json`
are entrypoint and contract surfaces, not the full operator instructions.

## Scaffolding Structure

- `.project.manifest.json`
  Canonical project definitions, scaffold paths, and the project review contract.
- `AGENTS.md`
  Thin repo entrypoint that points to the manifest, this instructions file, and
  the template authorities.
- `.workspace/templates/reviews/artifact_review.schema.json`
  Generic base review schema. This file is a hand-maintained source, not a
  generated artifact.
- `.workspace/templates/reviews/{project-profile,compatibility-schema,review-template}`
  Hand-maintained project review artifacts used directly by this repo.

## Review Surface

Treat the uploaded archive and its extracted workspace as the primary review
surface.

Work in the same workspace where the archive is extracted.

For `polyrepo_integration`, focus the review on the project-owned review surface:
- `analysis/`
- `modules/`
- `tools/`

Treat `.workspace/` as shared scaffold and contract context.

Review scaffold files deeply only when:
- a finding points to template or schema contract behavior
- the project-owned surface depends directly on scaffold behavior

## Priority Assets

Priority review assets are defined by `.project.manifest.json.priority_assets`.

Review must span the full indicated asset set before finalizing.

Do not stop after the first high-signal surface if additional indicated assets
remain unread or unassessed.

For `polyrepo_integration`, that means the review should cover:
- entrypoint files
- shared scaffold/context files as needed for contract interpretation
- every top-level project directory named by the manifest
- any manifest-listed extra paths

Use these manifest keys:

- `entrypoint_files`
  Top-level files to read first.
- `workspace_dirs`
  Top-level shared scaffold directories to use as contract/background context.
- `top_level_project_dirs`
  Top-level project-owned directories to treat as the primary review surface.
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
- do not finalize a review after only partial traversal of the indicated asset set
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

Be concise and exact.
