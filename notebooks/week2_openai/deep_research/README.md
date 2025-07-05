# 🔍 Deep Research System

A complete, production-ready agentic research system that combines web search, AI analysis, and professional reporting with HTML email delivery.

## ✨ Features

- **🤖 Multi-Agent Architecture**: Coordinated agents for planning, searching, writing, and email delivery
- **🌐 Intelligent Web Search**: Automated query planning with parallel search execution  
- **📝 Professional Reports**: Structured markdown reports with summaries and follow-up questions
- **📧 HTML Email Integration**: Beautiful email formatting with CSS styling
- **👁️ Preview Mode**: Generate and preview emails without sending
- **💾 File Output**: Save HTML reports to disk for sharing
- **🔍 Trace Monitoring**: Complete observability via OpenAI platform
- **⚙️ Configurable**: Flexible settings for email, output, and search parameters

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
# Copy example environment file
cp env_example.txt .env

# Edit .env with your API keys
# Required: OPENAI_API_KEY
# Optional: RESEND_API_KEY (for email features)
```

### 3. Run the System

**Web Interface (Recommended):**
```bash
python main.py
```

**Command Line:**
```bash
# Preview mode (no email)
python main.py --preview "Latest AI Agent frameworks in 2025"

# With email sending
python main.py --email "Quantum computing applications in finance"

# CLI only
python main.py --cli "Sustainable energy technologies"
```

## 📋 Usage Examples

### Web Interface
The Gradio web interface provides the easiest way to use the system:
- Enter your research query
- Choose whether to send emails
- Monitor progress in real-time
- View results and download HTML reports

### Programmatic Usage

```python
from research_manager import ResearchManager, quick_research

# Quick research with preview
result = await quick_research("AI trends 2025", send_email=False)

# Full configuration
manager = ResearchManager(
    send_email=True,
    save_html=True,  
    output_dir="my_reports"
)

async for update in manager.run("Your research query"):
    print(update)
```

### Advanced Configuration

```python
# Preview only mode
manager = ResearchManager(send_email=False)
result = await manager.preview_only("Research query")

# Get last generated HTML
html_content = manager.get_last_html()

# Get last report data
report = manager.get_last_report()
```

## ⚙️ Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Email Configuration (Optional)
RESEND_API_KEY=re_your-key-here
FROM_EMAIL=noreply@yourdomain.com
TO_EMAIL=recipient@example.com

# Research Settings (Optional)  
HOW_MANY_SEARCHES=3
OUTPUT_DIR=output
```

### Agent Configuration

Edit individual agent files to customize behavior:
- `planner_agent.py` - Search planning strategy
- `search_agent.py` - Web search instructions  
- `writer_agent.py` - Report writing style
- `email_agent.py` - Email formatting rules

## 📊 System Architecture

```
Research Query
     ↓
Planner Agent → Search Plan (3-5 searches)
     ↓
Search Agent → Parallel Web Searches
     ↓  
Writer Agent → Structured Report
     ↓
Email Agent → HTML Email + File Output
```

### Agent Specialization

| Agent | Model | Role | Key Functions |
|-------|-------|------|---------------|
| **Planner** | GPT-4o-mini | Strategy | Query analysis, search planning |
| **Search** | GPT-4o-mini | Research | Web search, result summarization |
| **Writer** | GPT-4o-mini | Synthesis | Report structuring, content creation |
| **Email** | GPT-4o-mini | Delivery | HTML conversion, email formatting |

## 💰 Cost Analysis

**Typical costs per research query:**
- WebSearchTool: $0.025 × 3 searches = $0.075
- GPT-4o-mini processing: ~$0.01-0.02  
- **Total: ~$0.08-0.10 per query**

Cost optimization tips:
- Use `search_context_size="low"` for cheaper searches
- Limit number of searches (3-5 recommended)
- Cache results for repeated queries

## 🛠️ Development

### Project Structure

```
deep_research/
├── main.py              # Main entry point
├── research_manager.py  # Core orchestration logic
├── planner_agent.py     # Search planning agent
├── search_agent.py      # Web search agent  
├── writer_agent.py      # Report writing agent
├── email_agent.py       # Email formatting agent
├── requirements.txt     # Dependencies
├── env_example.txt      # Environment template
└── output/             # Generated reports
```

### Adding New Features

**Custom Search Sources:**
Edit `search_agent.py` to integrate additional APIs or databases.

**Report Templates:**
Modify `writer_agent.py` instructions for industry-specific formats.

**Email Styling:**
Update CSS in `email_agent.py` for custom branding.

**New Output Formats:**
Add agents for PDF, Word, or other format generation.

## 🔍 Troubleshooting

### Common Issues

**"HTML email showing as code":**
- Verify `RESEND_API_KEY` is set correctly
- Check that email agent uses `'html'` field not `'text'`
- Test with preview mode first

**"WebSearchTool not working":**
- Verify `OPENAI_API_KEY` has sufficient credits
- Check tool_choice="required" in search agent
- Monitor usage at platform.openai.com

**"Report quality issues":**
- Increase search context size (costs more)
- Add more searches in planner agent
- Enhance writer agent instructions

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View traces at: https://platform.openai.com/traces

## 📈 Performance Benchmarks

**Typical execution times:**
- Search planning: 5-10 seconds
- Parallel searches: 15-30 seconds  
- Report generation: 20-45 seconds
- Email formatting: 5-15 seconds
- **Total: 45-100 seconds end-to-end**

## 🏢 Commercial Applications

- **Business Intelligence**: Market research, competitive analysis
- **Due Diligence**: Investment research, company analysis
- **Content Creation**: Research-backed articles, reports
- **Academic Research**: Literature reviews, trend analysis
- **News Monitoring**: Industry updates, regulatory changes

## 📄 License

MIT License - see individual notebook for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request with clear description

## 📞 Support

- Check existing issues in the main repository
- Review trace logs at OpenAI platform
- Test with preview mode before reporting email issues

---

**Built with OpenAI Agents SDK - The lightweight, flexible framework for production AI agents.** 