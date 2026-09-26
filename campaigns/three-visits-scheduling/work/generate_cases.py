"""Fix seeded 2-Visits deadline instances before constructing a reduction."""

import json
import random
from pathlib import Path


EDGE_CASES = [
    ([1], True), ([2], True), ([10], True),
    ([1,1], False), ([1,2], False), ([2,2], True),
    ([1,3], True), ([1,4], True), ([2,3], True),
    ([1,1,1], False), ([3,3,3], True),
    ([1,2,3], False), ([1,3,3], False), ([2,2,3], False),
    ([2,3,3], False), ([2,3,4], True), ([1,2,6], False),
    ([1,3,6], True),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(2,6)
    if seed % 2 == 0:
        deadlines = sorted(rng.randint(n,3*n) for _ in range(n))
    else:
        deadlines = sorted(rng.randint(1,n+1) for _ in range(n))
    return {"deadlines":deadlines}


def build_cases():
    from check import solve_visits
    cases, seen = [], set()

    def add(source, kind, seed=None, hand_answer=None):
        key = json.dumps(source,sort_keys=True,separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_visits(source,2)
        if hand_answer is not None and ("schedule" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for deadlines, expected in EDGE_CASES:
        add({"deadlines":deadlines},"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
