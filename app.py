from env import InboxEnv

print("🚀 Starting AI Inbox Environment...")

env = InboxEnv()
obs = env.reset()

print("✅ Environment started successfully")
print("📩 Emails Loaded:", len(obs.emails))
print("🧠 Overwhelm Score:", obs.overwhelm_score)