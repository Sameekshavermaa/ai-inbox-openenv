def grade(pred_ranking, true_ranking):
    correct = sum([p == t for p, t in zip(pred_ranking, true_ranking)])
    score = correct / len(true_ranking)
    return max(0.05, min(0.95, score))

task = {
    "name": "medium",
    "description": "Email prioritization ranking",
    "grader": grade,
}
