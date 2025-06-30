## AI Agent App


**📁 Proposed Folder Structure**

```sh
agents/
│
├── src/                          ← your real application lives here
│   ├── foundations/              ← basic building blocks (lab1, tools, prompts, etc.)
│   ├── openai/                   ← OpenAI-based agents
│   ├── crew/                     ← multi-agent teams (e.g., CrewAI style)
│   ├── langgraph/                ← graph workflows and LangGraph agents
│   ├── autogen/                  ← agents built using AutoGen
│   ├── mcp/                      ← market coordination protocols, trading agents
│   └── common/                   ← shared utilities, config, logging, etc.
│
├── notebooks/                    ← Jupyter notebooks from the course
│   ├── 1_foundations/
│   ├── 2_openai/
│   ├── 3_crew/
│   └── ...
│
├── assets/                       ← images, designs, visual aids
├── guides/                       ← tutorials, notes, and theory
├── setup/                        ← setup scripts and environment fixes
│
├── README.md
├── pyproject.toml / requirements.txt
├── .env.example / .env           ← environment variables (API keys, etc.)
└── LICENSE
```


| Course Folder    | App Module in `src/` | Purpose                                             |
| ---------------- | -------------------- | --------------------------------------------------- |
| `1_foundations/` | `src/foundations/`   | Basic tools, helper functions, config, prompts      |
| `2_openai/`      | `src/openai/`        | Simple agents using OpenAI APIs                     |
| `3_crew/`        | `src/crew/`          | Multi-agent teams collaborating on tasks            |
| `4_langgraph/`   | `src/langgraph/`     | Graph-based workflows and structured agents         |
| `5_autogen/`     | `src/autogen/`       | Executor/Planner agents via AutoGen framework       |
| `6_mcp/`         | `src/mcp/`           | Market simulation with traders and external systems |
| Global Logic     | `src/common/`        | Config, logging, shared memory, decorators, utils   |

**Best Practices**
* Use src/ layout as recommended by the Python Packaging Authority
* Use pyproject.toml instead of setup.py (modern toolchain)
* Use snake_case for Python modules (agent_core.py, data_loader.py, etc.)
* Separate notebooks from reusable code
* Include .env support with python-dotenv
* Use common/ or utils/ for shared helpers and sandbox/ for experiments
* Add __init__.py files to treat subfolders as proper Python packages

```sh
# Create main folders
mkdir -p src/{foundations,openai,crew,langgraph,autogen,mcp,common}
mkdir -p notebooks/{1_foundations,2_openai,3_crew,4_langgraph,5_autogen,6_mcp}
mkdir -p assets guides setup

# Create placeholder app.py and README.md in each src submodule
for module in foundations openai crew langgraph autogen mcp common; do
  touch src/$module/app.py
  mod_cap="$(echo $module | sed -E 's/(.)(.*)/\U\1\L\2/')"
  echo "# $mod_cap Module" > src/$module/README.md
done


# Create .env.example file
cat <<EOL > .env.example
# API Keys
OPENAI_API_KEY=your-key-here
SERPAPI_API_KEY=your-key-here
EOL

# Create root README.md
cat <<EOL > README.md
# AI Agents Project

This is a modular and scalable AI agent system, built incrementally through structured labs.

## Structure

- \`src/\`: the real application modules (agents, memory, APIs, logic)
- \`notebooks/\`: course notebooks
- \`assets/\`: images and supporting material
- \`setup/\`: environment and setup scripts
- \`.env.example\`: environment variables (e.g. API keys)

Each module under \`src/\` corresponds to a specific phase of the course.

EOL

```

**After running this:**

```sh
agents/
├── src/
│   ├── foundations/
│   ├── openai/
│   ├── crew/
│   ├── langgraph/
│   ├── autogen/
│   ├── mcp/
│   └── common/
├── notebooks/
│   ├── 1_foundations/
│   ├── 2_openai/
│   ├── ...
├── .env.example
├── README.md
└── ...

```

**Install uv**

```sh
➜  my_agents curl -Ls https://astral.sh/uv/install.sh | sh

downloading uv 0.7.13 x86_64-apple-darwin
no checksums to verify
installing to /Users/alex/.local/bin
  uv
  uvx
everything's installed!
```

**Create your project with uv or poetry**
Option A: Using `uv` (recommended, fast, modern)

```sh
uv init
uv pip install openai langchain python-dotenv
```
Option B: Using `poetry`

```sh
poetry init
poetry add openai langchain
```

**Create the environment and install dependencies:**
```sh
uv venv agents_env
source agents_env/bin/activate     # Linux/macOS
# Or on Windows: agents_env\Scripts\activate

Activate with: source agents_env/bin/activate
(agents_env) ➜  my_agents 
```

**install from pyproject.toml with uv.lock**
```sh
uv pip install -e .
```
```sh
(agents_env) ➜  my_agents uv pip install ipykernel

Using Python 3.12.11 environment at: agents_env
Resolved 30 packages in 3.59s
Prepared 1 package in 182ms
Installed 8 packages in 67ms
 + appnope==0.1.4
 + debugpy==1.8.14
 + ipykernel==6.29.5
 + jupyter-client==8.6.3
 + jupyter-core==5.8.1
 + platformdirs==4.3.8
 + pyzmq==27.0.0
 + tornado==6.5.1
(agents_env) ➜  my_agents python -m ipykernel install --user --name=agents_env --display-name "Python (agents_env)"

Installed kernelspec agents_env in /Users/alex/Library/Jupyter/kernels/agents_env
(agents_env) ➜  my_agents python src/foundations/app.py
```

