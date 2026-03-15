# Polyrepo Integration

Bounded integration canvas for cross-repo semantic analysis, validation, and scaffold projection.

This repo is for:
- hosting the shared `.workspace` scaffold
- carrying integration-only analysis artifacts under `analysis/`
- carrying imported or pinned repo state under `modules/`
- carrying integration-local tools under `tools/`

This repo is not:
- the ACM policy authority surface
- the `polyrepo_workspace` contract authority
- the `git_asset` bootstrap authority

Current seeded tool:
- `tools/json_tool`

Scaffold command:
- `./.workspace/scripts/build_overrides.sh`
