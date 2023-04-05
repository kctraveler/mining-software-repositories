from msr_code_size import get_code_size
import pandas as pd
from datetime import datetime
from github import RateLimitExceededException
import logging
import utils
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


def get_commits(repo, lookback_date: datetime, cache=True, code_size_step_value=20):
    """This is the public function used to get commits for the given repo.

    Args:
        repo (github.Repository.Repository): The repository to get the commits from
        lookback_date (datetime.datetime, optional): Lookback date and time to gather commits. Defaults to Jan 1, 2000.
        save (bool, optional): Whether or not the output should be saved to a csv file. Defaults to True.

    Returns:
        pandas.DataFrame: Pandas dataframe containing all of the data gathered.
    """
    if cache:
        data, lookback_date = utils.load_cache(
            repo.name, "commit", lookback_date, "commit_date")
    else:
        data = pd.DataFrame()
    commits = repo.get_commits(since=lookback_date)
    logging.info("Getting %d commits since %s",
                 commits.totalCount, lookback_date)
    commit_list = []
    for commit in commits:
        try:
            commit_list.append(
                {"commit_ID": commit.sha,
                 "commit_date": commit.commit.author.date,
                 "commit_url": commit.html_url,
                 "code_size": None
                 })
            # Always get code size on first commit in case new commits received < 20
            if len(commit_list) % code_size_step_value == 0 or len(commit_list) == 1:
                commit_list[-1]["code_size"] = get_code_size(commit)

        except RateLimitExceededException as rate:
            logging.critical('RATE LIMIT EXCEEDED at Commit %d\n Last Commit Date: %s\n%s', len(
                commit_list), commit_list[0].commit_date, rate)

    new_data = utils.convert_df(commit_list, "commit")
    if not data.empty:
        logging.info('data not empty')
        data = pd.concat([data, new_data])
    else:
        data = new_data
    if cache:
        utils.cache(data, repo.name)
    return data

""" Plot for Commits over Time """
def analyze(commit_df: pd.DataFrame):
    commit_df["commit_date"] = pd.to_datetime(commit_df['commit_date'])
    
    plt.rcParams["figure.autolayout"] = True
    ax = commit_df["commit_date"].hist(bins=20)
    ax.set_title("Commits Over Time(No. Bins equals 20)")
    ax.set_ylabel('Commit Count')
    ax.set_xlabel('Date')
    plt.xticks(rotation=45)
    

    