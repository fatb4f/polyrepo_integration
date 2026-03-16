#!/usr/bin/env python3

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPO = Path("/home/_404/src/polyrepo_integration")
OUT = REPO / "review" / "git_log.json"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True)


def load_existing() -> dict:
    if OUT.exists():
        return json.loads(OUT.read_text())
    return {}


def classify(subject: str) -> str:
    lowered = subject.lower()
    if "review contract" in lowered or "review templates" in lowered:
        return "review_contract"
    if "manifest" in lowered:
        return "review_contract"
    if "boundary" in lowered:
        return "review_boundary"
    if "meta plan" in lowered:
        return "meta_plan_contract"
    if "diff" in lowered:
        return "artifact_hygiene"
    if "scaffold" in lowered or "surface" in lowered:
        return "scaffold_reset"
    if "context" in lowered or "review manifest" in lowered:
        return "context_surface"
    return "unclassified"


def default_effects(subject: str) -> list[str]:
    return [subject]


def build() -> dict:
    existing = load_existing()
    existing_timeline = {
        item["commit"]: item for item in existing.get("timeline", [])
    }
    current_state = existing.get("current_state", {})

    remote_url = git("remote", "get-url", "origin").strip()
    lines = git("log", "--pretty=format:%H%x1f%h%x1f%aI%x1f%s", "-n", "16").splitlines()
    commits = []
    for ordinal, line in enumerate(reversed(lines), start=1):
        full, short, date, subject = line.split("\x1f")
        prev = existing_timeline.get(full, {})
        commits.append(
            {
                "ordinal": ordinal,
                "commit": full,
                "short": short,
                "date": date,
                "subject": subject,
                "classification": prev.get("classification", classify(subject)),
                "effects": prev.get("effects", default_effects(subject)),
            }
        )

    head_full, head_short, head_date, head_subject = lines[0].split("\x1f")
    return {
        "kind": "project_git_log_tracker.v1",
        "project_id": "polyrepo_integration",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_path": str(REPO),
        "remote_url": remote_url,
        "head_commit": {
            "commit": head_full,
            "short": head_short,
            "date": head_date,
            "subject": head_subject,
        },
        "timeline": commits,
        "current_state": {
            "status": "active",
            "phase": current_state.get("phase", "review_objects_in_repo"),
            "summary": current_state.get(
                "summary",
                "The repo carries evolving review and git-log objects under review/ while concrete review artifacts may remain local.",
            ),
            "authoritative_artifacts": current_state.get(
                "authoritative_artifacts",
                [
                    str(REPO / "AGENTS.md"),
                    str(REPO / ".templates" / "artifact_review.schema.json"),
                    str(REPO / ".templates" / "polyrepo_integration.review.schema.json"),
                    str(REPO / ".templates" / "review.schema.json"),
                    str(REPO / ".templates" / "review.json.template"),
                    str(REPO / "analysis" / "meta_plan.json"),
                    str(REPO / "project.manifest.json"),
                    str(REPO / "review" / "review_pipeline.json"),
                    str(REPO / "review" / "git_log.json"),
                ],
            ),
            "open_items": current_state.get(
                "open_items",
                [
                    "Append one review_pipeline entry per submitted HEAD review instead of replacing prior entries.",
                    "Keep the local review artifact and tracker symlink aligned with the latest appended review entry.",
                    "Promote the git-log object as the canonical incremental context surface for future review corrections.",
                ],
            ),
        },
    }


def main() -> None:
    OUT.write_text(json.dumps(build(), indent=2) + "\n")


if __name__ == "__main__":
    main()
