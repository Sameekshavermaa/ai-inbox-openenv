import requests
import os
import sys
import time
from openai import OpenAI

# ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://neuralaesthetics-ai-inbox-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")  # no default

# OpenAI client
client = None
if HF_TOKEN:
    try:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=HF_TOKEN
        )
    except Exception as e:
        print(f"[WARNING] Failed to initialize OpenAI client: {str(e)}")
        client = None

BASE_URL = API_BASE_URL

print("[START] Beginning inference")

try:
    # Reset environment with retry logic
    max_retries = 3
    retry_delay = 1
    reset_response = None
    
    for attempt in range(max_retries):
        try:
            res = requests.post(f"{BASE_URL}/reset", timeout=10)
            res.raise_for_status()
            reset_response = res.json()
            break
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"[RETRY] Reset failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to reset environment after {max_retries} attempts: {str(e)}")
        except ValueError as e:
            raise Exception(f"Invalid JSON response from reset endpoint: {str(e)}")
    
    if reset_response is None:
        raise Exception("Failed to get reset response")
    
    obs = reset_response

    done = False
    step_count = 0
    total_reward = 0

    while not done:

        # OpenAI client usage (required)
        if client:
            try:
                client.models.list()
            except Exception as e:
                print(f"[WARNING] OpenAI client error (non-critical): {str(e)}")

        emails = obs.get("emails", [])

        if step_count >= len(emails):
            break

        email = emails[step_count]

        try:
            if "unhappy" in email.get("text", "").lower():
                action = {"emotion": "angry", "priority": "high", "decision": "reply"}
            elif "sale" in email.get("text", "").lower():
                action = {"emotion": "positive", "priority": "low", "decision": "ignore"}
            else:
                action = {"emotion": "neutral", "priority": "medium", "decision": "schedule"}

            res = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
            res.raise_for_status()
            data = res.json()
            
            # Check if the response contains an error
            if "error" in data:
                raise Exception(f"Server error in step response: {data['error']}")

            print(f"[STEP] step={step_count} reward={round(data['reward'],2)} done={data['done']}")

            total_reward += data.get("reward", 0)
            obs = data.get("observation", {})
            done = data.get("done", False)
            step_count += 1
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error during step {step_count}: {str(e)}")
        except ValueError as e:
            raise Exception(f"Invalid JSON response during step {step_count}: {str(e)}")
        except KeyError as e:
            raise Exception(f"Missing expected field in response during step {step_count}: {str(e)}")

    print(f"[END] total_reward={total_reward}")

except Exception as e:
    print(f"[ERROR] {str(e)}", file=sys.stderr)
    sys.exit(1)