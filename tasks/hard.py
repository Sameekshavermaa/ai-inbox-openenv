def grade(action, email):
    if email["priority"] == "high" and action == "reply":
        score = 0.9
    elif email["priority"] == "low" and action == "ignore":
        score = 0.9
    elif email["priority"] == "medium":
        score = 0.5
    else:
        score = 0.1
    return max(0.05, min(0.95, score))  # ✅ never 0.0 or 1.0

task = {
    "name": "hard",
    "description": "Action recommendation under cognitive load",
    "grader": grade,
}
