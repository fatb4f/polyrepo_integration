#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
SEED = ROOT / "instances" / "seed"
REPORT = ROOT / "validation" / "d1.validation_report.json"

FILES = {
    "workspace.manifest": ("workspace.manifest.schema.json", "workspace.manifest.json"),
    "repo_registry": ("repo_registry.schema.json", "repo_registry.json"),
    "repo_relations": ("repo_relations.schema.json", "repo_relations.json"),
    "change_lineage": ("change_lineage.schema.json", "change_lineage.json"),
    "commit_observations": ("commit_observations.schema.json", "commit_observations.json"),
    "run_journal": ("run_journal.schema.json", "run_journal.json"),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check(name: str, passed: bool, detail: str) -> dict:
    return {"name": name, "passed": passed, "detail": detail}


def main() -> int:
    schema_checks: list[dict] = []
    join_checks: list[dict] = []
    docs: dict[str, dict] = {}

    for artifact_name, (schema_file, instance_file) in FILES.items():
        schema = load_json(SCHEMAS / schema_file)
        instance = load_json(SEED / instance_file)
        docs[artifact_name] = instance
        try:
            jsonschema.Draft202012Validator(schema).validate(instance)
            schema_checks.append(check(artifact_name, True, f"{instance_file} matches {schema_file}"))
        except jsonschema.ValidationError as exc:
            schema_checks.append(check(artifact_name, False, str(exc)))

    manifest = docs["workspace.manifest"]
    repo_registry = docs["repo_registry"]
    repo_relations = docs["repo_relations"]
    change_lineage = docs["change_lineage"]
    commit_observations = docs["commit_observations"]
    run_journal = docs["run_journal"]

    workspace_id = manifest["workspace_id"]
    workspace_match = all(
        doc["workspace_id"] == workspace_id
        for doc in [
            repo_registry,
            repo_relations,
            change_lineage,
            commit_observations,
            run_journal,
        ]
    )
    join_checks.append(
        check(
            "workspace_id_alignment",
            workspace_match,
            "all artifacts share the manifest workspace_id",
        )
    )

    registry_files_match = manifest["registries"] == {
        "repo_registry": "repo_registry.json",
        "repo_relations": "repo_relations.json",
        "change_lineage": "change_lineage.json",
        "commit_observations": "commit_observations.json",
        "run_journal": "run_journal.json",
    }
    join_checks.append(
        check(
            "manifest_registry_refs",
            registry_files_match,
            "workspace manifest registry refs match the seeded artifact file names",
        )
    )

    repo_ids = [repo["repo_id"] for repo in repo_registry["repos"]]
    repo_id_set = set(repo_ids)
    join_checks.append(
        check("repo_ids_unique", len(repo_ids) == len(repo_id_set), "repo_ids are unique")
    )

    valid_relations = all(
        relation["from_repo_id"] in repo_id_set and relation["to_repo_id"] in repo_id_set
        for relation in repo_relations["relations"]
    )
    join_checks.append(
        check(
            "relation_repo_refs",
            valid_relations,
            "all repo relation endpoints resolve to repo_registry repo_ids",
        )
    )

    change_ids = [change["change_id"] for change in change_lineage["changes"]]
    change_id_set = set(change_ids)
    valid_change_repos = all(
        set(change["repo_ids"]).issubset(repo_id_set) for change in change_lineage["changes"]
    )
    join_checks.append(
        check(
            "change_repo_refs",
            valid_change_repos,
            "all change_lineage repo_ids resolve to repo_registry repo_ids",
        )
    )

    observation_ids = [observation["observation_id"] for observation in commit_observations["observations"]]
    observation_id_set = set(observation_ids)
    valid_observation_refs = all(
        observation["repo_id"] in repo_id_set and observation["change_id"] in change_id_set
        for observation in commit_observations["observations"]
    )
    join_checks.append(
        check(
            "observation_refs",
            valid_observation_refs,
            "all commit observations resolve to repo_registry repo_ids and change_lineage change_ids",
        )
    )

    current_keys: list[tuple[str, str, str]] = [
        (observation["change_id"], observation["repo_id"], observation["branch"])
        for observation in commit_observations["observations"]
        if observation["status"] == "current"
    ]
    join_checks.append(
        check(
            "current_observation_uniqueness",
            len(current_keys) == len(set(current_keys)),
            "at most one current observation exists per change_id/repo_id/branch tuple",
        )
    )

    valid_run_refs = True
    for run in run_journal["runs"]:
        if not set(run["targeted_repo_ids"]).issubset(repo_id_set):
            valid_run_refs = False
        if not {entry["repo_id"] for entry in run["preflight"]}.issubset(repo_id_set):
            valid_run_refs = False
        if not set(run["completed_repo_ids"]).issubset(repo_id_set):
            valid_run_refs = False
        if not set(run["pending_repo_ids"]).issubset(repo_id_set):
            valid_run_refs = False
        if not {entry["repo_id"] for entry in run["failures"]}.issubset(repo_id_set):
            valid_run_refs = False
        if not set(run["requested_change_ids"]).issubset(change_id_set):
            valid_run_refs = False
        if not set(run["emitted_observation_ids"]).issubset(observation_id_set):
            valid_run_refs = False
    join_checks.append(
        check(
            "run_journal_refs",
            valid_run_refs,
            "run_journal repo, change, and observation references resolve locally",
        )
    )

    all_pass = all(item["passed"] for item in schema_checks + join_checks)
    report = {
        "report_id": "d1-schema-pack-validation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "all_pass": all_pass,
        "schema_checks": schema_checks,
        "join_checks": join_checks,
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
