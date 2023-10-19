from typing import List

import pandas as pd

from trn10_table_football.constants import DEFAULT_MATCHES_FILE_PATH
from trn10_table_football.utils import setup_logger


logger = setup_logger(__name__)


def load_matches(path: str = DEFAULT_MATCHES_FILE_PATH) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        logger.warn(e)
        return None


def save_matches(matches: pd.DataFrame, path: str = DEFAULT_MATCHES_FILE_PATH):
    matches.to_csv(path, index=False)
