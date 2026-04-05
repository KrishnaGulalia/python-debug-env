"""
EASY tasks — syntax errors that prevent the code from even running.
An LLM should solve these in 1 attempt.
"""

EASY_TASKS = [
    {
        "id": "easy_sum_list",
        "difficulty": "easy",
        "description": (
            "Fix the function `sum_list` that should return the sum of all numbers "
            "in a list. The function has a syntax error (missing colon)."
        ),
        "function_signature": "def sum_list(numbers: list) -> int",
        "buggy_code": """\
def sum_list(numbers)
    total = 0
    for num in numbers:
        total += num
    return total
""",
        "solution": """\
def sum_list(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
""",
        "test_cases": [
            {"input": ([1, 2, 3],),    "expected": 6},
            {"input": ([0, 0, 0],),    "expected": 0},
            {"input": ([-1, 1, -2, 2],), "expected": 0},
            {"input": ([10],),         "expected": 10},
            {"input": ([],),           "expected": 0},
        ],
    },
    {
        "id": "easy_count_evens",
        "difficulty": "easy",
        "description": (
            "Fix the function `count_evens` that counts how many even numbers are "
            "in a list. The function uses a wrong keyword (`retrun` instead of `return`)."
        ),
        "function_signature": "def count_evens(numbers: list) -> int",
        "buggy_code": """\
def count_evens(numbers):
    count = 0
    for n in numbers:
        if n % 2 == 0:
            count += 1
    retrun count
""",
        "solution": """\
def count_evens(numbers):
    count = 0
    for n in numbers:
        if n % 2 == 0:
            count += 1
    return count
""",
        "test_cases": [
            {"input": ([1, 2, 3, 4],),  "expected": 2},
            {"input": ([1, 3, 5],),     "expected": 0},
            {"input": ([2, 4, 6],),     "expected": 3},
            {"input": ([],),            "expected": 0},
            {"input": ([0, -2, 7],),    "expected": 2},
        ],
    },
]

EASY_TASK_BY_ID = {t["id"]: t for t in EASY_TASKS}