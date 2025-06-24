"""
Command Line Interface for AI Agents System
"""
from week1_foundations.interface import launch_interface
from week1_foundations.agent import run_agent, run_agent_with_multiple_models
from week1_foundations.evaluation import run_agent_with_evaluation, run_comparative_analysis
from week1_foundations.models import model_manager
import sys

def console_demo():
    """Run a console demonstration of the system"""
    print("=== AI Agents System Console Demo ===")
    print()
    
    # Check for available models
    available_models = model_manager.get_available_models()
    if not available_models:
        print("No models available. Please check your API configuration.")
        return
    
    print(f"Available models: {available_models}")
    print()
    print("Testing basic functionality...")
    
    # Test basic agent
    test_question = "What is artificial intelligence?"
    print(f"\nQuestion: {test_question}")
    response = run_agent(test_question)
    print(f"Response: {response[:200]}...")
    
    # Test evaluation
    print("\nTesting with evaluation...")
    eval_result = run_agent_with_evaluation("What is 2+2?")
    print(f"Score: {eval_result['evaluation'].score}/10")
    
    print("\nTesting multi-model comparison...")
    comparison = run_comparative_analysis("Explain machine learning in one sentence")
    print(f"Best model: {comparison['comparison'].best_model}")
    
    print("\nConsole demo complete!")

def interactive_chat():
    """Run interactive chat mode"""
    print("=== Interactive AI Chat ===")
    print("Type 'quit' to exit, 'models' to see available models")
    
    available_models = model_manager.get_available_models()
    if not available_models:
        print("No models available. Please check your API configuration.")
        return
    
    current_model = available_models[0]
    print(f"Current model: {current_model}")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if user_input.lower() == 'models':
                print(f"Available models: {available_models}")
                continue
            
            if user_input.startswith('model '):
                new_model = user_input[6:].strip()
                if new_model in available_models:
                    current_model = new_model
                    print(f"Current model: {current_model}")
                    print(f"Switched to {current_model}")
                else:
                    print(f"Model '{new_model}' not available")
                continue
            
            if user_input.startswith('eval '):
                question = user_input[5:].strip()
                result = run_agent_with_evaluation(question, current_model)
                print(f"Response: {result['response']}")
                print(f"Score: {result['evaluation'].score}/10")
                continue
            
            if user_input.startswith('compare '):
                question = user_input[8:].strip()
                analysis = run_comparative_analysis(question)
                print(f"Best model: {analysis['comparison'].best_model}")
                print("All responses:")
                for model, response in analysis['responses'].items():
                    score = analysis['evaluations'][model].score
                    print(f"{model} ({score}/10): {response[:100]}...")
                continue
            
            if not user_input:
                continue
            
            response = run_agent(user_input, current_model)
            print(f"Agent: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode in ['web', 'interface', 'gradio']:
            print("Starting web interface...")
            launch_interface(share=False, port=7860)
        
        elif mode in ['chat', 'interactive']:
            interactive_chat()
        
        elif mode in ['demo', 'test']:
            console_demo()
        
        elif mode in ['help', '--help', '-h']:
            print("""
AI Agents System - Usage:

python app.py [mode]

Modes:
  web       - Launch web interface (default)
  chat      - Interactive chat mode
  demo      - Run console demonstration
  help      - Show this help

Examples:
  python app.py web
  python app.py chat
  python app.py demo
""")
        else:
            print("Invalid mode")
            print("Use 'python app.py help' for usage information")
    
    else:
        # Default to web interface
        print("Starting web interface...")
        launch_interface(share=False, port=7860)

if __name__ == "__main__":
    main()
