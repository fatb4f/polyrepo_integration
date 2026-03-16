# Polyrepo Workspace Delivery v0

## Purpose

Define a fast path from control-spec to production through stacked mini-deliverables.

This document assumes the control contract in [polyrepo_workspace_v0.md](/home/_404/src/polyrepo_workspace/polyrepo_workspace_v0.md) and focuses on:
- MVP scope
- fastest credible path to production
- iterative expansion into fuller schema-backed policy models

## Delivery Principles

1. Build the authority plane first.
2. Prefer usable, reviewable contracts over broad feature coverage.
3. Ship read and preflight surfaces before write automation.
4. Treat GitHub Projects as projection only until local authority is stable.
5. Add policy depth by iteration, not in the first cut.

## MVP Definition

The MVP is not a proof of concept.

The MVP is the minimum production-capable controller that can:
- load a local manifest as sole authority
- model repo registry, repo relations, change lineage, and commit observations
- classify repo preflight state
- execute read fan-out safely
- deny unsafe writes deterministically
- journal every controller run
- project local state outward without surrendering authority

The MVP does not need:
- automatic GitHub writeback
- full policy DSL coverage
- compensating rollback automation
- complex reconcile logic
- broad multi-engine support

## Production Goal

The first production target is:

> one operator can safely inspect, preflight, track, and project a small polyrepo workspace from a local authority manifest, with write operations gated by explicit preflight and journal semantics.

That is enough to be real infrastructure, even before deeper policy formalization lands.

## Mini-Deliverable Stack

### D0: Control Contract Freeze

Goal:
- freeze the authority, lineage, observation, and execution model

Primary artifacts:
- [polyrepo_workspace_v0.md](/home/_404/src/polyrepo_workspace/polyrepo_workspace_v0.md)

Acceptance:
- authority plane and projection plane are distinct
- durable identity is not SHA-based
- write workflows are explicitly journaled, not atomic

Defers:
- machine-validated schemas
- runtime implementation

### D1: Manifest and Registry Schema MVP

Goal:
- define the minimum canonical artifact family

Required artifact families:
- `workspace.manifest.json`
- `repo_registry.json`
- `repo_relations.json`
- `change_lineage.json`
- `commit_observations.json`
- `run_journal.json`

Required schema work:
- JSON Schema for each artifact family
- one seed instance per family

Acceptance:
- each artifact has one canonical schema authority
- each artifact has one canonical instance authority
- all core joins validate locally

Defers:
- CUE policy narrowing
- GitHub integration

### D2: Read-Only Controller MVP

Goal:
- get to production quickly with a safe read-only controller

Minimum command surface:
- `workspace inspect`
- `workspace export-graph`
- `workspace preflight`
- `workspace exec-read`
- `workspace journal show`

Behavior:
- load manifest
- enumerate repos
- classify preflight state
- emit journal for each run
- never mutate repo state

Acceptance:
- controller runs cleanly against a real local workspace
- preflight classification works across all target repos
- read fan-out failures are collected, not hidden

Defers:
- write execution
- GitHub projection

### D3: Projection MVP

Goal:
- project local authority into GitHub Projects without introducing writeback

Minimum scope:
- project item export
- status projection
- change-to-project linking
- repo membership projection

Acceptance:
- local authority state can be rendered into GitHub Projects
- projection can be repeated idempotently
- no GitHub-side edits mutate local state

Defers:
- reconcile/import
- bidirectional sync

### D4: Single-Workflow Write MVP

Goal:
- introduce the smallest production-safe write lane

Scope:
- one write workflow class
- one tracked branch policy
- sequential execution only
- stop on first failure

Suggested first workflow:
- branch prepare or branch pin update

Required controls:
- preflight gate
- journal emission
- explicit failure classification
- no implicit rollback

Acceptance:
- one write workflow can run safely across a small workspace
- failures leave a usable journal and clear pending/completed state

Defers:
- push
- multi-step mutation orchestration
- compensating rollback

### D5: Change-Lineage Workflow MVP

Goal:
- make cross-repo work identity operational

Scope:
- stable `change_id`
- stable `item_id`
- per-repo commit observations
- latest-valid-observation resolution

Acceptance:
- one cross-repo change can be tracked through rebases without losing lineage
- observations remain historical evidence
- current state can be computed from observations

Defers:
- issue automation
- PR automation

### D6: Reconcile Patch Mode

Goal:
- allow controlled GitHub-to-local proposals without breaking authority

Scope:
- read GitHub Project field changes
- emit proposed manifest patch
- require review before apply

Acceptance:
- reconcile output is patch-shaped and reviewable
- no direct authority mutation occurs from GitHub input

Defers:
- auto-apply
- field-level conflict resolution beyond patch generation

### D7: Policy Model Expansion

Goal:
- deepen policy only after the controller is already useful

Candidate policy families:
- branch policy
- divergence policy
- dirty-worktree policy
- write permission policy
- rollback eligibility policy
- projection field policy

Recommended layering:
- JSON Schema for canonical shape
- CUE for narrowing and cross-field constraints
- rendered docs only as projection

Acceptance:
- controller behavior can be derived from schema-backed policy artifacts
- policy families are versioned independently from runtime code

## Fastest Path to Production

The shortest credible production sequence is:

1. `D0` freeze the control contract
2. `D1` define schema-backed core artifacts
3. `D2` ship the read-only controller
4. `D3` add GitHub projection
5. `D4` add one narrow write workflow

That gets a real operator-facing system into production before deeper policy work.

## What Not To Do In The MVP

Do not:
- treat GitHub as authority
- build bidirectional sync first
- model all Git workflows up front
- add multiple workspace engines
- mix speculative policy DSL work into the first controller delivery
- make cross-repo writes look transactional

## Artifact Authority Rules

For each new artifact family introduced in this stack, define:
- schema authority
- instance authority
- actuation authority
- rendering boundary

The default rule is:
- JSON Schema = canonical structure
- local JSON artifact = canonical state
- controller = actuator
- GitHub/UI/docs = projection

## Suggested Iteration Rhythm

Each iteration should produce:
- one new canonical artifact family or one new command family
- one validation path
- one acceptance sample
- one explicit defer list for the next iteration

That keeps the loop cumulative and reviewable.

## Exit Condition For MVP

The MVP is done when:
- local manifest authority is real
- core schemas exist and validate
- read-only controller works against a real workspace
- GitHub projection works without writeback
- one write workflow is safely gated and journaled

Everything after that is expansion, not prerequisite.
