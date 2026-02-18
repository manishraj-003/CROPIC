import csv
from pathlib import Path

def classification_accuracy(y_true: list[str], y_pred: list[str]) -> float:
    if not y_true:
        return 0.0
    return sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true)


def binary_iou(y_true: list[int], y_pred: list[int], positive: int = 1) -> float:
    if not y_true:
        return 0.0
    intersection = sum(1 for a, b in zip(y_true, y_pred) if a == positive and b == positive)
    union = sum(1 for a, b in zip(y_true, y_pred) if a == positive or b == positive)
    return (intersection / union) if union else 1.0


def precision_recall(y_true: list[int], y_pred: list[int], positive: int = 1) -> tuple[float, float]:
    tp = sum(1 for a, b in zip(y_true, y_pred) if a == positive and b == positive)
    fp = sum(1 for a, b in zip(y_true, y_pred) if a != positive and b == positive)
    fn = sum(1 for a, b in zip(y_true, y_pred) if a == positive and b != positive)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return precision, recall


CLASSIFICATION_CSV = Path("docs/execution/classification_eval.csv")
SEGMENTATION_CSV = Path("docs/execution/segmentation_eval.csv")
FRAUD_CSV = Path("docs/execution/fraud_eval.csv")
OUT = Path("docs/execution/success_metrics_report.txt")


def load_pairs(path: Path, y_true_col: str, y_pred_col: str) -> tuple[list, list]:
    if not path.exists():
        return [], []
    y_true, y_pred = [], []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            y_true.append(row[y_true_col])
            y_pred.append(row[y_pred_col])
    return y_true, y_pred


def main() -> None:
    class_true, class_pred = load_pairs(CLASSIFICATION_CSV, "true_label", "pred_label")
    seg_true_str, seg_pred_str = load_pairs(SEGMENTATION_CSV, "true_mask_bin", "pred_mask_bin")
    fraud_true_str, fraud_pred_str = load_pairs(FRAUD_CSV, "true_flag", "pred_flag")

    class_acc = classification_accuracy(class_true, class_pred) if class_true else 0.0
    seg_true = [int(x) for x in seg_true_str] if seg_true_str else []
    seg_pred = [int(x) for x in seg_pred_str] if seg_pred_str else []
    seg_iou = binary_iou(seg_true, seg_pred, positive=1) if seg_true else 0.0

    fraud_true = [int(x) for x in fraud_true_str] if fraud_true_str else []
    fraud_pred = [int(x) for x in fraud_pred_str] if fraud_pred_str else []
    precision, recall = precision_recall(fraud_true, fraud_pred, positive=1) if fraud_true else (0.0, 0.0)

    lines = [
        "Success Metrics Report",
        "======================",
        f"classification_accuracy={class_acc:.4f}",
        f"segmentation_iou={seg_iou:.4f}",
        f"fraud_precision={precision:.4f}",
        f"fraud_recall={recall:.4f}",
        f"classification_target_met={class_acc >= 0.85}",
        f"segmentation_target_met={seg_iou >= 0.80}",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
