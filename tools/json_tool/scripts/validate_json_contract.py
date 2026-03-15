#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_local_registry(schema_path: Path) -> Registry:
    schema = load_json(schema_path)
    schema_dir = schema_path.parent
    resources: dict[str, Resource] = {}
    root_id = schema.get("$id")
    root_base = ""
    if isinstance(root_id, str) and "/" in root_id:
        root_base = root_id.rsplit("/", 1)[0] + "/"

    for candidate in schema_dir.rglob("*.json"):
        try:
            doc = load_json(candidate)
            resource = Resource.from_contents(doc)
        except Exception:
            continue
        resources[candidate.resolve().as_uri()] = resource
        doc_id = doc.get("$id")
        if isinstance(doc_id, str) and doc_id:
            resources[doc_id] = resource
        if root_base:
            relative_path = candidate.relative_to(schema_dir).as_posix()
            resources[root_base + relative_path] = resource

    return Registry().with_resources(resources.items())


def validate(schema_path: Path, data_path: Path) -> list[str]:
    schema = load_json(schema_path)
    data = load_json(data_path)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
        registry=build_local_registry(schema_path),
    )
    errors = []
    try:
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            loc = '/'.join(str(p) for p in error.path) or '<root>'
            errors.append(f'{data_path}: {loc}: {error.message}')
    except Exception as exc:
        errors.append(f'{data_path}: <validator>: {exc}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate JSON files against JSON Schema 2020-12 contracts.')
    parser.add_argument('schema', help='Schema path')
    parser.add_argument('files', nargs='+', help='One or more JSON files to validate')
    parser.add_argument(
        '--report-out',
        help='Optional path for a machine-readable validation report artifact.',
    )
    parser.add_argument(
        '--accepted-json-out',
        help='Optional path for the accepted JSON artifact. Only valid when a single input file is provided and validation succeeds.',
    )
    args = parser.parse_args()

    schema_path = Path(args.schema).expanduser().resolve()
    file_paths = [Path(file_arg).expanduser().resolve() for file_arg in args.files]
    if args.accepted_json_out and len(file_paths) != 1:
        print('FAIL')
        print('- --accepted-json-out requires exactly one input JSON file')
        return 1

    all_errors: list[str] = []
    for file_path in file_paths:
        all_errors.extend(validate(schema_path, file_path))

    report_payload = {
        'kind': 'json_tool.validation_report.v1',
        'schema_ref': str(schema_path),
        'files': [str(path) for path in file_paths],
        'valid': not bool(all_errors),
        'errors': all_errors,
    }
    if args.report_out:
        write_json(Path(args.report_out).expanduser().resolve(), report_payload)

    if all_errors:
        print('FAIL')
        for err in all_errors:
            print(f'- {err}')
        return 1

    if args.accepted_json_out:
        accepted_path = Path(args.accepted_json_out).expanduser().resolve()
        write_json(accepted_path, load_json(file_paths[0]))
    print('OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
