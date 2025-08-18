import asyncio
from accounts_client import read_accounts_resource, read_strategy_resource

async def test_accounts_server():
    try:
        print("Testing accounts server...")
        
        # Test reading account resource
        print("Reading Ed's account...")
        ed_account = await read_accounts_resource("Ed")
        print("✅ Ed's account loaded successfully")
        print(f"Account info: {ed_account[:200]}...")
        
        # Test reading strategy resource
        print("\nReading Ed's strategy...")
        ed_strategy = await read_strategy_resource("Ed")
        print("✅ Ed's strategy loaded successfully")
        print(f"Strategy: {ed_strategy[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing accounts server: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_accounts_server())
    print(f"\nTest {'succeeded' if success else 'failed'}") 