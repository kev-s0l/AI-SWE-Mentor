# Phase 1 — Local AI Senior Software Engineer Mentor

**Project:** AI Engineering Companion  
**Phase:** 1 — Software-only MVP  
**Environment:** Windows, VS Code, Python, Ollama  
**Hardware:** NVIDIA GeForce RTX 3060 (12 GB VRAM), 16 GB RAM  
**Estimated duration:** 2–3 weeks (flexible)

## 1. Objective

Build a locally hosted AI mentor that acts like a senior software engineer. It should review code only when explicitly requested, question implementation decisions, identify potential issues, and teach engineering principles. Its primary goal is to develop the user's problem-solving ability rather than generate solutions.

**Example interaction**

> **Developer:** Review my implementation of this authentication middleware.
>
> **Mentor:** I noticed you're validating the token, but what happens when it expires?
>
> **Developer:** It should throw an exception.
>
> **Mentor:** Where is that exception caught, and what HTTP response will the application return?

## 2. Scope

### Included

- Local LLM through Ollama, initially Qwen2.5-Coder 7B.
- Python CLI usable from VS Code's integrated terminal.
- Senior-engineer mentoring persona with Socratic questioning.
- On-demand review of pasted snippets or explicitly selected files.
- Progressive hints and technical explanations.
- Short-term conversation history with bounded context.
- Read-only code inspection with no project file modification or code execution.
- Automated tests and practical evaluation.

### Deferred

- Physical robot, display, microphone, speaker, and voice interface.
- Timed technical interview mode.
- GitHub repository integration.
- Obsidian, persistent memory, and daily summaries.
- Automatic monitoring or autonomous project actions.
- Full VS Code extension.
- Cloud-model integration.

## 3. Architecture

```text
VS Code integrated terminal
  | User questions / pasted code / explicit file paths
  v
Python mentor CLI
  |-- Prompt manager (mentoring instructions)
  |-- Context manager (bounded conversation history)
  |-- Code reviewer (review request formatting)
  `-- Read-only file loader (approved project root only)
  |
  v
Ollama local HTTP API
  |
  v
Qwen2.5-Coder 7B (local inference, preferably GPU)
  |
  v
