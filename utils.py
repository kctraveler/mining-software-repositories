import os
import shutil
import pandas as pd
import logging

CACHE_DIR = os.path.join(os.getcwd(), "/cache")


def create_cache(repo_name, data_type, df: pd.DataFrame):
    try:
        repo_cache_dir = os.path.join(CACHE_DIR, "/", repo_name)
        os.mkdir(repo_cache_dir)
        return repo_cache_dir
    except FileExistsError:
        None
    df.to_csv(os.path.join(repo_cache_dir, "/", data_type, ".csv"))


def load_cache(repo_name, data_type):
    try:
        cache_file_path = "%s/%s/%s.csv".format(
            CACHE_DIR, repo_name, data_type)
        data = pd.read_csv(cache_file_path, parse_dates=True)
        return data
    except OSError:
        logging.error("Unable to load cache file")
        return None


def delete_cache(repo_name, data_type="ALL"):
    try:
        if (data_type == "ALL"):
            cache_file_path = "%s/%s".format(CACHE_DIR, repo_name)
            shutil.rmtree(cache_file_path)
        else:
            cache_file_path = "%s/%s/%s.csv".format(
                CACHE_DIR, repo_name, data_type)
            os.remove(cache_file_path)
    except OSError:
        logging.warn("Cache file could not be removed")


def get_last_entry_dttm(pd_cache: pd.DataFrame, date_index=1):
    pd_cache.sort_values(by=[date_index])
    return pd_cache.max(axis=[1])
