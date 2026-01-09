---
name: gemini-consultant
description: Get a second opinion from Gemini 3 Pro. CRITICAL: Success depends on providing EXTREME amounts of context (hundreds of lines of code, logs, and history).
allowed-tools: Bash(uv:*), Read
---

# Gemini Consultant

Get a second opinion from Google's Gemini 3 Pro (`gemini-3-pro-preview`) with real-time Google Search grounding.

**CRITICAL: GEMINI IS BLIND.** It knows nothing about your current session, file system, conversation history, or previous errors unless you explicitly force-feed it that data.

## The "Dump Everything" Rule

The `-c/--context` argument is effectively unlimited. To get a useful answer, you must dump **EVERYTHING** relevant into the context.

* **Quantity:** We are talking about **10, 100, or 500+ lines** of context.
* **Scope:** Include the file in question, *all* related files (imports, types, configs), the *full* error traceback, your current hypothesis, and a summary of what you have already tried.
* **History:** If you are deep in a debugging session, dump the relevant parts of the conversation history into the context.

**If you think a file is even tangentially related, INCLUDE IT.**

## Prerequisites

`GEMINI_API_KEY` environment variable must be set.

## Usage

```bash
uv run /path/to/skills/gemini-consultant/consult.py "Detailed Question" -c "MASSIVE CONTEXT STRING"
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `question` | The prompt. Be specific. "Given error X and code Y (in context), why is logic Z failing?" |
| `-c`, `--context` | **THE DATA DUMP.** Concatenate everything here. Code, logs, history, configs. Can be used multiple times. |
| `-i`, `--image` | Image file paths (screenshots, diagrams). |
| `--media-resolution` | `low`, `medium` (default), `high`, `ultra_high`. |
| `--no-search` | Disable web search (pure code logic). |
| `--thinking` | `low` or `high` (default). Use `high` for code. |

## Examples

### BAD (Lazy = Failure)

```bash
# WRONG: Context is missing.
uv run consult.py "Why is this crashing?" -c "Error: 500 Internal Server Error"
```

```bash
# WRONG: Single file provided, ignoring dependencies.
uv run consult.py "Fix this function." -c "$(cat src/broken_file.py)"
```

### GOOD (Exhaustive = Success)

*NOTE: Real-world usages are usually 10-100x longer than the snippets below.*

```bash
# CORRECT: Providing File, Imports, Types, and Errors
uv run consult.py "I am getting a RecursionError in the serialization logic. Analyze the relationship between the Model and the Schema." \
  -c "FILE: src/models.py
$(cat src/models.py)

FILE: src/schemas.py
$(cat src/schemas.py)

FILE: src/config/db_settings.py
$(cat src/config/db_settings.py)

ERROR LOG:
$(cat logs/error_dump.txt)

PREVIOUS ATTEMPTS:
I tried removing the circular reference in schema.py line 40 but it broke the API validation."
```

```bash
# CORRECT: Architecture review with full project scope
uv run consult.py "Review this authentication flow for security flaws." \
  -c "MIDDLEWARE: $(cat src/middleware/auth.ts)
MODELS: $(cat src/models/user.ts)
ROUTES: $(cat src/routes/auth.ts)
CONFIG: $(cat src/config/security.ts)
TYPES: $(cat src/types/express.d.ts)"
```

### Web Search (No Code Context Needed)

```bash
uv run consult.py "What is the latest version of Next.js and what are its new features?"
```
