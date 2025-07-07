
- [Crew AI](#crew-ai)
- [Core Concepts of Crew AI](#core-concepts-of-crew-ai)
- [LightLLM and CrewAI Project Setup](#lightllm-and-crewai-project-setup)
- [LightLLM and Model Flexibility in CrewAI](#lightllm-and-model-flexibility-in-crewai)
- [Structure and Workflow of a CrewAI Project](#core-concepts-of-crew-ai∫)



## Crew AI

This marks a transition from the familiar **OpenAI Agents SDK** to the world of **Crew AI**. Although the shift may feel abrupt, it's part of an ongoing process of exploring different agent frameworks. Each one offers unique perspectives and tools, and each will be more or less suited depending on the project at hand.

You’re encouraged to:

* Note the similarities and differences between frameworks.
* Decide for yourself which tool best suits your needs.
* Learn something valuable from each one.


**What Is Crew AI?**

**Crew AI** refers to multiple things, depending on context. These include:

**1. Crew AI Enterprise**

Also called the **Crew AI Platform**, this is a commercial platform for:

* Deploying agents
* Monitoring agent behavior
* Managing workflows through various dashboards

You can visit it at: **crewai.com** (not **crew\.ai**)

**2. Crew AI UI Studio**

A **low-code/no-code** tool for:

* Building agent interactions visually
* Allowing end-users to create workflows without coding

**3. Crew AI Framework**

An **open-source** Python framework built for:

> “Orchestrating high-performing AI agents with ease and scale.”

This is the focus of the course: writing code and building agents from scratch using the open-source framework, not the commercial tools.


**Commercial Strategy of Crew AI**

Unlike OpenAI or Anthropic (which monetize via their LLMs), Crew AI:

* Needs a business model built around its tooling
* Offers the **free framework** as entry
* Monetizes through **hosting**, **deployment**, and **enterprise tools**

This is why the website includes heavy upselling — it aims to convert open-source users into paying enterprise customers.


**Two Modes in the Crew AI Framework**

Once inside the open-source framework, there are **two major approaches**:

**1. Crew AI Cruise**

* Teams of agents collaborating
* Roles are assigned to different agents
* Supports **autonomous**, **creative**, or **exploratory** solutions
* Suitable for agentic, unscripted workflows

“Crew” = A team of agents working together

**2. Crew AI Flows**

* Structured and linear workflows
* Tasks are broken into **deterministic steps**
* Includes decision points and expected outcomes
* Useful for **auditability**, **control**, or **predictable behavior**

This is likely a newer addition, possibly a response to concerns about the unpredictability of Cruise-style setups in production environments.


**When to Use Each Mode**

| Mode       | Best For                                                              |
| ---------- | --------------------------------------------------------------------- |
| **Cruise** | Autonomous problem-solving, creative collaboration, exploratory tasks |
| **Flows**  | Deterministic workflows, precision, audit trails                      |


## Core Concepts of Crew AI

**Agent**

An **agent** is the smallest autonomous unit in Crew AI. It is linked to an LLM and includes:

* **Role**: A description of what the agent does
* **Goal**: The purpose or objective of the agent
* **Backstory**: Context or background information for priming
* **Memory**: Optional storage for past interactions
* **Tools**: Optional tools the agent can use

Agents resemble those in OpenAI Agents SDK but are more prescriptive: instead of a single `instruction`, Crew AI uses multiple structured fields (role, goal, backstory).

**Task**

A **task** is a unit of work assigned to an agent. It includes:

* **Description**: What the task is
* **Expected Output**: The desired result
* **Agent**: The agent responsible for executing it

Tasks are a new construct, not present in OpenAI Agents SDK, and help separate logic from behavior.

**Crew**

A **crew** is a combination of:

* Multiple **agents**
* Multiple **tasks**

It defines how agents and tasks work together to solve a problem.

Crew can operate in two modes:

* **Sequential**: Tasks are executed in a defined order
* **Hierarchical**: A manager LLM dynamically assigns tasks to agents

---

**Comparison with OpenAI Agents SDK**

Crew AI is:

* **More opinionated**: Requires structured agent configuration
* **More prescriptive**: Enforces concepts like roles and backstories
* **Less transparent**: The system prompt is generated from multiple fields rather than a single `instruction`, which can make debugging more complex
* **Configurable**: Uses YAML to separate configuration from code

**Configuration via YAML**

Crew AI supports agent and task configuration via YAML files.
Advantages:

* **Separation of concerns**: Prompts and configuration are outside the main Python code
* **Easier to manage**: Especially for larger projects with many agents
* **Readable**: YAML is easy for humans to read and write

You can create agents by:

* Writing code: `Agent(...)`
* Referring to a YAML configuration: e.g. `"config.agent_config['researcher']"

**Python Structure: `crew.py`**

This is the main module where agents, tasks, and crews are defined.

**Decorators**

Crew AI uses decorators to structure the code:

| Decorator    | Purpose                                        |
| ------------ | ---------------------------------------------- |
| `@crew_base` | Marks the main class managing the crew         |
| `@agent`     | Decorates a method that defines an agent       |
| `@task`      | Decorates a method that defines a task         |
| `@crew`      | Decorates the function that assembles the crew |

These decorators:

* Register agents and tasks automatically
* Allow referencing `self.agents`, `self.tasks` in the final crew assembly
* Specify mode (`sequential` or `hierarchical`) within the `@crew` function



## LightLLM and CrewAI Project Setup

CrewAI uses **LightLLM**, a minimal and ultra-flexible framework, to connect with any LLM. Unlike heavier frameworks like LangChain, LightLLM allows you to:

* Connect instantly to hosted or local LLMs
* Use almost any provider or model
* Configure access easily in code or `.env` files

**Example usage**

```python
llm = LLM(model="openai/gpt-4o-mini")
llm = LLM(model="anthropic/claude-3-5-sonnet-latest")
llm = LLM(model="gemini/gemini-2-0-flash")
llm = LLM(model="groq/llama-3-70b-versatile")
llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
llm = LLM(
    model="openrouter/deepseek/deepseek-r1",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)
```

* The model format: `"provider/model"`
* Supports OpenAI, Anthropic, Gemini, Groq, Ollama, OpenRouter, etc.
* Can also run local models (e.g., via Ollama)



## LightLLM and Model Flexibility in CrewAI

One of the key advantages of CrewAI is its lightweight and flexible way of interacting with LLMs. Under the hood, it uses a framework called LightLLM. LightLLM is a very minimalistic and straightforward tool to interface with actual LLM providers. The speaker likes LightLLM a lot because of its simplicity and lack of overhead, especially compared to frameworks like LangChain, which add a lot of structure.

LightLLM allows you to connect to any LLM easily. In CrewAI, you just create an LLM by passing a model name. The naming structure follows this pattern: provider name followed by a slash, then the model name. This makes it easy to switch between different providers and models.

Examples include GPT-4 from OpenAI, Claude from Anthropic, 3.5 and 3.7 versions, Gemini, Flash, Grok (with a “Q” or a “K”), and local models using Ollama. For local models, you can configure them by providing a base URL. You can also use OpenRouter, which acts as an abstraction layer over multiple LLMs. Configuring OpenRouter involves setting a base URL and an API key.

The idea behind all of this is to provide a simple and flexible system for connecting to any model you need. The speaker believes this gives CrewAI a clear advantage over OpenAI Agents SDK, which is more tightly coupled to a specific provider.


## Structure and Workflow of a CrewAI Project

The next major topic is how CrewAI handles projects. In earlier weeks of the course, everything was done inside Python notebooks (like in Cursor), or occasionally through basic Python modules. CrewAI, however, does not work that way. It requires working with actual Python code and comes with its own project and directory structure.

The CrewAI framework has already been installed using this command:

```bash
uv tool install crewai
```

That means when you clone the repo, the framework is already available.

To create a new Crew project, you use this command:

```bash
crewai create crew my_crew
```

You can name the project whatever you want. For example, “my\_crew” or “my\_project.”

Alternatively, if you want to work with flows instead of crews (i.e., fixed workflows rather than agent-based ones), you can use:

```bash
crewai create flow my_project
```

However, in the course, the focus is on crews, not flows.

Running the `crewai create crew` command generates a full directory structure. At the top level is the project directory, such as `my_crew`. Inside that is a subdirectory called `src`. Within `src`, there is another directory with the name of your project, such as `my_crew` again.


```bash
(agents_env) ➜  my_agents git:(main) ✗ cd notebooks/week3_crew 
(agents_env) ➜  week3_crew git:(main) ✗ crewai create crew debate
Creating folder debate...
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
  - Created debate/.gitignore
  - Created debate/pyproject.toml
  - Created debate/README.md
  - Created debate/knowledge/user_preference.txt
  - Created debate/src/debate/__init__.py
  - Created debate/src/debate/main.py
  - Created debate/src/debate/crew.py
  - Created debate/src/debate/tools/custom_tool.py
  - Created debate/src/debate/tools/__init__.py
  - Created debate/src/debate/config/agents.yaml
  - Created debate/src/debate/config/tasks.yaml
Crew debate created successfully!
```


```bash
(agents_env) ➜  week3_crew git:(main) ✗ cd debate
(agents_env) ➜  debate git:(main) ✗ tree
.
├── README.md
├── knowledge
│   └── user_preference.txt
├── pyproject.toml              # UV project configuration
├── src
│   └── debate
│       ├── __init__.py
│       ├── config
│       │   ├── agents.yaml     # Agent definitions
│       │   └── tasks.yaml      # Task definitions
│       ├── crew.py             # Main logic with decorators
│       ├── main.py             # Entry point for running the crew
│       └── tools
│           ├── __init__.py
│           └── custom_tool.py
└── tests

7 directories, 10 files
```

**Inside debate/:**

Contains a subfolder: `knowledge/`
* File: user_preference.yaml
* Contains user-specific background info.
* Used to pass context to the model (not used in this example).
```bash
(agents_env) ➜  week3_crew git:(main) cat debate/knowledge/user_preference.txt
User name is John Doe.
User is an AI Engineer.
User is interested in AI Agents.
User is based in San Francisco, California.
```

**source/ Folder**:

Path: `debate/source/debate/`

This nested structure exists because the project name is also **debate**.  

Subfolder: `config/` This folder contains two YAML files by default:
* `agents.yaml`, where you define agent configurations.
* `tasks.yaml`, where you define task configurations.
* Both with defeault examples.

Subfolder: `tools/`
* Empty or with placeholder code
* For adding custom tools later (not used in this example)

Python files:  
Also in the same directory are two important Python modules:
* `crew.py`, which is where you define your crew using decorators.
* `main.py`, which is the script that starts the execution of your crew.

```sh
mkdir other # ← optional dummy folder to make VS Code show tree view properly
```

**Now we going to define our YAML**

our configuration for our `agents.yaml` :

And this contains some default, some sort of scaffolding, some example agents that are called the Researcher and the Reporting Analyst are the two examples it's given and we're going to change these to being what we're looking to build, and of course **we're looking to build a little debate team**, and in fact we only need **two agents** for what we're looking to do. We want an agent that will be the debater. One agent is going to play both roles of being for and against the motion 

```yaml
debater:
  role: >
    A compelling debater
  goal: >
    Present a clear argument either in favor of or against the motion. The motion is: {motion}
```
So now we have a back story... you're an experienced debater with a knack for giving concise but convincing arguments. You can also specify what model to use... GPT-40 Mini... or OpenAI/GPT-40 Mini...

```yaml
  backstory: >
    You're an experienced debator with a knack for giving concise but convincing arguments.
    The motion is: {motion}
  llm: openai/gpt-4o-mini
```
> Note : the `{motion}` fields acts as a dynamic template that will in `main.py`

But now let’s define our judge... the role we will say is decide the winner of the debate.. 

```yaml
judge:
  role: >
    Decide the winner of the debate based on the arguments presented
  goal: >
    Given arguments for and against this motion: {motion}, decide which side is more convincing,
    based purely on the arguments presented.
```

You’re a fair judge with a reputation for weighing up arguments without factoring in your own views... You can just have GPT-40 Mini, or... anthropic/claude-3-7-sonnet-latest...

```yaml
  backstory: >
    You are a fair judge with a reputation for weighing up arguments without factoring in
    your own views, and making a decision based purely on the merits of the argument.
    The motion is: {motion}
  llm: anthropic/claude-3-7-sonnet-latest
```

Next up is `tasks.yaml`:

The first task is to propose the motion — that is, give a strong argument in favor of it.
This task is assigned to the debater agent. 

```yaml
propose:
  description: >
    You are proposing the motion: {motion}.
    Come up with a clear argument in favor of the motion.
    Be very convincing.
  expected_output: >
    Your clear argument in favor of the motion, in a concise manner.
  agent: debater
  output_file: output/propose.md
```

The second task is to oppose the motion — that is, produce a strong argument against it.
Again, the same debater agent is used, but now in oposición.

```yaml
oppose:
  description: >
    You are in opposition to the motion: {motion}.
    Come up with a clear argument against the motion.
    Be very convincing.
  expected_output: >
    Your clear argument against the motion, in a concise manner.
  agent: debater
  output_file: output/oppose.md
```
Finally, the judge reviews the arguments and makes a decision about which side is more convincing.

```yaml
decide:
  description: >
    Review the arguments presented by the debaters and decide which side is more convincing.
  expected_output: >
    Your decision on which side is more convincing, and why.
  agent: judge
  output_file: output/decide.md
```

final result:

```yaml
propose  →  debater  →  output/propose.md
oppose   →  debater  →  output/oppose.md
decide   →  judge    →  output/decide.md
```





To run the project, use:

```bash
crewai run
```

Internally, this runs:

```bash
uv run main.py
```

This setup creates a complete UV (micro) project. So when you run `crewai create crew`, it automatically generates UV project configuration files. These UV projects will be nested within the larger UV project that contains the entire course. This structure will become more intuitive once you see it in practice.

**Final Note Before Practice**

The course is now ready to start using CrewAI hands-on. Everything is set up with UV, CrewAI is installed, and the directory structure has been generated. The next step is to go ahead and actually try it out by building your own crew.
