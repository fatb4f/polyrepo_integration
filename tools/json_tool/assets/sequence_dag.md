# JSON Tool Sequence DAG

Machine-readable equivalent:
- `assets/workflow.json`

1. `J0_route`
- Route by `input_kind=external_ds|json_instance`.

2. `J1_extract` (optional)
- Only for unstructured or mixed-source ingress.
- Emit `candidate_envelope`.

3. `J2_validate`
- Validate accepted JSON against canonical contracts.
- Use `scripts/validate_json_contract.py` to emit durable validation artifacts.

4. `J3_exit`
- Exit after validation.
- Do not force validated inputs through derive or policy stages that are not bundled here.
