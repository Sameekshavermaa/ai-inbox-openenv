def grade(pred_ranking, true_ranking):
    correct = sum([p == t for p, t in zip(pred_ranking, true_ranking)])
    score = correct / len(true_ranking)
    # Clamp to strictly (0, 1)
    return max(0.05, min(0.95, score))
