from src.metrics import binary_iou, classification_accuracy, precision_recall


def test_accuracy():
    acc = classification_accuracy(["a", "b", "c"], ["a", "x", "c"])
    assert abs(acc - (2 / 3)) < 1e-9


def test_iou():
    iou = binary_iou([1, 0, 1, 0], [1, 1, 1, 0], positive=1)
    assert abs(iou - (2 / 3)) < 1e-9


def test_precision_recall():
    p, r = precision_recall([1, 0, 1, 0], [1, 1, 1, 0], positive=1)
    assert abs(p - (2 / 3)) < 1e-9
    assert abs(r - 1.0) < 1e-9
