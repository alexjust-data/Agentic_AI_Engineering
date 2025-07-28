import os
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain.agents import Tool
import requests
import asyncio

# --- 1. Load .env (edit path if needed) ---
load_dotenv("/Users/alex/Desktop/00_projects/AI_agents/my_agents/.env", override=True)

# --- 2. Define your tools (push notification, etc) ---

pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"

def push(text: str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data={"token": pushover_token, "user": pushover_user, "message": text})

tool_push = Tool(
    name="send_push_notification",
    func=push,
    description="useful for when you want to send a push notification"
)

# --- 3. Safe lazy tool initialization for Playwright ---
# Only initializes once and only inside async context (prevents event loop problems!)

import functools

@functools.cache
def get_browser_tools():
    async_browser = create_async_playwright_browser(headless=True)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    return toolkit.get_tools()

def get_all_tools():
    # All tools, including the push notification
    return get_browser_tools() + [tool_push]

# --- 4. LLM and State setup ---
llm = ChatOpenAI(model="gpt-4o-mini")

class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- 5. Build the graph ---
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

graph_builder = StateGraph(State)

def chatbot(state: State):
    # Always bind fresh tools to avoid async issues!
    tools = get_all_tools()
    llm_with_tools = llm.bind_tools(tools)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=get_all_tools()))
graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "10"}}

# --- 6. Gradio chat function ---
async def chat(user_input: str, history):
    result = await graph.ainvoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
    messages = result["messages"]
    # Find last message from the assistant
    last = ""
    for msg in reversed(messages):
        # If using LCEL/AIMessage, use .content; if dict, use ["content"]
        if hasattr(msg, "content"):
            last = msg.content
            break
        elif isinstance(msg, dict) and msg.get("role") == "assistant":
            last = msg.get("content", "")
            break
    return last

# --- 7. Gradio Interface ---
iface = gr.ChatInterface(chat, type="messages")

if __name__ == "__main__":
    # You can pick a custom port if you want!
    iface.launch(server_port=7860)

