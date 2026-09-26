# 2-Visits scheduling → 3-Visits scheduling

Category: Complexity open

## Source

The source gives task deadlines. Its outputs are finite schedules visiting each task exactly twice, meeting first-visit and successive-gap deadlines with no final-tail condition, or NO-SOLUTION.

## Target

A k-Visits solution is a finite word containing each task exactly k times, with its first visit and every successive same-task gap bounded by the task deadline. There is no final-tail constraint. The source has k=2 and the target k=3.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The question isolates the effect of adding one required visit in a recurring scheduling model.

## Difficulty

An extra visit must be forced into a recoverable role; arbitrary placement can invalidate decoding to two visits.

## Literature context

The finite-visit model constrains first visits and internal gaps without a final-tail condition. Periodic scheduling results therefore do not automatically apply.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Finite Pinwheel Scheduling: the k-Visits Problem](https://arxiv.org/html/2507.11681v2): Kanellopoulos et al., Finite Pinwheel Scheduling: the k-Visits Problem, arXiv:2507.11681v2, Definition 4, Theorem 8 and Section 7, defines this finite semantics and proves 2-Visits hard. Its conclusion asks about k greater than two.
- [ICALP 2026 follow-up](https://drops.dagstuhl.de/storage/00lipics/lipics-vol374-icalp2026/html/LIPIcs.ICALP.2026.122/LIPIcs.ICALP.2026.122.html): The ICALP 2026 follow-up, Section 7, Lemmas 59 and 61, Conjecture 62 and Section 8, retains the three-visit question and shows that two key two-visit structural properties fail. Its full preprint, Section 7, supplies those counterexample proofs. Variable deadlines and mixed one/two-visit tasks are different languages; their results do not settle the fixed three-visit target.
- [full preprint](https://arxiv.org/html/2604.16030v1): The ICALP 2026 follow-up, Section 7, Lemmas 59 and 61, Conjecture 62 and Section 8, retains the three-visit question and shows that two key two-visit structural properties fail. Its full preprint, Section 7, supplies those counterexample proofs. Variable deadlines and mixed one/two-visit tasks are different languages; their results do not settle the fixed three-visit target.
- [Kleinberg and Mishra (2026)](https://arxiv.org/html/2604.13974v1): The infinite Pinwheel NP-hardness question is superseded by Kleinberg and Mishra (2026), Section 4. That construction does not specify a three-occurrence horizon. No reduction from its infinite witnesses to this fixed finite language was established. Do not reuse the older infinite-open-status statements.

Fixed from board record `website/questions/three-visits-scheduling.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
