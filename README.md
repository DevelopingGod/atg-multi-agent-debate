# ATG Multi-Agent Debate System

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![LangGraph](https://img.shields.io/badge/LangGraph-0.1-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

A robust, multi-agent debate simulation powered by **LangGraph** and **Llama 3** (via Groq). The system orchestrates a structured argument between two distinct AI personas (Scientist vs. Philosopher), enforcing strict turn-taking, memory management, and logical coherence, concluding with an impartial judgment.

**Developed for the ATG Machine Learning Intern Technical Assignment.**

---

## 🚀 Features

* **Cyclic State Graph:** Implements a custom LangGraph workflow (Scientist ↔ Philosopher) with a dedicated Rounds Controller.
* **Structured Memory:** Agents receive only relevant context slices (last 2 turns) to simulate realistic rebuttal dynamics.
* **Deterministic Validation:** Includes CLI flags for random seeds to ensure reproducible testing (`--seed`).
* **Robust Error Handling:** Features retry logic and "HumanMessage" injection to prevent LLM silence or hallucination.
* **Comprehensive Logging:** Detailed JSON logs of every state transition, message, and verdict.
* **Visual DAG:** Automatically generates a visual representation of the state machine (`debate_dag.png`).

---

## 📂 Project Structure

```text
debate_assignment/
│
├── nodes/                  # Core Logic Modules
│   ├── agents.py           # Scientist & Philosopher node definitions
│   ├── judge.py            # Final verdict logic
│   ├── memory.py           # Round counting & coherence checks
│   └── tools.py            # Utilities (Logging, Input Validation)
│
├── personas/               # Persona Definitions
│   ├── scientist.txt       # "Empirical, data-driven"
│   └── philosopher.txt     # "Ethical, abstract, reasoning"
│
├── tests/                  # Unit Test Suite
│   └── test_debate.py      # Validates turn limits & agent loading
│
├── logs/                   # Execution Logs (JSON)
├── config.py               # Global Configuration (Models, Keys)
├── graph.py                # LangGraph DAG Construction
├── run_debate.py           # Main CLI Entry Point
└── requirements.txt        # Dependency List
```
---
## 🛠️ Installation
### Prerequisites
1. Python 3.10 or higher

2. Graphviz (Required for DAG visualization)

### Setup

1. Clone the Repository

``` Bash

git clone [https://github.com/YourUsername/debate_assignment.git](https://github.com/YourUsername/debate_assignment.git)
cd debate_assignment
```

2. Install Dependencies

``` Bash

pip install -r requirements.txt
Configure API Keys Create a .env file in the root directory:
```

Code snippet
```
# Using Groq (Free Tier) for Llama 3
GROQ_API_KEY=gsk_your_actual_key_here
```
---

### 🏃‍♂️ Usage
- Interactive Mode
- Run the debate and enter a topic when prompted:

``` Bash
python run_debate.py
```
- Deterministic / Testing Mode

- Run with a specific seed to force temperature=0 for reproducible results:
``` Bash
python run_debate.py --topic "Is AI dangerous?" --seed 42
```

- Custom Logging

- Specify a custom directory for log files:
``` Bash
python run_debate.py --log-path ./my_audit_logs
```
---

### 🧪 Testing
Run the automated test suite to verify turn enforcement, topic validation, and agent initialization:
``` Bash
python -m unittest discover tests
```
---

### 🧠 Design Decisions
1. The "HumanMessage" Injection
- Llama 3 is optimized for Chat (User -> AI). If the history ends with an AIMessage (the opponent's turn), the model may refuse to speak, believing the conversation is paused. I implemented a logic layer in nodes/agents.py that injects a hidden HumanMessage ("Your opponent just argued X, please rebut") to strictly force a response.

2. Global Configuration & State
- The config.py uses a dynamic SET_DETERMINISTIC function. This allows the CLI arguments to override the LLM temperature at runtime without complex dependency injection, ensuring the --seed flag works across all nodes instantly.

3. Separation of Concerns
- Graph Logic: Handled purely in graph.py.

- Execution: Handled in run_debate.py.

- Business Logic: Encapsulated in nodes/. This structure allows for easy scaling (e.g., adding a "Moderator" node) without breaking the existing workflow.

---
## Developer: Sankalp S. Indish
- LinkedIn: https://www.linkedin.com/in/sankalp-indish/
- GitHub: https://github.com/DevelopingGod
