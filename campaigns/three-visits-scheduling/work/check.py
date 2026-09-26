"""Exact 2-Visits and 3-Visits schedule oracles."""

import argparse
import json
import subprocess
import sys
from collections import Counter
from itertools import product
from pathlib import Path

import z3


def legal_instance(instance):
    if not isinstance(instance, dict) or not isinstance(instance.get("deadlines"), list):
        return False
    deadlines = instance["deadlines"]
    return (bool(deadlines) and all(type(d) is int and d > 0 for d in deadlines)
            and deadlines == sorted(deadlines))


def direct_schedule(instance, visits, schedule):
    if not legal_instance(instance) or not isinstance(schedule,list):
        return False
    deadlines = instance["deadlines"]
    n = len(deadlines)
    if len(schedule) != n*visits or any(type(task) is not int or not 0 <= task < n for task in schedule):
        return False
    if any(count != visits for count in Counter(schedule).values()):
        return False
    last = [0]*n
    for position, task in enumerate(schedule,1):
        if position-last[task] > deadlines[task]:
            return False
        last[task] = position
    return True


def visit_solutions(instance, visits, limit=3):
    if not legal_instance(instance) or visits not in (2,3):
        raise ValueError("Illegal finite-visit instance")
    deadlines = instance["deadlines"]
    n = len(deadlines)
    positions = [[z3.Int(f"p_{i}_{j}") for j in range(visits)] for i in range(n)]
    flat = [position for row in positions for position in row]
    solver = z3.Solver()
    solver.add(z3.Distinct(*flat))
    for i,row in enumerate(positions):
        for position in row:
            solver.add(position >= 1, position <= n*visits)
        solver.add(row[0] <= deadlines[i])
        for before,after in zip(row,row[1:]):
            solver.add(before < after, after-before <= deadlines[i])
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive visit solver: {result}")
        model = solver.model()
        schedule = [None]*(n*visits)
        for i,row in enumerate(positions):
            for position in row:
                schedule[model.eval(position).as_long()-1] = i
        if not direct_schedule(instance,visits,schedule):
            raise AssertionError("Z3 schedule violates direct validation")
        outputs.append({"schedule":schedule})
        solver.add(z3.Or(*[position != model.eval(position) for position in flat]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_visits(instance, visits):
    return visit_solutions(instance,visits,1)[0]


def valid_visits(instance, visits, output):
    if not legal_instance(instance) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_visits(instance,visits) == output
    return set(output) == {"schedule"} and direct_schedule(instance,visits,output["schedule"])


def exhaustive_visits(instance, visits):
    deadlines = instance["deadlines"]
    n = len(deadlines)
    counts, last, schedule = [0]*n, [0]*n, []

    def search():
        if len(schedule) == n*visits:
            return list(schedule)
        position = len(schedule)+1
        for task in range(n):
            if counts[task] == visits or position-last[task] > deadlines[task]:
                continue
            old = last[task]
            counts[task] += 1
            last[task] = position
            schedule.append(task)
            result = search()
            if result is not None:
                return result
            schedule.pop()
            last[task] = old
            counts[task] -= 1
        return None

    found = search()
    return {"schedule":found} if found is not None else {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for deadlines, expected in EDGE_CASES:
        assert ("schedule" in solve_visits({"deadlines":deadlines},2)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_visits(source,2)
        assert ("schedule" in current) == ("schedule" in case["expected"])
        assert valid_visits(source,2,current) and valid_visits(source,2,case["expected"])
    test_hand_cases()
    checked = 0
    for n in range(1,4):
        for deadlines in product(range(1,6),repeat=n):
            if tuple(sorted(deadlines)) != deadlines:
                continue
            instance = {"deadlines":list(deadlines)}
            for visits in (2,3):
                assert ("schedule" in solve_visits(instance,visits)) == ("schedule" in exhaustive_visits(instance,visits))
                checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive visit instances")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_instance(target):
            raise AssertionError(f"Illegal 3-Visits target: {target}")
        for output in visit_solutions(target,3):
            if not valid_visits(target,3,output):
                raise AssertionError(f"Target oracle returned invalid output: {output}")
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_visits(source,2,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
