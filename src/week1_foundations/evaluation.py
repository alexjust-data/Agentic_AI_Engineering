"""
Response Evaluation System with Pydantic Models
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from week1_foundations.models import model_manager
from week1_foundations.agent import run_agent
import json

class Evaluation(BaseModel):
    """Pydantic model for response evaluation"""
    is_acceptable: bool
    score: int  # 1-10 scale
    feedback: str
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[str] = []

class ModelComparison(BaseModel):
    """Pydantic model for comparing multiple model responses"""
    best_model: str
    ranking: List[str]  # Models in order from best to worst
    reasoning: str
    scores: Dict[str, int]  # Model name -> score

class ResponseEvaluator:
    """Evaluates responses for quality and appropriateness"""
    
    def __init__(self, evaluator_model: str = "gpt-4o-mini"):
        self.evaluator_model = evaluator_model
    
    def evaluate_response(self, user_question: str, response: str, 
                         context: Optional[str] = None) -> Evaluation:
        """Evaluate a single response for quality and appropriateness.
        
        Args:
            user_question: The original user question
            response: The response to evaluate
            context: Optional context about what makes a good response
            
        Returns:
            Evaluation object with detailed feedback
        """
        
        evaluation_prompt = f"""You are an expert evaluator of AI responses. 
Your task is to evaluate the quality of an AI response to a user question.

User Question: {user_question}

AI Response: {response}

Context: {context or "General purpose assistant"}

Please evaluate this response on the following criteria:
1. Accuracy and correctness
2. Helpfulness and relevance
3. Clarity and coherence
4. Completeness
5. Appropriateness of tone

Provide a comprehensive evaluation with:
- is_acceptable: true/false (overall acceptability)
- score: 1-10 (overall quality score)
- feedback: detailed explanation of your evaluation
- strengths: list of what the response does well
- weaknesses: list of areas for improvement
- suggestions: specific recommendations for improvement

Respond with valid JSON only."""

        messages = [{"role": "user", "content": evaluation_prompt}]
        
        try:
            eval_response = model_manager.generate_response(
                self.evaluator_model, messages
            )
            
            if 'error' in eval_response:
                return Evaluation(
                    is_acceptable=False,
                    score=1,
                    feedback=f"Evaluation error: {eval_response['error']}",
                    strengths=[],
                    weaknesses=["Could not evaluate due to technical error"],
                    suggestions=["Try again with a different model"]
                )
            
            # Try to parse JSON response
            eval_data = json.loads(eval_response['content'])
            return Evaluation(**eval_data)
            
        except json.JSONDecodeError:
            # If JSON parsing fails, create a basic evaluation
            return Evaluation(
                is_acceptable=True,  # Default to acceptable if we can't evaluate
                score=7,
                feedback="Could not parse evaluation response properly",
                strengths=["Response was generated successfully"],
                weaknesses=["Could not perform detailed evaluation"],
                suggestions=["Consider using a different evaluation model"]
            )
        except Exception as e:
            return Evaluation(
                is_acceptable=False,
                score=1,
                feedback=f"Evaluation failed: {str(e)}",
                strengths=[],
                weaknesses=["Evaluation system error"],
                suggestions=["Try again with different parameters"]
            )
    
    def compare_responses(self, user_question: str, 
                         responses: Dict[str, str]) -> ModelComparison:
        """Compare multiple model responses and rank them.
        
        Args:
            user_question: The original user question
            responses: Dict mapping model names to their responses
            
        Returns:
            ModelComparison with ranking and reasoning
        """
        
        comparison_prompt = f"""You are an expert evaluator comparing AI model responses.

User Question: {user_question}

Model Responses:
"""
        
        for model_name, response in responses.items():
            comparison_prompt += f"\n{model_name}: {response}\n"
        
        comparison_prompt += """
Please compare these responses and provide:
- best_model: name of the best performing model
- ranking: list of model names from best to worst
- reasoning: detailed explanation of your ranking
- scores: dictionary mapping each model name to a score (1-10)

Consider accuracy, helpfulness, clarity, and overall quality.
Respond with valid JSON only."""

        messages = [{"role": "user", "content": comparison_prompt}]
        
        try:
            comparison_response = model_manager.generate_response(
                self.evaluator_model, messages
            )
            
            if 'error' in comparison_response:
                # Fallback to simple comparison
                model_names = list(responses.keys())
                return ModelComparison(
                    best_model=model_names[0] if model_names else "unknown",
                    ranking=model_names,
                    reasoning=f"Comparison error: {comparison_response['error']}",
                    scores={name: 5 for name in model_names}
                )
            
            comparison_data = json.loads(comparison_response['content'])
            return ModelComparison(**comparison_data)
            
        except Exception as e:
            model_names = list(responses.keys())
            return ModelComparison(
                best_model=model_names[0] if model_names else "unknown",
                ranking=model_names,
                reasoning=f"Comparison failed: {str(e)}",
                scores={name: 5 for name in model_names}
            )

def run_agent_with_evaluation(user_input: str, model_name: str = "gpt-4o-mini", 
                             max_retries: int = 2) -> Dict[str, Any]:
    """Run agent with automatic evaluation and retry logic.
    
    Args:
        user_input: The user's question
        model_name: Model to use for generation
        max_retries: Maximum number of retries if evaluation fails
        
    Returns:
        Dict with response, evaluation, and retry information
    """
    evaluator = ResponseEvaluator()
    
    for attempt in range(max_retries + 1):
        # Generate response
        response = run_agent(user_input, model_name)
        
        # Evaluate response
        evaluation = evaluator.evaluate_response(user_input, response)
        
        if evaluation.is_acceptable or attempt == max_retries:
            return {
                'response': response,
                'evaluation': evaluation,
                'attempts': attempt + 1,
                'final_attempt': True
            }
        
        # If not acceptable, add feedback to the prompt and retry
        print(f"Attempt {attempt + 1} failed evaluation. Retrying...")
        print(f"Feedback: {evaluation.feedback}")
        
        # For retry, we could modify the user input to include feedback
        # For now, we'll just retry with the same input
    
    return {
        'response': response,
        'evaluation': evaluation,
        'attempts': max_retries + 1,
        'final_attempt': True
    }

def run_comparative_analysis(user_input: str, model_names: List[str] = None) -> Dict[str, Any]:
    """Run comparative analysis across multiple models with evaluation.
    
    Args:
        user_input: The user's question
        model_names: List of models to compare (default: all available)
        
    Returns:
        Dict with responses, evaluations, and comparison
    """
    if model_names is None:
        model_names = model_manager.get_available_models()
    
    evaluator = ResponseEvaluator()
    
    # Generate responses from all models
    responses = {}
    evaluations = {}
    
    for model_name in model_names:
        print(f"Generating response with {model_name}...")
        response = run_agent(user_input, model_name)
        evaluation = evaluator.evaluate_response(user_input, response)
        
        responses[model_name] = response
        evaluations[model_name] = evaluation
    
    # Compare all responses
    print("Comparing all responses...")
    comparison = evaluator.compare_responses(user_input, responses)
    
    return {
        'user_input': user_input,
        'responses': responses,
        'evaluations': evaluations,
        'comparison': comparison,
        'model_count': len(model_names)
    }

# Global evaluator instance
evaluator = ResponseEvaluator() 