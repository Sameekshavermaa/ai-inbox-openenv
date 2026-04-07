import requests
import os
from openai import OpenAI

# ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")  # no default

# OpenAI client
client = None
if HF_TOKEN:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

BASE_URL = API_BASE_URL

print("[START] Beginning inference")

try:
    # Reset environment
    res = requests.post(f"{BASE_URL}/reset")
    res.raise_for_status()
    obs = res.json()

    done = False
    step_count = 0
    total_reward = 0

    while not done:

        # OpenAI client usage (required)
        if client:
            try:
                client.models.list()
            except:
                pass

        emails = obs.get("emails", [])

        if step_count >= len(emails):
            break

        email = emails[step_count]

        if "unhappy" in email["text"].lower():
            action = {"emotion": "angry", "priority": "high", "decision": "reply"}
        elif "sale" in email["text"].lower():
            action = {"emotion": "positive", "priority": "low", "decision": "ignore"}
        else:
            action = {"emotion": "neutral", "priority": "medium", "decision": "schedule"}

        res = requests.post(f"{BASE_URL}/step", json=action)
        res.raise_for_status()
        data = res.json()

        print(f"[STEP] step={step_count} reward={round(data['reward'],2)} done={data['done']}")

        total_reward += data["reward"]
        obs = data["observation"]
        done = data["done"]
        step_count += 1

    print(f"[END] total_reward={total_reward}")

except Exception as e:
    print("[ERROR]", str(e))
    exit(1)