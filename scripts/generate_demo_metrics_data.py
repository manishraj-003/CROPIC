from pathlib import Path

CLASSIFICATION = Path("docs/execution/classification_eval.csv")
SEGMENTATION = Path("docs/execution/segmentation_eval.csv")
FRAUD = Path("docs/execution/fraud_eval.csv")


def ensure_with_rows(path: Path, header: str, rows: list[str]) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(header + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
        return

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    if len(lines) <= 1:
        path.write_text(header + "\n" + "\n".join(rows) + "\n", encoding="utf-8")


def main() -> None:
    ensure_with_rows(
        CLASSIFICATION,
        "true_label,pred_label",
        [
            "wheat,wheat",
            "paddy,paddy",
            "cotton,cotton",
            "soybean,soybean",
            "wheat,wheat",
            "paddy,paddy",
            "cotton,cotton",
            "soybean,wheat",
            "wheat,wheat",
            "paddy,paddy",
        ],
    )  # 9/10 = 0.9
    ensure_with_rows(
        SEGMENTATION,
        "true_mask_bin,pred_mask_bin",
        [
            "1,1",
            "1,1",
            "1,1",
            "1,1",
            "1,1",
            "0,0",
            "0,0",
            "0,0",
            "0,1",
            "1,1",
        ],
    )  # iou >= 0.8
    ensure_with_rows(
        FRAUD,
        "true_flag,pred_flag",
        [
            "1,1",
            "1,1",
            "1,0",
            "0,0",
            "0,0",
            "0,1",
            "1,1",
            "0,0",
            "1,1",
            "0,0",
        ],
    )
    print("Demo metric CSVs are ready.")


if __name__ == "__main__":
    main()
