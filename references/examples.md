# Reference scenarios

These are behavioral acceptance scenarios, not claims of completed work. Use
them to evaluate formal-first ordering, useful assurance, scope, and reporting.
Run them through a harness's native loader or direct-file route. Judge behavior
and evidence, not tool-name equality. See `references/harnesses.md` for discovery
and activation smoke checks. No automated model evaluation is implied.

## Ordinary precise algorithm: T-3 without a mandatory pause

The user requests a finite-set normalization routine with a precise equivalence
contract. A small Lean implementation and suitable lemmas are available, and
proof work is proportionate. Investigate callers, state the guarantee, present
the abstract set specification and theorem, then implement/prove the reference
before porting. Review ordering/duplicate semantics and differential-test the port.
Do not reject T-3 merely because failure is not expensive. Do not introduce an
approval pause solely because the implementation uses Lean.

Expected review package: intended equivalence, domain and ordering assumptions,
whole-function theorem, accepted proof, and separately labeled port evidence.

## High-stakes pure arithmetic: H-10 applies

A billing computation has a precise contract, a modelable core, and substantial
financial consequences. Present the proposed spec, English/Lean theorem, units,
rounding behavior, input domain, and witness inputs. Wait for approval of
formal work or an explicit fallback decision before implementing the core.

If Lean is unavailable, disclose that blocker and the proposed T-2 evidence;
do not silently treat tools as a reason to bypass H-10. If approved, implement
and prove the reference before changing the production core. Review integration
and port correspondence separately from the arithmetic theorem.

## Numerical core: a plausible error must violate the guarantee

A time-based numerical routine uses large absolute timestamps and small offsets.
Define the ideal mathematical result independently from the binary64 evaluator,
and state the required error bound and supported inputs. Challenge converting
timestamps before subtraction versus subtracting exactly first. A real-arithmetic
identity is not a floating-point proof. The theorem must cover the actual evaluator
and useful whole-function outcomes, not just its ideal recurrence.

Do not assume an error bound transfers to physical measurement accuracy. Port
checks preserve operation order and use justified output comparison semantics.

## Tautological proof: not an assurance package

An agent defines `spec := implementation` and proves reflexive equality, or proves
a helper's identity while leaving the delivered evaluator unconstrained. Even if
the build and axiom audit pass, reject the adequacy claim under P-05/H-08. Recover
the intended semantic contract and prove the relevant connection. Do not add an
axiom or exclude troublesome valid inputs to make the obligation disappear (H-06).

## Local parser integration bug: reasoned T-2 fallback

The defect is at a framework decoding boundary with no tractable faithful Lean
model in the task's scope. It does not meet H-10's high-stakes condition. State
that concrete formal-fit reason, define accepted/rejected input properties with
useful generators, add the regression case, and fix locally. Perform the
H-12 focused parser review. Do not formalize a disconnected toy parser and imply
it proves the framework path. Escalate if investigation reveals high-stakes impact.

## UI interaction: T-1, not forced formalization

The user requests a focus/keyboard interaction change. The changed behavior is
browser interaction, not an algorithmic core. State that reason, define the
observable behavior, and exercise the relevant local interaction/regression checks.
Do not introduce Lean scaffolding or claim that a pure-state model alone proves
the browser integration.

## Documentation correction: T-0

The user asks to repair a command in a README. Read the actual CLI definition,
state the non-behavioral guarantee, edit the command, and inspect it against the
source or run the relevant help/parser check. Do not invent an integration flow,
proof package, or review artifact. Report only the evidence actually obtained.

## Changing a verified component

For an implementation bug, preserve the intended contract, repair the reference
and proof first where affected, then update the port and relevant tests. If the
requirement changes, review the new contract and assumptions first; renew H-10's
decision when applicable. Do not keep a green build by unregistering an obligation.
A port-only bug need not change an already-correct formal reference: use its
existing proof and rerun the relevant differential and integration checks.

## Review followed by fixes

A review-only request produces numbered impact-ranked findings. Inspect formal
specifications and theorem adequacy where present, without inferring historical
workflow violations from source alone. User says “fix 1 and 3”: implement those
under DURING rules without demanding another blanket approval. H-10 still applies
if the authorized work needs a new high-stakes contract decision. Leave finding 2
and unrelated cleanup untouched.

## Blocked proof or integration evidence

An agreed whole-function proof is unfinished, although useful helper lemmas pass.
Report BLOCKED with the unresolved obligation; do not move to a production port
and label T-3 complete. Propose a scope/contract decision or fallback without
silently weakening the promise.

Likewise, if focused tests pass but a required integration fixture cannot start,
report the command and gap as BLOCKED. Distinguish environment problems from
demonstrated code defects. Partial evidence is useful; it is not a completion claim.

## Harness without a skill tool or subagents

Read the entry at the installed path through an available file tool and perform
S1–S6 in the current agent. Formal-first does not require a separate prover agent.
Do not fabricate a skill/delegation API. For a full security audit requiring an
independent verifier, use an available fresh isolated session meeting the audit
contract or report incomplete coverage. Rewording the hunter as a “verifier” does
not create independence.
