# Launch Gatekeeper

AI-assisted launch readiness review with risk registers, blocker conditions, and human sign-off.

## Why this exists

Most launch reviews are too optimistic.

Risks are scattered across docs.
Dependencies are implicit.
QA notes stay tactical.
Teams do not clearly state what should block launch.

The recurring pattern in product ops is that launch risk is distributed across PRD, QA docs, rollout plans, and dependency notes — no single artifact surfaces what should block versus what should be monitored. By the time an incident occurs, the risk was visible in the inputs but not structured for review.

**Launch Gatekeeper** turns launch inputs into:
- structured risk register
- blocker conditions
- mitigation owner suggestions
- missing control checklist
- readiness summary memo
- abstention when coverage is too weak

This tool does not make a ship/no-ship decision.
It makes launch risk visible before it becomes incident reality.

## What it does

Input:
- PRD
- QA summary
- rollout plan
- dependency notes
- recent incident context

Output:
- risk register
- blocker conditions
- missing controls
- mitigation suggestions
- readiness memo
- abstention when launch evidence is incomplete

## What it does not do

- It does not replace engineering review
- It does not decide whether to launch
- It does not guarantee complete risk coverage

## Run

```bash
pip install -r requirements.txt
export PYTHONPATH=src
python -m launch_gatekeeper.cli examples/launch_case_01.json
python -m launch_gatekeeper.eval_runner eval/goldens/launch_cases.jsonl
streamlit run streamlit_app.py
```

## Design choices

- **Risk visibility, not autonomy** — blocker conditions are structured suggestions for human review, not automated ship/no-ship decisions
- **Bounded risk taxonomy** — risk categories are constrained and auditable. v1 uses heuristic detection against a defined taxonomy. This is intentional: a bounded, evaluable heuristic is safer in a launch review workflow than a model generating generic risk prose.
- **Abstention preferred over false readiness confidence** — when key launch inputs are missing, the system abstains rather than producing a partial readiness assessment that could be misread as sufficient coverage
- **Structured outputs for human review** — the readiness memo is designed to support a human reviewer, not replace the review

## Repo structure

- `src/launch_gatekeeper/` — core implementation
- `examples/` — sample launch packages
- `schemas/` — launch input and readiness output JSON schemas
- `eval/` — rubric and evaluation harness
- `demo/` — sample outputs

## Portfolio point

This repo is about launch-risk clarity, not launch automation theater. The PM design decisions are the risk taxonomy, blocker logic, and abstention conditions — not the detection sophistication.

## Known limitations

- launch risk detection is intentionally conservative and shallow in v1 — heuristic pattern matching, not semantic inference
- readiness is a support signal, not a decision engine
- sample launch packages are synthetic and should be expanded before stronger claims
- this repo is easiest to oversell — the trust boundary must stay explicit
- next upgrade: richer risk taxonomy, semantic inference layer, real incident pattern integration

## Where automation stops

- it does not approve launches
- it does not replace engineering, QA, or release management review
- blockers are recommendations for human review
- missing launch evidence forces abstention

## Trust boundary

This project is decision support, not automation. It produces structured risk outputs for human review and abstains when launch evidence is too incomplete for meaningful risk assessment.
