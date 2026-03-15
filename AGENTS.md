Treat the uploaded archive and its extracted workspace as the primary review surface.
Work in the same workspace where the archive is extracted.
Do not generate full review artifacts in chat UI.
Write review outputs to file in the internal `/mnt` workspace, archive them there, and return only the file link plus a minimal status note in chat.
Prefer machine-readable output first.
Validate review outputs against the project review schema before finalizing.
Keep findings severity-ordered.

For patch-based follow-up review:
- treat the uploaded diff as a proposed change against the current packaged review surface
- review whether the patch clears the named findings without inventing new file-absence defects
- distinguish clearly between:
  - findings still present in the packaged archive
  - findings cleared by the patch if applied
- keep the machine-readable review artifact on the project review contract; do not replace it with an ad hoc review schema
- validate patch-review outputs against the same project review schema used for archive review
- treat any `annotated diff patch` as a supplemental artifact, not as the machine-readable review artifact itself
- carry patch-specific notes inside the conforming review artifact evidence, details, verdict reasons, or companion files instead of adding non-contract top-level fields
- when asked to apply the patch, update the repo artifact and write the resulting `annotated diff patch` to file
- name the `annotated diff patch` artifact after the originating commit hash
