import asyncio
import os
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv(override=True)

async def debug_connection():
    """Debug the exact connection flow that's failing"""
    
    # Test 1: Individual server connections
    print("=== TEST 1: Individual server connections ===")
    
    # Accounts server
    try:
        print("Testing accounts server...")
        async with MCPServerStdio({"command": "python", "args": ["accounts_server.py"]}, client_session_timeout_seconds=30) as server:
            tools = await server.list_tools()
            print(f"✅ Accounts server: {len(tools)} tools")
    except Exception as e:
        print(f"❌ Accounts server failed: {type(e).__name__}: {e}")
    
    # Market server
    try:
        print("Testing market server...")
        async with MCPServerStdio({"command": "python", "args": ["market_server.py"]}, client_session_timeout_seconds=30) as server:
            tools = await server.list_tools()
            print(f"✅ Market server: {len(tools)} tools")
    except Exception as e:
        print(f"❌ Market server failed: {type(e).__name__}: {e}")
    
    # Push server
    try:
        print("Testing push server...")
        async with MCPServerStdio({"command": "python", "args": ["push_server.py"]}, client_session_timeout_seconds=30) as server:
            tools = await server.list_tools()
            print(f"✅ Push server: {len(tools)} tools")
    except Exception as e:
        print(f"❌ Push server failed: {type(e).__name__}: {e}")
    
    # Test 2: Multiple servers in sequence (like your notebook)
    print("\n=== TEST 2: Multiple servers in sequence ===")
    
    server_params = [
        {"command": "python", "args": ["accounts_server.py"]},
        {"command": "python", "args": ["market_server.py"]},
        {"command": "python", "args": ["push_server.py"]},
    ]
    
    servers = []
    try:
        for i, params in enumerate(server_params):
            print(f"Creating server {i+1}...")
            server = MCPServerStdio(params, client_session_timeout_seconds=30)
            servers.append(server)
        
        print("Connecting to all servers...")
        for i, server in enumerate(servers):
            print(f"Connecting to server {i+1}...")
            await server.connect()
            print(f"✅ Server {i+1} connected")
            
    except Exception as e:
        print(f"❌ Failed at server {i+1}: {type(e).__name__}: {e}")
    finally:
        # Clean up
        for server in servers:
            try:
                await server.aclose()
            except:
                pass

if __name__ == "__main__":
    asyncio.run(debug_connection()) 