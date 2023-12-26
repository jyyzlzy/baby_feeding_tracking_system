from typing import Dict
import yaml

REFRESH_RATE_MS = 100.0

def load_config(filepath: str) -> Dict:
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)
    return config
