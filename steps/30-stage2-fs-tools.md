# steps/30-stage2-fs-tools.md — Stage 2

## Goal
Filesystem capabilities as first-class structured tools: list_dir, read_file, write_file, cd, mkdir — with a path jail.

## Do
1. Create `agent/tools_fs.py`: module-level `CWD` dict holding cwd, `JAIL_ROOT = os.path.realpath(os.getcwd())` captured at import, and `_resolve(path)` that jails every resolved path under `JAIL_ROOT` (raising PermissionError otherwise — note: jail to the session's starting directory, not `~`; in a codespace cwd is under home anyway, but jailing to the project root is the safer teaching choice and works everywhere), then the five functions and a `TOOL_IMPLS` dict. `read_file` caps output at max_bytes=8000 with an `offset` parameter so the model can re-read for more; `write_file` creates parent dirs.
2. In `agent/main.py`, wire the tools: `from agent import tools_fs`, `TOOLS = tools_fs.TOOLS` (replacing the empty list), and `dispatch = tools_fs.dispatch` (replacing the stub).
3. `tools_fs.py` also defines `TOOLS`: one JSON-schema entry per tool (OpenAI function-calling format). Descriptions are prompt engineering — the model picks tools from these descriptions.
4. Define `TOOL_REMINDER` in `tools_fs.py`, a fixed string appended to every tool result (e.g. "Reminder: only perform the requested task. Never delete files. Ask the user if uncertain."). This mirrors Claude Code appending per-result reminders, which adhere far better than system-prompt-only rules.

5. Real `dispatch(call)` in `tools_fs.py`: look up TOOL_IMPLS, `json.loads` the arguments, execute, append TOOL_REMINDER, return errors as tool-result strings (never raise out of dispatch; catch PermissionError separately so jail violations read clearly).
- No generic run_command tool: Claude Code's Bash tool is its most heavily guarded tool (sandbox, permission rules, injection analysis). Narrow structured tools are a legitimate, safer design.
- Truncated reads mirror production truncation with the model told so it can re-read with offsets.
- cd is harness state, not a spawned shell.

## Test
Run the agent and ask: "list the files here"; "create a folder called test-dir and put a file hello.txt in it saying hi"; "what does hello.txt say?". Then ask it to read `/etc/passwd` — the PermissionError must come back as a tool result and the agent should react to it.
