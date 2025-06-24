"""
AI Models Manager - Unified interface for multiple AI providers
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class ModelConfig:
    """Configuration for AI models"""
    def __init__(self, name: str, provider: str, model_id: str, max_tokens: int = 1000, 
                 temperature: float = 0.7, available: bool = True):
        self.name = name
        self.provider = provider
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.available = available

class ModelManager:
    """Manages multiple AI model providers"""
    
    def __init__(self):
        self.clients = {}
        self.models = {}
        self._initialize_clients()
        self._initialize_models()
    
    def _initialize_clients(self):
        """Initialize API clients for different providers"""
        
        # OpenAI Client
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            self.clients['openai'] = OpenAI(api_key=openai_key)
            print("OpenAI client initialized")
        else:
            print("OpenAI API key not found")
        
        # Anthropic Client (prepared for future)
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            try:
                from anthropic import Anthropic
                self.clients['anthropic'] = Anthropic(api_key=anthropic_key)
                print("Anthropic client initialized")
            except ImportError:
                print("Anthropic library not installed")
        else:
            print("Anthropic API key not found")
        
        # Google Gemini Client (prepared for future)
        google_key = os.getenv('GOOGLE_API_KEY')
        if google_key:
            try:
                self.clients['google'] = OpenAI(
                    api_key=google_key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
                print("Google Gemini client initialized")
            except Exception as e:
                print(f"Google Gemini client failed: {e}")
        else:
            print("Google API key not found")
        
        # DeepSeek Client (prepared for future)
        deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        if deepseek_key:
            try:
                self.clients['deepseek'] = OpenAI(
                    api_key=deepseek_key,
                    base_url="https://api.deepseek.com/v1"
                )
                print("DeepSeek client initialized")
            except Exception as e:
                print(f"DeepSeek client failed: {e}")
        else:
            print("DeepSeek API key not found")
    
    def _initialize_models(self):
        """Initialize available models configuration"""
        
        # OpenAI Models
        if 'openai' in self.clients:
            self.models.update({
                'gpt-4o-mini': ModelConfig('GPT-4O Mini', 'openai', 'gpt-4o-mini', 4000, 0.7, True),
                'gpt-4o': ModelConfig('GPT-4O', 'openai', 'gpt-4o', 4000, 0.7, True),
                'gpt-4-turbo': ModelConfig('GPT-4 Turbo', 'openai', 'gpt-4-turbo', 4000, 0.7, True),
            })
        
        # Anthropic Models (prepared for future)
        if 'anthropic' in self.clients:
            self.models.update({
                'claude-3-sonnet': ModelConfig('Claude 3 Sonnet', 'anthropic', 'claude-3-sonnet-20240229', 4000, 0.7, True),
                'claude-3-haiku': ModelConfig('Claude 3 Haiku', 'anthropic', 'claude-3-haiku-20240307', 4000, 0.7, True),
            })
        
        # Google Models (prepared for future)
        if 'google' in self.clients:
            self.models.update({
                'gemini-2.0-flash': ModelConfig('Gemini 2.0 Flash', 'google', 'gemini-2.0-flash', 4000, 0.7, True),
            })
        
        # DeepSeek Models (prepared for future)
        if 'deepseek' in self.clients:
            self.models.update({
                'deepseek-chat': ModelConfig('DeepSeek Chat', 'deepseek', 'deepseek-chat', 4000, 0.7, True),
            })
    
    def get_available_models(self) -> List[str]:
        """Get list of available model names"""
        return [name for name, config in self.models.items() if config.available]
    
    def get_model_info(self, model_name: str) -> Optional[ModelConfig]:
        """Get configuration for a specific model"""
        return self.models.get(model_name)
    
    def generate_response(self, model_name: str, messages: List[Dict[str, str]], 
                         tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Generate response using specified model"""
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not available")
        
        config = self.models[model_name]
        client = self.clients[config.provider]
        
        try:
            # Handle different providers
            if config.provider == 'openai' or config.provider in ['google', 'deepseek']:
                params = {
                    'model': config.model_id,
                    'messages': messages,
                    'max_tokens': config.max_tokens,
                    'temperature': config.temperature
                }
                
                if tools:
                    params['tools'] = tools
                    params['tool_choice'] = 'auto'
                
                response = client.chat.completions.create(**params)
                
                return {
                    'model': model_name,
                    'provider': config.provider,
                    'content': response.choices[0].message.content,
                    'finish_reason': response.choices[0].finish_reason,
                    'tool_calls': response.choices[0].message.tool_calls,
                    'message': response.choices[0].message
                }
            
            elif config.provider == 'anthropic':
                # Anthropic has different API structure
                response = client.messages.create(
                    model=config.model_id,
                    messages=messages,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature
                )
                
                return {
                    'model': model_name,
                    'provider': config.provider,
                    'content': response.content[0].text,
                    'finish_reason': 'stop',
                    'tool_calls': None,
                    'message': response
                }
            
        except Exception as e:
            return {
                'model': model_name,
                'provider': config.provider,
                'error': str(e),
                'content': f"Error with {model_name}: {str(e)}"
            }
    
    def compare_models(self, prompt: str, model_names: List[str] = None) -> List[Dict[str, Any]]:
        """Compare responses from multiple models"""
        
        if model_names is None:
            model_names = self.get_available_models()
        
        messages = [{"role": "user", "content": prompt}]
        results = []
        
        for model_name in model_names:
            if model_name in self.models:
                print(f"Testing with {model_name}...")
                result = self.generate_response(model_name, messages)
                result['model_display'] = self.models[model_name].name
                results.append(result)
        
        return results

# Global instance
model_manager = ModelManager() 