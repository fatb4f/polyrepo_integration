# Review

- Uploaded archive: `polyrepo_workspace-HEAD.zip`
- Schema-normalized artifact name: `polyrepo_integration-polyrepo_workspace-HEAD.zip`
- Verdict: `REVISE`

## Confirmed progress

1. `analysis/meta_plan.json:181-190` now declares MP4 validation authority and narrowness criteria.
2. `analysis/meta_plan.json:28-48` improves artifact-contract coverage for the objective register input and DS# register, but only partially.

## Findings

### F1 — High — MP2 drops MP1 analysis outputs

- `analysis/meta_plan.json:105-110` makes MP1 emit `normalized_objective_register`, `objective_semantic_analysis`, `objective_dependency_gap_analysis`, and `canonical_objective_order`.
- `analysis/meta_plan.json:124-129` then lets MP2 operate on only `canonical_objective_order` plus `review_rationale_log`.
- The DS# register contract at `analysis/meta_plan.json:38-47` still expects dependency- and boundary-sensitive fields such as `blocking_dependencies`, `authority_boundary`, and `recomposition_constraints`.

**Why it matters:** MP2 can currently derive bounded sets from ordering alone, which is too weak for the stated dependency/authority-preserving purpose.

### F2 — High — Bootstrap replay contract is not machine-recoverable

- `project.manifest.json:65-69` declares `objective_analysis_context` as an entry artifact, but `project.manifest.json:97-108` also requires that same artifact for `draft_meta_plan` while the stage produces `analysis/meta_plan.json` again.
- `project.manifest.json:161-167` says stages may run only when inbound dependencies are already present, so the DAG only models revision of a pre-existing meta plan and does not expose a first-pass generation path.
- `analysis/meta_plan.json:59-61` also points `integration_manifest` at `repo://.project.manifest.json` and marks it `not_packaged_in_trimmed_archive`, even though `project.manifest.json` is actually bundled at repo root.

**Why it matters:** the shipped archive does not let a controller replay the initial meta-plan bootstrap path without inferring missing mode distinctions and source resolution rules.

### F3 — Medium — MP3 termination metrics are unbound

- `analysis/meta_plan.json:152-160` names `ambiguity_score_at_or_below_threshold` and `analysis_artifact_hash_stable_across_two_passes`.
- The archive never defines how `ambiguity_score` is computed, what artifact family is hashed, or how pass-to-pass normalization is performed before comparing hashes.

**Why it matters:** recursion stop/continue decisions remain judgment-based instead of mechanically replayable.

## Recommended next patch set

1. Wire MP2 to the semantic and dependency outputs of MP1.
2. Split bootstrap and revision workflow modes and bind `integration_manifest` to `project.manifest.json`.
3. Define MP3 scoring/hash evidence so termination can be replayed.
