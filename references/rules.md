# Stable rules

IDs are stable. H rules protect correctness and evidence; P rules require a
current purpose; Q rules guide maintainability. These categories are separate
from development/evidence routes T-0 through T-3. Apply rules to the requested scope,
not unrelated pre-existing code. Record reasons in conversation, not extra files.

## Hard gates

- **H-01 Guarantee before code.** State the guarantee, input domain, assumptions,
  and development route before implementation. For T-3, specify the contract and
  theorem before implementing the core. Read-only investigation needs no prior
  Guarantee Read; concise declarations are sufficient for simple tasks.
- **H-02 Investigate before editing.** Trace relevant callers, data flow, and
  checks. Scale investigation to scope; do not demand nonexistent callers for docs.
- **H-03 Never silence diagnostics to hide a defect.** Fix the cause. Casts,
  suppressions, unsafe operations, and assertions require a valid language/domain
  reason and evidence for their preconditions. A demonstrably incorrect diagnostic
  may receive a narrowly scoped suppression with its reason; moving a cast or
  weakening validation merely to pass a check is forbidden.
- **H-04 Never hide failure.** Do not turn an unexpected error into a plausible
  success value. Expected absence may be represented explicitly. A catch at an
  application boundary is valid when it preserves failure semantics and necessary
  diagnostics; broad catches are not automatically defects.
- **H-05 Every hunk serves the guarantee.** No drive-by changes. Necessary
  supporting edits count when their connection to the guarantee is explained.
- **H-06 Never game evidence.** Do not weaken, skip, or delete tests merely to get
  green. When the requirement changed or a test is wrong, explain that mismatch
  and update it with replacement coverage for the changed behavior. Avoid implementation-mirror
  assertions; choose relevant failure/boundary cases rather than demanding them
  mechanically for every test. Likewise, do not weaken a theorem, narrow supported
  inputs, add assumptions, or omit an obligation merely to make a proof pass.
  Expose a real requirements change for review rather than changing the target silently.
- **H-07 Comments must earn their place.** Do not add narration, decoration,
  apologies, signature echoes, or comments restating obvious code. Prefer names
  and structure. Keep necessary intent, constraints, workarounds, public API
  contracts, legal notices, tool directives, and subtle invariants. Use the shortest
  explanation that conveys the necessary facts; no arbitrary line limit.
- **H-08 Establish evidence before claiming completion.** T-0 may use inspection/static checks.
  Behavioral changes need the applicable T-1/T-2/T-3 evidence. Exercise an integration
  boundary when it is relevant to the change; a pure helper need not invent one.
  For T-3, the Lean implementation must satisfy the promised whole-function theorem
  before the production core is derived or changed; a helper lemma alone is not
  completion. Missing execution capability is BLOCKED, never a fabricated PASS.
- **H-09 Proportionate scope.** Prefer the local fix. A recurring root cause,
  simpler structural solution, impossible local fix, or design forcing repetition
  can justify restructuring. Explain the criterion. Obtain scope direction when
  the change exceeds authorization; split independently useful refactors.
- **H-10 Formal decision gate.** For a high-stakes formalizable core as defined in
  `SKILL.md`, present the spec, English/Lean whole-function theorem, assumptions,
  and non-vacuity evidence. Wait for approval of formal development or explicit
  acceptance of a lower-route fallback before implementing the deliverable core.
  Spec/proof exploration may precede approval. Ordinary T-3 work does not require
  this pause solely because it uses Lean; present its contract and proceed within
  scope. Material changes to an approved contract or assurance level require a
  renewed decision, not a silent weakening. Reuse an existing explicit approval
  when it covers the unchanged contract, assurance level, and current work scope.
- **H-11 Evidence over claims.** Name commands and results for execution claims;
  cite paths/observations for inspection claims. Distinguish mocked, static, and
  live checks. Never invent results, benchmarks, coverage, or proof guarantees.
- **H-12 Security-sensitive changes get a focused hunting pass.** For auth,
  sessions, crypto, deserialization, parsers, file/network/process boundaries,
  webhooks, IAM, or infrastructure, read `security-audit/ATTACK-CLASSES.md` and
  applicable class files. Use `references/security-review.md` for execution and
  reporting boundaries. Resolve or explicitly triage findings; an unresolved
  in-scope defect is not a PASS. Do not claim general safety from a narrow test.

## Purpose gates

- **P-01 New abstraction.** Name the current responsibility or duplication it
  removes. Indirection that only relocates code fails. One-implementation interfaces
  and forwarding wrappers can be justified by a real boundary or contract.
- **P-02 New dependency.** Explain the requirement existing dependencies and the
  standard library cannot adequately meet, and the complexity it replaces.
- **P-03 New option.** A flag, parameter, or environment variable must serve a
  concrete current need rather than defer a decision or anticipate imagined callers.
- **P-04 Retry/resilience.** Name the transient failure, bound attempts/time, and
  explain safe replay/idempotency. Do not conceal deterministic failures. A transient
  network failure is a legitimate reason a retry can change the outcome.
- **P-05 Formal scope.** Prove the complete needed behavior of the scoped function
  or component, not just a convenient lemma. Avoid unnecessary theorem generality
  or whole-system formalization. Trace the spec to intent, keep its definitions
  independent enough to expose implementation mistakes, and state assumptions and
  the model/production boundary. More agent work is justified by useful assurance,
  not by proof volume.
- **P-06 Wider diff.** Explain necessary supporting files outside the initial
  component. Unrelated work still fails H-05; a reason does not waive task scope.

## Quality locks

- **Q-01 Names convey responsibility.** Rename misleading or ambiguous names when
  in scope; signatures need not explain every implementation detail.
- **Q-02 Cohesive functions.** One coherent responsibility; split when it improves
  comprehension, not to meet a line count.
- **Q-03 Control-flow clarity.** Prefer early exits and shallow nesting. More than
  three levels is a review prompt, not an automatic defect; explain justified cases.
- **Q-04 Actionable errors.** Preserve enough context for callers/operators to
  distinguish and address failures without leaking sensitive data.
- **Q-05 Clean delivery diff.** Remove accidental debug output, dead code, and
  leftover scaffolding introduced by the change. Do not clean unrelated user work.
- **Q-06 State the formal-first route.** Name the T route and why it fits the
  guarantee. For behavioral work, explain why a useful T-3 core is selected or
  unsuitable before falling back. One concrete reason is enough; do not invent a
  theorem for a cosmetic edit. Name changed assurance and remaining gaps. Missing
  tools can justify a disclosed initial fallback for ordinary work, but cannot
  bypass H-10 or silently replace a requested/agreed proof.
- **Q-07 Teaching checks.** For a demonstrated recurring mistake, prefer an existing
  check or a small durable guard. Explain the repair in its error message. Add a new
  local checking mechanism only when recurrence and impact justify its maintenance; otherwise
  state why the existing check or scoped regression test is sufficient.
- **Q-08 Reviewer comprehension.** Organize the assurance package around the human's
  questions: intended semantics, theorem adequacy, assumptions, and production
  suitability. Make claim-to-evidence links easy to locate without asking the
  reviewer to re-derive the algorithm from a port. No arbitrary reading-time limit.
