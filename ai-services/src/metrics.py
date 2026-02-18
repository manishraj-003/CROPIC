def classification_accuracy(y_true: list[str], y_pred: list[str]) -> float:
    if not y_true:
        return 0.0
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return correct / len(y_true)


def binary_iou(y_true: list[int], y_pred: list[int], positive: int = 1) -> float:
    if not y_true:
        return 0.0
    intersection = sum(1 for a, b in zip(y_true, y_pred) if a == positive and b == positive)
    union = sum(1 for a, b in zip(y_true, y_pred) if a == positive or b == positive)
    if union == 0:
        return 1.0
    return intersection / union


def precision_recall(y_true: list[int], y_pred: list[int], positive: int = 1) -> tuple[float, float]:
    tp = sum(1 for a, b in zip(y_true, y_pred) if a == positive and b == positive)
    fp = sum(1 for a, b in zip(y_true, y_pred) if a != positive and b == positive)
    fn = sum(1 for a, b in zip(y_true, y_pred) if a == positive and b != positive)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return precision, recall
