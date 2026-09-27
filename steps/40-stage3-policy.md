# steps/40-stage3-policy.md — Stage 3

## Goal
Guardrails as a structural permission layer between the model and execution — never as prompt text.

## Do
1. Create `agent/policy.py` with `policy_check(name, args) -> "allow" | "deny" | "ask"`, driven by DENY and ASK sets. Start with DENY empty and ASK = {"write_file"}.
2. Update `dispatch`: unknown tool → error string; "deny" → a refusal string telling the model to choose another approach; "ask" → print `[approval] name(args) — allow? [y/N]` and read input, a non-"y" answer returns "User denied this tool call. Ask them why if unclear."; only then execute and append TOOL_REMINDER.

## Production parallels
- Prompt-level instructions are probabilistic; the permission system is the guarantee. Claude Code routes every tool-use request through permission checks before dispatch.
- Codex CLI: two-axis policy — sandbox level (read-only / workspace-write / danger-full-access) plus approval policy (when the human is asked). DENY/ASK/ALLOW is the toy version.
- Defence in depth: Codex backs policy with an OS sandbox (seatbelt/landlock); your equivalent is the path jail. If a shell tool is ever added, deny-listing the string "rm" is not sufficient — argument-level analysis or sandboxing is.

## Test
Prompt "write a file called notes.md with anything" — the y/N prompt must appear; answer N and confirm the agent asks why or proposes an alternative. Then temporarily add a `delete_file` tool to DENY, ask for a deletion, confirm refusal, remove the tool.
