"""
MEDIUM tasks — logic errors: off-by-one, wrong operator, wrong condition.
Code runs but produces wrong answers. Requires careful reasoning.
"""

MEDIUM_TASKS = [
    {
        "id": "medium_palindrome",
        "difficulty": "medium",
        "description": (
            "Fix the function `is_palindrome` that checks whether a string reads "
            "the same forwards and backwards. "
            "There is an off-by-one index error on the comparison."
        ),
        "function_signature": "def is_palindrome(s: str) -> bool",
        "buggy_code": """\
def is_palindrome(s):
    for i in range(len(s) // 2):
        if s[i] != s[len(s) - i]:   # BUG: should be len(s) - 1 - i
            return False
    return True
""",
        "solution": """\
def is_palindrome(s):
    for i in range(len(s) // 2):
        if s[i] != s[len(s) - 1 - i]:
            return False
    return True
""",
        "test_cases": [
            {"input": ("racecar",), "expected": True},
            {"input": ("hello",),   "expected": False},
            {"input": ("abba",),    "expected": True},
            {"input": ("a",),       "expected": True},
            {"input": ("ab",),      "expected": False},
            {"input": ("madam",),   "expected": True},
        ],
    },
    {
        "id": "medium_count_vowels",
        "difficulty": "medium",
        "description": (
            "Fix the function `count_vowels` that counts vowels in a string. "
            "It uses `=` (assignment) instead of `==` (comparison) inside the condition, "
            "making it always count every character."
        ),
        "function_signature": "def count_vowels(s: str) -> int",
        "buggy_code": """\
def count_vowels(s):
    vowels = 'aeiouAEIOU'
    count = 0
    for ch in s:
        if ch in vowels:
            count = count + 1   # this line is fine
    return count + 1            # BUG: should just be return count
""",
        "solution": """\
def count_vowels(s):
    vowels = 'aeiouAEIOU'
    count = 0
    for ch in s:
        if ch in vowels:
            count = count + 1
    return count
""",
        "test_cases": [
            {"input": ("hello",),      "expected": 2},
            {"input": ("rhythm",),     "expected": 0},
            {"input": ("aeiou",),      "expected": 5},
            {"input": ("",),           "expected": 0},
            {"input": ("Python",),     "expected": 1},
            {"input": ("AEIOU",),      "expected": 5},
        ],
    },
]

MEDIUM_TASK_BY_ID = {t["id"]: t for t in MEDIUM_TASKS}