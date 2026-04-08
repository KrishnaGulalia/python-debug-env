import os
import sys
import textwrap
from typing import List, Optional

# STRICT CONFIG (NO FALLBACKS)

API_KEY = os.environ["API_KEY"]
API_BASE_URL = os.environ["API_BASE_URL"]

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://krishnagulalia-python-debug-env.hf.space")

BENCHMARK = "python-debug-env"
MAX_STEPS = 5
TEMPERATURE = 0.2
MAX_TOKENS = 1024
SUCCESS_SCORE_THRESHOLD = 0.5

TASKS = [
    "easy_sum_list",
    "easy_count_evens",
    "medium_palindrome",
    "medium_count_vowels",
    "hard_binary_search",
    "hard_merge_sort",
    "hard_can_partition",
    "hard_min_edit_distance",
]



# LOGGING (DO NOT TOUCH)

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    action_compact = str(action).replace("\n", "\\n").replace("\r", "")[:200]
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action_compact!r} reward={reward:.2f} "
        f"done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards) if rewards else "0.00"
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.3f} rewards={rewards_str}",
        flush=True,
    )



# ENV CALLS

def env_reset(task_id: str) -> dict:
    import requests
    resp = requests.post(
        f"{ENV_BASE_URL}/reset",
        json={"task_id": task_id},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def env_step(fixed_code: str) -> dict:
    import requests
    resp = requests.post(
        f"{ENV_BASE_URL}/step",
        json={"fixed_code": fixed_code},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()



# LLM PROMPTS

SYSTEM_PROMPT = textwrap.dedent("""\
You are an expert Python programmer.
Return ONLY the corrected Python code — no explanations, no markdown fences.
Keep the function name exactly the same.
""")


def build_user_prompt(obs: dict, attempt: int) -> str:
    try:
        test_cases_str = "\n".join(
            f"Input: {tc['input']} -> Expected: {tc['expected']}"
            for tc in obs.get("test_cases", [])
        )

        feedback_section = (
            f"\nFeedback from last attempt:\n{obs['feedback']}\n"
            if obs.get("feedback") else ""
        )

        return (
            f"Task: {obs.get('description', '')}\n"
            f"Difficulty: {obs.get('difficulty', '')}\n\n"
            f"Buggy code:\n{obs.get('buggy_code', '')}\n\n"
            f"Function signature: {obs.get('function_signature', '')}\n\n"
            f"Test cases:\n{test_cases_str}\n"
            f"{feedback_section}"
            f"Attempt {attempt} — return ONLY the corrected Python code:"
        )
    except Exception:
        return f"Fix this buggy Python code:\n{obs.get('buggy_code', '')}"


def get_fixed_code(client, obs: dict, attempt: int) -> str:
    try:
        user_prompt = build_user_prompt(obs, attempt)

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

        text = (completion.choices[0].message.content or "").strip()

        # Clean markdown if model adds it
        if text.startswith("```python"):
            text = text[len("```python"):].strip()
        if text.startswith("```"):
            text = text[3:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()

        return text if text else obs.get("buggy_code", "")

    except Exception as exc:
        print(f"[DEBUG] LLM request failed: {exc}", flush=True)
        return obs.get("buggy_code", "")



# TASK RUNNER

def run_task(client, task_id: str) -> dict:
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)

    try:
        reset_result = env_reset(task_id)
        obs = reset_result.get("observation", {})
        done = reset_result.get("done", False)

        for step in range(1, MAX_STEPS + 1):
            if done:
                break

            fixed_code = get_fixed_code(client, obs, attempt=step)

            error_msg = None

            try:
                step_result = env_step(fixed_code)
                reward = float(step_result.get("reward", 0.0))
                done = step_result.get("done", False)
                obs = step_result.get("observation", obs)
            except Exception as e:
                reward = 0.0
                done = True
                error_msg = str(e)[:100]

            rewards.append(reward)
            steps_taken = step

            log_step(step, fixed_code, reward, done, error_msg)

            if done:
                break

        score = max(rewards) if rewards else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as outer_exc:
        print(f"[DEBUG] Episode error for {task_id}: {outer_exc}", flush=True)
        if not rewards:
            rewards = [0.0]
        steps_taken = max(steps_taken, 1)
        score = 0.0
        success = False

    finally:
        log_end(success, steps_taken, score, rewards)

    return {"task_id": task_id, "score": score, "success": success}



# MAIN

def main():
    from openai import OpenAI

    # MUST use provided proxy
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY,
    )

    print(f"[DEBUG] ENV_BASE_URL={ENV_BASE_URL}", flush=True)
    print(f"[DEBUG] MODEL={MODEL_NAME}", flush=True)

    results = []

    for task_id in TASKS:
        print(f"\n{'='*60}", flush=True)
        result = run_task(client, task_id)
        results.append(result)

    print(f"\n{'='*60}", flush=True)
    print("[SUMMARY]", flush=True)

    for r in results:
        status = "✓" if r["success"] else "✗"
        print(f"  {status}  {r['task_id']:40s}  score={r['score']:.3f}", flush=True)

    avg = sum(r["score"] for r in results) / len(results)
    print(f"\n  Average score: {avg:.3f}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] {e}", flush=True)