# Research instructions

Read the [fixed question](campaigns/three-visits-scheduling/question.md), [prior state](campaigns/three-visits-scheduling/state.md) and [preparation notes](campaigns/three-visits-scheduling/work/preparation.md). The fixed [test corpus](campaigns/three-visits-scheduling/work/cases.json) and [verifier](campaigns/three-visits-scheduling/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/three-visits-scheduling/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
