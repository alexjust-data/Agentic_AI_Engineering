import os
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

# 1. Carga .env (¡pon tu ruta real si hace falta!)
load_dotenv("/Users/alex/Desktop/00_projects/AI_agents/my_agents/.env", override=True)

# 2. Inicializa tus herramientas aquí (Playwright, push, etc)
# ... (IMPORTS y configuración de tus tools)
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain.agents import Tool
import requests

pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"

def push(text: str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})

tool_push = Tool(
    name="send_push_notification",
    func=push,
    description="useful for when you want to send a push notification"
)

# --- Playwright tools ---
async_browser = create_async_playwright_browser(headless=True)
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = toolkit.get_tools()
all_tools = tools + [tool_push]

# 3. Inicializa LLM con tools
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(all_tools)

# 4. Define el State para LangGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 5. Construye el grafo
graph_builder = StateGraph(State)

def chatbot(state: State):
    # Importante: produce un objeto State actualizado
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=all_tools))
graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "10"}}

# 6. Función de chat asíncrona para Gradio
async def chat(user_input: str, history):
    # Adaptar el formato de entrada para LangGraph
    result = await graph.ainvoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
    messages = result["messages"]
    # Extrae la última respuesta del asistente
    last = ""
    for msg in reversed(messages):
        if hasattr(msg, "content"):
            last = msg.content
            break
        elif isinstance(msg, dict) and msg.get("role") == "assistant":
            last = msg.get("content", "")
            break
    return last

# 7. Interfaz de Gradio
iface = gr.ChatInterface(chat, type="messages")

if __name__ == "__main__":
    iface.launch()



