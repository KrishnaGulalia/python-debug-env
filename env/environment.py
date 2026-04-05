"""
Core logic for the Python Debug Environment.
Handles state, stepping, resetting, and reward calculation.
"""

from typing import Optional
from env.models import DebugObservation, DebugAction, StepResult, ResetResult
from env.tasks  import ALL_TASKS, TASK_BY_ID

MAX_ATTEMPTS = 5   # episode ends after this many attempts or a perfect score


class PythonDebugEnv:
    def __init__(self):
        self._task    = None
        self._attempt = 0
        self._done    = False
        self._cumulative_reward = 0.0


    # Public OpenEnv API

    def reset(self, task_id: Optional[str] = None) -> ResetResult:
        """Start a fresh episode. Returns the initial observation."""
        if task_id and task_id in TASK_BY_ID:
            self._task = TASK_BY_ID[task_id]
        else:
            self._task = ALL_TASKS[0]   # default: first easy task

        self._attempt           = 0
        self._done              = False
        self._cumulative_reward = 0.0

        return ResetResult(
            observation=self._make_observation(feedback=None),
            done=False,
        )

    def step(self, action: DebugAction) -> StepResult:
        """Agent submits fixed code. Returns new observation, reward, done."""
        if self._done:
            raise RuntimeError("Episode is finished. Call reset() to start a new one.")

        self._attempt += 1
        reward, tests_passed, total_tests, feedback = self._grade(action.fixed_code)
        self._cumulative_reward += reward

        # Episode ends on perfect score OR max attempts reached
        self._done = (reward == 1.0) or (self._attempt >= MAX_ATTEMPTS)

        obs         = self._make_observation(feedback=feedback)
        obs.attempt = self._attempt

        return StepResult(
            observation=obs,
            reward=reward,
            done=self._done,
            info={
                "tests_passed":      tests_passed,
                "total_tests":       total_tests,
                "attempt":           self._attempt,
                "cumulative_reward": round(self._cumulative_reward, 4),
            },
        )

    def state(self) -> dict:
        """Return the full current state (for debugging / spec compliance)."""
        return {
            "task_id":           self._task["id"] if self._task else None,
            "difficulty":        self._task["difficulty"] if self._task else None,
            "attempt":           self._attempt,
            "done":              self._done,
            "cumulative_reward": round(self._cumulative_reward, 4),
            "max_attempts":      MAX_ATTEMPTS,
        }


    # Internal helpers


    def _make_observation(self, feedback: Optional[str]) -> DebugObservation:
        t = self._task
        agent_test_cases = [
            {"input": tc["input"], "expected": tc["expected"]}
            for tc in t["test_cases"]
        ]
        return DebugObservation(
            task_id=t["id"],
            difficulty=t["difficulty"],
            buggy_code=t["buggy_code"],
            description=t["description"],
            function_signature=t["function_signature"],
            test_cases=agent_test_cases,
            feedback=feedback,
            attempt=self._attempt,
        )

    def _grade(self, code: str):
        """
        Execute the fixed code against all test cases.
        Returns (reward, passed, total, feedback_string).
        Reward = fraction of tests passed  →  dense signal in [0.0, 1.0].
        """
        t             = self._task
        test_cases    = t["test_cases"]
        total         = len(test_cases)
        passed        = 0
        feedback_lines = []

        # Extract bare function name from signature  e.g. "def foo(..." → "foo"
        fn_name = t["function_signature"].split("(")[0].replace("def ", "").strip()

        for i, tc in enumerate(test_cases):
            try:
                namespace = {}
                exec(code, namespace)

                if fn_name not in namespace:
                    feedback_lines.append(
                        f"Test {i+1}: FAIL — function `{fn_name}` not found in submitted code."
                    )
                    continue

                fn     = namespace[fn_name]
                args   = tc["input"]
                result = fn(*args)

                if result == tc["expected"]:
                    passed += 1
                    feedback_lines.append(f"Test {i+1}: PASS")
                else:
                    feedback_lines.append(
                        f"Test {i+1}: FAIL — got {result!r}, expected {tc['expected']!r}"
                    )
            except SyntaxError as e:
                feedback_lines.append(f"Test {i+1}: SYNTAX ERROR — {e}")
            except Exception as e:
                feedback_lines.append(f"Test {i+1}: RUNTIME ERROR — {e}")

        reward   = round(passed / total, 4) if total > 0 else 0.0
        feedback = "\n".join(feedback_lines)
        return reward, passed, total, feedback