# Delivery Gate

Run all applicable checks internally. Report a concise evidence summary, not a
line per rule. Deliver the review map in `references/assurance-package.md`, not
just a checklist result. The coordinating agent owns the final assessment, even
when checks were delegated. Existing project requirements still apply.

| Status | Meaning |
|---|---|
| PASS | Applicable requirement satisfied by identified evidence |
| FAIL | Evidence demonstrates an unresolved in-scope defect |
| BLOCKED | Required evidence or decision is unavailable |
| N/A | Requirement does not apply; give a brief reason when not obvious |

Inspect all five blocks:

1. **Hard gates:** Guarantee Read and investigation precede implementation
   (H-01/H-02); no hidden diagnostics/errors, unrelated edits, manipulated tests,
   gratuitous comments, or unjustified scope changes (H-03–H-09). Formal decisions
   precede high-stakes core implementation where H-10 applies. Claims match
   evidence (H-11). A passing test/proof was not obtained by weakening the contract.
2. **Purpose:** reasons exist for new abstractions, dependencies, options,
   resilience, proof scope, and wider supporting changes (P-01–P-06).
3. **Quality:** names, cohesion, control flow, errors, diff cleanliness, tier
   rationale, recurrence checks, and reviewer comprehension are sound (Q-01–Q-08).
4. **Assurance:** the route was selected formal-first, with a concrete fallback
   reason when applicable. T-0 has inspection/static evidence; T-1 relevant
   behavioral examples; T-2 meaningful properties/generators/oracles and results.
   T-3 has a spec traced to intent, adequate whole-function theorem, satisfiable
   assumptions, executable reference, accepted proof and axiom audit, and local
   format checks. The proved reference preceded production-core derivation/change.
   Port and shell checks address their separate boundaries. The human-facing
   package distinguishes proved guarantees, sampled agreement, and assumptions.
   Review scope/coverage; an easy lemma or an empty/vacuous guarantee does not pass.
5. **Security:** H-12 review and findings disposition for sensitive surfaces;
   otherwise N/A. Source inspection is legitimate evidence for source claims,
   but does not establish unobserved runtime/deployment behavior.

Repair failures within scope and rerun affected checks. Do not silently broaden
scope to fix unrelated baseline failures. When blocked, stop with the exact gap
and next action; do not imply the change is fully verified. Do not suppress a
FAIL/BLOCKED report merely because completion is not possible.

Example behavioral delivery:

> PASS: malformed records now produce the documented error. Added a focused
> regression test; `pytest tests/test_records.py` passed (8 tests). Existing
> `pytest tests/integration/test_import.py` passed (2 tests). H-12 parser review
> found no additional in-scope issue. No broader security claim is made.

Example blocked delivery:

> BLOCKED: source changes and local unit tests are complete (`npm test -- parser`,
> 12 passing), but the required service integration check could not run because
> its local fixture is unavailable. Completion requires that check.
