# AGENTS

This repo is driven by [.project.manifest.json](./.project.manifest.json) and the hand-maintained templates under [`.workspace/templates`](/home/_404/src/polyrepo_integration/.workspace/templates).

Read [.project.manifest.json](./.project.manifest.json) first before doing review, runtime, schema, or planning work in this repo.

Use [review_workspace_instructions.md](./.workspace/docs/review_workspace_instructions.md) for the full review workflow and output contract.

## Required behavior

- read .workspace/docs/review_workspace_instructions.md for the full review workflow and output contract
- use the project review contract under .workspace/templates/reviews
- treat this repo as a bounded integration canvas for cross-repo analysis and validation, not as a semantic authority surface

## Review contract

Use these files:

- [.project.manifest.json](./.project.manifest.json)
- [artifact_review.schema.json](./.workspace/templates/reviews/artifact_review.schema.json)
- [polyrepo_integration.review.schema.json](./.workspace/templates/reviews/polyrepo_integration.review.schema.json)
- [review.schema.json](./.workspace/templates/reviews/review.schema.json)
- [review.json.template](./.workspace/templates/reviews/review.json.template)

Template root: `.workspace/templates/reviews`
Project id: `polyrepo_integration`

If there is any conflict between ad hoc assumptions and the manifest, follow the manifest.
