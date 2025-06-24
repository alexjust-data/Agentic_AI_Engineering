# 🧠 My AI Agents Learning Project

This is my personal implementation and learning journey through the **"Master AI Agentic Engineering"** course, building autonomous AI agents step by step.

## 📚 Course Structure & Progress

Following the 6-week course structure from [AI Agents Course](https://github.com/ed-donner/agents):

| Week | Module | Status | Description |
|------|--------|--------|-------------|
| 1️⃣ | **week1_foundations** | ✅ **COMPLETE** | Basic AI theory, multi-model support, evaluation |
| 2️⃣ | **week2_openai** | 🚧 **IN PROGRESS** | OpenAI Agents SDK, deep research systems |
| 3️⃣ | **week3_crew** | ⏳ **PLANNED** | CrewAI framework, multi-agent collaboration |
| 4️⃣ | **week4_langgraph** | ⏳ **PLANNED** | LangGraph workflows, complex agent orchestration |
| 5️⃣ | **week5_autogen** | ⏳ **PLANNED** | Microsoft AutoGen, distributed agent systems |
| 6️⃣ | **week6_mcp** | ⏳ **PLANNED** | Model Context Protocol, advanced integrations |

## 🚀 What I've Built So Far

### **✅ Week 1: Foundations (COMPLETED)**
- **Multi-model architecture** (OpenAI, Anthropic, Google, DeepSeek)
- **Automatic evaluation system** with Pydantic models
- **Web interface** with Gradio (4 interaction modes)
- **Tool integration** (time, weather)
- **Comparative analysis** across models
- **Quality scoring** and feedback systems

**🌐 Live Demo:** `python src/week1_foundations/app.py --mode web`

## 📁 Project Structure

```
my_agents/
├── src/                          # My implementations by week
│   ├── week1_foundations/       # ✅ Advanced agent system (COMPLETE)
│   ├── week2_openai/            # 🚧 OpenAI Agents SDK (IN PROGRESS)
│   ├── week3_crew/              # ⏳ CrewAI implementation (PLANNED)
│   ├── week4_langgraph/         # ⏳ LangGraph workflows (PLANNED)
│   ├── week5_autogen/           # ⏳ AutoGen systems (PLANNED)
│   └── week6_mcp/               # ⏳ MCP integration (PLANNED)
├── notebooks/                   # Learning notebooks by week
│   ├── week1_foundations/
│   ├── week2_openai/
│   ├── week3_crew/
│   ├── week4_langgraph/
│   ├── week5_autogen/
│   └── week6_mcp/
├── pyproject.toml              # Dependencies for all modules
└── readme.md                   # This file
```

## 🛠️ Setup & Installation

### **Prerequisites**
- Python 3.12+
- OpenAI API Key (required)
- Additional API keys (optional but recommended)

### **Quick Start**
```bash
# Clone/navigate to project
cd my_agents/

# Install dependencies
uv sync

# Setup environment variables
cp .env.example .env
# Add your API keys to .env

# Test Week 1 implementation
python src/week1_foundations/app.py --mode web
```

### **Environment Variables**
```env
# Required
OPENAI_API_KEY=sk-proj-your-key-here

# Optional (for multi-model comparison)
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-google-key-here
DEEPSEEK_API_KEY=your-deepseek-key-here
```

## 🎯 Learning Objectives & Achievements

### **What I've Learned:**
- ✅ **Agentic AI Theory** - Workflow vs Agent patterns
- ✅ **Multi-model Integration** - Working with multiple AI providers
- ✅ **Quality Evaluation** - Automatic response assessment
- ✅ **Tool Integration** - Dynamic function calling
- ✅ **Web Interfaces** - Professional UI development
- ✅ **Production Patterns** - Error handling, monitoring

### **Key Technical Skills Gained:**
- **Python Architecture** - Modular, scalable design
- **API Integration** - Multiple AI provider management
- **Pydantic Validation** - Structured data models
- **Gradio Development** - Interactive web interfaces
- **Evaluation Systems** - Quality assessment and feedback

## 📊 Week 1 Foundations - Detailed Features

Since Week 1 is complete, here are the advanced features implemented:

### **🤖 Multi-Model Support**
- OpenAI (GPT-4o, GPT-4o-mini, GPT-4-turbo)
- Anthropic (Claude 3 Sonnet, Haiku)
- Google (Gemini 2.0 Flash)
- DeepSeek (DeepSeek Chat)

### **📊 Evaluation System**
- Automatic quality scoring (1-10 scale)
- Detailed feedback and suggestions
- Retry loops for quality improvement
- Comparative ranking across models

### **🌐 Web Interface**
- **Simple Chat** - Direct model interaction
- **Chat with Evaluation** - Quality assessment
- **Multi-Model Comparison** - Side-by-side analysis
- **System Status** - Configuration monitoring

### **🔧 Tool System**
- Dynamic function calling
- Structured argument handling
- Current time retrieval
- Weather information (mock)

## 🚀 Usage Examples

### **Quick Test**
```bash
# Console demo
python src/week1_foundations/app.py --mode demo

# Interactive mode
python src/week1_foundations/app.py --mode interactive

# Web interface
python src/week1_foundations/app.py --mode web
```

### **Python API**
```python
# Basic usage
from week1_foundations.agent import run_agent
response = run_agent("What is quantum computing?")

# With evaluation
from week1_foundations.evaluation import run_agent_with_evaluation
result = run_agent_with_evaluation("Explain AI agents")
print(f"Quality: {result['evaluation'].score}/10")

# Multi-model comparison
from week1_foundations.evaluation import run_comparative_analysis
analysis = run_comparative_analysis("Compare Python vs JavaScript")
print(f"Best model: {analysis['comparison'].best_model}")
```

## 📈 Progress Tracking

### **Current Status:**
- 🎯 **Week 1**: 100% Complete - Advanced implementation
- 🎯 **Week 2**: Starting soon - OpenAI Agents SDK
- 🎯 **Overall Progress**: 16.7% (1/6 weeks complete)

### **Next Milestones:**
1. **Week 2: OpenAI Agents SDK** - Advanced agent workflows
2. **Week 3: CrewAI** - Multi-agent collaboration
3. **Week 4: LangGraph** - Complex orchestration patterns

## 🎓 Learning Philosophy

This project represents:
- **Learning by Building** - Implementing concepts immediately
- **Going Beyond Examples** - Adding advanced features
- **Production Readiness** - Building real-world capable systems
- **Progressive Complexity** - Each week builds on the previous

## 🔗 Resources

- **Original Course**: [AI Agents Course](https://github.com/ed-donner/agents)
- **Week 1 Detailed Docs**: [src/week1_foundations/README.md](src/week1_foundations/README.md)
- **Course Notes**: Available in `notebooks/` directory
- **Live Interface**: `http://localhost:7860` (when running)

---

**🎯 Ready to explore AI agents?** Start with Week 1:
```bash
python src/week1_foundations/app.py --mode web
```

**📚 Continue Learning:** Progress through each week following the course structure!

