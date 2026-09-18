# Harness capability contract

The same NSE rules apply in any harness. Adapt operations to available tools;
never assume a tool exists because another harness uses its name. Respect the
host's instruction hierarchy, permissions, repository boundaries, and user scope.

| Operation | Acceptable implementation | If unavailable |
|---|---|---|
| Load NSE | Native skill loader or read `SKILL.md` by its actual path | Ask for the package/path; do not claim to have loaded it |
| Read/search | File tools, editor search, or permitted shell commands | Request the necessary source; limit findings to visible evidence |
| Edit | Patch/edit/write tools or the host's normal editing facility | Provide a proposed patch, explicitly not an applied change |
| Execute checks | Harness terminal or local process tool | Report required runtime evidence as BLOCKED; source review remains possible |
| Ask a question | Ordinary conversation or a structured question tool | In unattended runs, report a pending decision instead of inventing approval |
| Formal-first development | Python and the pinned Lean/Lake toolchain | Disclose tools needed; an ordinary initial fallback needs a concrete reason, while H-10 or a requested/agreed proof needs an explicit decision before downgrade |
| Independent audit verification | Fresh isolated agent/session with the required source and evidence | Full audit is incomplete; do not call self-review independent |
| Sandboxed audit execution | OS-enforced controls required by the audit guide | Source-only analysis with explicit needs-validation gaps |

## Single-agent baseline

S1–S6, AFTER mode, and focused source reviews work without delegation, MCP,
background processes, task-list tools, or a special permission dialog. Keep
reasons and evidence in the conversation. A full security audit has additional
capability requirements; those do not become prerequisites for ordinary coding.
Formal-first development also works in a single agent: it does not require a
separate prover agent. Human review of intent/contract is distinct from independent
security-audit verification. Keep approval pauses scoped to H-10, explicit user
requests, or genuine requirements/scope decisions.

Pi's default toolset, for example, has no built-in subagents. Do ordinary work
directly. For an approved full audit, use a configured delegation extension or
separate fresh sessions only when they can meet the audit protocol's isolation contract.
If they cannot, disclose the missing capability. Do not install extensions or
launch another paid agent merely because the workflow mentions a role.

## Platform and path handling

`SKILL_DIR`, `PROJECT_DIR`, and `OUTPUT_DIR` in examples are explicit path labels.
They are not environment variables supplied by every harness. Locate the package
from the loaded entry, set actual absolute paths, quote them for the active shell,
and use the target checkout as the working directory only where appropriate.

The scripts use Python's standard library. On Windows, use `python` or `py -3`
when `python3` is not the installed launcher. The formal scaffold can be invoked
directly as `python scripts/setup_formal.py ...`; its Bash wrapper is optional.
Shell snippets target a POSIX shell; adapt syntax on
other shells rather than executing it verbatim. Native Windows script behavior
has not been exercised by this package's macOS validation.

Remote/cloud agents need the complete package inside their accessible filesystem.
A local absolute path or symlink to a developer's home is not a portable remote
installation. Commit a project copy or provision the package in that runtime.

## Context and evidence

If context compaction drops the rules, reread the required local references before
continuing. Preserve the actual guarantee, decisions, commands, and outstanding
gaps through the harness's conversation mechanism; do not invent repo logs.

Tool calls are evidence only for what they actually did. An IDE's code preview
is not a running application; a proposed shell command is not an executed test;
a skill appearing in a list is not proof its instructions were followed.