✅ Final checklist for now

| Task                         | Status              |
| ---------------------------- | ------------------- |
| `pyproject.toml` + `uv.lock` | ✅ done              |
| Virtual env (`agents_env`)   | ✅ done              |
| Installed dependencies       | ✅ done              |
| Set up Jupyter kernel        | ✅ done              |
| Bootstrapped `src/` layout   | ✅ done              |
| Git repo initialized         | 🔜 (if not yet)     |
| Actual code in `app.py`      | 🔜 (optional start) |

---

## `src/foundations/` structure from `/notebboks/1_fundations`


Excellent — I now have full access to all four labs as `.py` files. Here's a clear, **step-by-step breakdown** of each one, with the **educational logic**, **concept focus**, and how they **progressively build toward tool-augmented agents**.

---

**Lab 1 – Prompt Basics & System Role** (`1_lab1.py`)

**Educational goal:**

Introduce the concept of prompt messages: `system`, `user`, and `assistant`.
Students learn that prompt design = agent behavior control.

**What it does:**

* Sets an OpenAI API key from `.env`
* Sends a simple `ChatCompletion` using:

  * a `system` role prompt: *"You are a helpful assistant"*
  * a `user` question: *"What is 2+2?"*
* Prints the reply from the assistant

**Core concept:**

> Prompting is a conversation history. System role sets tone, user provides instruction.

**App mapping:**

Put this in `prompts.py` → `build_prompt_basic(user_input: str)`

---

**Lab 2 – Dynamic Prompt Templates** (`2_lab2.py`)

**Educational goal:**

Demonstrate how to **create dynamic, reusable prompts** (like a template engine).
Students start thinking in functions and templates.

**What it does:**

* Same logic as Lab 1, but now:

  * builds a prompt via a reusable function `build_prompt`
  * allows the user to pass in `context`, `question`, etc.
* Defines the prompt like:

  ```python
  prompt = [
    {"role": "system", "content": context},
    {"role": "user", "content": question}
  ]
  ```

**Core concept:**

> Clean abstraction and flexibility via templating. Essential for scalable agents.

App mapping:

* `prompts.py` → `build_prompt(context: str, question: str) -> list`

---

**Lab 3 – Basic Tool Use** (`3_lab3.py`)

**Educational goal:**

Introduce the idea of **agent tool use** (calling Python functions).
Agent doesn't have to “know” everything — it can ask tools for help.

**What it does:**

* Adds a custom Python function:

  ```python
  def get_current_time():
      return datetime.now().isoformat()
  ```
* Injects a **tool definition** into the `ChatCompletion.create(...)` call via the `tools` parameter
* Reads `function_call` from OpenAI response and **manually executes** matching function

**Core concept:**

> Agents can call functions you define — a core idea for agentic workflows.

App mapping:

* `tools.py` → `get_current_time()`
* `agent.py` → logic for parsing `function_call`, calling the function

---

**Lab 4 – Tool Arguments** (`4_lab4.py`)

**Educational goal:**

Expand tool usage by adding **structured arguments** to tools (e.g., `get_weather(city=...)`)

**What it does:**

* Adds a new tool: `get_weather(city: str)`
* Creates an OpenAI tool schema with `parameters` (type: object, properties)
* Handles dynamic tool calling with arguments parsed via `eval(...)`

**Core concept:**

> Tools can take structured inputs. You must define a schema and parse the call safely.

App mapping:

* `tools.py` → add `get_weather(city: str)`
* `agent.py` → improve `run_agent()` to handle tool arguments

---

✅ **Foundations Phase Summary**

| Lab | Concept                      | App Module             |
| --- | ---------------------------- | ---------------------- |
| 01  | Roles: system/user/assistant | `prompts.py`           |
| 02  | Templates                    | `prompts.py`           |
| 03  | Simple tool use              | `tools.py`, `agent.py` |
| 04  | Structured tools + parsing   | `tools.py`, `agent.py` |

---

🧩 `src/foundations/` File Overview

```text
src/foundations/
├── app.py            ← main loop or entry script
├── prompts.py        ← prompt builders for lab1 + lab2
├── tools.py          ← tool functions (lab3 + lab4)
├── agent.py          ← call OpenAI, handle tool calls
└── types.py (opt)    ← tool schemas, types (future labs)
```
**how each lab maps to your current app:**

| Lab | Concept                        | How to reproduce it                     |
| --- | ------------------------------ | --------------------------------------- |
| 1   | Basic system + user prompt     | `run_agent("What is 2 + 2?")`           |
| 2   | Dynamic prompt template        | Customize the system prompt or question |
| 3   | Tool use: `get_current_time()` | Ask: “What time is it?”                 |
| 4   | Tool with args: `get_weather`  | Ask: “What’s the weather in Barcelona?” |
