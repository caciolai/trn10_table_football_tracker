import os
from pathlib import Path
from datetime import datetime, timezone

LOG_FILE = Path(f"/tmp/omega_data_tools_{datetime.now(tz=timezone.utc).isoformat()}.log")

DATA_FOLDER = Path(os.path.abspath(os.path.expanduser(os.curdir))) / "data"
DEFAULT_MATCHES_FILE_PATH = DATA_FOLDER / "matches.csv"
