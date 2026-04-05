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
    {
        "id": "hard_can_partition",
        "difficulty": "hard",
        "description": (
            "Fix the function `can_partition` that determines if an array can be "
            "partitioned into two subsets with equal sum. "
            "The inner loop iterates in the wrong direction — it goes forward instead "
            "of backward, causing elements to be reused multiple times (unbounded knapsack "
            "behaviour instead of 0/1 knapsack). This makes the function incorrectly return "
            "True for inputs that should return False."
        ),
        "function_signature": "def can_partition(nums: list) -> bool",
        "buggy_code": """\
def can_partition(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for j in range(num, target + 1):   # BUG: forward loop reuses elements
            dp[j] = dp[j] or dp[j - num]

    return dp[target]
""",
        "solution": """\
def can_partition(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for j in range(target, num - 1, -1):   # iterate backwards: 0/1 knapsack
            dp[j] = dp[j] or dp[j - num]

    return dp[target]
""",
        "test_cases": [
            {"input": ([1, 5, 11, 5],),  "expected": True},
            {"input": ([1, 2, 3, 5],),   "expected": False},
            {"input": ([1, 1],),          "expected": True},
            {"input": ([1, 2, 5],),      "expected": False},
            {"input": ([3, 1],),         "expected": False},
            {"input": ([2, 2, 4],),      "expected": True},
            {"input": ([1, 3],),         "expected": False},
            {"input": ([100],),          "expected": False},
        ],
    },
    {
        "id": "hard_min_edit_distance",
        "difficulty": "hard",
        "description": (
            "Fix the function `min_edit_distance` that computes the Levenshtein "
            "(edit) distance between two strings using dynamic programming. "
            "The DP table is missing its base case initialization: the first column "
            "should be filled with range(m+1) and the first row with range(n+1), "
            "representing the cost of converting to/from an empty string. "
            "Without this, the function returns wrong results whenever either string "
            "is empty or a prefix must be deleted/inserted."
        ),
        "function_signature": "def min_edit_distance(word1: str, word2: str) -> int",
        "buggy_code": """\
def min_edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # BUG: missing base case initialization:
    #   for i in range(m + 1): dp[i][0] = i
    #   for j in range(n + 1): dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[m][n]
""",
        "solution": """\
def min_edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[m][n]
""",
        "test_cases": [
            {"input": ("horse",     "ros"),       "expected": 3},
            {"input": ("intention", "execution"), "expected": 5},
            {"input": ("",          "abc"),       "expected": 3},
            {"input": ("abc",       ""),          "expected": 3},
            {"input": ("abc",       "abc"),       "expected": 0},
            {"input": ("a",         "b"),         "expected": 1},
            {"input": ("kitten",    "sitting"),   "expected": 3},
            {"input": ("ab",        "bc"),        "expected": 2},
        ],
    },
]

HARD_TASK_BY_ID = {t["id"]: t for t in HARD_TASKS}