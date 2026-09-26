# Preparation evidence

Prepared on 2026-09-26 before constructing a candidate. The fixed corpus has
118 distinct legal two-visit instances: 18 hand-labelled edge cases and 100
seeded random cases. It contains 81 YES and 37 NO source decisions, two to
six tasks in random cases and one to three in edge cases. Applied to the
same deadlines, the three-visit target oracle finds 67 YES and 51 NO cases.
The generator and seeds are in `generate_cases.py`; expected source outputs
are in `cases.json`.

Z3 4.16.0 uses one integer position for every visit, constrains all positions
to be distinct in `1..nk`, orders each task's visits, and enforces the first
position and successive-gap bounds. A satisfying model yields precisely a
schedule and every valid schedule satisfies the constraints. Returned words
are checked again by direct counting and gap inspection. UNSAT is conclusive;
unknown is an error. Independent backtracking over schedule words agreed
with Z3 on 110 source and target instances with one to three tasks and
deadlines one to five. Hand fixtures cover repeated deadlines, no-solution,
first-visit and gap violations, and no final-tail requirement.

[Definition 4 of the primary paper](https://arxiv.org/html/2507.11681v2)
specifies the schedule's positions and the beginning at position zero.
During corpus construction, the hand label for `[2,3,3]` was corrected from
YES to NO: deadline two forces the first task's two visits among the first
three positions; the other two tasks both need first visits by position
three, which is impossible. This happened before the corpus was committed.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/three-visits-scheduling/work/check.py --self-test
```

The self-test begins with the corpus gate, regenerates seeded cases,
rechecks labels and returned schedules, and compares both visit oracles
against backtracking. The candidate runner uses separate forward and
recovery subprocesses and up to three three-visit schedules per case. An
incorrect injected candidate was rejected after target solving and source
validation. No actual reduction candidate exists; these finite checks do
not establish hardness or a general reduction.
