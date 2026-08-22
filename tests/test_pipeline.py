import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import answer_question

def run_pipeline_tests():
    print("Testing the Complete RAG Pipeline...\n")
    
    # --- TEST 1: Valid Question ---
    question_1 = "How many days of paid time off do employees get?"
    print(f"TEST 1 (Valid Question)\nQ: {question_1}")
    
    result_1 = answer_question(question_1)
    
    print(f"\nAnswer: {result_1['answer']}")
    print(f"Sources Used: {len(result_1['sources'])}")
    for s in result_1['sources']:
        print(f"  - {s['source']} (Page {s['page']})")
        
    print("\n" + "="*50 + "\n")
    
    # --- TEST 2: Unrelated Question (Hallucination Check) ---
    question_2 = "What is the weather in Pune today?"
    print(f"TEST 2 (Unrelated Question)\nQ: {question_2}")
    
    result_2 = answer_question(question_2)
    
    print(f"\nAnswer: {result_2['answer']}")
    print(f"Sources Used: {len(result_2['sources'])}")
    
if __name__ == "__main__":
    # Temporarily hide INFO logs just to make the test output clean
    import logging
    logging.getLogger("src.retriever").setLevel(logging.WARNING)
    logging.getLogger("src.rag_pipeline").setLevel(logging.WARNING)
    
    run_pipeline_tests()
