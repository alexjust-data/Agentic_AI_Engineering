"""
Test script for the Deep Research Agent
This script tests the core functionality without the Gradio interface
"""

import asyncio
from research_manager import ResearchManager
from deep_research import MockResearchManager

async def test_mock_research():
    """Test the mock research functionality"""
    print("🧪 Testing Mock Research Manager...")
    print("=" * 50)
    
    manager = MockResearchManager()
    query = "Latest AI developments in 2025"
    
    print(f"🔍 Query: {query}")
    print("📊 Progress updates:")
    
    final_report = None
    progress_updates = []
    
    async for update in manager.run(query):
        if isinstance(update, str):
            print(f"  • {update}")
            
            # Check if this looks like a final report
            if (update.startswith("## Final Research Report") or 
                update.startswith("# ") or
                (len(update) > 500 and "##" in update)):
                final_report = update
                print("  ✅ FINAL REPORT DETECTED!")
                break
            else:
                progress_updates.append(update)
    
    print("=" * 50)
    print("🎯 TEST RESULTS:")
    print(f"  - Progress updates: {len(progress_updates)}")
    print(f"  - Final report detected: {'✅ YES' if final_report else '❌ NO'}")
    
    if final_report:
        print(f"  - Report length: {len(final_report)} characters")
        print(f"  - Report preview: {final_report[:200]}...")
    
    return final_report is not None

async def test_real_research():
    """Test the real research functionality (will cost money)"""
    print("💰 Testing Real Research Manager...")
    print("⚠️  WARNING: This will cost approximately 12.5¢ in OpenAI API calls")
    print("=" * 50)
    
    manager = ResearchManager()
    query = "Quick test of AI research capabilities"
    
    print(f"🔍 Query: {query}")
    print("📊 Progress updates:")
    
    final_report = None
    progress_updates = []
    
    try:
        async for update in manager.run(query):
            if isinstance(update, str):
                print(f"  • {update}")
                
                # Check if this looks like a final report
                if (update.startswith("## Final Research Report") or 
                    update.startswith("# ") or
                    (len(update) > 500 and "##" in update)):
                    final_report = update
                    print("  ✅ FINAL REPORT DETECTED!")
                    break
                else:
                    progress_updates.append(update)
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("=" * 50)
    print("🎯 TEST RESULTS:")
    print(f"  - Progress updates: {len(progress_updates)}")
    print(f"  - Final report detected: {'✅ YES' if final_report else '❌ NO'}")
    
    if final_report:
        print(f"  - Report length: {len(final_report)} characters")
        print(f"  - Report preview: {final_report[:200]}...")
    
    return final_report is not None

async def main():
    """Run all tests"""
    print("🚀 Starting Deep Research Agent Tests")
    print("=" * 60)
    
    # Test 1: Mock research (free)
    mock_success = await test_mock_research()
    
    print("\n")
    
    # Test 2: Ask user if they want to test real research (costs money)
    test_real = input("❓ Do you want to test REAL research? (costs ~12.5¢) [y/N]: ").lower().strip()
    
    if test_real in ['y', 'yes']:
        real_success = await test_real_research()
    else:
        print("⏭️  Skipping real research test")
        real_success = True
    
    print("\n" + "=" * 60)
    print("🎯 FINAL TEST RESULTS:")
    print(f"  - Mock Research: {'✅ PASSED' if mock_success else '❌ FAILED'}")
    print(f"  - Real Research: {'✅ PASSED' if real_success else '⏭️ SKIPPED'}")
    
    if mock_success:
        print("\n✅ The research agent is working correctly!")
        print("💡 You can now run the Gradio interface with confidence")
        print("🚀 Run: python deep_research.py")
    else:
        print("\n❌ There are issues with the research agent")
        print("🔧 Check the error messages above for debugging")

if __name__ == "__main__":
    asyncio.run(main()) 