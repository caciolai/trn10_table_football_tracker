import os
import pathlib

import pandas as pd
import s3fs

from trn10_table_football.constants import (DEFAULT_MATCHES_FILE_PATH,
                                            DEFAULT_MATCHES_S3_BUCKET)
from trn10_table_football.utils import setup_logger

logger = setup_logger(__name__)


# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)


def read_data_s3(s3_bucket: str, s3_path: str):
    s3_src = f"s3://{os.path.join(s3_bucket, s3_path)}"
    logger.info(f"Loading data from {s3_src}")
    return pd.read_csv(s3_src)


def write_data_s3(df: pd.DataFrame, s3_bucket: str, s3_path: str):
    s3_dst = f"s3://{os.path.join(s3_bucket, s3_path)}"
    logger.info(f"Writing data to {s3_dst}")
    df.to_csv(s3_dst, index=False)


def load_matches(*args, **kwargs) -> pd.DataFrame:
    df = load_matches_s3(*args, **kwargs)
    if df is None:
        return df

    df["Date"] = pd.to_datetime(df["Date"])
    return df


def load_matches_local(path: str = DEFAULT_MATCHES_FILE_PATH) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        logger.warn(e)
        return None


def load_matches_s3(
    s3_bucket: str = DEFAULT_MATCHES_S3_BUCKET, s3_path: str = DEFAULT_MATCHES_FILE_PATH
) -> pd.DataFrame:
    try:
        df = read_data_s3(s3_bucket, s3_path)
        return df
    except Exception as e:
        logger.warn(e)
        return None


def save_matches(matches: pd.DataFrame, *args, **kwargs):
    save_matches_s3(matches, *args, **kwargs)


def save_matches_s3(
    matches: pd.DataFrame,
    s3_bucket: str = DEFAULT_MATCHES_S3_BUCKET,
    s3_path: str = DEFAULT_MATCHES_FILE_PATH,
):
    try:
        write_data_s3(matches, s3_bucket, s3_path)
    except Exception as e:
        logger.warn(e)


def save_matches_local(matches: pd.DataFrame, path: str = DEFAULT_MATCHES_FILE_PATH):
    if not pathlib.Path(path).parent.exists():
        os.makedirs(pathlib.Path(path).parent)

    matches.to_csv(path, index=False)
