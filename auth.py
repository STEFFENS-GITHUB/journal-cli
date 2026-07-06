import json
import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".journal-cli.conf"

def save_token(token: str) -> None:
    CONFIG_PATH.write_text(json.dumps({"access_token": token}))
    os.chmod(CONFIG_PATH, 0o600)

def load_token() -> str:
    return json.loads(CONFIG_PATH.read_text())["access_token"]

def clear_token() -> None:
    save_token("")
