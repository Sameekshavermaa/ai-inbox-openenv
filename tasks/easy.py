def grade(pred, true):
    score = 1.0 if pred == true else 0.0
    return max(0.05, min(0.95, score))  # ✅ never 0.0 or 1.0

task = {
    "name": "easy",
    "description": "Emotion and urgency classification",
    "grader": grade,
}
