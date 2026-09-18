# T-3: formalization-first development

Develop a reviewable reference before production code. The deliverable is a
specification, executable Lean implementation, whole-function proof,
and appropriately checked production integration. T-3 is useful for ordinary
precise algorithms as well as high-stakes cores; the latter invoke H-10's decision
gate. The gate is not the definition of formalization-first.

## 1. Translate intent into a contract

Identify the authoritative requirement: user intent, domain equations, a protocol,
or an existing documented contract. State supported inputs, units, representations,
outputs, errors, and exclusions. Resolve ambiguity rather than selecting whichever
interpretation is easiest to prove. A source paper or existing implementation is
evidence to interpret, not automatic authority for unspoken requirements.

Keep the specification recognizable to a domain reviewer. Prefer independent
semantic definitions, such as an abstract set result or real-number expression,
over defining correctness as equality to the same implementation. Shared trusted
definitions are fine; circular specifications and implementation-shaped oracles
are not. Do not assume the conclusion inside a precondition.

Specify the actual boundary. “Decoded message to position” excludes decoding;
“authorization decision over a supplied state” excludes the correctness/freshness
of that state. Those boundaries still need integration evidence.

## 2. State the whole-function guarantee

Present the claim in English and Lean. Use a claim of this shape where appropriate
(this is schematic, not a theorem to paste without domain adaptation):

```text
for every input in the supported domain,
the actual evaluator succeeds with a result satisfying the intended contract.
```

Include the observable outcomes that matter: success or specified rejection,
output validity, invariants, and numerical error bounds where relevant. State
which invalid-input classes are rejected and prove or test their behavior at the
boundary that actually enforces it. A theorem about valid inputs alone does not
prove rejection behavior. A state-machine theorem may quantify over supported
transitions/traces rather than a single scalar input.

Check adequacy, not merely satisfiability:

- Exhibit inputs satisfying the hypotheses, including important
  boundaries. An unconditional theorem is not automatically vacuous.
- Ensure input assumptions cover intended use and do not exclude the hard cases.
- Ask whether a plausible wrong implementation could still satisfy the theorem.
  Challenge it with a relevant counterexample or mutation when useful.
- Distinguish mathematical/model accuracy from implementation error and physical
  reality. A bound relative to an ideal algorithm is not a bound on sensor or
  modeling error. A real-arithmetic proof is not a floating-point error proof.
- List external/runtime assumptions, including numeric semantics, integer widths,
  clock/state validity, compiler behavior, and environment boundaries when relevant.

Present this contract before implementing the core. When H-10 applies, pause for
human approval of the contract and formal work, or explicit acceptance of a named
fallback and its lost assurance. Missing tools and uncertain proof cost do not
remove the high-stakes decision. For ordinary work within scope, the agent can
proceed after presenting the contract; no separate approval is required unless
requested. A draft Lean statement that has not been checked must be labeled as such.
Existing explicit approval can satisfy H-10 when the contract, assurance level,
and current work scope remain covered; repeated approval is not a station requirement.

## 3. Implement and prove in Lean together

Use the specification as the target and Lean as the core's development language.
Iterate implementation and proof together. A failed proof may reveal the wrong
algorithm, representation, precondition, operation order, or an inadequate model;
investigate rather than reflexively weakening the contract (H-06).

Prove the deliverable evaluator's relationship to the specification. Helper lemmas
support that theorem; they do not substitute for it. Use existing lemmas and small
coherent definitions rather than building a parallel theory. For numeric code,
model the operations actually executed, not just a convenient idealized algorithm.
For runtime performance or resource claims, obtain specific evidence; mathematical
termination is not a latency or memory bound.

Establish the promised theorem and audit its dependencies before deriving or
changing the production core. If a proof is blocked, report the exact obstruction
and proposed alternative evidence. Do not label the component T-3 complete or
silently proceed with an unproved port. A requested/agreed proof or H-10 fallback
requires the user's decision before changing the assurance commitment.

For an existing project, model the intended contract and a faithful scoped
reference before changing the production implementation. Do not rewrite unrelated
code or move the entire application into Lean to satisfy this workflow.

## 4. Derive and check production targets

Once the reference satisfies its theorem, derive the production implementation
from it. Preserve representations, operation order, validation/error semantics,
and domain assumptions. “Compile target” describes the development relationship;
an AI-written translation is still an unverified port.

Differential-test the port against the executable Lean reference over generated
inputs and boundaries, including rejection cases where supported.
Compare the right observable: exact values/bits when semantics require identity;
otherwise a justified equivalence or tolerance. Record commands, seeds, counts,
and results actually observed. Do not hide divergence behind a looser tolerance.

