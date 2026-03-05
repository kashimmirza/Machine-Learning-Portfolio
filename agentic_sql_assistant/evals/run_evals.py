import asyncio
import json
from app.api.v1.chatbot import agent
from app.schemas.chat import Message
from evals.judge import evaluate_response

# Sample Test Cases
# In a real app, load this from a dataset/JSON file
TEST_CASES = [
    {
        "question": "What are the top 5 products by revenue?",
        "ground_truth": "The top 5 products are A, B, C, D, E with revenues..."
    },
    {
        "question": "Who is the manager of the Sales department?",
        "ground_truth": "Alice Smith is the manager."
    }
]

async def run_evals():
    print("Starting LLM-as-a-Judge Evaluation...")
    results = []
    
    for case in TEST_CASES:
        q = case["question"]
        print(f"\nEvaluating: {q}")
        
        # 1. Get Agent Response
        # We use a dummy user/session for testing
        agent_response_msgs = await agent.get_response(
            [Message(role="user", content=q)], 
            session_id="eval-session", 
            user_id="eval-user"
        )
        response_text = agent_response_msgs[-1].content
        
        # 2. Judge validity
        eval_res = await evaluate_response(q, response_text, case["ground_truth"])
        
        print(f"  -> Score: {eval_res.score}/5")
        print(f"  -> Reasoning: {eval_res.reasoning}")
        
        results.append({
            "question": q,
            "response": response_text,
            "score": eval_res.score,
            "reasoning": eval_res.reasoning
        })
        
    # Save results
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nEvaluation Complete. Results saved to eval_results.json")

if __name__ == "__main__":
    # We need to initialize the DB first in a real scenario
    # For this script to work, the app env needs to be loaded
    asyncio.run(run_evals())
