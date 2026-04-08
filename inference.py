import requests
import os
import sys
import time
from openai import OpenAI

# API_BASE_URL = evaluator's LiteLLM server (for LLM calls)
API_BASE_URL = os.getenv("API_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")  # ✅ no default here (checklist requirement)

# Your own HF Space environment server (for reset/step)
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")

# OpenAI client (required by hackathon spec)
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN or "dummy")  # ✅ fallback only here

def run_task(task_id: str):
    base_url = os.getenv("OPENENV_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")
    print(f"[START] task={task_id}")

    # Reset with task_id
    for attempt in range(3):
        try:
            res = requests.post(f"{base_url}/reset", json={"task": task_id}, timeout=10)
            res.raise_for_status()
            obs = res.json()
            break
        except Exception as e:
            if attempt == 2:
                print(f"[ERROR] Reset failed: {e}", file=sys.stderr)
                return
            time.sleep(1)

    done = False
    step_count = 0
    total_reward = 0.0

    while not done:
        emails = obs.get("emails", [])
        if step_count >= len(emails):
            break

        email = emails[step_count]

        try:
            import json
            prompt = f"Email: {email.get('text', '')}. Reply with JSON: {{\"emotion\": \"angry|neutral|positive\", \"priority\": \"high|medium|low\", \"decision\": \"reply|schedule|ignore\"}}"
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            raw = response.choices[0].message.content.strip()
            action = json.loads(raw)
        except Exception:
            text = email.get("text", "").lower()
            if "unhappy" in text or "urgent" in text:
                action = {"emotion": "angry", "priority": "high", "decision": "reply"}
            elif "sale" in text or "offer" in text:
                action = {"emotion": "positive", "priority": "low", "decision": "ignore"}
            else:
                action = {"emotion": "neutral", "priority": "medium", "decision": "schedule"}

        try:
            res = requests.post(f"{base_url}/step", json=action, timeout=10)
            res.raise_for_status()
            data = res.json()
            reward = data.get("reward", 0.0)
            total_reward += reward
            obs = data.get("observation", {})
            done = data.get("done", False)
            print(f"[STEP] step={step_count} reward={round(reward, 4)} done={done}")
            step_count += 1
        except Exception as e:
            print(f"[ERROR] step {step_count}: {e}", file=sys.stderr)
            break

    print(f"[END] task={task_id} total_reward={round(total_reward, 4)} steps={step_count}")


def run_inference():
    # Task IDs must exactly match the `id:` fields in openenv.yaml
    tasks = ["easy", "medium", "hard"]
    for task in tasks:
        print(f"\n--- Running task: {task} ---")
        run_task(task)


if __name__ == "__main__":
    run_inference()

