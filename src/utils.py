import json
from pathlib import Path
from datetime import datetime
from typing import Dict

HISTORY_FILE = Path("output/history.json")
HISTORY_FILE.parent.mkdir(exist_ok=True)


def save_history(entry: Dict) -> None:
    data = []
    if HISTORY_FILE.exists():
        data = json.loads(HISTORY_FILE.read_text())
    data.append(entry)
    HISTORY_FILE.write_text(json.dumps(data, indent=2))
