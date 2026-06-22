import json
import os
from datetime import datetime, timezone
from config import LOG_FILE


def log_interaction(question: str, tier: str, response: str) -> None:
    """
    Append a structured record of this interaction to the audit log (LOG_FILE).
    Creates the logs/ directory if it doesn't exist. Prints a one-line summary.
    """
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    entry = {
        "timestamp": timestamp,
        "tier": tier,
        "question": question[:300],
        "response_preview": response[:200],
        "question_length": len(question),
        "response_length": len(response),
    }

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(
        f"[LOGGED] timestamp={timestamp} | tier={tier} | "
        f'question="{question[:50]}{"..." if len(question) > 50 else ""}" | '
        f"question_len={len(question)} | response_preview_len={len(response[:200])}"
    )
