import requests
import os
import sys
import time
import json
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://litellm.sclr.ac")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

TASKS = ["easy", "medium", "hard"]

for task_name in TASKS:
    rewards_list = []
    step_count = 0
    success = False

    print(f"[START] task={task_name} env=ai-inbox model={MODEL_NAME}")

    try:
        # Reset environment
        max_retries = 3
        reset_response = None
        for attempt in range(max_retries):
            try:
                res = requests.post(f"{ENV_BASE_URL}/reset", timeout=15)
                res.raise_for_status()
                reset_response = res.json()
                break
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    raise Exception(f"Reset failed: {str(e)}")

        obs = reset_response
        done = False

        while not done:
            emails = obs.get("emails", [])
            if step_count >= len(emails):
                break

            email = emails[step_count]
            email_text = email.get("text", "").lower()
            last_error = None

            # Use LLM
            try:
                prompt = f"""Analyze this email and respond ONLY with a JSON object with these exact keys:
- emotion: one of "angry", "neutral", "positive"
- priority: one of "high", "medium", "low"
- decision: one of "reply", "schedule", "ignore"

Email: {email.get('text', '')}

Respond with only the JSON, no explanation."""

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    temperature=0
                )
                text = response.choices[0].message.content.strip()
                text = text.replace("```json", "").replace("```", "").strip()
                action = json.loads(text)
            except Exception as e:
                last_error = str(e)
                # Rule-based fallback
                if any(w in email_text for w in ["urgent", "asap", "unhappy", "angry", "frustrated", "critical"]):
                    action = {"emotion": "angry", "priority": "high", "decision": "reply"}
                elif any(w in email_text for w in ["sale", "offer", "deal", "promo", "discount"]):
                    action = {"emotion": "positive", "priority": "low", "decision": "ignore"}
                else:
                    action = {"emotion": "neutral", "priority": "medium", "decision": "schedule"}

            # Step environment
            try:
                res = requests.post(f"{ENV_BASE_URL}/step", json=action, timeout=15)
                res.raise_for_status()
                data = res.json()

                if "error" in data:
                    raise Exception(data["error"])

                reward = data.get("reward", 0)
                rewards_list.append(reward)
                obs = data.get("observation", {})
                done = data.get("done", False)
                error_field = last_error if last_error else "null"

                print(f"[STEP] step={step_count + 1} action={json.dumps(action)} reward={reward:.2f} done={'true' if done else 'false'} error={error_field}")
                step_count += 1

                if done:
                    success = True

            except Exception as e:
                print(f"[STEP] step={step_count + 1} action={json.dumps(action)} reward=0.00 done=false error={str(e)}")
                break

    except Exception as e:
        print(f"[STEP] step={step_count + 1} action={{}} reward=0.00 done=false error={str(e)}", file=sys.stderr)

    rewards_str = ",".join(f"{r:.2f}" for r in rewards_list) if rewards_list else "0.00"
    print(f"[END] success={'true' if success else 'false'} steps={step_count} rewards={rewards_str}")
