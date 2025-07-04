# README

- [Sidebar: let's talk about `asyncio`](#sidebar-lets-talk-about-asyncio)
- [Introducing OpenAI Agents SDK](#introducing-openai-agents-sdk)
- [1_lab1 : Our first look at OpenAI Agents SDK](./1_lab1.ipynb) -> [Link 1_Lab1](./1_lab1.ipynb)
- [vibe coding](#vibe-coding)
- [Automated sales outreach](#automated-sales-outreach)
- [2_Lab2 : Our first Agentic Framework project](#2_lab2) -> [Link 2_Lab2](./2_lab2.ipynb)
- [3_Lab_3 : Multi-Model Integration: Using Gemini, DeepSeek & Grok with OpenAI Agents](#3_lab_3--multi-model-integration-several-openai-agents-models) -> [Link 2_Lab2](./3_lab3openAI.ipynb)
- [3_Lab_3 : Multi-Model Integration: several OpenAI Agents models](#3_lab_3_enhanced--advanced-openai-model-optimization) -> [Link 2_Lab2](./3_lab3_openAI_enhanced.ipynb)



## Sidebar: let's talk about `asyncio`

Everything that you've built up over the course of **/week2_openai** is all about the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), formerly known as `SWARM`. But before we get into the SDK, it's important to talk about asynchronous Python: `asyncio`.

* All the Agent Frameworks use asynchronous Python.
* You can get by ignoring it, but it will always bother you slightly.
* Bite the bullet! Spend 30 minutes on the guide—you will thank me!

Asynchronous programming is common across all agentic frameworks. You *can* surVibe by memorizing a couple of rules and applying them blindly, but that's unsatisfactory. If you spend just half an hour understanding what's really happening, you'll thank yourself later. You'll run into asynchronous Python again and again, and being comfortable with it will make a big difference. There are guides you can follow, and I'll give you a high-level summary here.

### The short version

- **All your methods and functions start `async`** The most important rule: anytime you write a function that will be used asynchronously, start it with `async def`.

- **Anytime you call them, use `await`** When you call an async function, you must use the `await` keyword. This is the basic rule, and if you just follow this, you can get most code to work, even if you don't understand all the internals.

- **AsyncIO provides a lightweight alternative to threading or multiprocessing** AsyncIO is a way of writing Python code that achieves concurrency, similar in effect to multithreading, but much lighter. In classic multithreading, you rely on the operating system to switch between threads, each running at the same time. That comes with a lot of complexity and "baggage." AsyncIO, introduced in Python 3.5, achieves concurrency entirely at the code level—without real OS threads or multiprocessing.

Because AsyncIO is so lightweight, you can run thousands or even tens of thousands of tasks at once, using very few resources. This is especially valuable when your code spends a lot of time waiting on input/output (I/O), like network calls.

**Why is this important for agent frameworks and LLMs?**

If you're working with large language models (LLMs), especially via paid APIs like OpenAI, most of your time is spent waiting for network responses. With async code, other parts of your program can continue running while one part is blocked, waiting for a model to respond. In multi-agent systems, where many agents may be hitting different APIs at once, using async is essential for performance and scalability.

All of the agent frameworks we'll look at use AsyncIO for this reason.

### Under the hood: coroutines, `async def`, and `await`

**Functions defined with `async def` are called coroutines**
If you use `async def` to define a function, you're actually creating a coroutine—a special kind of function that Python can pause and resume. Most people still call them functions, but technically, they're coroutines.

**Calling a coroutine doesn't execute it immediately—it returns a coroutine object**
When you call an async function, you don't get the result right away. Instead, you get a coroutine object. No code runs yet!

**To actually run a coroutine, you must `await` it, which schedules it for execution within an event loop**
To get the result from a coroutine, you must use `await` in front of it. This tells Python to run the coroutine in the event loop and return the result when it's finished.

**While a coroutine is waiting (e.g., for I/O), the event loop can run other coroutines**
The event loop can only execute one coroutine at a time. But if a coroutine gets stuck waiting for I/O (like waiting for a response from OpenAI), the event loop pauses that coroutine and runs another one that's ready to go. This allows thousands of tasks to run efficiently, as long as much of the work is I/O-bound.

### Example: The short version

```python
async def do_some_processing() -> str:
    # Do some work
    return "done!"

result = await do_some_processing()
```

* Here, the function starts with `async def`.
* When calling it, you must use `await`.
* This pattern covers 95% of real async Python usage in agentic frameworks.


### Example: Understanding coroutines and awaiting


```python
async def do_some_processing() -> str:
    return "done!"

# Calling the function returns a coroutine object (nothing happens yet)
my_coroutine = do_some_processing()

# Awaiting the coroutine actually runs it and gives the result
my_result = await my_coroutine
```


You might think that just calling `do_some_processing()` would run the function, but it doesn't. It only returns a coroutine object. To actually run it, you must await it.

You can simplify even further by writing:


```python
my_result = await do_some_processing()
```


This is what you'll do in most real code.

### Richer example: running multiple coroutines concurrently

---
```python
results = await asyncio.gather(
    do_some_processing(),
    do_other_processing(),
    do_yet_more_processing()
)
```


Here, `asyncio.gather()` is used to schedule multiple coroutines at once. The event loop will start all three, and whenever one is blocked waiting on I/O, another can run. The results come back as a list.

This is Python's way of implementing "fake" multithreading at the code level. It's not real OS-level threading, but it's often just what you need for highly concurrent, I/O-bound programs like LLM agent frameworks.

---

**Key points to remember**

* Use `async def` for every function that may need to run concurrently.
* Use `await` whenever you call one of these async functions.
* Just calling the function does not run it; it only creates a coroutine object.
* Use constructs like `asyncio.gather` to run multiple coroutines at once.

If you understand these rules and can recognize the code patterns in the examples, you'll be productive with async Python in LLM/agent projects.

> Spend a bit of time with the guide and try the examples—this is the most valuable investment you'll make for working with modern agentic frameworks in Python!

---



## Introducing OpenAI Agents SDK

The OpenAI Agents SDK (formerly known as `SWARM`) is the framework you'll use to build intelligent LLM agents in a highly flexible and efficient way. Before we dive into technical details, here's why it stands out:

* **Lightweight and flexible**
  The SDK is extremely lightweight and remarkably flexible. Unlike more "opinionated" frameworks that force you to work in a certain way, OpenAI Agents SDK gives you maximum freedom to structure your agents and workflows as you prefer.

* **Stays out of the way**
  This framework doesn't get in your way or clutter your code. All the repetitive boilerplate and JSON-handling you'd otherwise have to do is completely abstracted for you.

* **Makes common activities easy**
  Everyday tasks—like using tools, coordinating agent interactions, or applying controls—become trivial. The SDK automates all those low-level mechanics that otherwise slow you down and distract from the core logic.


### Minimal Terminology

OpenAI Agents SDK uses a deliberately minimal, clear vocabulary. There are just three main concepts you need to know:

* **Agents** represent LLMs encapsulated with a specific role or function in your solution.
* **Handoffs** are the interactions between agents. Whenever an agent "hands off" work or information to another, that's a handoff.
* **Guardrails** are the controls and restrictions you put in place to make sure the agent behaves as expected and doesn't go off track. (This term is also common in general software engineering.)

### Three Steps

Running an agent with OpenAI Agents SDK is as simple as following these three core steps:

1. **Create an instance of Agents**
   Instantiate your agent, configuring its purpose and core settings.

2. **Use `with trace()` to track the agents**
   Use the `with trace()` context to log all agent interactions. This makes monitoring and debugging straightforward, and integrates seamlessly with OpenAI's monitoring tools. While optional, it's the recommended approach.

3. **Call `runner.run()` to run the agents**
   Use `runner.run()` to actually execute the agent. Note: this is an async function (a coroutine), so you'll need to `await` it to trigger execution and collect the result.

That's really all there is to it—no complicated jargon, no convoluted rules. The core concepts are minimal and direct, and the SDK makes it easy to focus on agent logic, not plumbing.


OpenAI Agents SDK is my favorite framework because it strikes the perfect balance between flexibility, simplicity, and power. While other frameworks have their strengths and may be best for certain advanced cases, in most projects you'll both start and finish with OpenAI Agents SDK. And, as you move on to more advanced projects (such as MCP in week six), you'll return to this SDK to leverage its full capabilities.

Remember: all agent frameworks come with their own terminology and core ideas, but OpenAI Agents SDK stands out for its clarity, minimalism, and its ability to abstract away repetitive busywork—so you can focus on building smarter agents.

---

**In summary:**

* Create your agent.
* Trace and monitor interactions.
* Run with `runner.run()` and use `await`.

The SDK handles everything else for you. Now, let's walk through these steps in practice.



## vibe coding

**My tips for successful vibing**

* Good vibes – prompt well – ask short answer and latest APIs for today's date.
* Vibe but verify – ask 2 LLMs the same question.
* Step up the vibe – ask to break down your request into independently testable steps.
* Vibe and validate – ask an LLM then get another LLM to check.
* Vibe with variety – ask for 3 solutions to the same problem, pick the best.

**Sidebar: What is Vibe Coding?**

So, that concludes our very first foray into OpenAI Agents SDK, but before we wrap up Week 2 Day 1, I did want to have a second sidebar with you, and this time it's on the entertaining topic of **Vibe coding**, which is a term coined by the legendary Andrej Karpathy, who described this in, I think it was an ex-post that went viral, about the way that he was enjoying coding with LLMs and getting so much done in a way that you would sort of let the LLM generate some code and sort of go with it, tweak it a bit, generate some more, and just make so much progress in this sort of mode of working, this ad hoc Vibe coding way of navigating around things like new frameworks.



**Why Vibe Coding Works**

I think this is wonderful, and I strongly encourage Vibe coding, and I imagine that most of you are very good at it. I did want to give a few tips that I think are important to do it well, because I think it's easy to do Vibe coding and to get led astray by LLMs and get yourself in trouble and get stuck, which is very unpleasant. So, I have five tips to leave you with, but before we get into more detail with OpenAI Agents SDK, and here they are:

**1. Good Vibes**

It's important to spend time getting your prompt to the LLM to be really good, that you can reuse lots of times.
You should ask for short answers. LLMs tend to be quite verbose in the way that they're in their code that they generate.
They like packaging everything with lots of exception handlers, and they tend to do things in quite a long-winded way.
Try and ask it to come up with concise, clean code, and also mention today's date and say, please make sure that you use APIs that are current as of this date.
Otherwise, LLMs have a nasty tendency to use older APIs because that was in a lot of their training data. So, explicitly prompt for that.

**2. Vibe but Verify**

Don't just ask an LLM a question and go with it. Ask a couple of LLMs.
So, I often ask the same question to ChatGPT and to Claude, and I have them both up.
I ask the question because I'll learn from both of the answers.
Often, one of them is too long-winded or is missing the point of it, and one of them will be spot on.
And so, asking a couple or maybe even three so that you're verifying what answers you're getting is a really good technique.

**3. Step Up the Vibe**

This is saying, and I think this is such a great one.
Sometimes students send me problems saying, "I'm stuck with this," and they send me 200 lines of code and say, "It's not working."
It's immediately obvious that this is Vibe coding — you can tell it was LLM-generated and it's unwieldy, often full of bugs.
And I come back and say: It's no good generating 200 lines of code and then saying, "It's broken."
Instead:

* Always try to get LLMs to generate function-by-function.
* Break it into small, independently testable parts — like 10 lines at a time.
* Think of dividing your problem into bite-sized chunks.

> **Tip**: If you don't know how to break it down, ask an LLM:
>
> "I'm trying to solve the following problem [...] — please list 4–5 small steps where each can be tested independently."
>
>Then ask for code (and tests) for each step one by one.
> Build your full solution 10 working lines at a time.

**4. Vibe and Validate**

Similar to "vibe but verify", but here the goal is **refinement**.

* Ask an LLM a question and get an answer.
* Then ask another LLM (or even the same one):

  > "Is this a good answer? Can it be improved? More concise? Clearer? Are there any bugs?"

It often improves the result.
This mirrors a common **agentic design pattern**: evaluator + optimizer.
You can do it manually with two LLMs, inspired by agentic ideas.

**5. Vibe with Variety**

Don't just ask: "Can you generate code for this?"
Instead, say:

> "Give me 3 different solutions to the same problem."

Why?

* Forces the LLM to think differently.
* Encourages multiple perspectives on the same task.
* Often gives better solutions.

Also ask for explanations of the differences and rationale.
That way:

* You'll understand better.
* The LLM is forced to reason through its decisions.
* You stay connected to what's going on.

**Final Note**

This leads to one final, implicit rule:

> Always ask the LLM to explain things clearly if you don't understand.

**Vibe coding is super fun, productive, and powerful.**
But if you don't follow what's happening, it becomes painful and frustrating when something breaks.
**Stay in touch with the logic. Understand every step.**



## Three Layers of Agentic Architecture

We're going to be building **three different pieces**, or layers, of **agentic architecture**:

1. **Basic Agent Workflow**

   * Start simple.
   * A straightforward sequence of agent calls.

2. **Agent with Tool Use**

   * Add complexity.
   * Introduce an agent that can **use a tool**.
   * Recall: we did this manually in Week 1 using JSON and boilerplate.

3. **Agents Calling Other Agents**

   * The most advanced.
   * Two ways to implement this:

     * **Agents as Tools**.
     * **Handoffs** — the special construct introduced earlier.

* Keep this **three-layer structure** in mind.
* This is how we'll be building up complexity in our lab.
* A lot of coding ahead — let's get started.



## 2_Lab2

**Resend Email - Complete Technical Breakdown**

This comprehensive breakdown explains every code and conceptual component of the  
[2_lab2_with_resend_email.ipynb](./2_lab2_with_resend_email.ipynb) implementation.



**1. Prerequisites & Environment Configuration**

* External API Integration Setup
* Environment Security & Validation

**2. Agent Workflow Architecture**

* Multi-Personality Agent Design
* Streaming & Asynchronous Processing
* Agent Selection & Decision Making

**3. Tool Integration & Function Decoration**

* Function-to-Tool Conversion Pattern
* Email Sending Implementation
* Agent-as-Tool Pattern

**4. Multi-Agent Orchestration**

* Planning Agent Architecture
* Workflow Execution

**5. Handoffs vs Tools Architecture**

* Handoff Mechanism
* Email Manager Agent
* Complete Workflow Integration

**6. Agentic Design Patterns Analysis**

* Core Patterns Implemented
* Commercial Applications

**7. Advanced Features & Enhancements**

* Mail Merge System
* CRM Integration

**8. Advanced Challenge: Reply Automation**

* Webhook Integration System
* Self-Sustaining Conversations


## 3_Lab_3 : Multi-Model Integration: several OpenAI Agents models


**Recap - 3 interactions : Agent Tools, Handoffs, and Next Steps**

1. **Tool Decorators** : We simplified the creation of tools using a decorator, eliminating the need for verbose JSON definitions as seen in Week 1.
2. **Agents as Tools** : By using `asTool`, we wrapped agents and exposed them as callable tools—making agent chaining easier and more modular.
3. **Understanding Handoffs vs Tools**
   * **Tools** → Think of it like a *function call*: control returns to the calling agent.
   * **Handoffs** → A *transfer of control*: the receiving agent continues the workflow from that point forward.

**What's Coming Next**

We're now going to **extend** the previous work in **three new directions**:

1. **Using Non-OpenAI Models**
   Learn how to use the **OpenAI Agents SDK** with other models like **Gemini** or **DeepSeek**.
2. **Structured Outputs**
   Make agents return **structured data**, such as custom objects with named fields, instead of plain text.
3. **Guardrails**
   Add **input/output controls** to enforce safety, validity, or formatting constraints in the agent pipeline.

---

**Main Agents:**


| **Agent Name**  | **Model**     | **Role**                   | **Key Functions**                                                           | **Style / Specialty**       |
| --------------- | ------------- | -------------------------- | --------------------------------------------------------------------------- | --------------------------- |
| Sales Manager   | GPT-4o        | Main coordinator           | Evaluates email versions<br>Selects best email<br>Makes strategic decisions | Effectiveness & Strategy    |
| Sales Agent 1   | GPT-4o        | Sales Agent                | Generates email variant                                                     | Professional & serious      |
| Sales Agent 2   | GPT-4o-mini   | Sales Agent                | Generates email variant                                                     | Humorous & engaging         |
| Sales Agent 3   | GPT-3.5-turbo | Sales Agent                | Generates email variant                                                     | Concise & direct            |
| Email Manager   | GPT-4o-mini   | Format specialist          | Generates attractive subjects<br>Converts to HTML<br>Sends via Resend API   | Email formatting & delivery |
| Guardrail Agent | GPT-4o-mini   | Security / Input Validator | Detects personal names<br>Blocks dangerous requests<br>Validates all inputs | Guardrails & Safety         |


**Security Features** : Input Guardrails  
- **Personal name detection**: Prevents use of sensitive information
- **Automatic validation**: Blocks requests before processing
- **Structured outputs**: Ensures consistent data format

**Protection Example:**
```python
# ❌ BLOCKED: "Send email from Alice"
# ✅ ALLOWED: "Send email from Head of Business Development" 
```

**💡 Key Concepts Demonstrated**

1. **Model Comparison**
- **GPT-4o**: Best for complex reasoning and decision-making
- **GPT-4o-mini**: Cost-performance balance for intermediate tasks
- **GPT-3.5-turbo**: Optimal for simple tasks and quick responses

2. **Agent Specialization**  
- Each agent has a specific and optimized role
- Different models for different types of tasks
- Efficient coordination between agents

3. **Structured Outputs**  
```python
class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str
```

4. **Traceability**  
- Complete traces in OpenAI Platform
- Debugging and decision monitoring
- Performance analysis by model

**System Benefits:**

1. **Complete Automation**: From generation to delivery
2. **Multiple Styles**: Variety of tones and approaches
3. **Integrated Security**: Automatic protection against risks
4. **Cost Optimization**: Right model for each task
5. **Scalability**: Easy to add new agents or models

**Real-World Use Cases:**

- **Sales Teams**: Automatic generation of personalized emails
- **Marketing**: A/B testing of different styles
- **Compliance**: Automatic content validation
- **Productivity**: Reduction of time on repetitive tasks


**Key Learnings**

- **Different OpenAI models excel at different tasks**
- **Guardrails are essential for production systems**
- **Agent specialization improves output quality**
- **Structured outputs ensure consistency**
- **Traceability facilitates debugging and optimization**

This system demonstrates how to build **robust and secure AI applications** that intelligently combine multiple models to solve complex real-world problems. 


## 3_Lab_3_Enhanced : Advanced OpenAI Model Optimization

**Enhanced version with comprehensive testing and performance analysis**

**Model Configuration Testing**
- **5 different OpenAI configurations**: Creative (temp=0.9), Balanced (temp=0.7), Precise (temp=0.2), Fast (GPT-4o-mini), Quick (GPT-3.5-turbo)
- **Parameter comparison**: Temperature and max_tokens impact on output quality
- **Agent instruction optimization**: Configurations guide agent behavior for consistent results

**Enhanced Guardrails System**
- **Input validation**: Personal info, inappropriate content, competitor mentions, spam detection
- **Output validation**: Professionalism, compliance, quality scoring
- **Structured validation**: Pydantic models for consistent data validation
- **Multi-layered protection**: Comprehensive security with detailed feedback

**Structured Outputs & Performance Monitoring**
- **EmailOutput model**: Subject, body, tone, key points, CTA, response rate estimation
- **Performance tracking**: Response time, cost estimation, quality scoring
- **Real-time benchmarking**: Comprehensive agent comparison across configurations
- **Efficiency analysis**: Quality-per-dollar optimization

**Key Insights & Results**
| **Configuration** | **Best Use Case** | **Performance** |
|------------------|-------------------|-----------------|
| GPT-4o Creative  | Complex reasoning, high-stakes emails | High quality, higher cost |
| GPT-4o Balanced  | Most business applications | Optimal balance |
| GPT-4o Precise   | Consistent, predictable outputs | High consistency |
| GPT-4o-mini Fast | Cost-effective general tasks | Best value |
| GPT-3.5-turbo Quick | High-volume simple tasks | Fastest, cheapest |

**Production Recommendations**
- **Cost optimization**: Choose model based on specific requirements
- **Quality vs. efficiency**: Balance performance with budget constraints
- **Comprehensive monitoring**: Track metrics continuously for optimization
- **Scalable architecture**: Easy to add new models and configurations

**Enhanced Features**: Multi-configuration testing, advanced guardrails, performance analytics, structured outputs, and production-ready optimization insights. 