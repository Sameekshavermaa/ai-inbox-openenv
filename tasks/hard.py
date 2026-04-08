def grade(action, email):
    if email["priority"] == "high" and action == "reply":
        score = 0.95
    elif email["priority"] == "low" and action == "ignore":
        score = 0.95
    elif email["priority"] == "medium":
        score = 0.5
    else:
        score = 0.05
    return score

task = {
    "name": "hard",
    "description": "Action recommendation under cognitive load",
    "grader": grade,
}
