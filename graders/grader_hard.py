"""
Grader for HARD tasks.
Scores a fixed code submission for any hard task.
Returns score in [0.0, 1.0].

Usage:
    python graders/grader_hard.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.environment import PythonDebugEnv
from env.models      import DebugAction
from env.tasks.hard  import HARD_TASKS, HARD_TASK_BY_ID


def grade_hard(task_id: str, fixed_code: str) -> dict:
    """
    Grade a code submission for a hard task.

    Args:
        task_id:    One of the hard task IDs (see HARD_TASK_BY_ID).
        fixed_code: The agent's Python code as a string.

    Returns:
        {task_id, difficulty, score, tests_passed, total_tests, feedback}
    """
    assert task_id in HARD_TASK_BY_ID, (
        f"Unknown hard task '{task_id}'. Available: {list(HARD_TASK_BY_ID)}"
    )

    env = PythonDebugEnv()
    env.reset(task_id=task_id)
    result = env.step(DebugAction(fixed_code=fixed_code))

    return {
        "task_id":      task_id,
        "difficulty":   "hard",
        "score":        result.reward,
        "tests_passed": result.info["tests_passed"],
        "total_tests":  result.info["total_tests"],
        "feedback":     result.observation.feedback,
    }


if __name__ == "__main__":
    print("=== Hard Grader Self-Test ===\n")
    for task in HARD_TASKS:
        result = grade_hard(task["id"], task["solution"])
        status = "✓ PASS" if result["score"] == 1.0 else "✗ FAIL"
        print(f"{status}  {task['id']}  score={result['score']}")
        assert result["score"] == 1.0, f"Solution failed: {result['feedback']}"

        result_buggy = grade_hard(task["id"], task["buggy_code"])
        status = "✓ PASS" if result_buggy["score"] < 1.0 else "✗ FAIL"
        print(f"{status}  {task['id']} (buggy)  score={result_buggy['score']}")

    print("\nAll hard grader tests passed!")