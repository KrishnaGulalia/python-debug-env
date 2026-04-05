"""
Grader for MEDIUM tasks.
Scores a fixed code submission for any medium task.
Returns score in [0.0, 1.0].

Usage:
    python graders/grader_medium.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.environment  import PythonDebugEnv
from env.models       import DebugAction
from env.tasks.medium import MEDIUM_TASKS, MEDIUM_TASK_BY_ID


def grade_medium(task_id: str, fixed_code: str) -> dict:
    """
    Grade a code submission for a medium task.

    Args:
        task_id:    One of the medium task IDs (see MEDIUM_TASK_BY_ID).
        fixed_code: The agent's Python code as a string.

    Returns:
        {task_id, difficulty, score, tests_passed, total_tests, feedback}
    """
    assert task_id in MEDIUM_TASK_BY_ID, (
        f"Unknown medium task '{task_id}'. Available: {list(MEDIUM_TASK_BY_ID)}"
    )

    env = PythonDebugEnv()
    env.reset(task_id=task_id)
    result = env.step(DebugAction(fixed_code=fixed_code))

    return {
        "task_id":      task_id,
        "difficulty":   "medium",
        "score":        result.reward,
        "tests_passed": result.info["tests_passed"],
        "total_tests":  result.info["total_tests"],
        "feedback":     result.observation.feedback,
    }


if __name__ == "__main__":
    print("=== Medium Grader Self-Test ===\n")
    for task in MEDIUM_TASKS:
        result = grade_medium(task["id"], task["solution"])
        status = "✓ PASS" if result["score"] == 1.0 else "✗ FAIL"
        print(f"{status}  {task['id']}  score={result['score']}")
        assert result["score"] == 1.0, f"Solution failed: {result['feedback']}"

        result_buggy = grade_medium(task["id"], task["buggy_code"])
        status = "✓ PASS" if result_buggy["score"] < 1.0 else "✗ FAIL"
        print(f"{status}  {task['id']} (buggy)  score={result_buggy['score']}")

    print("\nAll medium grader tests passed!")