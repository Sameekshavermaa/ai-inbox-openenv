def grade(action, email):
    if email["priority"] == "high" and action == "reply":
        return 1.0
    elif email["priority"] == "low" and action == "ignore":
        return 1.0
    return 0.0