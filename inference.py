import requests
import os
import sys
import time
from openai import OpenAI

# API_BASE_URL = evaluator's LiteLLM server (for LLM calls)
API_BASE_URL = os.getenv("API_BASE_URL", "https://litellm.sclr.ac")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# Your own HF Space environment server (for reset/step)
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")

# OpenAI client pointing to evaluator's LiteLLM
client = None
if HF_TOKEN:
    try:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=HF_TOKEN
        )
    except Exception as e:
        print(f"[WARNING] Failed to initialize OpenAI client: {str(e)}")

print("[START] Beginning inference")

try:
    # Reset YOUR environment (HF Space)
    max_retries = 3
    retry_delay = 2
    reset_response = None

    for attempt in range(max_retries):
        try:
            res = requests.post(f"{ENV_BASE_URL}/reset", timeout=15)
            res.raise_for_status()
            reset_response = res.json()
            break
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"[RETRY] Reset failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to reset environment after {max_retries} attempts: {str(e)}")

    if reset_response is None:
        raise Exception("Failed to get reset response")

    obs = reset_response
    done = False
    step_count = 0
    total_reward = 0

    while not done:
        emails = obs.get("emails", [])

        if step_count >= len(emails):
            break

        email = emails[step_count]
        email_text = email.get("text", "").lower()

        # Use LLM to decide action (uses evaluator's LiteLLM)
        action = {"emotion": "neutral", "priority": "medium", "decision": "schedule"}  # safe default

        if client:
            try:
                prompt = f"""You are an email assistant. Analyze this email and respond ONLY with a JSON object with these exact keys:
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
                import json
                text = response.choices[0].message.content.strip()
                # Strip markdown fences if present
                text = text.replace("```json", "").replace("```", "").strip()
                action = json.loads(text)
            except Exception as e:
                print(f"[WARNING] LLM call failed, using rule-based fallback: {str(e)}")
                # Rule-based fallback
                if any(w in email_text for w in ["urgent", "asap", "critical", "unhappy", "angry", "frustrated"]):
                    action = {"emotion": "angry", "priority": "high", "decision": "reply"}
                elif any(w in email_text for w in ["sale", "offer", "deal", "promo", "discount"]):
                    action = {"emotion": "positive", "priority": "low", "decision": "ignore"}
                else:
                    action = {"emotion": "neutral", "priority": "medium", "decision": "schedule"}

        # Send action to YOUR environment (HF Space)
        try:
            res = requests.post(f"{ENV_BASE_URL}/step", json=action, timeout=15)
            res.raise_for_status()
            data = res.json()

            if "error" in data:
                raise Exception(f"Server error in step response: {data['error']}")

            reward = data.get("reward", 0)
            total_reward += reward
            obs = data.get("observation", {})
            done = data.get("done", False)

            print(f"[STEP] step={step_count} action={action} reward={round(reward, 2)} done={done}")
            step_count += 1

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error during step {step_count}: {str(e)}")
        except Exception as e:
            raise Exception(f"Step {step_count} failed: {str(e)}")

    print(f"[END] total_reward={round(total_reward, 2)} steps={step_count}")

except Exception as e:
    print(f"[ERROR] {str(e)}", file=sys.stderr)
    sys.exit(1)
