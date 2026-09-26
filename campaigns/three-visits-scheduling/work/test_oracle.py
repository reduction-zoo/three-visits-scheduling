from check import legal_instance, solve_visits, valid_visits


def test_hand_cases():
    assert solve_visits({"deadlines":[1]},2) == {"schedule":[0,0]}
    assert solve_visits({"deadlines":[1,1]},2) == {"status":"NO-SOLUTION"}
    assert valid_visits({"deadlines":[2,2]},2,{"schedule":[0,1,0,1]})
    assert not valid_visits({"deadlines":[1,2]},2,{"schedule":[0,1,0,1]})
    assert valid_visits({"deadlines":[2,2]},3,{"schedule":[0,1,0,1,0,1]})
    assert solve_visits({"deadlines":[1,1]},3) == {"status":"NO-SOLUTION"}
    assert not legal_instance({"deadlines":[2,1]})


if __name__ == "__main__":
    test_hand_cases()
