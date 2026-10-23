# Self-Programming Engine

[English](README.md) | [简体中文](README_CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/downloads/)
[![Architecture: Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent%20Pipeline-orange.svg)]()
[![Safety: Git Sandbox](https://img.shields.io/badge/Safety-Git%20Sandbox%20%2B%20Whitelist-success.svg)]()

> **Autonomous multi-agent code self-evolution and self-programming engine featuring Git sandbox isolation, AST/fuzzy patch application, and multi-agent review governance.**

---

> [!IMPORTANT]
> **Release & Commercial Notice**
>
> - **Open Source Baseline**: The code in this public repository represents a functional baseline release from approximately **12 months ago**, shared for academic research, technical study, and architectural reference.
> - **Commercial & Production Edition**: Advanced industrial-grade features, enhanced reliability, and ongoing evolutions are part of our **proprietary commercial suite**. For commercial inquiries or enterprise deployments, please contact the team.

---

## 🌟 Architecture & Pipeline

Traditional LLM code generation often suffers from "hallucinated syntax", destructive overwrites of surrounding code, and lack of test-driven validation.

`Self-Programming Engine` divides code modification into a strict, governed multi-agent assembly line:

```
┌─────────────────────────────────────────────────────────────┐
│                    ProgrammingTask Input                    │
│             (Task description, target files, risk)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Architect Agent                                          │
│    - Performs impact analysis & safety boundary audit       │
│    - Generates DevPlan (work items, test plan, invariants)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Programmer Agent                                         │
│    - Produces CodePatchSet (atomic hunks with before/after) │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. FilePatcher (Deterministic Patch Engine)                 │
│    - Applies exact match; falls back to AST & fuzzy match   │
│    - Enforces safety whitelist (blocks secrets & core exec) │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Tester Agent                                             │
│    - Executes targeted test plans in isolated Git sandbox   │
│    - Generates TestReport (pass/fail, stdout/stderr)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Reviewer Agent                                           │
│    - Multi-criteria audit (syntax, regression, safety)      │
│    - Decision: APPROVE (auto-merge candidate) or REJECT    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Safety & Governance

- **Git Branch Sandbox**: All changes are executed on temporary feature branches (`ai-dev/<task_id>-<uuid>`). Main working trees are never mutated until approval.
- **Strict File Whitelist**: Sensitive paths (e.g., `.env`, credentials, core execution daemons) are permanently blocked by `SAFE_FILES_WHITELIST`.
- **Fuzzy & AST Patching**: Uses exact-first, fuzzy-fallback hunk replacement to prevent LLM whitespace/indentation hallucinations from destroying valid files.
- **Multi-LLM Tool Agnostic**: Pluggable backend supporting:
  - Local LLMs (Ollama / vLLM / llama.cpp)
  - Gemini CLI (`aichat`, Gemini API)
  - OpenAI / Codex CLI
  - Aider CLI wrapper

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/chanaliuxing/self-programming.git
cd self-programming

python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

### 2. Run Validation Tests

```bash
python3 tests/test_self_programming.py
# ======================================================================
#   Results: 6/6 tests passed
# ======================================================================
# 🎉 ALL VALIDATION TESTS PASSED! 🎉
```

### 3. Python API Example

```python
from self_programming.engine import SelfProgrammingEngine
from self_programming.schema import ProgrammingTask

# 1. Initialize engine (pluggable tool: "local", "gemini", "codex", or False for stub)
engine = SelfProgrammingEngine(use_llm=False)

# 2. Define a concrete coding task
task = ProgrammingTask(
    task_id="task-001",
    origin="user_request",
    description="Add docstring and error handling to calculate_factorial in demo.py",
    repo_root=".",
    related_files=["demo.py"],
    constraints={"risk_level": "low"},
    acceptance_criteria=["Tests must pass"],
)

# 3. Execute self-programming in an isolated Git sandbox
result = engine.run(task, use_sandbox=False)

print(f"Status: {result.review.status}")
print(f"Summary: {result.dev_plan.task_summary}")
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
