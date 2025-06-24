"""
Gradio Web Interface for AI Agents System
"""
import gradio as gr
from typing import List, Tuple, Dict, Any
from week1_foundations.agent import run_agent, run_agent_with_multiple_models
from week1_foundations.evaluation import run_agent_with_evaluation, run_comparative_analysis
from week1_foundations.models import model_manager
import os

class AgentInterface:
    """Gradio interface for AI agents system"""
    
    def __init__(self):
        self.default_model = "gpt-4o-mini"
    
    def simple_chat(self, message: str, model: str) -> str:
        """Simple chat interface"""
        if not message.strip():
            return "Please enter a message"
        
        try:
            response = run_agent(message, model)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat_with_evaluation(self, message: str, model: str) -> Tuple[str, str]:
        """Chat with automatic evaluation"""
        if not message.strip():
            return "Please enter a message", "No evaluation available"
        
        try:
            result = run_agent_with_evaluation(message, model, max_retries=1)
            
            response = result['response']
            evaluation = result['evaluation']
            
            eval_markdown = f"""
**Evaluation Summary:**
- **Score:** {evaluation.score}/10
- **Acceptable:** {'Yes' if evaluation.is_acceptable else 'No'}
- **Attempts:** {result['attempts']}

**Feedback:**
{evaluation.feedback}

**Strengths:**
{chr(10).join(['- ' + strength for strength in evaluation.strengths])}

**Suggestions:**
{chr(10).join(['- ' + suggestion for suggestion in evaluation.suggestions])}
"""
            
            return response, eval_markdown
            
        except Exception as e:
            return f"Error: {str(e)}", "Evaluation failed"
    
    def multi_model_comparison(self, message: str, selected_models: List[str]) -> Tuple[str, str, str]:
        """Compare responses across multiple models"""
        if not message.strip():
            return "Please enter a message", "", "No comparison available"
        
        if not selected_models:
            return "Please select at least one model", "", "No models selected"
        
        try:
            analysis = run_comparative_analysis(message, selected_models)
            
            # Format individual responses
            responses_md = "# Model Responses\n\n"
            
            for model_name, response in analysis['responses'].items():
                evaluation = analysis['evaluations'][model_name]
                model_info = model_manager.get_model_info(model_name)
                display_name = model_info.name if model_info else model_name
                
                responses_md += f"## {display_name}\n"
                responses_md += f"**Score:** {evaluation.score}/10\n\n"
                responses_md += f"{response}\n\n---\n\n"
            
            # Comparison Results
            comparison = analysis['comparison']
            best_model_info = model_manager.get_model_info(comparison.best_model)
            best_display = best_model_info.name if best_model_info else comparison.best_model
            
            comparison_md = f"""
## Model Rankings

**Winner:** {best_display}

**Complete Ranking:**
{chr(10).join([f'{i+1}. {model}' for i, model in enumerate(comparison.ranking)])}

**Reasoning:**
{comparison.reasoning}

**Individual Scores:**
{chr(10).join([f'- {model}: {score}/10' for model, score in comparison.scores.items()])}
"""
            
            status = f"Analyzed {len(analysis['responses'])} models successfully!"
            
            return responses_md, comparison_md, status
            
        except Exception as e:
            return f"Error: {str(e)}", "", "Comparison failed"
    
    def get_system_status(self) -> str:
        """Get system status information"""
        status_md = "# System Status\n\n"
        
        # Available models
        available_models = model_manager.get_available_models()
        status_md += "## Available Models\n\n"
        
        for model_name in available_models:
            info = model_manager.get_model_info(model_name)
            status_md += f"- **{info.name}** ({info.provider})\n"
        
        status_md += f"\n**Total Models:** {len(available_models)}\n\n"
        status_md += "\n## API Configuration\n\n"
        
        # API Keys status
        apis = [
            ("OpenAI", "OPENAI_API_KEY"),
            ("Anthropic", "ANTHROPIC_API_KEY"), 
            ("Google", "GOOGLE_API_KEY"),
            ("DeepSeek", "DEEPSEEK_API_KEY")
        ]
        
        for name, env_var in apis:
            key = os.getenv(env_var)
            if key:
                status_md += f"- **{name}**: Configured\n"
            else:
                status_md += f"- **{name}**: Not configured (optional)\n"
        
        status_md += "\n## System Health\n\n"
        
        if available_models:
            status_md += "- **Status**: Ready for production\n"
            status_md += f"- **Default Model**: {self.default_model}\n"
        else:
            status_md += "- **Status**: Needs configuration\n"
            status_md += "- **Issue**: No models available\n"
        
        return status_md

