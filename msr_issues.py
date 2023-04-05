import logging
from github import RateLimitExceededException
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pyplot as figure
import utils
import matplotlib.dates as mdates


def get_issues(repo, lookback_date, cache=True):
    if cache:
        data, lookback_date = utils.load_cache(
            repo.name, "issue", lookback_date, "last_update")
    else:
        data = pd.DataFrame()
    issues = repo.get_issues(since=lookback_date)
    logging.info("getting %d issues since %s",
                 issues.totalCount, lookback_date)
    issue_list = []

    for issue in issues:
        # TODO add checking to update issues already in the cached data
        try:
            issue_list.append(
                {
                    "id": issue.id,
                    "state": issue.state,
                    "labels": issue.labels,
                    "assignees": issue.assignees,
                    "comments": issue.comments,
                    "closed_at": issue.closed_at,
                    "created_at": issue.created_at,
                    "locked": issue.locked,
                    "last_update": issue.updated_at})
        except RateLimitExceededException as rate:
            logging.critical(
                f'RATE LIMIT EXCEEDED at Issue {issue.id} Last Updated date: {issue.updated_at}')

    new_data = utils.convert_df(issue_list, "issue")
    if not data.empty:
        pd.concat([data, new_data])
    else:
        data = new_data
    if cache:
        utils.cache(data, repo.name)

    return data


def analyze(issues: pd.DataFrame):
    issues['created_at'] = pd.to_datetime(issues['created_at'])

    start_date = issues['created_at'].min().date()
    end_date = issues['created_at'].max().date()
    date_range = pd.date_range(start=start_date, end=end_date, freq='m')

    plt.figure(figsize=(10, 5))
    plt.title('Issues Opened By Date Range')

    plt.hist(issues['created_at'], bins=date_range, align="right")
    # plt.bar(date_range, issues['created_at'], align= "right")

    plt.xticks(rotation=45, ha='center', ticks=date_range, labels=date_range)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

    # plt.show()
