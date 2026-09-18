---
name: no-slop-engineering
description: >-
  Apply to every coding, debugging, refactoring, and code-review task in the
  configured scope. Use formalization-first development for suitable cores:
  intent, precise specification, Lean implementation and proof, then checked
  production targets. Fall back deliberately to properties, examples, or review.
  Deliver scoped code with an evidence-backed assurance package.
license: MIT
---

# No-Slop Engineering (NSE)

NSE is a harness-agnostic, formalization-first engineering system. Its central
question is: **what must be true, and what evidence would let a human review that
claim without reconstructing correctness from generated production code?**

For a suitable core, develop in this order:

**Human intent → precise specification and theorem → Lean implementation + proof
→ production target + boundary checks → assurance package.**

Lean is the development language for that core. The proof obligation shapes the
implementation; it is not a certificate added after production coding. Prefer a
whole-function guarantee over an easy lemma unrelated to delivery.
Humans review intent, specifications, assumptions, and guarantees; agents carry
out implementation, proof search, and checked ports. Production integration and
maintainability still need review.

Formalization-first is the default question, not a demand to prove every edit.
Keep the component and effort proportionate. YAGNI applies equally to abstractions,
tests, proof generality, dependencies, and reporting. Load this entry through native
Agent Skills discovery or read it through the harness's project instructions.

## Activation and paths

NSE's intended policy is always-on for coding, debugging, refactoring, and review
within the configured project/user scope. Setup requires both the package and the
pointer from **adapters/activation.md** in automatically loaded instructions.
Discovery alone is incomplete setup for that policy. Use the harness's native
skill loader when available, or read this file through its ordinary file tools.
Reuse instructions already in context; reread them if context loss requires it.
Installation routes are documented in **references/harnesses.md**; they do not
change the engineering rules.
Higher-priority instructions, tool permissions, and explicit task scope apply.
Only actual checks enforce machine-checkable rules; prose cannot grant permissions.

Resolve `SKILL_DIR` to the directory containing the loaded `SKILL.md`, using its
actual file path or loader-supplied base directory. Resolve `PROJECT_DIR` separately
to the target checkout. These are path labels, not automatically set environment
variables; set them explicitly before shell examples. Supporting paths are relative
to `SKILL_DIR`, never implicitly to the checkout. Read **references/rules.md**
before work. Load other references only for the applicable mode or verification method.

Use available equivalents for reading, editing, searching, command execution,
and user questions; no named tool, API, model, or plugin is required. Ordinary
work runs in one agent. Load **references/capabilities.md** when a needed tool is
missing or a workflow requires independent verification. Missing capabilities
are explicit evidence gaps, not permission to invent tool calls or lower a gate.

## Modes

- **DURING:** implement a requested change through S1–S6.
- **AFTER:** review existing work using **references/review-protocol.md**. Report
  findings before editing. A request to fix findings authorizes that scope;
  do not require another approval when the user already gave it.
- **SECURITY:** read **references/security-review.md**. Focused security questions
  use guidance mode; explicit full audits use the bundled six-phase workflow.

## The factory model

One change is one unit. Keep the stations, scale their effort to the task.
**Gates stop completion**, not honest communication about a defect or blocker.
**Poka-yoke:** recurring mistakes merit a proportionate teaching check (Q-07).
**Jidoka:** run local checks that stop completion when a guarantee fails; add
checks when their value justifies maintenance. **Standard parts:** reuse suitable
existing code, specifications, lemmas, and checks instead of creating parallel systems.

## Stations

1. **S1 Intake:** identify the requested behavior, component, and stakes.
2. **S2 Investigation:** trace relevant callers, data flow, and existing checks.
   Classify as local bug, architectural problem, or correct behavior. Unfamiliar
   is not wrong. Find the smallest useful formal boundary without forcing a rewrite.
