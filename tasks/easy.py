def grade(pred, true):
    score = 1.0 if pred == true else 0.0
    # Clamp to strictly (0, 1)
    return max(0.05, min(0.95, score))
