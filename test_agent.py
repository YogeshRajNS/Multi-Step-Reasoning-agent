"""
Test suite for the Multi-Step Reasoning Agent
Tests include easy and tricky questions to validate the agent's capabilities.
"""

import json
import os
from reasoning_agent import ReasoningAgent


# Test cases categorized by difficulty
EASY_TESTS = [
    {
        "question": "If a train leaves at 14:30 and arrives at 18:05, how long is the journey?",
        "expected_answer_contains": ["3 hours 35 minutes", "3:35", "215 minutes"],
        "description": "Basic time difference calculation"
    },
    {
        "question": "Alice has 3 red apples and twice as many green apples as red. How many apples does she have in total?",
        "expected_answer_contains": ["9", "nine"],
        "description": "Simple arithmetic with multiplication"
    },
    {
        "question": "What is 25 + 37?",
        "expected_answer_contains": ["62"],
        "description": "Basic addition"
    },
    {
        "question": "If a book costs $15 and I have $50, how many books can I buy?",
        "expected_answer_contains": ["3"],
        "description": "Division with remainders"
    },
    {
        "question": "A rectangle has length 8 and width 5. What is its perimeter?",
        "expected_answer_contains": ["26"],
        "description": "Geometry - perimeter calculation"
    },
    {
        "question": "What is 20% of 80?",
        "expected_answer_contains": ["16"],
        "description": "Percentage calculation"
    },
    {
        "question": "If I start with 100 dollars and spend 35 dollars, how much do I have left?",
        "expected_answer_contains": ["65"],
        "description": "Basic subtraction"
    },
    {
        "question": "A meeting starts at 10:00 and lasts 45 minutes. When does it end?",
        "expected_answer_contains": ["10:45"],
        "description": "Time addition"
    },
]

TRICKY_TESTS = [
    {
        "question": "A meeting needs 60 minutes. There are free slots: 09:00–09:30, 09:45–10:30, 11:00–12:00. Which slots can fit the meeting?",
        "expected_answer_contains": ["09:45–10:30", "11:00–12:00", "09:45", "11:00"],
        "description": "Multi-constraint time slot matching"
    },
    {
        "question": "Bob is twice as old as Alice. In 5 years, Bob will be 25. How old is Alice now?",
        "expected_answer_contains": ["10"],
        "description": "Multi-step age problem requiring working backwards"
    },
    {
        "question": "A basket has apples and oranges. There are 12 fruits total. If there are 3 more apples than oranges, how many oranges are there?",
        "expected_answer_contains": ["4.5", "cannot", "impossible"],
        "description": "Problem with non-integer solution (edge case)"
    },
    {
        "question": "Train A leaves at 14:00 traveling at 60 km/h. Train B leaves at 14:30 from the same station in the same direction at 80 km/h. How long until Train B catches up?",
        "expected_answer_contains": ["1.5 hours", "90 minutes", "1 hour 30"],
        "description": "Relative motion problem"
    },
    {
        "question": "A store offers 20% off, then an additional 10% off the reduced price. What is the total discount on a $100 item?",
        "expected_answer_contains": ["28", "$28"],
        "description": "Compound percentage (not additive)"
    },
]


def check_answer(answer: str, expected_contains: list) -> bool:
    """
    Check if the answer contains any of the expected substrings.
    
    Args:
        answer: The actual answer from the agent
        expected_contains: List of acceptable answer substrings
        
    Returns:
        True if answer contains any expected substring
    """
    answer_lower = answer.lower()
    return any(expected.lower() in answer_lower for expected in expected_contains)


