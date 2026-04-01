import requests
import os

# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")

BASE_URL = API_BASE_URL

print("[START] Beginning inference")

# Reset environment
response = requests.post(f"{BASE_URL}/reset")
obs = response.json()

done = False
step_count = 0
total_reward = 0

while not done:
    email = obs["emails"][step_count]

    # Simple rule-based agent
    if "unhappy" in email["text"].lower():
        action = {
            "emotion": "angry",
            "priority": "high",
            "decision": "reply"
        }
    elif "sale" in email["text"].lower():
        action = {
            "emotion": "positive",
            "priority": "low",
            "decision": "ignore"
        }
    else:
        action = {
            "emotion": "neutral",
            "priority": "medium",
            "decision": "schedule"
        }

    # Step
    response = requests.post(f"{BASE_URL}/step", json=action)
    data = response.json()

    print(f"[STEP] step={step_count} reward={data['reward']} done={data['done']}")

    total_reward += data["reward"]
    obs = data["observation"]
    done = data["done"]
    step_count += 1

print(f"[END] total_reward={total_reward}")