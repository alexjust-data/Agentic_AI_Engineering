#!/usr/bin/env python3
"""
Deep Research System - Main Entry Point

This script provides multiple ways to run the deep research system:
1. Gradio web interface (default)
2. Command line interface
3. Programmatic usage

Usage:
    python main.py                          # Launch Gradio UI
    python main.py --cli "query here"       # CLI mode
    python main.py --preview "query here"   # Preview mode (no email)
    python main.py --help                   # Show help
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from research_manager import ResearchManager, quick_research, research_with_email

def load_environment():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path, override=True)
        print("✅ Loaded environment variables from .env")
    else:
        print("⚠️ No .env file found. Create one from env_example.txt")
        # Try to load from parent directories
        load_dotenv(override=True)

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file or environment")
        return False
    
    # Check optional vars
    if not os.getenv('RESEND_API_KEY'):
        print("⚠️ RESEND_API_KEY not set - email features will be disabled")
    
    return True

async def cli_research(query: str, send_email: bool = False, preview_only: bool = False):
    """Run research via command line interface"""
    print(f"🔍 Starting research for: {query}")
    print(f"📧 Email sending: {'enabled' if send_email else 'disabled'}")
    print("=" * 60)
    
    manager = ResearchManager(
        send_email=send_email and not preview_only,
        save_html=True,
        output_dir="output"
    )
    
    # Run research and display progress
    async for update in manager.run(query):
        if isinstance(update, str):
            print(update)
        elif isinstance(update, dict):
            # Final result
            print("\n" + "=" * 60)
            print("📊 RESEARCH SUMMARY:")
            print(f"  Status: {update.get('status', 'unknown')}")
            print(f"  Searches: {update.get('searches_performed', 0)}")
            print(f"  Duration: {update.get('duration_seconds', 0):.1f}s")
            if update.get('html_file'):
                print(f"  HTML saved: {update['html_file']}")
            print("=" * 60)
            
            # Show last HTML if available
            html_content = manager.get_last_html()
            if html_content:
                print(f"\n📧 EMAIL HTML PREVIEW (first 300 chars):")
                print(html_content[:300] + "..." if len(html_content) > 300 else html_content)
            
            return update
    
    return {"status": "completed"}

def launch_gradio():
    """Launch the Gradio web interface"""
    try:
        import gradio as gr
    except ImportError:
        print("❌ Gradio not installed. Run: pip install gradio")
        return
    
    async def run_research(query: str, send_email_enabled: bool = False):
        """Gradio interface function"""
        if not query.strip():
            return "❌ Please enter a research query"
        
        manager = ResearchManager(
            send_email=send_email_enabled,
            save_html=True,
            output_dir="output"
        )
        
        output_text = ""
        async for update in manager.run(query):
            if isinstance(update, str):
                output_text += update + "\n"
                yield output_text
            elif isinstance(update, dict):
                output_text += f"\n📊 Research completed!\n"
                output_text += f"Status: {update.get('status', 'unknown')}\n"
                output_text += f"Duration: {update.get('duration_seconds', 0):.1f}s\n"
                if update.get('html_file'):
                    output_text += f"HTML saved: {update['html_file']}\n"
                yield output_text
    
    # Create Gradio interface
    with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as interface:
        gr.Markdown("# 🔍 Deep Research System")
        gr.Markdown("Enter a research query and get a comprehensive report with sources!")
        
        with gr.Row():
            with gr.Column(scale=3):
                query_input = gr.Textbox(
                    label="Research Query",
                    placeholder="e.g., Latest AI Agent frameworks in 2025",
                    lines=2
                )
            with gr.Column(scale=1):
                email_checkbox = gr.Checkbox(
                    label="Send Email",
                    value=False,
                    info="Enable to send results via email"
                )
        
        run_button = gr.Button("🚀 Start Research", variant="primary", size="lg")
        
        output_display = gr.Textbox(
            label="Research Progress & Results",
            lines=20,
            max_lines=30,
            show_copy_button=True
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
        
        # Add examples
        gr.Examples(
            examples=[
                ["Latest AI Agent frameworks in 2025"],
                ["Best practices for machine learning deployment"],
                ["Quantum computing applications in finance"],
                ["Sustainable energy technologies 2024"],
                ["Cybersecurity trends and threats"]
            ],
            inputs=query_input
        )
        
        gr.Markdown("""
        ### 📝 Features:
        - **Automated web search** with intelligent query planning
        - **Parallel search execution** for faster results  
        - **Professional report generation** with structured outputs
        - **HTML email formatting** with CSS styling
        - **Trace monitoring** via OpenAI platform
        - **File output** - HTML reports saved to `output/` directory
        
        ### ⚙️ Configuration:
        - Set up your `.env` file with API keys (see `env_example.txt`)
        - Configure email settings in environment variables
        - Monitor costs - WebSearchTool costs ~$0.025 per search
        """)
    
    print("🚀 Launching Gradio interface...")
    print("💡 Access the web interface in your browser")
    interface.launch(inbrowser=True, share=False)

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Deep Research System - Automated web research with AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                                    # Launch web interface
    python main.py --cli "AI frameworks 2025"         # CLI research
    python main.py --preview "quantum computing"      # Preview mode
    python main.py --email "latest ML trends"         # With email sending
        """
    )
    
    parser.add_argument(
        '--cli', 
        type=str, 
        help='Run research query via command line'
    )
    parser.add_argument(
        '--preview', 
        type=str, 
        help='Run research in preview mode (no email sending)'
    )
    parser.add_argument(
        '--email', 
        type=str, 
        help='Run research with email sending enabled'
    )
    parser.add_argument(
        '--no-save', 
        action='store_true',
        help='Disable saving HTML files'
    )
    
    args = parser.parse_args()
    
    # Load environment
    load_environment()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run based on arguments
    if args.cli:
        await cli_research(args.cli, send_email=False)
    elif args.preview:
        await cli_research(args.preview, send_email=False, preview_only=True)
    elif args.email:
        await cli_research(args.email, send_email=True)
    else:
        # Default: launch Gradio interface
        launch_gradio()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1) 