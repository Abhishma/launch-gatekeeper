
from __future__ import annotations
from typing import Any

from .logic import (
    detect_missing_controls,
    should_abstain,
    detect_risks,
    blockers_for_risks,
    mitigation_suggestions,
    readiness_band,
    memo,
)
from .validator import validate_launch, validate_output

def review_launch(launch: dict[str, Any]) -> dict[str, Any]:
    validate_launch(launch)

    missing_controls = detect_missing_controls(launch)
    abstain, reasons = should_abstain(launch, missing_controls)
    if abstain:
        report = {
            "launch_id": launch["launch_id"],
            "status": "abstained",
            "readiness_band": "low",
            "risks": ["mixed_or_unclear"],
            "blockers": [],
            "missing_controls": list(dict.fromkeys(missing_controls + reasons)),
            "mitigation_suggestions": [
                "Provide QA summary",
                "Provide rollout plan",
                "Re-run review with fuller launch evidence"
            ],
            "memo": "Readiness cannot be assessed safely because core launch evidence is missing."
        }
        validate_output(report)
        return report

    risks = detect_risks(launch)
    blockers = blockers_for_risks(risks, launch)
    report = {
        "launch_id": launch["launch_id"],
        "status": "review_ready",
        "readiness_band": readiness_band(risks, blockers),
        "risks": risks,
        "blockers": blockers,
        "missing_controls": missing_controls,
        "mitigation_suggestions": mitigation_suggestions(risks),
        "memo": memo(launch, readiness_band(risks, blockers), blockers)
    }
    validate_output(report)
    return report
