# No-Slop Engineering (NSE)

AI slop kinda sucks. This is my way of trying to mitigate slop in the backend with agentic coding.

This skill doesn't touch design so you can use your own design skills, etc.

This is my personalized skill, workflow, and system for developing quality, proven software with AI
coding agents. It gives the agent more of the implementation and proof work so
humans can review smaller, higher-leverage artifacts: intent, specification,
assumptions, and guarantees. Use it with Codex, Claude Code, Pi, OpenCode, Kilo,
Cursor, Gemini CLI, GitHub Copilot, or another coding agent.

`SKILL.md` is the portable entry point. Hosts supporting Agent Skills discover
it natively; other hosts read it through their ordinary instructions. The
system does not depend on a particular plugin API, tool name, model, or
delegation feature.

## How development works

```text
Human intent
    ↓
Precise specification + whole-function theorem
    ↓
Executable Lean reference + proof, developed together
    ↓
Production target + differential and integration checks
    ↓
Assurance package for human review
```

This tries to use a formal-first approach. Uses Lean to write proofs and changes the role in how humans review. From reviewing code to reviewing intent.

In simplistic terms you as a human would be reviewing and shaping the intent and the hard spec. Then AI will write proofs to ensure that the code proves it matches the final spec or the intent of the human.

This doesn't mean everything needs a proof. If proving something would be overkill or just doesn't fit the task, there's a deliberate fallback. If the stakes are high (billing, auth, crypto, safety stuff), the spec and theorem get a human sign-off before the real implementation starts. And whichever route a change takes, the wrap-up says plainly what's proved, what's tested, and what's still assumed. No pretending.

Start with `SKILL.md`. The detailed workflow is in
`references/formal-verification.md`; the human review contract is in
`references/assurance-package.md`.

## Install

Clone this repository, then from its root choose your harness and scope:

```sh
git clone https://github.com/PatrickYu17/nse.git
cd nse
python3 scripts/install.py --harness codex --global
python3 scripts/install.py --harness claude-code --project /absolute/path/to/repo
python3 scripts/install.py --harness pi --global --dry-run
```

The repository is named `nse`; the installer installs the skill under a
`no-slop-engineering` directory, because Agent Skills requires a lowercase
kebab-case ID matching the frontmatter name. If you copy the folder into a
skills directory manually, name the copy `no-slop-engineering`.

These are alternatives, not a sequence. Targets: `shared`, `codex`, `claude-code`,
`pi`, `opencode`, `kilo`, `cursor`, `gemini`, and `copilot`. The `shared` target uses
`.agents/skills` for compatible hosts; it is not a universal discovery directory.
The installer copies local files, needs Python 3.9+, and refuses existing targets.
It does not alter harness settings or project instruction files.

For a custom layout or a host without native discovery:

```sh
python3 scripts/install.py --destination /absolute/path/to/no-slop-engineering
```

Manual copying of the complete directory works too. See
**references/harnesses.md** for the per-harness location/activation matrix,
documentation sources, remote-agent setup, and a smoke-check prompt.

To upgrade, first move the previous installation outside all skill-discovery
directories, preserving any local customizations, then copy the new folder.
Do not merge this version over the old one: a stale
`security-audit/SKILL.md` would register an unwanted second skill. Only the root
`SKILL.md` should remain discoverable.

## Complete setup: always-on activation

NSE is intended to apply to every coding, debugging, refactoring, and review task
in your configured scope. Copying the package is step one; persistent activation
is the required second step. Merge **adapters/activation.md** into the appropriate
project/user instruction surface (`AGENTS.md`, `CLAUDE.md`, configured rules, or
another host-supported surface), replacing its path placeholder. Keep existing
instructions intact.

Then reload/start a session and verify that the persistent instruction is loaded.
Native skill matching or a one-off invocation alone does not complete always-on
setup. The installer reports activation as pending because it does not edit your
instruction files.

Supporting files load on demand. Native discovery does not guarantee activation.
Local tests, lint, proof checks, and tool permissions provide mechanical enforcement.
Follow the harness's higher-priority instructions. **references/capabilities.md** explains
equivalent tools, missing-capability behavior, independent audit sessions, and
cross-platform path handling.

## Prerequisites

Verification runs through the harness's terminal or local process tools. No
GitHub account, Actions workflow, hosted pipeline, or runner service is required.

- Reading/applying the workflow requires no additional runtime; executing a
  selected route needs its tools. Always-on activation does not mean always-on Lean.
- Installation, formal scaffolding, and proof checking: Python 3.9+. Bash is only
  needed for the optional `setup-formal.sh` wrapper; `scripts/setup_formal.py` can
  be invoked directly. Full verification also needs elan/Lake and the toolchain
  pinned in `vendor/leanfmt/lean-toolchain`.
- Full audit artifact validation: Node.js. Audit execution additionally requires
  the sandbox and agent capabilities described in `security-audit/GUIDE.md`.
- Mathlib is optional, not bundled. See `references/formal-verification.md` for
  toolchain/dependency provisioning and the offline boundary.

For T-3 work, the delivery commands from the project's `formal/` directory are:

```sh
python3 check-proofs.py
lake exe fmt --check -r Formal.lean Formal
```

The proof checker builds the formal target and audits registered theorem axioms.
It does not decide whether a theorem is adequate or covers the requested behavior.
For T-2/T-1/T-0 work, use the relevant local property, example, or static checks.

## Validate this package

From the package root:

```sh
python3 -B -m unittest discover -s tests -v
bash -n scripts/setup-formal.sh
```

The default suite exercises installer routing and real package copies, temporary
project scaffolding and conflicts, package metadata/discovery/link integrity,
and the axiom-output parser. Its mocked-Lake case verifies failure propagation
only. It explicitly skips the live Lean case. Installer tests are filesystem
checks, not end-to-end sessions in each harness.

With the pinned toolchain provisioned:

```sh
NSE_LIVE_LEAN=1 python3 -B -m unittest discover -s tests -v
```

The live case builds a fresh scaffold, accepts a real proof, rejects `sorryAx`
and an arbitrary project axiom, formats and rechecks the proof, and confirms that
format drift fails without rewriting files. Allow several minutes for a cold
formatter build (about nine minutes in the recorded macOS run). Live checks can
download the pinned toolchain through elan if it has not been provisioned.

`references/examples.md` provides manual behavioral acceptance scenarios. These
are expectations for agents using the skill, not automated model evaluations.

## License

MIT for original work; see `LICENSE`. The `security-audit/` and `vendor/leanfmt/`
directories keep their own license files.
