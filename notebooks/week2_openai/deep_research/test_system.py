#!/usr/bin/env python3
"""
Quick Test Script for Deep Research System

Use this script to test the system without setting up email configuration.
Only requires OPENAI_API_KEY.
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from research_manager import ResearchManager

def load_env():
    """Load environment variables"""
    load_dotenv(override=True)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in environment")
        print("Set it with: export OPENAI_API_KEY=your-key-here")
        return False
    
    print("✅ OpenAI API key found")
    return True

async def test_research(query: str = "Latest trends in artificial intelligence 2025"):
    """Test the research system with preview mode only"""
    
    print("🔬 TESTING DEEP RESEARCH SYSTEM")
    print("=" * 50)
    print(f"Query: {query}")
    print(f"Mode: Preview only (no email sending)")
    print("=" * 50)
    
    # Initialize with email disabled for testing
    manager = ResearchManager(
        send_email=False,  # Disable email for testing
        save_html=True,    # Save HTML to files
        output_dir="test_output"
    )
    
    try:
        async for update in manager.run(query):
            if isinstance(update, str):
                print(update)
            elif isinstance(update, dict):
                print("\n" + "=" * 50)
                print("🎉 TEST COMPLETED!")
                print(f"Status: {update.get('status')}")
                print(f"Searches: {update.get('searches_performed', 0)}")
                print(f"Duration: {update.get('duration_seconds', 0):.1f}s")
                
                if update.get('html_file'):
                    print(f"HTML saved: {update['html_file']}")
                
                # Show HTML preview
                html_content = manager.get_last_html()
                if html_content:
                    print(f"\n📧 EMAIL HTML PREVIEW (first 500 chars):")
                    print("-" * 30)
                    print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
                    print("-" * 30)
                
                print("=" * 50)
                return update
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

async def interactive_test():
    """Interactive test mode"""
    print("🔬 INTERACTIVE TEST MODE")
    print("Enter research queries to test the system")
    print("Type 'quit' to exit\n")
    
    while True:
        query = input("🔍 Research query (or 'quit'): ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not query:
            print("Please enter a query")
            continue
        
        print()
        await test_research(query)
        print("\n" + "="*50 + "\n")

def main():
    """Main test function"""
    if not load_env():
        sys.exit(1)
    
    import argparse
    parser = argparse.ArgumentParser(description="Test Deep Research System")
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('--query', '-q', type=str,
                       help='Single query to test')
    
    args = parser.parse_args()
    
    if args.interactive:
        asyncio.run(interactive_test())
    elif args.query:
        asyncio.run(test_research(args.query))
    else:
        # Default test
        print("Running default test...")
        result = asyncio.run(test_research())
        
        if result and result.get('status') == 'success':
            print("\n✅ System test PASSED!")
            print("🚀 You can now run the full system with:")
            print("   python main.py")
        else:
            print("\n❌ System test FAILED!")
            print("Check your OpenAI API key and network connection")

if __name__ == "__main__":
    main() 