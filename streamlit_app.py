
from __future__ import annotations
from pathlib import Path
import streamlit as st

from launch_gatekeeper.pipeline import review_launch
from launch_gatekeeper.utils import load_json, load_jsonl

ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
GOLDS = ROOT / "eval" / "goldens" / "launch_cases.jsonl"

st.set_page_config(page_title="Launch Gatekeeper", layout="wide")
st.title("Launch Gatekeeper")
st.caption("AI-assisted launch readiness review with blockers, missing controls, and abstention.")

example = st.sidebar.selectbox("Example launch", [
    "launch_case_01.json", "launch_case_02.json", "launch_case_03.json", "launch_case_04.json"
])
launch = load_json(EXAMPLES / example)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Launch input")
    st.json(launch)

with col2:
    st.subheader("Readiness output")
    report = review_launch(launch)
    st.json(report)
    if report["status"] == "abstained":
        st.warning("System abstained because the launch evidence is incomplete.")
    else:
        st.success(f"Review ready. Readiness: {report['readiness_band']}")
    if report["blockers"]:
        st.error("Blocker-worthy conditions detected.")

st.markdown("---")
st.subheader("Quick evaluation snapshot")
if st.button("Run eval on gold launch cases"):
    golds = load_jsonl(GOLDS)
    total = len(golds)
    risk_score = 0
    abstain_ok = 0
    rows = []
    for g in golds:
        pred = review_launch(g["launch"])
        expected = set(g["expected_risks"])
        predicted = set(pred["risks"])
        risk_score += len(expected & predicted) / max(len(expected), 1)
        ok = (pred["status"] == "abstained") == g["should_abstain"]
        abstain_ok += int(ok)
        rows.append({
            "case_id": g["case_id"],
            "predicted": sorted(predicted),
            "expected": sorted(expected),
            "status": pred["status"],
            "abstain_ok": ok
        })
    c1, c2 = st.columns(2)
    c1.metric("Risk match score", f"{risk_score/total:.0%}")
    c2.metric("Abstention accuracy", f"{abstain_ok/total:.0%}")
    st.dataframe(rows, use_container_width=True)

st.markdown("---")
st.subheader("Portfolio interpretation")
if report["status"] == "abstained":
    st.write("This refusal is a feature. The system will not invent launch readiness when the input package is incomplete.")
else:
    st.write("This repo is about making launch risk visible early, not automating launch approvals.")
