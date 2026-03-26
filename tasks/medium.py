def grade(pred_ranking, true_ranking):
    correct = sum([p == t for p, t in zip(pred_ranking, true_ranking)])
    return correct / len(true_ranking)