# Harness installation and activation

NSE has one shared workflow and rule set. `SKILL.md` is the Agent Skills entry
and is also readable as an ordinary instruction document. No harness-specific
plugin, API key, MCP server, or runtime fetching of these instructions is needed.

## Native skill locations

Each path below is a **skills parent**. Install the entire package in its
`no-slop-engineering/` child, retaining scripts, references, assets, and vendors.
These are documented default locations; honor custom host configuration.

| Harness / installer target | User skills parent | Project skills parent | Activation |
|---|---|---|---|
| Shared / `shared` | `~/.agents/skills/` | `.agents/skills/` | Shared discovery where supported; explicit request or instruction pointer |
| Codex / `codex` | `~/.agents/skills/` | `.agents/skills/` | `$no-slop-engineering` or `/skills`; pointer in `AGENTS.md` |
| Claude Code / `claude-code` | `~/.claude/skills/` | `.claude/skills/` | `/no-slop-engineering`; pointer in `CLAUDE.md` |
| Pi / `pi` | `~/.pi/agent/skills/` | `.pi/skills/` | `/skill:no-slop-engineering`; pointer in `AGENTS.md` |
| OpenCode V2 / `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | Ask to load `no-slop-engineering` using native discovery, or use the pointer |
| Kilo / `kilo` | `~/.kilo/skills/` | `.kilo/skills/` | Ask to use `no-slop-engineering`; pointer in `AGENTS.md` or configured instructions |
| Cursor / `cursor` | `~/.cursor/skills/` | `.cursor/skills/` | Select the skill from `/` in Agent chat; use a persistent instruction for ongoing activation |
| Gemini CLI / `gemini` | `~/.gemini/skills/` | `.gemini/skills/` | Ask to activate the skill; pointer in `GEMINI.md` |
| GitHub Copilot / `copilot` | `~/.copilot/skills/` | `.github/skills/` | Ask to use the skill in a skills-capable agent surface |

Codex, Pi, OpenCode V2, current Kilo, Cursor, Gemini CLI, and Copilot document
`.agents/skills` compatibility. Claude Code's documented native route is
`.claude/skills`; do not assume one shared directory is automatically read by
every harness. Older Kilo distributions may use `.kilocode/skills`; use a custom
destination matching that installed version rather than creating both copies.

## Install the package

Run from this package's root; Python 3.9+ is sufficient:

```sh
python3 scripts/install.py --harness codex --global
python3 scripts/install.py --harness claude-code --project /absolute/path/to/repo
python3 scripts/install.py --harness pi --global --dry-run
```

Choose the relevant command, rather than installing every copy. Use `--harness
shared` for hosts already sharing `.agents/skills`. A custom destination must be
the full `no-slop-engineering` directory, not merely its parent:

```sh
python3 scripts/install.py --destination /custom/skills/no-slop-engineering
```

The installer copies local files only and refuses an existing destination. It does
not edit host settings or instruction files. On upgrade, move the old copy outside
discovery roots, preserve local customizations, then install the new package. Do
not merge over old versions: stale skill entry files can remain discoverable.
Avoid multiple copies visible to one harness; name-collision precedence differs.

For OpenCode user installs, the installer honors `XDG_CONFIG_HOME`; for Pi it
honors `PI_CODING_AGENT_DIR`. For other nondefault layouts, use `--destination`.

## Required always-on activation

Complete setup by adding the snippet in **adapters/activation.md** to an
automatically loaded instruction surface, with the package path filled in.
NSE applies to every engineering task in that scope; discovery-match alone is
not the intended default. Typical choices for the five primary harnesses:

- **Codex:** project `AGENTS.md`, or user `~/.codex/AGENTS.md` (under `CODEX_HOME`
  when overridden). Respect an existing `AGENTS.override.md`.
- **Claude Code:** project `CLAUDE.md` or user `~/.claude/CLAUDE.md`.
- **Pi:** project `AGENTS.md` or user `~/.pi/agent/AGENTS.md`.
- **OpenCode V2:** project `AGENTS.md` or user `~/.config/opencode/AGENTS.md`.
  V2 currently accepts but does not load the config `instructions` array; use
  `AGENTS.md` for active guidance.
- **Kilo:** project `AGENTS.md`, or a file included by the `instructions` array
  in `kilo.jsonc`. Merge the pointer; do not replace existing configuration.

The pointer can refer to a shared package even if native discovery is absent.
Use direct file reading when no skill tool exists. Installation and activation
are distinct, and both remain subject to the host's permissions/trust settings.
Verify the persistent instruction is loaded in a fresh session. The explicit
smoke check below tests package access and understanding; by itself it does not
demonstrate automatic activation. Also try a small coding task without naming NSE
and inspect whether its rules are loaded and applied.

## Other harnesses and older versions

For Cline, Roo Code, Windsurf, Aider, custom API agents, or any host whose native
skill discovery has not been checked here, use the direct-file route:

1. Place the complete package at a known readable path.
2. Put the activation snippet in that host's supported rules, instructions,
   read-only context, or task prompt. Supply the actual path.
3. Have the agent read `SKILL.md`, `references/rules.md`, and the relevant mode.
4. Map operations using `references/capabilities.md`; report unavailable evidence.

This is a documented fallback, not a claim that those hosts scan `.agents/skills`
or implement a particular slash command. A text-only host can apply review guidance
to supplied files; it cannot claim applied edits or executed verification.

## Installation smoke check

In a new/reloaded session, ask:

> Load No-Slop Engineering. Without editing files or running project commands,
> identify the entry path and rule-file path you actually read, explain the
> formal-first development order, why T-3 can fit an ordinary algorithm, and when
> H-10 requires a human decision. Say how you would distinguish a proved reference
> from a tested production port, and report a missing required check or verifier.

Inspect the actual file/skill loading events, not just the model's assertion.
Then use `references/examples.md` for a representative behavior check. Local
package/installer tests validate files and routing, not a model's compliance.

## Documentation basis

Installation/discovery guidance checked against these sources on 2026-09-18.
These are maintainer references; agents do not need to fetch them to run NSE.
No end-to-end session was run in each listed harness during this packaging change.

- Agent Skills: https://agentskills.io/specification
- Codex: https://developers.openai.com/codex/build-skills
- Codex instructions: https://developers.openai.com/codex/agent-configuration/agents-md
- Claude Code: https://code.claude.com/docs/en/skills
- Claude Code instructions: https://code.claude.com/docs/en/memory
- Pi: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md
- Pi context/capabilities: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md
- OpenCode V2: https://opencode.ai/v2/docs/skills
- OpenCode V2 instructions: https://opencode.ai/v2/docs/instructions
- Kilo: https://kilo.ai/docs/customize/skills
- Kilo instructions: https://kilo.ai/docs/customize/agents-md
- Cursor: https://cursor.com/docs/context/skills
- Gemini CLI: https://geminicli.com/docs/cli/skills/
- Copilot: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