def create_interface() -> gr.Blocks:
    """Create the Gradio interface"""
    
    interface = AgentInterface()
    available_models = model_manager.get_available_models()
    
    if not available_models:
        return gr.Blocks().launch(share=False, prevent_thread_lock=True)
    
    # Custom CSS for better styling
    css = """
    .gradio-container {
        max-width: 1200px !important;
    }
    .model-selection {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
    }
    """
    
    with gr.Blocks(css=css, title="AI Agents Laboratory", theme=gr.themes.Soft()) as demo:
        
        gr.Markdown("""
        # AI Agents Foundation Laboratory
        
        ## Features
        - Multiple AI model support (OpenAI, Anthropic, Google, DeepSeek)
        - Automatic response evaluation with Pydantic models
        - Tool usage (time, weather)
        - Model comparison and ranking
        - Quality scoring and feedback
        
        **Note:** This system implements advanced agentic patterns including evaluation loops, multi-model coordination, and structured tool calling.
        """)
        
        with gr.Tab("Simple Chat"):
            gr.Markdown("### Direct interaction with AI models")
            
            with gr.Row():
                with gr.Column(scale=3):
                    chat_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Ask anything...",
                        lines=3
                    )
                with gr.Column(scale=1):
                    chat_model = gr.Dropdown(
                        choices=available_models,
                        value=available_models[0],
                        label="Model",
                        elem_classes=["model-selection"]
                    )
            
            chat_button = gr.Button("Send", variant="primary")
            chat_output = gr.Textbox(
                label="Response",
                lines=10,
                max_lines=20
            )
            
            chat_button.click(
                interface.simple_chat,
                inputs=[chat_input, chat_model],
                outputs=[chat_output]
            )
        
        with gr.Tab("Chat with Evaluation"):
            gr.Markdown("### AI responses with automatic quality evaluation")
            
            with gr.Row():
                with gr.Column(scale=3):
                    eval_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Ask anything for evaluation...",
                        lines=3
                    )
                with gr.Column(scale=1):
                    eval_model = gr.Dropdown(
                        choices=available_models,
                        value=available_models[0],
                        label="Model",
                        elem_classes=["model-selection"]
                    )
            
            eval_button = gr.Button("Send with Evaluation", variant="primary")
            
            with gr.Row():
                with gr.Column():
                    eval_response = gr.Textbox(
                        label="Model Response",
                        lines=8
                    )
                with gr.Column():
                    eval_details = gr.Markdown(
                        label="Evaluation Details",
                        value="Evaluation will appear here..."
                    )
            
            eval_button.click(
                interface.chat_with_evaluation,
                inputs=[eval_input, eval_model],
                outputs=[eval_response, eval_details]
            )
        
        with gr.Tab("Multi-Model Comparison"):
            gr.Markdown("### Compare responses across multiple AI models")
            
            comparison_input = gr.Textbox(
                label="Your Question",
                placeholder="Enter a question to compare across models...",
                lines=3
            )
            
            model_selection = gr.CheckboxGroup(
                choices=available_models,
                value=available_models[:3] if len(available_models) >= 3 else available_models,
                label="Select Models to Compare",
                elem_classes=["model-selection"]
            )
            
            compare_button = gr.Button("Compare Models", variant="primary")
            
            with gr.Row():
                with gr.Column():
                    comparison_responses = gr.Markdown(
                        label="All Responses",
                        value="Model responses will appear here..."
                    )
                with gr.Column():
                    comparison_analysis = gr.Markdown(
                        label="Comparison Analysis",
                        value="Analysis will appear here..."
                    )
            
            comparison_status = gr.Textbox(label="Status", interactive=False)
            
            compare_button.click(
                interface.multi_model_comparison,
                inputs=[comparison_input, model_selection],
                outputs=[comparison_responses, comparison_analysis, comparison_status]
            )
        
        with gr.Tab("System Status"):
            gr.Markdown("### System configuration and health check")
            
            status_button = gr.Button("Refresh Status", variant="secondary")
            status_display = gr.Markdown(
                value=interface.get_system_status(),
                label="System Information"
            )
            
            status_button.click(
                interface.get_system_status,
                outputs=[status_display]
            )
        
        gr.Markdown("""
        ---
        **Powered by:**
        - OpenAI GPT Models
        - Anthropic Claude (when configured)
        - Google Gemini (when configured)
        - DeepSeek Models (when configured)
        - Pydantic for structured validation
        - Gradio for web interface
        """)
    
    return demo

def launch_interface(share: bool = False, port: int = 7860) -> None:
    """Launch the Gradio interface"""
    demo = create_interface()
    demo.launch(share=share, server_port=port, prevent_thread_lock=True)

if __name__ == "__main__":
    launch_interface() 