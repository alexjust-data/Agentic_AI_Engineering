"""
Basic AI Agent Implementation with Tool Support
"""
from typing import Dict, Any, List, Optional
from week1_foundations.models import model_manager
from week1_foundations.tools import get_available_tools, execute_tool
import json

def run_agent(user_input: str, model_name: str = "gpt-4o-mini", 
              max_iterations: int = 3) -> str:
    """Run AI agent with optional tool usage.
    
    Args:
        user_input: User's question or request
        model_name: Model to use for generation
        max_iterations: Maximum number of tool calling iterations
        
    Returns:
        Final response string
    """
    
    if model_name not in model_manager.get_available_models():
        return f"Error: Model {model_name} not available"
    
    # System prompt with tool instructions
    system_prompt = """You are a helpful AI assistant with access to tools.
When you need to use a tool, call it appropriately.
Always provide helpful, accurate responses."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    tools = get_available_tools()
    iteration_count = 0
    
    try:
        while iteration_count < max_iterations:
            # Get response from model
            response = model_manager.generate_response(
                model_name, messages, tools=tools
            )
            
            if 'error' in response:
                return f"Model error: {response['error']}"
            
            # Check if model wants to use tools
            if response['tool_calls']:
                # Execute tool calls
                for tool_call in response['tool_calls']:
                    try:
                        tool_args = json.loads(tool_call.function.arguments)
                        tool_result = execute_tool(
                            tool_call.function.name, 
                            tool_args
                        )
                    except json.JSONDecodeError as e:
                        return f"Failed to parse tool arguments: {e}"
                    
                    # Add tool call and result to conversation
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call]
                    })
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_result),
                        "tool_call_id": tool_call.id
                    })
                
                # Get follow-up response after tool usage
                follow_up = model_manager.generate_response(
                    model_name, messages
                )
                
                if 'error' in follow_up:
                    return f"Follow-up error: {follow_up['error']}"
                
                if follow_up['content']:
                    return follow_up['content']
                
                iteration_count += 1
            else:
                # No tools needed, return response
                return response['content'] or "No response generated"
        
        return "Maximum iterations reached"
        
    except Exception as e:
        return f"Agent error: {str(e)}"

def run_agent_with_multiple_models(user_input: str, 
                                  model_names: List[str] = None) -> Dict[str, Dict[str, Any]]:
    """Run the same query across multiple models for comparison.
    
    Args:
        user_input: User's question or request
        model_names: List of models to test (default: all available)
        
    Returns:
        Dict mapping model names to their responses and metadata
    """
    if model_names is None:
        model_names = model_manager.get_available_models()
    
    results = {}
    
    for model_name in model_names:
        print(f"Testing with {model_name}...")
        
        try:
            response = run_agent(user_input, model_name)
            model_info = model_manager.get_model_info(model_name)
            
            results[model_name] = {
                'response': response,
                'model_display': model_info.name if model_info else model_name,
                'provider': model_info.provider if model_info else 'unknown',
                'success': True
            }
        except Exception as e:
            results[model_name] = {
                'response': f"Error: {str(e)}",
                'model_display': model_name,
                'provider': 'unknown',
                'success': False
            }
    
    return results

