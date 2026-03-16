# Polyrepo Workspace Tool Selection v1

This note records the final tool recommendation after the control-spec correction in [polyrepo_workspace_v0.md](/home/_404/src/polyrepo_workspace/polyrepo_workspace_v0.md) and the delivery sequencing in [polyrepo_workspace_delivery_v0.md](/home/_404/src/polyrepo_workspace/polyrepo_workspace_delivery_v0.md).

## Final Stack

| Role | Tool | Decision | Why |
| --- | --- | --- | --- |
| Local multi-repo authority + execution | `gitopolis` | Primary | It matches the spec's authority model and fan-out execution needs. If unavailable, the controller degrades to read-only local inspection. |
| Per-repo history UX | `git-branchless` | Add | Good fit for smartlog, restack, sync, and per-repo commit-stack hygiene. |
| Tracking / projection plane | GitHub Projects | Keep | Strong operator-facing dashboard and projection surface, but not the authority plane. |
| Git workflow policy support | `git-workflow-manager` | Keep, but narrow | Useful for branch/review/release policy support, not for workspace authority or lineage. |

## Architectural Correction

Cross-repo commit graphs are not the main identity mechanism.

The controller uses:
- durable identity = `change_id` + `item_id`
- commit SHAs = observations
- rebase/restack/force-push = new observations
- SHA-to-SHA edges = overlay evidence, not durable lineage

So:
- yes, maintain a cross-repo commit observation graph
- no, do not make it the authority plane

## Ownership Boundaries

### `gitopolis`

Owns:
- repo registry bootstrap
- local repo inventory
- local fan-out read/write execution
- repo grouping and tagging
- operator command surface

### `git-branchless`

Owns:
- per-repo smartlog
- restack / rebase repair
- local patch-stack ergonomics
- single-repo commit graph visualization

### GitHub Projects

Owns:
- project items
- custom projection fields such as `change_id`
- assignee/state/dashboard views
- dependency and cross-repo tracking visibility

### `git-workflow-manager`

Owns:
- branching conventions
- commit hygiene
- PR flow
- release-policy support

Does not own:
- workspace registry
- cross-repo lineage
- journaling
- manifest authority

## What Is Actually Missing

The main gap is not another Git tool.

The main missing layer is the local artifact/controller surface:
- `workspace.manifest.json`
- `repo_registry.json`
- `repo_relations.json`
- `change_lineage.json`
- `commit_observations.json`
- `run_journal.json`

Those artifacts are the authority substrate. The tools operate beneath or beside them.

## Fastest Credible Sequence

The fastest credible path remains:

1. `D0` freeze the control contract
2. `D1` define schema-backed artifacts
3. `D2` ship the read-only controller
4. `D3` add GitHub projection
5. `D4` add one narrow write workflow

That gets a real operator-facing system into production before deeper policy modeling.

## Immediate Next Move

Turn `D1` into a concrete schema pack plus a minimal controller skeleton for:
- `workspace inspect`
- `workspace preflight`
- `workspace journal show`
