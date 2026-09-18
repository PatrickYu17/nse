# No-Slop Engineering activation

This required setup step implements NSE's always-on policy within the chosen
project/user scope. This is an instruction snippet, not another skill. Copy it into
the harness's supported project/user instruction surface, preserving existing
instructions. Replace `<NSE_ROOT>` with the package's absolute path or an explicit
project-root-relative path. See `references/harnesses.md` for native locations.

```text
Apply No-Slop Engineering to every coding, debugging, refactoring, and code-review
task in this instruction file's scope, without requiring an explicit invocation.
Load the no-slop-engineering skill if available; otherwise read
<NSE_ROOT>/SKILL.md directly. Resolve its supporting files from that package's
directory, separately from the target project. Read references/rules.md and the
applicable mode references before implementation or findings. Follow S1–S6.
Consider formalization-first for suitable cores: specification and theorem,
then executable Lean reference and proof, then checked production targets.
High stakes are not required for this route; apply H-10's human decision gate
when its high-stakes criteria hold. Otherwise justify a proportionate fallback.
Deliver an assurance package distinguishing proved, tested, and assumed behavior,
with concrete evidence and blockers. Keep ordinary-task reasons in conversation.
Use this harness's available tools; do not assume another harness's APIs,
subagents, permissions, or shell. Follow higher-priority instructions.
Reuse rules already present in context; reload them when missing or compacted away.
```

Put this in an automatically loaded instruction surface to complete setup.
A one-off prompt can activate NSE for one task, but does not establish always-on
behavior for later tasks. Native discovery alone does not guarantee invocation. Install only the
adapter(s) needed for your environment; do not replace existing instruction files
or generate a separate copy of the NSE rules for each harness.
