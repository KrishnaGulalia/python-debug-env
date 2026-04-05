# Python Debug Environment 

An **OpenEnv** environment where an AI agent is given buggy Python functions and must return corrected code.



## Environment Description

The agent receives a Python function with a deliberate bug and must submit a fixed version. Grading is fully deterministic: the submitted code is executed against a hidden test suite, and the reward equals the fraction of tests passed.

This models a real task that every developer does daily — **code debugging**.



## Action & Observation Spaces

### Observation
| Field | Type | Description |
|---|---|---|
| `task_id` | string | Unique task identifier |
| `difficulty` | string | `easy`, `medium`, or `hard` |
| `buggy_code` | string | The Python function with a bug |
| `description` | string | Plain-English description of what the function should do |
| `function_signature` | string | Expected function signature |
| `test_cases` | list | `[{input, expected}]` — public test cases |
| `feedback` | string or null | Test results from the last attempt |
| `attempt` | int | Current attempt number (1-indexed) |

### Action
| Field | Type | Description |
|---|---|---|
| `fixed_code` | string | The agent's corrected Python code |

### Reward
- **Type**: `float` in `[0.0, 1.0]`
- **Formula**: `tests_passed / total_tests`
- **Dense**: partial credit is awarded — fixing half the bugs scores 0.5
- **Terminal**: episode ends on a perfect score of `1.0` or after `MAX_STEPS=5` attempts



## Tasks

| Task ID | Difficulty | Bug Type | Description |
|---|---|---|---|
| `easy_sum_list` | Easy | Syntax error | Missing colon in function definition |
| `medium_palindrome` | Medium | Off-by-one error | Wrong index in palindrome check |
| `hard_binary_search` | Hard | Algorithmic bug | Wrong boundary in binary search |

### Baseline Scores (Qwen2.5-72B-Instruct)
| Task | Score |
|---|---|
| easy_sum_list | 1.00 |
| medium_palindrome | 1.00 |
| hard_binary_search | 0.71 |



## Setup & Usage

### Local (without Docker)

```bash
pip install -r requirements.txt
python server.py
# Server runs at http://localhost:8000
```

```python
import requests

# Start episode
obs = requests.post("http://localhost:8000/reset", json={"task_id": "easy_sum_list"}).json()

# Submit fix
result = requests.post("http://localhost:8000/step", json={
    "fixed_code": "def sum_list(numbers):\n    return sum(numbers)"
}).json()

print(result["reward"])   # 1.0 if correct
```

### Docker

```bash
docker build -t python-debug-env .
docker run -p 8000:8000 python-debug-env
```

### Run baseline inference

```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
export HF_TOKEN="hf_..."
export ENV_BASE_URL="http://localhost:8000"

python inference.py
```



## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Liveness probe |
| `/reset` | POST | Start new episode. Body: `{"task_id": "..."}` |
| `/step` | POST | Submit action. Body: `{"fixed_code": "..."}` |
| `/state` | GET | Current environment state |
| `/tasks` | GET | List all tasks with metadata |



## Project Structure

```
python-debug-env/
├── env/
│   ├── __init__.py
│   ├── models.py        # Pydantic: Observation, Action, StepResult
│   ├── environment.py   # Core env logic (reset/step/state/grading)
│   └── tasks.py         # All task definitions (buggy code + test cases)
├── graders/
│   ├── __init__.py
│   └── grader.py        # Standalone graders per difficulty
├── server.py            # FastAPI HTTP server
├── inference.py         # Baseline inference script (OpenAI client)
├── openenv.yaml         # OpenEnv metadata
├── requirements.txt
├── Dockerfile
└── README.md
```