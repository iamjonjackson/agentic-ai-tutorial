# steps/31-stage2-search-tool.md — Stage 2 (search)

## Goal
A grep-style content-search tool, and the result-handling discipline that makes search tools work inside an agent loop.

## Do
1. In `agent/tools_fs.py`, add `search_files(pattern, path=None, max_results=50)`: `os.walk` from `_resolve(path)`, skip hidden directories, open each file with errors="ignore", regex-match per line, collect `path:line:stripped-line-clipped-to-200-chars`, and cap at max_results. On the cap, append a truncation notice telling the model to narrow the pattern or path and search again. Skip unreadable/binary files silently (catch OSError, UnicodeDecodeError). No matches returns `(no matches for '...')`.
2. Register in TOOL_IMPLS and TOOLS with a description like: "Search file contents recursively under the working directory (or path) for a regex pattern. Returns matching lines as path:line:text."

## Production parallels
Claude Code's Grep tool shells out to ripgrep; production equivalents respect .gitignore and are much faster. The result-handling rules are the real lesson: results are capped and state their truncation (the model re-searches narrower); returns matches not files so the natural next call is read_file; long lines clipped; read failures skipped silently.

## Test
Put a file containing the word TODO somewhere in a subfolder, then ask the agent "where in this project is the word TODO mentioned?" — watch it search, pick a hit, and read the file.