def run_test(agent: ReasoningAgent, test: dict, test_num: int, category: str) -> dict:
    """
    Run a single test case and return results.
    
    Args:
        agent: The reasoning agent instance
        test: Test case dictionary
        test_num: Test number for display
        category: "EASY" or "TRICKY"
        
    Returns:
        Dictionary with test results
    """
    print(f"\n{'='*70}")
    print(f"Test #{test_num} [{category}]: {test['description']}")
    print(f"{'='*70}")
    print(f"Question: {test['question']}")
    
    try:
        result = agent.solve(test['question'])
        
        print(f"\nAnswer: {result.answer}")
        print(f"Status: {result.status}")
        print(f"Reasoning: {result.reasoning_visible_to_user}")
        print(f"\nMetadata:")
        print(f"  - Retries: {result.metadata['retries']}")
        print(f"  - Checks performed: {len(result.metadata['checks'])}")
        
        # Show check results
        print(f"  - Check results:")
        for check in result.metadata['checks']:
            status = "✓" if check['passed'] else "✗"
            print(f"    {status} {check['check_name']}: {check['details'][:100]}")
        
        # Verify answer
        answer_correct = check_answer(result.answer, test['expected_answer_contains'])
        print(f"\n{'✓' if answer_correct else '✗'} Expected answer validation: "
              f"{'PASS' if answer_correct else 'FAIL'}")
        
        if not answer_correct:
            print(f"  Expected one of: {test['expected_answer_contains']}")
        
        return {
            "test_num": test_num,
            "category": category,
            "description": test['description'],
            "question": test['question'],
            "answer": result.answer,
            "status": result.status,
            "answer_correct": answer_correct,
            "retries": result.metadata['retries'],
            "checks_passed": all(c['passed'] for c in result.metadata['checks']),
            "full_result": result.to_dict()
        }
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return {
            "test_num": test_num,
            "category": category,
            "description": test['description'],
            "question": test['question'],
            "error": str(e),
            "status": "error"
        }


def run_all_tests():
    """Run all test cases and generate a summary report"""
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        print("Please set it with: export GEMINI_API_KEY='your-key-here'")
        print("\nTo get a FREE API key:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Click 'Create API Key'")
        print("3. Copy the key and set it in your environment")
        return
    
    print("=" * 70)
    print("MULTI-STEP REASONING AGENT - TEST SUITE")
    print("=" * 70)
    
    agent = ReasoningAgent(max_retries=2)
    results = []
    
    # Run easy tests
    print(f"\n\n{'#'*70}")
    print("# EASY TESTS")
    print(f"{'#'*70}")
    
    for i, test in enumerate(EASY_TESTS, 1):
        result = run_test(agent, test, i, "EASY")
        results.append(result)
    
    # Run tricky tests
    print(f"\n\n{'#'*70}")
    print("# TRICKY TESTS")
    print(f"{'#'*70}")
    
    for i, test in enumerate(TRICKY_TESTS, len(EASY_TESTS) + 1):
        result = run_test(agent, test, i, "TRICKY")
        results.append(result)
    
    # Generate summary
    print(f"\n\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    
    total_tests = len(results)
    successful_status = sum(1 for r in results if r.get('status') == 'success')
    correct_answers = sum(1 for r in results if r.get('answer_correct', False))
    errors = sum(1 for r in results if r.get('status') == 'error')
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Successful Status: {successful_status}/{total_tests} "
          f"({successful_status/total_tests*100:.1f}%)")
    print(f"Correct Answers: {correct_answers}/{total_tests} "
          f"({correct_answers/total_tests*100:.1f}%)")
    print(f"Errors: {errors}/{total_tests}")
    
    # Category breakdown
    easy_results = [r for r in results if r.get('category') == 'EASY']
    tricky_results = [r for r in results if r.get('category') == 'TRICKY']
    
    easy_correct = sum(1 for r in easy_results if r.get('answer_correct', False))
    tricky_correct = sum(1 for r in tricky_results if r.get('answer_correct', False))
    
    print(f"\nEasy Tests: {easy_correct}/{len(easy_results)} correct")
    print(f"Tricky Tests: {tricky_correct}/{len(tricky_results)} correct")
    
    # Save results to JSON
    output_file = "test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")
    
    return results


def run_single_test(question: str):
    """
    Run a single custom test question.
    
    Args:
        question: The question to test
    """
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        print("Please set it with: export GEMINI_API_KEY='your-key-here'")
        return
    
    agent = ReasoningAgent()
    result = agent.solve(question)
    
    print("\n" + "="*70)
    print("RESULT")
    print("="*70)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run single test with provided question
        question = " ".join(sys.argv[1:])
        run_single_test(question)
    else:
        # Run full test suite
        run_all_tests()
