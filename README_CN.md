# Self-Programming Engine

[English](README.md) | [简体中文](README_CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/downloads/)
[![Architecture: Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent%20Pipeline-orange.svg)]()
[![Safety: Git Sandbox](https://img.shields.io/badge/Safety-Git%20Sandbox%20%2B%20Whitelist-success.svg)]()

> **具备 Git 物理沙箱隔离、AST/模糊匹配代码打补丁、多智能体协同治理的自主代码迭代与自编程引擎。**

---

> [!IMPORTANT]
> **版本与商业化说明**
>
> - **开源基线版本**：本仓库公开的代码为约 **12 个月前的基线版本（Baseline Release from ~12 months ago）**，主要供开源社区进行技术研究、架构参考与交流学习。
> - **商业/企业专有版**：具备更高稳定性、工业级高可用与持续演化的**最新版本已作为商业化/企业版交付**。如需了解最新企业版架构或洽谈商业合作，请联系项目维护团队。

---

## 🌟 核心架构与流水线

传统的大语言模型代码生成往往存在“语法幻觉”、破坏性覆盖周围上下文、缺乏测试驱动与回归验证等问题。

`Self-Programming Engine` 将代码自演化解耦为严格治理的多智能体装配流水线：

```
┌─────────────────────────────────────────────────────────────┐
│                    ProgrammingTask 输入                     │
│               (任务描述、目标文件清单、风险等级)             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Architect Agent (架构师智能体)                           │
│    - 执行影响面分析与安全边界审查                            │
│    - 生成 DevPlan (开发计划、测试方案、不变量约束)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Programmer Agent (程序员智能体)                          │
│    - 生成 CodePatchSet (原子化的代码变更块 before/after)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. FilePatcher (确定性代码补丁引擎)                         │
│    - 执行精准匹配；自适应回退至 AST 语法匹配与模糊匹配      │
│    - 强制执行安全白名单 (拦截敏感配置、凭证与核心守护进程)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Tester Agent (测试智能体)                                │
│    - 在隔离的临时 Git 沙箱分支中执行针对性回归测试套件      │
│    - 生成 TestReport (通过/失败状态、stdout/stderr 捕获)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Reviewer Agent (审查智能体)                              │
│    - 多维度代码审查 (语法合法性、回归风险、安全准则)        │
│    - 裁决：APPROVE (准予合并) 或 REJECT (拒绝并附整改要求)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛡️ 安全防护与治理机制

- **Git 分支物理沙箱**：所有自编程修改均在临时特性分支（`ai-dev/<task_id>-<uuid>`）上运行。在通过审查与全部测试前，绝不污染主工作树。
- **严格文件白名单**：敏感路径（如 `.env`、密钥凭证、核心守护进程）被底层 `SAFE_FILES_WHITELIST` 永久物理拦截。
- **模糊与 AST 补丁算法**：采用“精确匹配优先、模糊与 AST 自适应回退”，杜绝大模型微小缩进或空格幻觉导致破坏周围完好代码。
- **支持多 LLM 接入**：
  - 本地模型（Ollama / vLLM / llama.cpp）
  - Gemini CLI / API
  - OpenAI / Codex CLI
  - Aider CLI 包装器

---

## 🚀 快速上手

### 1. 安装

```bash
git clone https://github.com/chanaliuxing/self-programming.git
cd self-programming

python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

### 2. 运行自检测试

```bash
python3 tests/test_self_programming.py
# ======================================================================
#   Results: 6/6 tests passed
# ======================================================================
# 🎉 ALL VALIDATION TESTS PASSED! 🎉
```

### 3. Python API 调用示例

```python
from self_programming.engine import SelfProgrammingEngine
from self_programming.schema import ProgrammingTask

# 1. 初始化引擎 (可选工具: "local", "gemini", "codex", 或 False 测试桩模式)
engine = SelfProgrammingEngine(use_llm=False)

# 2. 定义编程任务
task = ProgrammingTask(
    task_id="task-001",
    origin="user_request",
    description="为 demo.py 中的函数增加类型注解与异常处理",
    repo_root=".",
    related_files=["demo.py"],
    constraints={"risk_level": "low"},
    acceptance_criteria=["必须通过单元测试"],
)

# 3. 在沙箱环境中执行自编程闭环
result = engine.run(task, use_sandbox=False)

print(f"审查状态: {result.review.status}")
print(f"开发计划: {result.dev_plan.task_summary}")
```

---

## 📄 License

本项目采用 [MIT 许可证](LICENSE)。
