from datetime import datetime
from pathlib import Path

LOG_FILE = Path("audit.log")


def write_audit(event: str, actor: str, payload: dict) -> None:
    line = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "actor": actor,
        "payload": payload,
    }
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{line}\\n")
