import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.chains.rag_chain import get_rag_chain

def run_evaluation():
    test_file = "evaluation/test_questions.json"
    results_dir = "evaluation/results"
    os.makedirs(results_dir, exist_ok=True)
    
    if not os.path.exists(test_file):
        print(f"❌ Test questions file nahi mili: {test_file}")
        return

    with open(test_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    chain = get_rag_chain()
    evaluation_results = []
    
    print(f"🚀 Running Evaluation on {len(test_cases)} test cases...\n")
    
    for case in test_cases:
        test_id = case["id"]
        question = case["question"]
        category = case["category"]
        
        print(f"Testing [{test_id}] ({category}): {question}")
        
        try:
            # Invoke chain
            response = chain.invoke({"input": question, "chat_history": []})
            
            # Response handling (SupportResponse object ya string check)
            if hasattr(response, 'answer'):
                ans_text = response.answer
                is_answered = getattr(response, 'answered', True)
                sources_used = getattr(response, 'sources', [])
            elif isinstance(response, dict) and 'answer' in response:
                ans_obj = response['answer']
                ans_text = getattr(ans_obj, 'answer', str(ans_obj))
                is_answered = getattr(ans_obj, 'answered', True)
                sources_used = getattr(ans_obj, 'sources', [])
            else:
                ans_text = str(response)
                is_answered = "I cannot find" not in ans_text
                sources_used = []
            
            # Verdict logic
            verdict = "PASS"
            if category == "Unanswerable":
                if "cannot find" in ans_text.lower() or not is_answered:
                    verdict = "PASS (Correct Refusal)"
                else:
                    verdict = "FAIL (Should have refused)"
            else:
                if "cannot find" in ans_text.lower():
                    verdict = "FAIL (Unexpected refusal)"
                else:
                    verdict = "PASS"
                    
            evaluation_results.append({
                "id": test_id,
                "question": question,
                "category": category,
                "answer": ans_text,
                "sources": sources_used,
                "answered": is_answered,
                "verdict": verdict
            })
            print(f"   ➔ Verdict: {verdict}\n")
            
        except Exception as e:
            print(f"   ➔ Error: {e}\n")
            evaluation_results.append({
                "id": test_id,
                "question": question,
                "category": category,
                "error": str(e),
                "verdict": "ERROR"
            })

    # Save results artifact
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(results_dir, f"eval_report_{timestamp}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(evaluation_results, f, indent=4)
        
    print(f"✅ Evaluation complete! Report saved to: {output_file}")

if __name__ == "__main__":
    run_evaluation()