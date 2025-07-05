#!/usr/bin/env python3
"""
Deep Research System - Gradio Interface

A streamlined web interface for the deep research system.
For more options, use main.py
"""

import gradio as gr
import asyncio
from dotenv import load_dotenv
from research_manager import ResearchManager

# Load environment variables
load_dotenv(override=True)

async def run_research(query: str, send_email: bool = False):
    """
    Run research and yield progress updates for Gradio
    
    Args:
        query: Research query string
        send_email: Whether to send email or just preview
    """
    if not query.strip():
        yield "❌ Please enter a research query"
        return
    
    # Initialize research manager
    manager = ResearchManager(
        send_email=send_email,
        save_html=True,
        output_dir="output"
    )
    
    # Run research and stream updates
    output_text = "Starting Deep Research...\n\n"
    yield output_text
    
    try:
        async for update in manager.run(query):
            if isinstance(update, str):
                # Progress update
                output_text += update + "\n"
                yield output_text
            elif isinstance(update, dict):
                # Final result
                if update.get('status') == 'success':
                    output_text += "\n" + "="*50 + "\n"
                    output_text += "✅ RESEARCH COMPLETED!\n"
                    output_text += f"Searches performed: {update.get('searches_performed', 0)}\n"
                    output_text += f"⏱Duration: {update.get('duration_seconds', 0):.1f} seconds\n"
                    
                    if update.get('html_file'):
                        output_text += f"💾 HTML report saved: {update['html_file']}\n"
                    
                    email_result = update.get('email_result', {})
                    if email_result.get('status') == 'sent':
                        output_text += "📧 Email sent successfully!\n"
                    elif email_result.get('status') == 'preview':
                        output_text += "Email preview generated (check output/ directory)\n"
                    elif email_result.get('status') == 'failed':
                        output_text += f"❌ Email failed: {email_result.get('error', 'Unknown error')}\n"
                    
                    output_text += "="*50 + "\n\n"
                    yield output_text
                else:
                    # Error case
                    output_text += f"\n❌ Research failed: {update.get('error', 'Unknown error')}\n"
                    yield output_text
                
    except Exception as e:
        output_text += f"\n❌ Unexpected error: {str(e)}\n"
        yield output_text

# Create Gradio interface
with gr.Blocks(
    theme=gr.themes.Default(primary_hue="sky"),
    title="Deep Research System",
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    .gr-button-primary {
        background: linear-gradient(45deg, #007bff, #0056b3) !important;
    }
    """
) as interface:
    
    # Header
    gr.Markdown("""
    # 🔍 Deep Research System
    ### Automated AI-Powered Research with Professional Reporting
    
    Enter a research topic and get a comprehensive report with sources, analysis, and professional formatting.
    """)
    
    # Main interface
    with gr.Row():
        with gr.Column(scale=2):
            query_input = gr.Textbox(
                label="Research Query",
                placeholder="e.g., Latest AI Agent frameworks in 2025, Quantum computing applications in finance",
                lines=3,
                max_lines=5
            )
            
            with gr.Row():
                email_checkbox = gr.Checkbox(
                    label="📧 Send Email Report",
                    value=False,
                    info="Send formatted report to configured email address"
                )
                run_button = gr.Button(
                    "Start Research", 
                    variant="primary", 
                    size="lg",
                    scale=2
                )
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### Quick Tips:
            - **Be specific** in your queries
            - **Check costs** - ~$0.08 per research
            - **Monitor progress** in real-time
            - **HTML reports** saved to `output/`
            - **Email features** require RESEND_API_KEY
            """)
    
    # Output area
    output_display = gr.Textbox(
        label="Research Progress & Results",
        lines=25,
        max_lines=35,
        show_copy_button=True,
        interactive=False
    )
    
    # Examples section
    gr.Markdown("### 💡 Example Queries:")
    gr.Examples(
        examples=[
            ["Latest AI Agent frameworks in 2025"],
            ["Best practices for machine learning deployment in production"],
            ["Quantum computing applications in financial services"],
            ["Sustainable energy technologies and market trends 2024"],
            ["Cybersecurity threats and defense strategies for SMBs"],
            ["Future of autonomous vehicles and regulatory challenges"],
            ["Blockchain adoption in supply chain management"],
            ["Mental health technology solutions and effectiveness"]
        ],
        inputs=query_input,
        label="Click any example to try it"
    )
    
    # Event handlers
    run_button.click(
        fn=run_research,
        inputs=[query_input, email_checkbox],
        outputs=output_display
    )
    
    query_input.submit(
        fn=run_research,
        inputs=[query_input, email_checkbox],
        outputs=output_display
    )
    
    # Footer information
    gr.Markdown("""
    ---
    
    ### 🛠️ System Information:
    - **Multi-Agent Architecture**: Planner → Search → Writer → Email
    - **Parallel Processing**: Concurrent web searches for speed
    - **Professional Output**: Structured reports with HTML formatting
    - **Cost Effective**: ~$0.08-0.10 per comprehensive research query
    - **Traceable**: Full observability via OpenAI traces
    
    ### 📧 Email Features:
    Set up your environment variables for email functionality:
    - `RESEND_API_KEY` - Your Resend API key
    - `FROM_EMAIL` - Sender email address  
    - `TO_EMAIL` - Recipient email address
    
    ### Advanced Usage:
    For command-line interface and programmatic access, use `main.py`
    
    **Built with OpenAI Agents SDK**
    """)

if __name__ == "__main__":
    print("Launching Deep Research System...")
    print("Email features:", "enabled" if gr.utils.get_space_from_environ() else "check your .env file")
    print("Access the interface in your browser")
    
    interface.launch(
        inbrowser=True,
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )

