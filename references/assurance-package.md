# The assurance package

Deliver code with a reviewable account of **what it means, what is established,
and where that assurance ends**. The package is the existing source/proof/test
artifacts plus a concise conversation summary with paths and evidence. It is not
a new report file, archive, dashboard, or telemetry requirement. Ordinary tasks
still create no process artifacts. Keep persistent T-3 proofs beside the project.

## Organize around the human's review questions

| Review question | T-3 evidence to point to |
|---|---|
| Does this express the intended behavior? | Source requirement and recognizable formal specification; units, domain, errors, exclusions |
| Is the promise sufficient? | English and Lean whole-function theorem; satisfiable hypotheses, witnesses/boundaries, rejected counterexamples |
| Does the reference satisfy it? | Executable Lean definition, connecting theorem, local build and axiom-audit result |
| Does the deployed code correspond? | Port mapping, differential checks, language-specific review, actual input/output boundary tests |
| Is this maintainable and reproducible? | Scoped diff, clear names, local commands, toolchain/dependency identity, remaining assumptions |

Reviewing theorem adequacy is different from replaying its proof. A kernel-checked
proof supports the Lean claim; it does not establish that the claim is the one
the user needs. Registered theorem names are pointers, not a completeness metric.
The axiom checker enforces its dependency policy, not specification quality.

## Keep the assurance boundary explicit

Separate three layers in reports:

1. **Proved:** the exact Lean implementation, theorem, domain, and assumptions.
2. **Tested:** properties, port agreement, boundary checks, and concrete runs.
3. **Assumed or unresolved:** model fidelity, external state, runtime/compiler
   correspondence, unavailable checks, and anything outside the theorem.

Never report the whole application as verified because one core has a proof.
Never report a source-only observation as an executed check. Explain the exact
loss of assurance for a fallback; do not rename passing tests as proof.

## Scale the package to the development route

- **T-3:** spec + executable reference + whole-function proof + axiom audit +
  checked production target (if any) + relevant shell evidence. Each major claim
  points to the actual declaration/file and run that supports it.
- **T-2:** a precise property, why formal development was unsuitable or declined,
  generator domain, independent oracle or invariant, boundary examples, actual
  results, and the limits of sampling. No Lean package is required.
- **T-1:** the concrete behavioral contract, why examples/integration fit better,
  focused regression cases and executed checks, with their limitations.
- **T-0:** the non-behavioral guarantee and inspection/static evidence. A short
  paragraph is normally sufficient; do not construct a proof-review ceremony.

Mixed changes can use different routes per component. Do not assign the whole
change T-3 because a small helper was proved while the important behavior was not.

## Final response shape

Lead with the outcome and applicable PASS/FAIL/BLOCKED status. Then explain, as
briefly as the task permits:

- **Guarantee and scope:** the behavior, route, and important assumptions.
- **Review points:** locations of the spec/theorem/reference or test contract.
- **Evidence:** commands and observed results, distinguishing proof from sampling.
- **Boundary and gaps:** what remains assumed, untested, or blocked.

This is a content guide, not a mandatory four-heading template. The Delivery Gate
checks completeness; the human-facing summary makes the useful evidence easy to review.
