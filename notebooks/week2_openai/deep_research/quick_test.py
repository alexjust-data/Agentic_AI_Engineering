#!/usr/bin/env python3
"""
Quick test script for the Deep Research Agent
Run this before launching the Gradio interface to verify everything works
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from deep_research import run_research_sync, MockResearchManager

def test_sync_function():
    """Test the synchronous function that Gradio uses"""
    print("🧪 Testing synchronous function (used by Gradio)...")
    
    try:
        query = "Test query for AI research"
        progress, report = run_research_sync(query, use_test_mode=True)
        
        print(f"✅ Progress: {len(progress)} characters")
        print(f"✅ Report: {len(report)} characters")
        print(f"✅ Report has structure: {'##' in report}")
        
        if len(report) > 100:
            print("🎉 SUCCESS: Sync function works correctly!")
            return True
        else:
            print("❌ FAILED: Report too short")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

async def test_async_function():
    """Test the async function directly"""
    print("🧪 Testing async function (direct)...")
    
    try:
        manager = MockResearchManager()
        query = "Test query for AI research"
        
        results = []
        async for chunk in manager.run(query):
            results.append(chunk)
        
        print(f"✅ Generated {len(results)} chunks")
        
        # Check if we have a final report
        final_report = None
        for chunk in results:
            if isinstance(chunk, str) and len(chunk) > 500:
                final_report = chunk
                break
        
        if final_report:
            print("🎉 SUCCESS: Async function works correctly!")
            return True
        else:
            print("❌ FAILED: No final report found")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Deep Research Agent - Quick Test")
    print("=" * 50)
    
    # Test 1: Synchronous function (what Gradio uses)
    sync_ok = test_sync_function()
    
    print("\n" + "-" * 30)
    
    # Test 2: Async function (direct test)
    async_ok = asyncio.run(test_async_function())
    
    print("\n" + "=" * 50)
    print("🎯 FINAL RESULTS:")
    print(f"- Sync function: {'✅ PASS' if sync_ok else '❌ FAIL'}")
    print(f"- Async function: {'✅ PASS' if async_ok else '❌ FAIL'}")
    
    if sync_ok and async_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Ready to launch the Gradio interface!")
        print("💡 Run: python deep_research.py")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("🔧 Check the error messages above")
        
    return sync_ok and async_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 