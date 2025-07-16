
## Building AI Teams: Configure Crew AI for Collaborative Development

In this project, we’re transforming our CODA into a **full engineering team**, composed of specialized agents: an engineering lead, a back-end engineer, a front-end engineer, and a test engineer. Each agent is given a **clear role and a specific task**, and they collaborate to create a complete Python module with a simple UI and unit tests.

```sh
(agents) ➜  my_agents git:(main) cd notebooks/week3_crew 
(agents) ➜  week3_crew git:(main) crewai create crew engineering_team
Creating folder engineering_team...
Cache expired or not found. Fetching provider data from the web...
Downloading  [####################################]  577286/26936
Select a provider to set up:
1. openai
2. anthropic
3. gemini
4. nvidia_nim
5. groq
6. huggingface
7. ollama
8. watson
9. bedrock
10. azure
11. cerebras
12. sambanova
13. other
q. Quit
Enter the number of your choice or 'q' to quit: 1
Select a model to use for Openai:
1. gpt-4
2. gpt-4.1
3. gpt-4.1-mini-2025-04-14
4. gpt-4.1-nano-2025-04-14
5. gpt-4o
6. gpt-4o-mini
7. o1-mini
8. o1-preview
q. Quit
Enter the number of your choice or 'q' to quit: 3
Enter your OPENAI API key (press Enter to skip): 
API keys and model saved to .env file
Selected model: gpt-4.1-mini-2025-04-14
  - Created engineering_team/.gitignore
  - Created engineering_team/pyproject.toml
  - Created engineering_team/README.md
  - Created engineering_team/knowledge/user_preference.txt
  - Created engineering_team/src/engineering_team/__init__.py
  - Created engineering_team/src/engineering_team/main.py
  - Created engineering_team/src/engineering_team/crew.py
  - Created engineering_team/src/engineering_team/tools/custom_tool.py
  - Created engineering_team/src/engineering_team/tools/__init__.py
  - Created engineering_team/src/engineering_team/config/agents.yaml
  - Created engineering_team/src/engineering_team/config/tasks.yaml
Crew engineering_team created successfully!
(agents) ➜  week3_crew git:(main) ✗ 
```



### Defined in `agents.yaml`

We start by deleting the boilerplate agents (`researcher` and `reporting_analyst`) and defining four custom agents:

**Engineering Lead**

* **Role**: Takes high-level requirements and produces a **detailed design** (in Markdown) for a single Python module.
* **LLM**: `gpt-4o` (chosen for planning and synthesis).
* **Backstory**: A seasoned lead who writes clear and concise designs.

**Backend Engineer**

* **Role**: Implements the Python module based on the design.
* **LLM**: `claude-3-sonnet` (excellent for clean, efficient code).
* **Backstory**: A Python expert who follows designs carefully.

**Frontend Engineer**

* **Role**: Builds a **Gradio UI** (`app.py`) that demonstrates the backend module.
* **LLM**: Also uses `claude-3-sonnet`.
* **Backstory**: A Gradio expert who builds clean prototypes.

**Test Engineer**

* **Role**: Writes **unit tests** for the backend module (`test_<module_name>.py`).
* **LLM**: `deepseek-chat` (diversified for test logic).
* **Backstory**: A QA-focused coder who anticipates edge cases.

Each agent receives relevant **inputs**, like `requirements`, `module_name`, and `class_name`, which are passed dynamically.

### Defined in `tasks.yaml`

Each agent is assigned one task. These tasks act like **user prompts**, while the agents define the **system behavior**.

**`design_task`**

The **engineering lead** uses this task to produce a Markdown blueprint of the module structure, classes, and methods.

```yaml
description: >
  Take the high level requirements described here and prepare a detailed design for the engineer;
  everything should be in 1 python module, but outline the classes and methods in the module.
  Here are the requirements: {requirements}
  IMPORTANT: Only output the design in markdown format, laying out in detail the classes and functions in the module, describing the functionality.
expected_output: >
  A detailed design for the engineer, identifying the classes and functions in the module.
agent: engineering_lead
output_file: output/{module_name}_design.md
```

**`code_task`**

The **backend engineer** receives both the high-level requirements and the design output, then implements it as a valid Python file. The task **explicitly warns** against markdown formatting to avoid corrupting the Python output.

```yaml
description: >
  Write a python module that implements the design described by the engineering lead, in order to achieve the requirements.
  Here are the requirements: {requirements}
expected_output: >
  A python module that implements the design and achieves the requirements.
  IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, or backticks.
agent: backend_engineer
context:
  - design_task
output_file: output/{module_name}
```


**`frontend_task`**

The **frontend engineer** builds a Gradio demo UI that imports and interacts with the backend module. It also inherits context from the `code_task` to correctly reference the backend code.

```yaml
description: >
  Write a gradio UI in a module app.py that demonstrates the given backend class in {module_name}.
  Assume there is only 1 user, and keep the UI very simple indeed - just a prototype or demo.
  Here are the requirements: {requirements}
expected_output: >
  A gradio UI in module app.py that demonstrates the given backend class.
  The file should be ready so that it can be run as-is, in the same directory as the backend module, and it should import the backend class from {module_name}.
  IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, or backticks.
agent: frontend_engineer
context:
  - code_task
output_file: output/app.py
```


**`test_task`**

Finally, the **test engineer** uses the backend module as context and writes a complete suite of unit tests for it. Like the others, it outputs pure code only.

```yaml
description: >
  Write unit tests for the given backend module {module_name} and create a test_{module_name} in the same directory as the backend module.
expected_output: >
  A test_{module_name} module that tests the given backend module.
  IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, or backticks.
agent: test_engineer
context:
  - code_task
output_file: output/test_{module_name}
```
