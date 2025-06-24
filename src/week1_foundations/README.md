# 🧠 Week 1: Advanced Foundations Implementation

This module represents my **advanced implementation** of Week 1 from the AI Agents course, going far beyond the basic examples to create a production-ready, multi-model AI agent system.

## 📋 **RECENT UPDATES & FIXES**

### 🚨 **Critical Issues Resolved** 
- ✅ **Notebook Lab 2 Error Fixed**: Resolved `Markdown expects text, not ['gpt-4o-mini', 'gpt-4o', 'gpt-4-turbo']` error
- ✅ **Import Path Corrections**: Updated from `foundations` to `week1_foundations` module paths
- ✅ **Directory Structure**: Renamed from `1_foundations` to `week1_foundations` (Python-compatible)
- ⚠️ **Port 7860 Conflict**: Added alternative port options (7861, 7862, etc.)
- ✅ **Error Handling**: Robust try/catch blocks added to all notebook cells

### 🔧 **Known Issues & Solutions**
1. **Port Already in Use**: If port 7860 is busy, use `--port 7861` or set `GRADIO_SERVER_PORT=7861`
2. **Virtual Environment**: Always activate with `source .venv/bin/activate` before running
3. **Import Errors**: Run `sys.path.append('src')` in notebooks if imports fail

## 🚀 Advanced Features Implemented

### ✅ **Core Capabilities**
- **Multi-Model Architecture**: Support for OpenAI, Anthropic, Google Gemini, and DeepSeek
- **Automatic Evaluation**: Pydantic-based response quality assessment with scoring
- **Tool Integration**: Dynamic function calling with structured arguments
- **Comparative Analysis**: Side-by-side model performance comparison and ranking
- **Web Interface**: Beautiful Gradio-based UI with 4 interaction modes
- **Error Handling**: Robust error management and graceful degradation
- **Notebook Integration**: Complete Jupyter notebook with all features demonstrated

