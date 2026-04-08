import requests
import os
import sys
import time
from openai import OpenAI

# ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# OpenAI client (required)
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN or "dummy")


def run_task(task_id: str):
    base_url = os.getenv("OPENENV_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")

    print(f"[START] task={task_id} env=ai_inbox model={MODEL_NAME}")

    # RESET
    for attempt in range(3):
        try:
            res = requests.post(f"{base_url}/reset", json={"task": task_id}, timeout=10)
            res.raise_for_status()
            obs = res.json()
            break
        except Exception as e:
            if attempt == 2:
                print(f"[ERROR] Reset failed: {e}", file=sys.stderr)
                print(f"[END] success=false steps=0 score=0.05 rewards=")
                return
            time.sleep(1)

    done = False
    step_count = 0
    total_reward = 0.0
    rewards = []   # ✅ FIXED

    while not done:
        emails = obs.get("emails", [])

        if not isinstance(emails, list) or step_count >= len(emails):
            break

        email = emails[step_count]

        # Try LLM
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
            # Fallback logic
            text = email.get("text", "").lower()

            if "unhappy" in text or "urgent" in text:
                action = {"emotion": "angry", "priority": "high", "decision": "reply"}
            elif "sale" in text or "offer" in text:
                action = {"emotion": "positive", "priority": "low", "decision": "ignore"}
            else:
                action = {"emotion": "neutral", "priority": "medium", "decision": "schedule"}

        # STEP
        try:
            res = requests.post(f"{base_url}/step", json=action, timeout=10)
            res.raise_for_status()
            data = res.json()

            reward = float(data.get("reward", 0.0))
            done = data.get("done", False)
            obs = data.get("observation", {})

            rewards.append(reward)
            total_reward += reward

            print(f"[STEP] step={step_count} action={action.get('decision','none')} reward={round(reward,2)} done={str(done).lower()} error=null")

            step_count += 1

        except Exception as e:
            print(f"[STEP] step={step_count} action=error reward=0.05 done=true error={str(e)}")
            break

    # FINAL SCORE
    score = total_reward / step_count if step_count > 0 else 0.0
    score = max(0.05, min(0.95, score))  # clamp strictly between (0,1)

    success = score > 0
    rewards_str = ",".join([f"{round(r,2)}" for r in rewards])

    print(f"[END] success={str(success).lower()} steps={step_count} score={round(score,2)} rewards={rewards_str}")


def run_inference():
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        print(f"\n--- Running task: {task} ---")
        run_task(task)


if __name__ == "__main__":
    run_inference()
