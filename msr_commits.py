from msr_code_size import get_code_size
import pandas as pd
from datetime import datetime
from github import RateLimitExceededException
import logging
import utils
from matplotlib import pyplot as plt


def get_commits(repo, lookback_date: datetime, cache=True, code_size_step_value=20):
    """This is the public function used to get commits for the given repo.

    Args:
        repo (github.Repository.Repository): The repository to get the commits from
        lookback_date (datetime.datetime, optional): Lookback date and time to gather commits. Defaults to Jan 1, 2000.
        save (bool, optional): Whether or not the output should be saved to a csv file. Defaults to True.

    Returns:
        pandas.DataFrame: Pandas dataframe containing all of the data gathered.
    """
    logging.info(cache)
    data, lookback_date = utils.load_cache(
        repo.name, "commit", lookback_date, "commit_date")
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
            if len(commit_list) % code_size_step_value == 0 or len(commit_list) == 1:
                commit_list[-1]["code_size"] = get_code_size(commit)

        except RateLimitExceededException as rate:
            logging.critical('RATE LIMIT EXCEEDED at Commit %d\n Last Commit Date: %s\n%s', len(
                commit_list), commit_list[0].commit_date, rate)

    new_data = utils.convert_df(commit_list, "commit")
    if not data.empty:
        logging.info('data not empty')
        pd.concat([data, new_data])
    else:
        data = new_data
    if cache:
        utils.cache(data, repo.name)
    return data


def analyze(commit_df):
    plt.figure(figsize=(10, 5))
    plt.scatter(commit_df.commit_date, commit_df.commit_ID, alpha=0.25)
    # [plt.text(x=['commit_date'], y=['commit_ID'], s=['commit_url'])]

    plt.xlabel('Commit Date Timeline')
    plt.ylabel('Commit ID')
    plt.title('Commit Timeline')
    plt.show()
