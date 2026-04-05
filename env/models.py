from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class DebugObservation(BaseModel):
    task_id: str
    difficulty: str                  # "easy" | "medium" | "hard"
    buggy_code: str
    description: str
    function_signature: str
    test_cases: List[Dict[str, Any]]  # [{"input": ..., "expected": ...}]
    feedback: Optional[str] = None    # error msg or partial result from last attempt
    attempt: int = 0


class DebugAction(BaseModel):
    fixed_code: str   # the agent's corrected Python code


class DebugReward(BaseModel):
    reward: float
    tests_passed: int
    total_tests: int
    message: str


class StepResult(BaseModel):
    observation: DebugObservation
    reward: float
    done: bool
    info: Dict[str, Any] = {}


class ResetResult(BaseModel):
    observation: DebugObservation
    done: bool = False