### 🔧 **Agentic Design Patterns Implemented**
Based on [Anthropic's Agentic AI Framework](https://www.anthropic.com/news/agentic-ai):

#### **Workflow Patterns:**
- ✅ **Parallelization**: Multiple models running simultaneously
- ✅ **Evaluator-Optimizer**: Automatic evaluation with retry loops
- ✅ **Tool Use**: Dynamic function calling with arguments

#### **Agent Patterns:**
- ✅ **Multi-model coordination**: Intelligent model selection and comparison
- ✅ **Quality Assessment**: Continuous response evaluation and improvement

## 📁 Module Structure

```
src/week1_foundations/         # ← Updated directory name
├── agent.py                   # Enhanced agent with multi-model support
├── models.py                  # Multi-provider model management system
├── evaluation.py              # Pydantic-based evaluation and comparison
├── interface.py               # Gradio web interface (4 modes)
├── prompts.py                 # Dynamic prompt templating system
├── tools.py                   # Tool implementations (time, weather)
├── app.py                     # Main application entry point
└── README.md                  # This file

notebooks/week1_foundations/   # ← Updated directory name
└── foundations_demo.ipynb     # Complete demo notebook (FIXED)
```

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.12+
- OpenAI API Key (required)
- Additional API keys (optional but recommended for full features)

### **Environment Variables**
Create a `.env` file in the project root (`my_agents/.env`):
```env
# Required
OPENAI_API_KEY=sk-proj-your-key-here

# Optional (for multi-model comparison)
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-google-key-here
DEEPSEEK_API_KEY=your-deepseek-key-here

# Optional (to avoid port conflicts)
GRADIO_SERVER_PORT=7861
```

### **Dependencies**
All dependencies are managed in the main `pyproject.toml`. Install with:
```bash
cd my_agents/
uv sync  # or pip install -e .
```

## 🚀 Usage

### **Quick Start (Updated Paths)**
```bash
# Method 1: Using launcher script (RECOMMENDED)
python run_week1.py --mode web

# Method 2: Direct execution
source .venv/bin/activate
PYTHONPATH=src python src/week1_foundations/app.py --mode web

# Method 3: Alternative ports (if 7860 is busy)
python run_week1.py --mode web --port 7861
```

### **Troubleshooting Commands**
```bash
# If port 7860 is busy
python run_week1.py --mode web --port 7861

# If import errors occur
PYTHONPATH=src python run_week1.py --mode demo

# Test all systems
PYTHONPATH=src python -c "
import sys; sys.path.append('src')
from week1_foundations.agent import run_agent
print('✅ System working:', run_agent('Hello'))
"
```

### **Notebook Usage**
```bash
# Activate environment first
source .venv/bin/activate

# Launch Jupyter
jupyter notebook notebooks/week1_foundations/foundations_demo.ipynb

# Or use JupyterLab
jupyter lab notebooks/week1_foundations/foundations_demo.ipynb
```

### **Python API Usage**

#### **Basic Agent**
```python
from week1_foundations.agent import run_agent  # Updated import

# Simple query
response = run_agent("What is 2 + 2?")
print(response)  # "2 + 2 equals 4"

# With specific model
response = run_agent("What's the weather in Tokyo?", model_name="gpt-4o")
```

#### **Multi-Model Comparison**
```python
from week1_foundations.agent import run_agent_with_multiple_models

# Compare across all available models
results = run_agent_with_multiple_models("What is the capital of France?")
for model, result in results.items():
    print(f"{model}: {result['response']}")
```

#### **Automatic Evaluation**
```python
from week1_foundations.evaluation import run_agent_with_evaluation

# Get response with quality assessment
result = run_agent_with_evaluation("Explain quantum computing")
print(f"Response: {result['response']}")
print(f"Quality Score: {result['evaluation'].score}/10")
print(f"Feedback: {result['evaluation'].feedback}")
```

#### **Comprehensive Analysis**
```python
from week1_foundations.evaluation import run_comparative_analysis

# Full analysis with evaluation and ranking
analysis = run_comparative_analysis("Compare Python and JavaScript")
print(f"Best Model: {analysis['comparison'].best_model}")

# FIXED: Convert ranking list to formatted text
ranking_text = "\n".join([f"{i+1}. {model}" for i, model in enumerate(analysis['comparison'].ranking)])
print(f"Ranking:\n{ranking_text}")
```

## 🌐 Web Interface Features

Access at `http://localhost:7860` (or alternative port if specified):

### 💬 **Simple Chat**
- Direct conversation with selected model
- Tool usage (time, weather)
- Real-time responses
- Model selection dropdown

### 📊 **Chat with Evaluation**
- Automatic response quality assessment
- Detailed feedback and scoring (1-10 scale)
- Strengths and improvement suggestions
- Retry attempts tracking

### 🏆 **Multi-Model Comparison**
- Side-by-side model comparison
- Automatic ranking and scoring
- Performance analytics
- Detailed reasoning for rankings

### ⚙️ **System Status**
- Model availability monitoring
- API configuration status
- System health checks
- Real-time configuration display

## 🔧 Technical Architecture

### **Multi-Model Support**
- **OpenAI**: GPT-4o, GPT-4o-mini, GPT-4-turbo
- **Anthropic**: Claude 3 Sonnet, Claude 3 Haiku
- **Google**: Gemini 2.0 Flash
- **DeepSeek**: DeepSeek Chat

### **Evaluation System**
The system evaluates responses on:
- **Accuracy and correctness**
- **Helpfulness and relevance**
- **Clarity and coherence**
- **Completeness**
- **Appropriateness of tone**

Returns structured evaluation with:
- Overall acceptability (boolean)
- Quality score (1-10)
- Detailed feedback
- Strengths list
- Weaknesses list
- Improvement suggestions

### **Tool System**
Currently implemented tools:
- `get_current_time()`: System time retrieval
- `get_weather(city)`: Weather information (mock data)

**Extensible architecture** for adding new tools:
```python
def new_tool(arg1: str, arg2: int) -> str:
    """Tool description for LLM"""
    return f"Result based on {arg1} and {arg2}"

# Automatically converted to OpenAI tool format
```

### **Error Handling**
- Graceful degradation when models are unavailable
- Comprehensive error logging
- Fallback to available models
- User-friendly error messages
- **Notebook error recovery** with try/catch blocks

## 🚨 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **1. Port Already in Use Error**
```bash
# Error: OSError: Cannot find empty port in range: 7860-7860
# Solution:
python run_week1.py --mode web --port 7861
# Or set environment variable:
export GRADIO_SERVER_PORT=7861
```

#### **2. Import Errors in Notebook**
```python
# Error: ModuleNotFoundError: No module named 'week1_foundations'
# Solution: Add this to notebook cell:
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.getcwd()), 'src'))
```

#### **3. Virtual Environment Issues**
```bash
# Error: Command not found or import errors
# Solution: Always activate environment first
source .venv/bin/activate
```

#### **4. Lab 2 Notebook Error (FIXED)**
```python
# Error: Markdown expects text, not ['gpt-4o-mini', 'gpt-4o', 'gpt-4-turbo']
# Solution: Already fixed in notebook - converts lists to formatted text
ranking_text = "\n".join([f"{i+1}. {model}" for i, model in enumerate(ranking)])
```

### **Diagnostic Commands**
```bash
# Test all imports
python -c "
import sys; sys.path.append('src')
from week1_foundations.agent import run_agent
from week1_foundations.models import model_manager
print('✅ Available models:', model_manager.get_available_models())
"

# Test basic functionality
python run_week1.py --mode demo

# Check port availability
lsof -i :7860  # Shows what's using port 7860
```

## 📊 Performance & Monitoring

### **Quality Metrics**
- Response quality scoring (1-10 scale)
- Model performance comparison
- Response time tracking
- Success/failure rates

### **Monitoring Features**
- Real-time model availability
- API usage tracking
- Error rate monitoring
- Performance analytics

## 🎯 Comparison with Course Labs

| Feature | Course Lab 1 | Course Lab 2 | Course Lab 3 | Course Lab 4 | My Implementation |
|---------|--------------|--------------|--------------|--------------|-------------------|
| **Basic LLM** | ✅ Simple | ✅ Multi-model | ❌ | ❌ | ✅ **Advanced Multi-model** |
| **Evaluation** | ❌ | ❌ | ✅ Basic | ❌ | ✅ **Pydantic + Scoring** |
| **Tools** | ❌ | ❌ | ❌ | ✅ Basic | ✅ **Dynamic + Structured** |
| **Interface** | ❌ Console | ❌ Console | ✅ Gradio | ✅ Gradio | ✅ **Advanced Web UI** |
| **Comparison** | ❌ | ✅ Manual | ❌ | ❌ | ✅ **Automatic Ranking** |
| **Error Handling** | ❌ | ❌ | ❌ | ❌ | ✅ **Comprehensive** |
| **Production Ready** | ❌ | ❌ | ❌ | ❌ | ✅ **Full Production** |

## 🧪 Testing & Validation

### **System Validation**
```python
# Run comprehensive system test
python run_week1.py --mode demo

# Check model availability
from week1_foundations.models import model_manager
print(model_manager.get_available_models())

# Test evaluation system
from week1_foundations.evaluation import evaluator
result = evaluator.evaluate_response("Test", "Test response")
print(f"Score: {result.score}/10")
```

### **Notebook Validation**
```bash
# Test notebook functionality
source .venv/bin/activate
jupyter nbconvert --to notebook --execute notebooks/week1_foundations/foundations_demo.ipynb
```

### **Unit Tests**
The system includes validation for:
- Model initialization
- Tool calling functionality
- Evaluation system accuracy
- Error handling scenarios
- Notebook cell execution

## 🔒 Security & Best Practices

- **Environment variable protection** for API keys
- **Input validation** and sanitization
- **Error handling** with graceful degradation
- **Rate limiting** awareness
- **Secure model selection**
- **No sensitive data logging**

## 🚀 Deployment Options

### **Local Development**
```bash
# Standard launch
python run_week1.py --mode web

# Alternative port
python run_week1.py --mode web --port 7861

# Background mode
nohup python run_week1.py --mode web --port 7861 > app.log 2>&1 &
```

### **Production Deployment**
```bash
# Public sharing (temporary)
python run_week1.py --mode web --share true

# Custom port with sharing
python run_week1.py --mode web --port 8080 --share true
```

### **HuggingFace Spaces**
Ready for deployment to HuggingFace Spaces with minimal configuration:
1. Upload files to HuggingFace Space
2. Add API keys to Space secrets
3. Set `app.py` as the main file
4. Update port configuration if needed

## 📈 Future Enhancements

### **Planned Improvements:**
- 📄 **Document Processing** (PDF, Word, web scraping)
- 🔗 **Real External APIs** (weather, news, search)
- 💾 **Persistent Memory** and conversation history
- 🔐 **Authentication** and user management
- 📊 **Advanced Analytics** dashboard
- 🤖 **Agent Orchestration** patterns
- 🌍 **Multi-language Support**

### **Resolved Issues (Completed):**
- ✅ **Notebook error fixes** (Lab 2 Markdown issue)
- ✅ **Import path corrections** (foundations → week1_foundations)
- ✅ **Directory structure updates** (Python-compatible naming)
- ✅ **Port conflict handling** (alternative ports)
- ✅ **Error handling improvements** (try/catch blocks)

## 🎓 Educational Value

This implementation demonstrates:
- **Real-world production patterns**
- **Multi-provider AI integration**
- **Quality assurance systems**
- **Modern Python architecture**
- **Web interface development**
- **Evaluation and monitoring**
- **Error handling and debugging**
- **Notebook-based development**

## 🔗 Related Resources

- **Main Project**: [../../README.md](../../README.md)
- **Course Notebooks**: [../../notebooks/week1_foundations/](../../notebooks/week1_foundations/)
- **Original Course**: [agents/1_foundations/](https://github.com/ed-donner/agents/tree/main/1_foundations)
- **Launcher Script**: [../../run_week1.py](../../run_week1.py)
- **Live Demo**: Run `python run_week1.py --mode web` and visit `http://localhost:7860`

## 📋 **Change Log**

### **2024-12-XX - Major Updates**
- 🚨 **FIXED**: Notebook Lab 2 error (`Markdown expects text, not list`)
- 🔧 **UPDATED**: All import paths from `foundations` to `week1_foundations`
- 📁 **RENAMED**: Directory from `1_foundations` to `week1_foundations`
- ⚠️ **ADDED**: Port conflict handling and alternative ports
- ✅ **IMPROVED**: Error handling throughout notebook
- 📝 **UPDATED**: All documentation and usage instructions

---

**🎯 This Week 1 implementation goes far beyond the course requirements, providing a professional-grade foundation for building advanced AI agent systems.**

**🚀 Ready to test?** 

**Basic Usage:**
```bash
python run_week1.py --mode web
```

**If port 7860 is busy:**
```bash
python run_week1.py --mode web --port 7861
```

**For notebook:**
```bash
source .venv/bin/activate
jupyter notebook notebooks/week1_foundations/foundations_demo.ipynb
```
