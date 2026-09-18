# AFTER mode

1. Read the intended behavior, relevant callers, data flow, tests, and requested
   diff or component. Where formal artifacts exist, review the spec and theorem
   before reconstructing behavior from the production implementation. Use
   `references/assurance-package.md` to separate claims and evidence boundaries.
2. Report numbered actionable findings with impact, rule ID, file:line, evidence,
   and a focused recommendation. Distinguish confirmed defects from questions.
3. Rank by consequence and likelihood, not H/P/Q category:
   - **High:** likely correctness, security, data-integrity, or delivery failure.
   - **Medium:** real reliability or maintenance cost in the reviewed scope.
   - **Low:** localized clarity or consistency issue with a concrete benefit.
4. Keep preferences and uncertain hypotheses out of the defect list. Do not
   infer historical violations (such as a missing pre-edit Guarantee Read) from
   source alone. Existing abstractions do not require retroactive paperwork.
5. A review-only request authorizes findings, not edits. If the user asks to fix
   identified findings, apply DURING mode to that scope. If they select numbers,
   leave unselected findings alone. No repeated approval ritual is needed.

## Diagnostic prompts, not a ban list

Look for casts masking invalid assumptions, success-shaped error fallbacks,
configuration for nonexistent callers, forwarding layers without responsibility,
misleading names, unexplained dependencies, deterministic retry loops, unrelated
cleanup, weakened tests, and comments that narrate instead of explain.

For proofs, distinguish an unsatisfiable precondition from a theorem with **no**
hypotheses: an unconditional theorem is not inherently vacuous. Check that the
conclusion establishes the promised property under satisfiable assumptions.
Trace the theorem to the actual evaluator, not just a helper; check whether the
caller establishes its preconditions. Review numeric representations, rejection
behavior, and production-port correspondence. An axiom-audit PASS is not evidence
that every needed obligation was specified. Missing historical formalization-first
ordering cannot be inferred from a finished diff, and absence of a proof alone is
not a retrospective defect in code whose agreed contract did not require one.
