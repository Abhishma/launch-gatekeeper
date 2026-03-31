
from __future__ import annotations
from pathlib import Path
from jsonschema import validate

from .utils import load_json

ROOT = Path(__file__).resolve().parents[2]

def validate_launch(launch: dict) -> None:
    schema = load_json(ROOT / "schemas" / "launch_input.schema.json")
    validate(instance=launch, schema=schema)

def validate_output(report: dict) -> None:
    schema = load_json(ROOT / "schemas" / "readiness_output.schema.json")
    validate(instance=report, schema=schema)
