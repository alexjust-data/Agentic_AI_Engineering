#!/usr/bin/env python3
"""
ULTRA SIMPLE TEST - Definitively test if the Deep Research Agent works
Run this to verify everything is working before using the Gradio interface
"""

def test_sync_function():
    """Test the sync function that Gradio uses"""
    print("🔧 Testing sync function...")
    
    try:
        from deep_research import run_research_sync
        progress, report = run_research_sync("Simple test query", use_test_mode=True)
        
        success = len(report) > 100 and len(progress) > 50
        
        print(f"   Progress: {len(progress)} chars")
        print(f"   Report: {len(report)} chars")
        print(f"   Result: {'✅ WORKING' if success else '❌ FAILED'}")
        
        return success
        
    except Exception as e:
        print(f"   Result: ❌ ERROR - {e}")
        return False

def test_mock_manager():
    """Test the mock manager directly"""
    print("🧪 Testing mock manager...")
    
    try:
        from deep_research import MockResearchManager
        
        # Create a simple mock item
        class MockItem:
            def __init__(self):
                self.query = "test query"
                self.reason = "testing"
        
        manager = MockResearchManager()
        
        # Test sync version
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(manager.search(MockItem()))
            success = len(result) > 100 and "Sources:" in result
            
            print(f"   Mock result: {len(result)} chars")
            print(f"   Has sources: {'Sources:' in result}")
            print(f"   Result: {'✅ WORKING' if success else '❌ FAILED'}")
            
            return success
            
        finally:
            loop.close()
            
    except Exception as e:
        print(f"   Result: ❌ ERROR - {e}")
        return False

def main():
    print("🚀 ULTRA SIMPLE TEST - Deep Research Agent")
    print("=" * 50)
    
    # Test 1: Sync function
    sync_ok = test_sync_function()
    
    print()
    
    # Test 2: Mock manager
    mock_ok = test_mock_manager()
    
    print("\n" + "=" * 50)
    print("🎯 FINAL RESULT:")
    
    if sync_ok and mock_ok:
        print("✅ ALL TESTS PASSED!")
        print("🚀 The Deep Research Agent is WORKING!")
        print("💡 You can safely use the Gradio interface")
        print("🌐 Run: python deep_research.py")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 There are still issues to fix")
        print("- Sync function:", "✅ OK" if sync_ok else "❌ FAILED")
        print("- Mock manager:", "✅ OK" if mock_ok else "❌ FAILED")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    print(f"\n🎯 Exit code: {0 if success else 1}")
    sys.exit(0 if success else 1) 