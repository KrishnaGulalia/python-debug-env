"""
HARD tasks — algorithmic bugs in DSA problems.
Code runs, passes some tests, but fails on edge cases.
Requires deep understanding of the algorithm to fix.
"""

HARD_TASKS = [
    {
        "id": "hard_binary_search",
        "difficulty": "hard",
        "description": (
            "Fix the function `binary_search` that searches for a target value in a "
            "sorted array and returns its index, or -1 if not found. "
            "The initial `right` boundary is wrong, causing an IndexError on non-empty arrays."
        ),
        "function_signature": "def binary_search(arr: list, target: int) -> int",
        "buggy_code": """\
def binary_search(arr, target):
    left, right = 0, len(arr)       # BUG: should be len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
        "solution": """\
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
        "test_cases": [
            {"input": ([1, 3, 5, 7, 9], 5),         "expected": 2},
            {"input": ([1, 3, 5, 7, 9], 1),         "expected": 0},
            {"input": ([1, 3, 5, 7, 9], 9),         "expected": 4},
            {"input": ([1, 3, 5, 7, 9], 4),         "expected": -1},
            {"input": ([2],             2),          "expected": 0},
            {"input": ([2],             3),          "expected": -1},
            {"input": (list(range(0, 100, 2)), 64), "expected": 32},
        ],
    },
    {
        "id": "hard_merge_sort",
        "difficulty": "hard",
        "description": (
            "Fix the function `merge_sort` that sorts a list using the merge sort algorithm. "
            "The merge step has a bug: when one half is exhausted it stops instead of "
            "appending the remaining elements from the other half."
        ),
        "function_signature": "def merge_sort(arr: list) -> list",
        "buggy_code": """\
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):   # BUG: stops too early
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # BUG: missing the lines that drain the remaining elements
    return result
""",
        "solution": """\
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
""",
        "test_cases": [
            {"input": ([3, 1, 4, 1, 5, 9, 2, 6],), "expected": [1, 1, 2, 3, 4, 5, 6, 9]},
            {"input": ([1],),                        "expected": [1]},
            {"input": ([],),                         "expected": []},
            {"input": ([5, 4, 3, 2, 1],),            "expected": [1, 2, 3, 4, 5]},
            {"input": ([1, 2, 3, 4, 5],),            "expected": [1, 2, 3, 4, 5]},
            {"input": ([-3, 0, -1, 2],),             "expected": [-3, -1, 0, 2]},
        ],
    },
]

HARD_TASK_BY_ID = {t["id"]: t for t in HARD_TASKS}