3. **S3 Guarantee Read:** before implementation, specify:
   `Guarantee: <behavior over inputs, assumptions, and exclusions>. Route: <T-3/T-2/T-1/T-0> because <reason>.`
   For T-3, present the spec and whole-function theorem in English and Lean before
   implementing the core. Apply H-10 when human approval is required.
4. **S4 Develop the reference:** for T-3, implement and prove in Lean together;
   let failed obligations expose design mistakes. Establish the promised theorem
   before deriving or modifying the production core. For fallbacks, establish
   properties or regression expectations before/alongside the smallest local fix.
5. **S5 Integrate and check:** port a proved reference where needed; differential-test
   the port and exercise relevant shell/integration behavior. Recheck the proof
   after changes. Distinguish proved facts, tested agreement, and unverified assumptions.
6. **S6 Deliver assurance:** read **references/assurance-package.md** and
   **references/delivery-gate.md**. Give the reviewer a concise map from intent
   to specification, guarantee, implementation, evidence, and remaining gaps.

No decision logs, review files, or telemetry are created for ordinary tasks.
Normal implementation files and justified tests/checks remain allowed. T-3 adds
the agreed formal package; full security audits use their own artifacts.

## Formal-first route selection

For a behavioral change, consider T-3 first: can a **precisely defined
component** be developed and proved with proportionate effort using available or
justified tooling? Favor it when precise semantics, reusable lemmas, or subtle
edge cases make the formal artifact a better review object. High stakes strengthen
the case but are **not a prerequisite**. A well-defined ordinary algorithm can qualify.
Do not create a Lean package for an obvious edit merely to claim a higher tier.

If formalization is not a useful fit, state the concrete reason and fall through
to T-2, then T-1. Non-behavioral changes can go directly to T-0. A reason such as
“DOM interaction is the changed behavior; the math core is untouched” is useful;
“this is not safety-critical” alone does not explain why a tractable proof is unsuitable.

The existing T IDs describe development/evidence routes, not a claim that a proof
supersedes every kind of test. Choose per component: a T-3 core may have a T-1 shell.

| Route | Development artifact | Appropriate scope |
|---|---|---|
| T-3 | Precise spec, executable Lean core, whole-function proof, checked production target | A tractable formal core with a useful reviewable guarantee |
| T-2 | Explicit properties, meaningful generators/oracles, example and boundary checks | A useful invariant where formal development is unsuitable or an accepted fallback |
| T-1 | Behavioral examples/regressions; TDD where useful | Example-shaped behavior or integration with external systems |
| T-0 | Inspection or relevant static evidence | Documentation, cosmetic, or trivial non-behavioral edits |

### H-10: when to stop for a human decision

The mandatory decision gate applies when the changed core has a precise or
statable contract, can be modeled as deterministic computation or explicit state
transitions, **and** failure has substantial financial, security, safety, or
data-integrity consequences. Tool unavailability or uncertain proof cost does not
exempt that core: present the proposed spec, theorem, assumptions, and non-vacuity
evidence; obtain approval of formal work or explicit acceptance of a fallback.
An existing explicit approval covering the unchanged contract, assurance level,
and current work scope satisfies the gate; do not ask for the same decision again.

For ordinary tractable T-3 work already within scope, present the same review
material and proceed without an additional approval ritual unless the user asks
for one. Resolve genuine ambiguity or scope/budget changes before proceeding.
Never silently downgrade a user-requested or already-agreed proof deliverable.
Read **references/formal-verification.md** before T-3 work or an H-10 decision.

## Delivery summary

Report the result, meaningful changes, commands/observations supporting it, and
remaining gaps. Use **PASS**, **FAIL**, **BLOCKED**, or **N/A** precisely. Only
applicable passing gates justify a completion claim. A concise blocked report
is a valid terminal response; it is not a completed implementation.

Run verification through the harness's local terminal or process tools. No hosted
pipeline, GitHub account, or runner service is required. Resources are bundled
locally; toolchain provisioning, existing project dependencies, and optional
Mathlib can require network access. See the formal reference for that boundary.
