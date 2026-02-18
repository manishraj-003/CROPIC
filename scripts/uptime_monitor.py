import time
import requests

BASE = "http://localhost:8000/health"
INTERVAL_SEC = 30
WINDOW = 20
ALERT_THRESHOLD = 0.995


def main() -> None:
    history: list[bool] = []
    while True:
        ok = False
        try:
            r = requests.get(BASE, timeout=3)
            ok = r.status_code == 200
        except Exception:
            ok = False

        history.append(ok)
        if len(history) > WINDOW:
            history.pop(0)

        uptime = sum(history) / len(history)
        print(f"uptime_window={uptime:.4f} samples={len(history)} status={'ok' if ok else 'down'}")

        if len(history) == WINDOW and uptime < ALERT_THRESHOLD:
            print("ALERT: uptime below threshold")

        time.sleep(INTERVAL_SEC)


if __name__ == "__main__":
    main()
