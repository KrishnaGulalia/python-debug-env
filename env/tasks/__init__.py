from env.tasks.easy   import EASY_TASKS,   EASY_TASK_BY_ID
from env.tasks.medium import MEDIUM_TASKS, MEDIUM_TASK_BY_ID
from env.tasks.hard   import HARD_TASKS,   HARD_TASK_BY_ID

ALL_TASKS = EASY_TASKS + MEDIUM_TASKS + HARD_TASKS

TASK_BY_ID = {
    **EASY_TASK_BY_ID,
    **MEDIUM_TASK_BY_ID,
    **HARD_TASK_BY_ID,
}

TASK_BY_DIFFICULTY = {
    "easy":   EASY_TASKS,
    "medium": MEDIUM_TASKS,
    "hard":   HARD_TASKS,
}

__all__ = [
    "ALL_TASKS",
    "TASK_BY_ID",
    "TASK_BY_DIFFICULTY",
    "EASY_TASKS",
    "MEDIUM_TASKS",
    "HARD_TASKS",
]