
from __future__ import annotations
from typing import Any

def detect_missing_controls(launch: dict[str, Any]) -> list[str]:
    missing = []
    qa = launch.get("qa_summary", "").lower()
    rollout = launch.get("rollout_plan", "").lower()
    if not qa.strip():
        missing.append("QA summary missing")
    elif "not fully covered" in qa or "desktop only" in qa or "no tracking validation" in qa:
        missing.append("Critical QA coverage is incomplete")
    if not rollout.strip():
        missing.append("Rollout plan missing")
    elif "100%" in rollout and "phase" not in rollout:
        missing.append("No explicit phased rollout guardrails")
    if not launch.get("owners_defined", False):
        missing.append("Mitigation ownership is unclear")
    return missing

def should_abstain(launch: dict[str, Any], missing_controls: list[str]) -> tuple[bool, list[str]]:
    reasons = []
    if not launch.get("qa_summary", "").strip():
        reasons.append("Cannot assess readiness without QA summary")
    if not launch.get("rollout_plan", "").strip():
        reasons.append("Cannot assess rollout risk without rollout plan")
    if len(launch.get("prd_summary", "").strip()) < 20:
        reasons.append("PRD summary too sparse to assess safely")
    return bool(reasons), reasons

def detect_risks(launch: dict[str, Any]) -> list[str]:
    prd = launch.get("prd_summary", "").lower()
    qa = launch.get("qa_summary", "").lower()
    rollout = launch.get("rollout_plan", "").lower()
    deps = launch.get("dependency_notes", "").lower()
    incidents = launch.get("incident_context", "").lower()
    risks = []

    if "unresolved" in deps or "still in progress" in deps:
        risks.append("dependency_unresolved")
    if "100%" in rollout or "immediately" in rollout:
        risks.append("rollout_scope_too_broad")
    if "not fully covered" in qa or "desktop only" in qa or "no tracking validation" in qa:
        risks.append("qa_coverage_gap")
    if "tracking" in prd or "analytics" in deps or "tracking regressions" in incidents:
        risks.append("monitoring_gap")
    if "incident" in incidents or "incidents" in incidents:
        risks.append("incident_repeat_risk")
    if not launch.get("owners_defined", False):
        risks.append("owner_gap")
    if not risks:
        risks.append("mixed_or_unclear")
    return list(dict.fromkeys(risks))

def blockers_for_risks(risks: list[str], launch: dict[str, Any]) -> list[str]:
    blockers = []
    if "dependency_unresolved" in risks:
        blockers.append("Critical dependency remains unresolved for this launch")
    if "rollout_scope_too_broad" in risks and ("dependency_unresolved" in risks or "qa_coverage_gap" in risks):
        blockers.append("Broad rollout is not justified given current risk coverage")
    if "qa_coverage_gap" in risks and "checkout" in launch.get("title", "").lower():
        blockers.append("Critical checkout QA coverage is incomplete")
    if "owner_gap" in risks:
        blockers.append("Mitigation ownership is unclear")
    return blockers

def mitigation_suggestions(risks: list[str]) -> list[str]:
    out = []
    if "dependency_unresolved" in risks:
        out.append("Resolve or explicitly mitigate dependency risk before broader rollout")
    if "rollout_scope_too_broad" in risks:
        out.append("Phase rollout with clear guardrails instead of immediate full exposure")
    if "qa_coverage_gap" in risks:
        out.append("Close critical QA gaps and document what remains untested")
    if "monitoring_gap" in risks:
        out.append("Define monitoring, alerting, and rollback criteria before launch")
    if "incident_repeat_risk" in risks:
        out.append("Tie launch readiness to mitigation of the recent incident class")
    if "owner_gap" in risks:
        out.append("Assign mitigation owners before launch review")
    return out[:6]

def readiness_band(risks: list[str], blockers: list[str]) -> str:
    if blockers:
        return "low"
    if any(r in risks for r in ["dependency_unresolved", "qa_coverage_gap", "incident_repeat_risk"]):
        return "medium"
    return "high"

def memo(launch: dict[str, Any], readiness: str, blockers: list[str]) -> str:
    title = launch.get("title", "Launch")
    if blockers:
        return f"{title}: readiness is {readiness}. One or more blocker-worthy conditions require human review before any launch decision."
    return f"{title}: readiness is {readiness}. Risks are visible but no explicit blockers were detected in the current evidence."
