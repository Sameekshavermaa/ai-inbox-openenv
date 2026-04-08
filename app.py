from fastapi import FastAPI
from env import InboxEnv
from models import Action
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI()
env = InboxEnv()

# ✅ ROOT (just for sanity)
@app.get("/")
def home():
    return {"status": "running"}

# ✅ RESET (POST - used by OpenEnv)
@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "emails": obs.emails,
        "overwhelm_score": obs.overwhelm_score
    }

# ✅ RESET (GET - for browser testing)
@app.get("/reset")
def reset_get():
    obs = env.reset()
    return {
        "emails": obs.emails,
        "overwhelm_score": obs.overwhelm_score
    }

# ✅ STEP
@app.post("/step")
def step(action: dict):
    try:
        action_obj = Action(**action)
        obs, reward, done, info = env.step(action_obj)

        return {
            "observation": {
                "emails": obs.emails,
                "overwhelm_score": obs.overwhelm_score
            },
            "reward": reward.score,
            "done": done,
            "info": info
        }
    except Exception as e:
        return {
            "error": str(e),
            "observation": None,
            "reward": 0,
            "done": False,
            "info": {}
        }

# ✅ STATE
@app.get("/state")
def state():
    return env.state()