Review language-specific risks such as overflow, signedness, floating-point
contraction, exceptions, ownership, and serialization. Test the impure shell and
the path that supplies values to the core. A valid-input proof does not show that
callers establish its preconditions. For a Lean-only deployment, a port check is
N/A, but its runtime boundary still needs the applicable evidence.

Only a separately justified verified extraction/translation can transfer the proof
to generated target code. Differential agreement is empirical evidence, never a
machine-checked cross-language equivalence claim.

## 5. Package evidence for human review

Follow `references/assurance-package.md`. Lead with the contract, theorem,
assumptions, and their source locations. Separately identify the proved Lean core,
tested production port, and integration evidence. A reviewer should be able to
assess the meaning and adequacy of the guarantee without reconstructing the
correctness argument from generated target-language code.

## Local tooling: scaffold

Requires Python 3.9+; normal setup also requires provisioned `elan` and `lake`.
The shell wrapper requires Bash. In any harness or shell, you may instead invoke
`scripts/setup_formal.py` directly with the same arguments using the installed
Python launcher. See `references/capabilities.md` for platform/path conventions.
The project directory must already exist. Run with absolute paths:

```sh
"$SKILL_DIR/scripts/setup-formal.sh" "$PROJECT_DIR"
```

For structural preparation without invoking Lean:

```sh
"$SKILL_DIR/scripts/setup-formal.sh" --scaffold-only "$PROJECT_DIR"
```

The latter is not a build or proof check. Setup creates:

```text
formal/
  lakefile.toml
  lean-toolchain
  Formal.lean
  Formal/Spec.lean
  Formal/Impl.lean
  Formal/Proofs.lean
  theorems.txt
  check-proofs.py
  .gitignore
vendor/leanfmt/
```

The generated configuration pins the bundled formatter's toolchain and explicitly
builds `Formal`. Setup refuses existing incompatible configurations, Lean-config
packages, conflicting files, symlinked managed paths, and different vendor copies.
It does not migrate existing packages. On a repeat run it preserves edited Lean
sources and theorem registrations. A partial failed scaffold is reported for
manual inspection rather than overwritten. Existing packages require a deliberate
integration diff; format only changed files when adopting the formatter.

## Local tooling: proof acceptance

Replace the empty stubs with the agreed specification, executable model, and
proofs. Import every deliverable proof through `Formal.lean`. Register each
fully qualified guarantee theorem on its own line in `theorems.txt`; comments
start with `#`. An empty inventory deliberately fails the delivery proof check.
Review that the inventory covers the agreed guarantee: neither a build nor this
checker detects a deliberately omitted obligation or a weak specification.

From `formal/`:

```sh
python3 check-proofs.py
lake exe fmt --check -r Formal.lean Formal
```

Use `lake exe fmt -r Formal.lean Formal` to format locally. The checker builds
`Formal`, queries Lean's `#print axioms` for each registered theorem, and rejects
missing or unrecognized audit results and any axiom outside `propext`,
`Classical.choice`, and `Quot.sound`. In particular, `sorryAx` and project-defined
axioms are rejected. The configuration also treats compiler warnings as errors.
Axiom auditing is separate because warnings alone do not establish completeness.

Review each registered declaration's statement and its relation to the spec.
The automated checker enforces dependency policy, not theorem relevance, model
fidelity, or the truth of external assumptions. Changing the allowed axiom policy
requires explicit review; do not add an axiom just to get a green build.

Run these commands locally before claiming completion, and rerun affected checks
after changes. Keep the formal package, generated lockfile, and formatter vendor
with the project so another harness can repeat the same checks. The initial empty
scaffold is not a deliverable proof and fails the inventory gate until implemented.

Reuse existing local lemmas where suitable. Mathlib is optional and **not bundled**;
adding it changes the dependency and offline story and requires P-02/P-05 review.

## Revising a verified component

For a bug fix, establish whether the contract, reference implementation, port,
or shell is wrong. Preserve an unchanged guarantee when repairing its implementation.
If the intended behavior changes, revise and review the contract first; apply H-10
again when that decision gate is relevant. Reprove affected obligations, regenerate
or update the port, and rerun affected local checks. Do not weaken a theorem or
drop a registered obligation just to preserve a passing build.

## Network and portability

Skill references, audit validators, and leanfmt sources are bundled. The fresh
scaffold has only a local-path formatter dependency; its released graph depends
only on Lean. Toolchain provisioning via elan can download Lean.
Existing/optional project dependencies may need separate
provisioning; do not describe those cases as offline.

For strict offline use, provision the pinned Lean toolchain beforehand and use
`--scaffold-only` until that is done. The script is not a network sandbox.
One `formal/` package per project is supported; for monorepos pass the package
directory explicitly and run verification from that package's `formal/` directory.
