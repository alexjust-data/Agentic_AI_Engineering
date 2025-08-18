import asyncio
import os
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

async def test_polygon_server():
    load_dotenv(override=True)
    polygon_api_key = os.getenv("POLYGON_API_KEY")
    
    if not polygon_api_key:
        print("POLYGON_API_KEY not set")
        return False
    
    params = {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/polygon-io/mcp_polygon@v0.1.0", "mcp_polygon"],
        "env": {"POLYGON_API_KEY": polygon_api_key}
    }
    
    try:
        print("Attempting to connect to Polygon.io MCP server...")
        print(f"Using API key: {polygon_api_key[:10]}...")
        
        async with MCPServerStdio(params=params, client_session_timeout_seconds=60) as server:
            print("Connected successfully! Listing tools...")
            tools = await server.list_tools()
            print(f"Found {len(tools)} tools:")
            for tool in tools[:5]:  # Show first 5 tools
                print(f"  - {tool.name}: {tool.description[:100]}...")
            if len(tools) > 5:
                print(f"  ... and {len(tools) - 5} more tools")
            return True
            
    except Exception as e:
        print(f"Error testing Polygon server: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_polygon_server())
    print(f"\nTest {'succeeded' if success else 'failed'}") 