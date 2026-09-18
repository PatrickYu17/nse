# Security integration

The audit entry is **security-audit/GUIDE.md**. It is intentionally not named
`SKILL.md` and has no discovery frontmatter, so recursive and Markdown skill
scanners do not register a second skill or collide with another installation.
Its companion files reference it by that name.

For focused questions or H-12, read the entry's guidance-mode and execution
rules, `security-audit/ATTACK-CLASSES.md`, and the relevant hunting classes.
Do not start the full workflow or create audit artifacts merely because a diff
touches a parser. Report source-grounded findings and execution gaps precisely.

For an explicit full codebase audit/pen-test or requested audit artifacts, follow
the entry's six phases, including sandbox requirements, independent verification,
coverage accounting, and its incomplete-run terminal state. Those requirements
govern this mode; ordinary delivery reporting does not replace its artifacts.
If required sandbox/delegation capabilities are unavailable, disclose the exact
blocker rather than weakening the evidence bar or claiming a completed audit.
Map the audit protocol's parent/research/general roles to available capabilities
as described
in `references/capabilities.md`. A separate fresh agent session can satisfy the
independence requirement when its isolation and evidence access meet the audit
contract; a second pass in the hunter's own context cannot. Built-in subagents are
not assumed, and ordinary coding/focused source review does not require them.

Resolve the skill and output directories separately. Validate retained artifacts:

```sh
node "$SKILL_DIR/security-audit/validate-findings.cjs" "$OUTPUT_DIR/findings.json"
node "$SKILL_DIR/security-audit/validate-coverage-ledger.cjs" "$OUTPUT_DIR/coverage-ledger.json"
```

Node.js is required; these validators have no external runtime dependencies.
The audit protocol's own impact-based severity and certainty rules apply.