Mentor response: findings, questions, hints, explanations
```

The model runs locally. No cloud API is required for Phase 1. The application must not expose arbitrary shell execution or file-writing tools to the model.

## 4. Development roadmap

### Milestone 1 — Local AI environment (Days 1–2)

- [ ] Install Ollama and download Qwen2.5-Coder 7B.
- [ ] Confirm GPU acceleration with `ollama ps` and `nvidia-smi`.
- [ ] Create a Python virtual environment in VS Code.
- [ ] Verify Python can communicate with Ollama's local API.

**Acceptance:** A Python request receives a response from the local model.

### Milestone 2 — Basic mentor CLI (Days 3–5)

- [ ] Create the project structure and initialize Git.
- [ ] Implement a Python client for Ollama.
- [ ] Build a terminal-based conversation loop.
- [ ] Handle connection failures and exit commands.
- [ ] Add basic unit tests for request handling.

**Acceptance:** A user can have a multi-turn terminal conversation and exit cleanly.

### Milestone 3 — Mentoring behavior (Days 6–8)

- [ ] Write a system prompt defining senior-engineer mentoring behavior.
- [ ] Implement progressive hints instead of immediate solutions.
- [ ] Support explanations and follow-up questions.
- [ ] Test uncertainty handling and incorrect assumptions.
- [ ] Create representative sample conversations to evaluate mentoring quality.

**Acceptance:** On representative tasks, the mentor guides rather than immediately supplies full implementations, and acknowledges insufficient evidence.

### Milestone 4 — Read-only code review (Days 9–12)

- [ ] Support pasted snippets and explicitly selected local files.
- [ ] Restrict file reads to an approved project directory.
- [ ] Reject paths outside the approved root, including symlink escapes, and block sensitive files such as `.env`.
- [ ] Format review findings with location/evidence, severity, and reasoning.
- [ ] Ask follow-up questions without automatically generating replacement code.
- [ ] Test that no project files are changed by review operations.

**Acceptance:** The user can request a review of an approved file; forbidden files are inaccessible and project files remain unchanged.

### Milestone 5 — Context and reliability (Days 13–15)

- [ ] Implement short-term conversation history.
- [ ] Set a configurable token/context budget.
- [ ] Trim or summarize older turns while preserving current objectives and relevant evidence.
- [ ] Keep source content separate from system instructions.
- [ ] Test long conversations, unsupported claims, and malicious instructions embedded in comments.

**Acceptance:** Long conversations remain usable and source-code text is never treated as higher-priority instructions.

### Milestone 6 — Evaluation and refinement (Days 16–18)

- [ ] Test real Python and TypeScript examples.
- [ ] Measure response latency and GPU memory usage.
- [ ] Evaluate technical accuracy, relevance, uncertainty, and hint quality.
- [ ] Verify read-only permissions and no shell execution.
- [ ] Document known limitations and the next-phase backlog.

**Acceptance:** The mentor performs reliably on at least three realistic coding scenarios and passes permission tests.

## 5. Proposed project structure

```text
engineering-mentor/
├── main.py                 # CLI entry point
├── mentor.py               # Mentoring logic and conversation handling
├── llm.py                  # Ollama API client
├── context.py              # Short-term context management
├── reviewer.py             # Read-only inspection and review requests
├── config.py               # Model and application configuration
├── prompts/
│   └── mentor.md           # Senior engineer behavior instructions
├── tests/                  # Unit, integration, and behavior tests
├── requirements.txt        # Python dependencies
├── README.md               # Setup and usage
└── .gitignore
```

Keep the implementation simple and modular. Do not introduce agent frameworks, vector databases, or complex orchestration until requirements justify them.

## 6. Mentoring principles

1. **Understand before advising.** Ask for expected behavior or requirements when unclear.
2. **Guide before solving.** Use questions and progressively stronger hints rather than immediately writing a full solution.
3. **Discuss tradeoffs.** Address correctness, maintainability, performance, security, and design when relevant.
4. **Ground claims in evidence.** Distinguish confirmed bugs from suspicions; cite supplied lines or code when possible.
5. **Respect developer independence.** Never modify files or apply changes. Do not automatically provide complete implementations.
6. **Acknowledge uncertainty.** Say when context is insufficient and suggest how to verify a hypothesis.
7. **Review only on request.** No continuous observation of the editor or repository.

These are behavior targets, not security guarantees. Security restrictions must be enforced outside the model.

## 7. Functional acceptance tests

| Test | Expected result |
| --- | --- |
| Ask a programming question | Technically grounded explanation |
| Submit code with a bug | Evidence-based concern and a guiding question |
| Ask for a hint | Progressively stronger hint |
| Submit correct code | No invented defects |
| Provide insufficient context | Requests context or states uncertainty |
| Review approved file | Reads file without modifying it |
| Request a path outside approved root | Denied |
| Include malicious instructions in a code comment | Treated as untrusted source content |
| Continue a long conversation | Relevant context retained within budget |
| Stop Ollama during a request | Recoverable connection error |

## 8. Security constraints

- No arbitrary shell-command execution by the mentor.
- No write, delete, commit, push, or auto-fix tools.
- Explicit user request required for each code inspection.
- Allowlisted project root and file types; deny sensitive files and traversal/symlink escapes.
- Treat source files, comments, logs, and model output as untrusted data.
- For stronger guarantees, run inspection under an OS account or sandbox with read-only access to the project.
- No external code transmission in the default local-only configuration.

## 9. Definition of done

Phase 1 is complete when:

- [ ] Ollama runs the selected model locally on the RTX 3060.
- [ ] The mentor is accessible from VS Code's integrated terminal.
- [ ] Code is submitted for review only on explicit request.
- [ ] The mentor provides useful, evidence-based guidance rather than defaulting to solutions.
- [ ] Short conversations retain relevant context and long ones are bounded.
- [ ] The application cannot modify or execute project code.
- [ ] Automated tests cover core behavior and permission boundaries.
- [ ] At least three realistic coding scenarios have been evaluated.

## 10. Getting started

Install Ollama from <https://ollama.com/download>, then run:

```powershell
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b
```

In another terminal, check GPU utilization:

```powershell
ollama ps
nvidia-smi
```

After confirming local inference, create the Python project and connect it to Ollama.

## 11. Guidance for Codex in VS Code

Use this document as the Phase 1 specification. Work **one milestone at a time**. Before implementing a milestone, briefly explain the proposed design and any tradeoffs. Prefer small, reviewable changes and tests. Do not implement deferred features or expand scope without explicit approval. The AI mentor being built must not have write privileges to the user's other projects; development tools such as Codex may edit **this mentor project's source** only when explicitly authorized by the user.
