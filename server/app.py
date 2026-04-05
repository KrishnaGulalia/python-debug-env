"""
FastAPI server for the Python Debug Environment.
Exposes the OpenEnv HTTP API:
  POST /reset           → start new episode
  POST /step            → submit action
  GET  /state           → current state
  GET  /health          → liveness probe
  GET  /tasks           → list available tasks
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

from env.environment import PythonDebugEnv
from env.models import DebugAction, StepResult, ResetResult

app = FastAPI(
    title="Python Debug Environment",
    description="OpenEnv environment for training agents to fix Python bugs.",
    version="1.0.0",
)

# One global env instance (stateless per request via reset/step)
_env = PythonDebugEnv()


class ResetRequest(BaseModel):
    task_id: Optional[str] = None



# Endpoints


@app.get("/health")
def health():
    return {"status": "ok", "env": "python-debug-env"}


@app.post("/reset")
def reset(body: ResetRequest = ResetRequest()) -> ResetResult:
    """Start a fresh episode. Optionally specify task_id."""
    result = _env.reset(task_id=body.task_id)
    return result


@app.post("/step")
def step(action: DebugAction) -> StepResult:
    """Submit fixed code as an action."""
    try:
        result = _env.step(action)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    """Return the current environment state."""
    return _env.state()


@app.get("/tasks")
def list_tasks():
    """List all available tasks with metadata (no solutions)."""
    from env.tasks import ALL_TASKS as TASKS
    return [
        {
            "id": t["id"],
            "difficulty": t["difficulty"],
            "description": t["description"],
            "function_signature": t["function_signature"],
            "num_test_cases": len(t["test_cases"]),
        }
        for t in TASKS
    ]


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=7860, reload=False)

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()