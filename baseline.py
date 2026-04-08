from env import InboxEnv
from models import Action

env = InboxEnv()
obs = env.reset()

done = False
total_score = 0
steps = 0

while not done:
    email = obs.emails[steps]

    if "unhappy" in email["text"].lower():
        action = Action(emotion="angry", priority="high", decision="reply")
    elif "sale" in email["text"].lower():
        action = Action(emotion="positive", priority="low", decision="ignore")
    else:
        action = Action(emotion="neutral", priority="medium", decision="schedule")

    obs, reward, done, _ = env.step(action)

    total_score += reward.score
    steps += 1

# 👇 THIS is the important line
def safe_score(x):
    return max(0.05, min(0.95, float(x)))

final_score = safe_score(total_score / steps)
print(f"Baseline Score: {round(final_score, 2)}")
