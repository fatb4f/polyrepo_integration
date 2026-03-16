# Polyrepo Workspace v0

## Purpose

Define the minimum control contract for a local-first polyrepo workspace controller.

Delivery sequencing for this contract is defined in [polyrepo_workspace_delivery_v0.md](/home/_404/src/polyrepo_workspace/polyrepo_workspace_delivery_v0.md).

This spec is for:
- repo registry and repo relations
- cross-repo tracking and lineage
- safe fan-out execution
- GitHub Project projection

This spec is not for:
- release policy details
- CI/CD pipeline design
- per-repo branching conventions beyond what the controller must validate

## Core Invariants

1. **Authority invariant**
   The local manifest is the only authority plane.
2. **Projection invariant**
   GitHub Projects is a tracking and projection plane, not the authority plane.
3. **Identity invariant**
   Cross-repo lineage is identified by stable `change_id` and `item_id`, not by commit SHA.
4. **Observation invariant**
   Commit SHAs are observations attached to lineage, not durable identity.
5. **Execution invariant**
   Multi-repo writes are journaled workflows, not distributed transactions.
6. **Selection invariant**
   `gitopolis` is the primary workspace engine. If unavailable, the controller degrades to read-only local inspection.

## Control Planes

| Plane | Role | Authority |
| --- | --- | --- |
| Authority plane | Repo registry, relations, policies, branch/base pins, tracking IDs, lineage, observations | Local manifest only |
| Projection plane | Dashboard, status, assignee/state, cross-repo visibility | GitHub Projects |

### Write Direction

Default write direction is:

```text
local manifest -> GitHub Projects
```

Automatic GitHub-to-local writeback is forbidden.

## Reconcile Modes

Two modes are allowed:

1. **Projection-only**
   GitHub Projects is read-only from the controller's perspective.
2. **Proposed-writeback**
   The controller may read GitHub field changes and generate a reviewable reconcile patch against the local manifest.

No mode may mutate local authority state implicitly.

## Required Registries and Graphs

The workspace maintains five distinct structures.

### 1. Repo Registry

Canonical inventory of local repos.

Required fields:
- `repo_id`
- `name`
- `path`
- `remote`
- `default_branch`
- `engine`
- `active`

### 2. Repo Relationship Graph

Cross-repo topology and dependency semantics.

Allowed relation examples:
- `depends_on`
- `uses_schema_from`
- `publishes_to`
- `mirrors`
- `owned_with`

### 3. Tracking Graph

External work items and operator-facing tracking entities.

Examples:
- issue
- PR
- packet
- project item

### 4. Change Lineage Graph

Durable cross-repo work identity.

Required IDs:
- `change_id`
- `item_id`
- optional `run_id`

### 5. Commit Observation Graph

Per-repo observed commits tied to lineage at a point in time.

Required IDs:
- `observation_id`
- `change_id`
- `repo_id`

## Identity Model

### Stable IDs

- `workspace_id`: workspace authority root
- `repo_id`: canonical repo identity
- `tracking_id`: external issue/PR/project item identity
- `change_id`: durable cross-repo work identity
- `observation_id`: point-in-time commit observation
- `run_id`: optional execution run / controller invocation identity

### Rule

Only `change_id`, `item_id`, and other registry IDs are durable join keys.

Commit SHAs, branches, and patch IDs are observations.

## Schema Sketches

### Manifest

```yaml
workspace_id: ws-main
engine: gitopolis
repos:
  - repo_id: api
    path: /src/api
    remote: git@github.com:org/api.git
    default_branch: main
    branch_policy:
      tracked_branch: feat/WC-20260314-001
      base_ref: origin/main
tracking:
  project_id: GH-PROJ-12
policies:
  allow_dirty: false
  continue_on_error: false
```

### Change Lineage

```yaml
change_id: WC-20260314-001
item_id: org/platform#123
title: Add cross-repo auth envelope
repos:
  - repo_id: api
  - repo_id: web
tracking_ids:
  - GH-PROJ-12:ITEM-44
```

### Commit Observation

```yaml
observation_id: OBS-20260314-001
change_id: WC-20260314-001
repo_id: api
commit_oid: abc1234
patch_id: p_api_001
branch: feat/WC-20260314-001
base_ref: origin/main
observed_at: 2026-03-14T15:00:00Z
status: current
```

## Rewrite-Safe Lineage Rules

- Rebases, restacks, and force-pushes create new observations.
- Old observations remain valid historical evidence unless explicitly invalidated.
- The controller resolves current state from the latest valid observation for a tracked branch/ref.
- Synthetic edges between raw SHAs are never treated as durable lineage.

## Repo Preflight State Machine

Every target repo must be classified before any operation.

Allowed states:
- `CLEAN`
- `DIRTY`
- `DETACHED`
- `DIVERGED`
- `MISSING`
- `UNBORN`
- `CONFLICTED`

### Write Gate

Write fan-out is denied unless all targeted repos satisfy:
- repo exists
- branch policy matches, or detached mode is explicitly allowed
- expected base ref is known
- no uncommitted changes, unless `allow_dirty: true`
- no merge or rebase conflict state
- divergence policy is satisfied

## Operation Classes

| Class | Examples | Default concurrency | Failure policy |
| --- | --- | ---: | --- |
| READ | status, fetch metadata, graph export | parallel | continue and collect failures |
| WRITE | branch create, pull/rebase, commit, tag, push | sequential | stop on first failure |

`continue_on_error` for writes must be explicit.

## Journaled Execution Contract

Multi-repo operations are journaled workflows.

Each run records:
- `run_id`
- requested operation
- targeted repos
- preflight state per repo
- completed repos
- failed repo and reason
- pending repos
- emitted observations
- suggested compensating actions

### Rollback

Implicit rollback is forbidden.

Allowed rollback modes:
1. `none`
2. `compensating`

`compensating` rollback requires an explicit inverse action declared in policy.

## GitHub Project Projection Mapping

GitHub Projects is a projection of local authority state.

Project fields should map from local authority records, for example:
- `change_id` -> project custom field
- `item_id` -> source issue/PR field
- status -> derived from journal / manifest state
- assignee -> operator-facing projection
- linked repos -> derived from change lineage membership

GitHub field edits do not mutate the manifest directly.

In proposed-writeback mode, imported changes must be emitted as a reconcile patch.

## Tooling Model

- Primary workspace engine: `gitopolis`
- Optional per-repo history UX: `git-branchless`
- Tracking/projection UI: GitHub Projects
- Existing `git-workflow-manager` may remain as narrowed release-policy support

If `gitopolis` is unavailable:
- allow read-only inspection
- deny write workflows

No parity fallback to `mr` or `git for-each-repo`.

## Minimum Command Surface

- `workspace inspect`
- `workspace export-graph`
- `workspace preflight`
- `workspace exec-read`
- `workspace exec-write`
- `workspace project-sync`
- `workspace project-reconcile`
- `workspace journal show <run_id>`

## Acceptance Criteria

This spec is minimally satisfied when:
- one local manifest can describe multiple repos and their relations
- one change can be tracked across multiple repos without using SHAs as identity
- rebases create new observations without destroying lineage
- write fan-out is blocked on failed preflight
- every write run emits a journal
- GitHub Projects can be projected from local state without becoming the authority
