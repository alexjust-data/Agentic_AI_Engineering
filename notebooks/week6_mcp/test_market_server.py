import asyncio
from agents.mcp import MCPServerStdio

async def test_market_server():
    params = {"command": "python", "args": ["market_server.py"]}
    
    try:
        async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
            tools = await server.list_tools()
            print("Market server tools:", tools)
            return True
    except Exception as e:
        print(f"Error testing market server: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_market_server())
    print(f"Test {'succeeded' if success else 'failed'}") 