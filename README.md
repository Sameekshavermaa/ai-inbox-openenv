Hugging Face's logo
Hugging Face
Models
Datasets
Spaces
Buckets
new
Docs
Pricing


Spaces:
NeuralAesthetics
/
ai-inbox-openenv


like
0

App
Files
Community
Settings
ai-inbox-openenv/
README.md
Metadata UI
license

title

AI Inbox OpenEnv
sdk


Docker
emoji


+ Add Emoji
colorFrom


blue
colorTo


purple
pinned

thumbnail

No file chosen
short_description


1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
---

title: AI Inbox OpenEnv
emoji: "📩"
colorFrom: blue
colorTo: purple
sdk: docker
---

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
