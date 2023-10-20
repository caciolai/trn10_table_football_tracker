from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path(
    f"/tmp/omega_data_tools_{datetime.now(tz=timezone.utc).isoformat()}.log"
)

DEFAULT_MATCHES_FILE_PATH = "matches.csv"
DEFAULT_MATCHES_S3_BUCKET = "trn10-table-football-tracker"
