# Prepared input and output contract

Both source and target inputs use `{"deadlines": [d0, ...]}`: a nonempty
nondecreasing list of positive integer deadlines. Tasks are indexed from
zero; repeated deadlines are distinct tasks. The source requires two visits
per task and the target requires three. An output is `{"schedule": [task,
...]}`, a word of length `n*k` containing each task exactly `k` times.
Positions start at one. A task's first position is at most its deadline,
and the difference between each successive pair of its positions is at
most its deadline. No condition is imposed after its last visit.
`{"status": "NO-SOLUTION"}` is valid exactly when no such word exists.

A candidate `algorithm.py` reads one source JSON object from stdin and writes
one legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes one valid
two-visit source output. The processes share no memory, exit nonzero on
errors, and send diagnostics to stderr. They must be deterministic and
polynomial time, and recovery must work for every valid three-visit output.

`check.py --candidate PATH` independently solves each constructed target on
the fixed source corpus and directly validates recovered source schedules.
