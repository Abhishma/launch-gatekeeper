
from launch_gatekeeper.pipeline import review_launch

def test_abstain_on_missing_qa_and_rollout():
    launch = {
        "launch_id": "T-1",
        "title": "Policy update",
        "prd_summary": "Update policy messaging and flows.",
        "qa_summary": "",
        "rollout_plan": "",
        "dependency_notes": "",
        "incident_context": "",
        "owners_defined": False
    }
    report = review_launch(launch)
    assert report["status"] == "abstained"

def test_detects_broad_rollout_risk():
    launch = {
        "launch_id": "T-2",
        "title": "Checkout change",
        "prd_summary": "Redesign checkout payment step.",
        "qa_summary": "Core happy path tested. Promo edge cases not fully covered.",
        "rollout_plan": "Roll out to 100% immediately.",
        "dependency_notes": "Payment migration still in progress.",
        "incident_context": "Recent payment incident.",
        "owners_defined": True
    }
    report = review_launch(launch)
    assert "rollout_scope_too_broad" in report["risks"]
