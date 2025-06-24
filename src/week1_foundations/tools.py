"""
Tool Functions for AI Agents
"""
from datetime import datetime
from typing import Dict, List, Any

def get_current_time() -> str:
    """Get the current system time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weather(city: str) -> str:
    """Get weather information for a city (mocked data)"""
    # Mocked function - replace with real API call if needed
    weather_data = {
        "Barcelona": "22°C, sunny",
        "New York": "17°C, cloudy", 
        "Tokyo": "25°C, raining",
        "London": "15°C, foggy",
        "Paris": "18°C, partly cloudy",
        "Sydney": "26°C, clear"
    }
    return weather_data.get(city, f"No weather data available for {city}.")

def get_available_tools() -> List[Dict[str, Any]]:
    """Get list of available tools for the AI agent"""
    return [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current system time",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function", 
            "function": {
                "name": "get_weather",
                "description": "Get weather information for a given city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]

def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Execute a tool function with given arguments"""
    if tool_name == "get_current_time":
        return get_current_time()
    elif tool_name == "get_weather":
        city = arguments.get("city", "")
        if not city:
            return "Error: City parameter is required for weather information"
        return get_weather(city)
    else:
        return f"Error: Unknown tool '{tool_name}'"
