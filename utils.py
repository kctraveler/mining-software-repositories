import os
import shutil
import pandas as pd
import logging
from datetime import datetime

CACHE_DIR = ("./cache")


def convert_df(list, data_type):
    df = pd.DataFrame(list)
    df.index.name = data_type
    return df


def cache(df: pd.DataFrame, repo_name: str):
    out_dir = os.path.join(CACHE_DIR, repo_name)
    file_name = f'{df.index.name}.csv'
    if not os.path.exists(CACHE_DIR):
        logging.info(f"Creating directory {out_dir}")
        os.mkdir(CACHE_DIR)
        os.mkdir(out_dir)
    elif not os.path.exists(out_dir):
        os.mkdir(out_dir)
    df.to_csv(os.path.join(out_dir, file_name))


def load_cache(repo_name: str, data_type: str, lookback_date: datetime, since_key: str):
    try:
        logging.info(f"Loading {data_type} cache")
        cache_file = f'{CACHE_DIR}/{repo_name}/{data_type}.csv'
        df = pd.read_csv(cache_file, index_col=data_type)
        df[since_key] = pd.to_datetime(
            df[since_key], infer_datetime_format=True)
        if df[since_key].min() > lookback_date:
            logging.info(
                f'Cache data invalid for given lookback date, ignoring cache')
            return (pd.DataFrame(), lookback_date)
        else:
            lookback_date = df[since_key].max().to_pydatetime()
            logging.info(
                f"Cache loaded. Setting lookback date to {lookback_date}")
            return (df, lookback_date)
    except FileNotFoundError:
        logging.info(f"{cache_file} not found")
        return (pd.DataFrame(), lookback_date)
