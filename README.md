# 🧠 AI Inbox: Emotion-Aware OpenEnv Environment

> Evaluating AI agents on emotional intelligence, prioritization, and decision-making under cognitive overload.

---

## 🚀 Overview

Modern email systems optimize for organization — not for human well-being.

Users today face:

* 📩 Information overload
* 😵 Decision fatigue
* 😡 Emotionally stressful communication

This project introduces an **AI-powered inbox simulation environment** designed to evaluate how well AI agents can:

* Understand emotional tone
* Prioritize important messages
* Take appropriate actions
* Reduce cognitive overload

---

## 💡 Key Innovation

This environment introduces an **Overwhelm Score** to simulate cognitive load, enabling evaluation of emotionally intelligent AI agents in high-stress communication scenarios.

---

## 🌍 Real-World Applications

* Workplace productivity tools
* Customer support automation
* AI personal assistants
* Mental load-aware systems

---

## ⚙️ Environment Design

This environment follows the OpenEnv specification.

### 🔁 Core API

* `reset()` → Initializes inbox with predefined emails
* `step(action)` → Executes agent action
* `state()` → Returns current environment state

---

## 👀 Observation Space

The agent receives:

* Email content (text)
* Metadata (sender, timestamp)
* Inbox summary
* Overwhelm Score

---

## ⚡ Action Space

The agent can:

* Classify emotion → angry / neutral / positive
* Assign priority → high / medium / low
* Decide action → reply / schedule / ignore

---

## 🎯 Reward System

### ✅ Rewards

* Correct emotion detection → +0.3
* Correct prioritization → +0.5
* Correct action → +0.7

### ❌ Penalties

* Ignoring urgent email → -1.0
* Wrong emotional classification → -0.8
* Poor decision → -0.5

---

## 🧩 Tasks

### 😌 Easy — Emotion & Urgency Classification

Identify tone and urgency.
Scored using accuracy (0.0–1.0)

---

### 😐 Medium — Email Prioritization

Rank emails based on importance.
Evaluated against ideal ranking.

---

### 😤 Hard — Action Recommendation

Decide best action for each email.
Tests contextual and emotional reasoning.

---

## 🤖 Baseline Performance

Run the baseline agent:

python3 baseline.py

Example output:
Baseline Score: 0.77

---

## 🐳 Deployment

This project is containerized and runs on Hugging Face Spaces.

To run locally:

docker build -t ai-inbox .
docker run ai-inbox

---

## 📦 Installation

pip install -r requirements.txt

---

## 📁 Project Structure

```
ai-inbox-openenv/
│
├── env.py
├── models.py
├── baseline.py
├── tasks/
├── data/
├── openenv.yaml
├── Dockerfile
└── README.md
```

---

## 🧠 Why This Matters

Most AI environments focus on games or static tasks.

This project focuses on:

* Human behavior
* Emotional intelligence
* Decision-making under stress

---

## 🏁 Conclusion

This environment provides a realistic benchmark to evaluate how AI agents:

* Understand people
* Manage priorities
* Reduce cognitive load

---

## ✨ Future Improvements

* Multi-user inbox simulation
* Dynamic email generation
* Advanced emotional modeling

---

## 🤝 Acknowledgements

Built for the Meta x Hugging Face OpenEnv Hackathon.

Commit directly to the
main
branch
Open as a pull request to the
main
branch
Commit changes
Upload images, audio, and videos by dragging in the text input, pasting, or clicking here.# ai-inbox-openenv
