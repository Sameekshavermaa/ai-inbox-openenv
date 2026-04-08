import random
from models import Observation, Action, Reward

class InboxEnv:

    def __init__(self):
        self.emails = []
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        self.emails = self.load_emails()
        return Observation(emails=self.emails, overwhelm_score=self.calc_overwhelm())

    def step(self, action: Action):
        email = self.emails[self.current_step]
        reward = self.evaluate(action, email)
        self.current_step += 1
        done = self.current_step >= len(self.emails)
        return (
            Observation(emails=self.emails, overwhelm_score=self.calc_overwhelm()),
            Reward(score=reward),
            done,
            {}
        )

    def state(self):
        return {
            "step": self.current_step,
            "emails": self.emails
        }

    def load_emails(self):
        return [
            {"text": "I am very unhappy with your service!", "emotion": "angry", "priority": "high"},
            {"text": "Meeting tomorrow at 5", "emotion": "neutral", "priority": "medium"},
            {"text": "Check out our sale!", "emotion": "positive", "priority": "low"},
        ]

    def calc_overwhelm(self):
        return len(self.emails) - self.current_step

    def evaluate(self, action, email):
        score = 0
        if action.emotion == email["emotion"]:
            score += 0.3
        if action.priority == email["priority"]:
            score += 0.5
        if action.decision == "reply" and email["priority"] == "high":
            score += 0.7
        elif action.decision == "ignore" and email["priority"] == "low":
            score += 0.7
        else:
            score -= 0.5
        return max(0.05, min(0.95, score))  # ✅ strictly between 0 and 1
