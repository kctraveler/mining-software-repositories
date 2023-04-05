import logging
from github import RateLimitExceededException
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pyplot as figure
import utils
import matplotlib.dates as mdates


def get_issues(repo, lookback_date, cache=True):
    bug_labels = ['bug', "Bug"]
    if cache:
        data, lookback_date = utils.load_cache(
            repo.name, "issue", lookback_date, "last_update")
    else:
        data = pd.DataFrame()
    issues = repo.get_issues(
        since=lookback_date, state='all')
    logging.info("getting %d issues since %s",
                 issues.totalCount, lookback_date)
    issue_list = []
    for issue in issues:
        # TODO add checking to update issues already in the cached data
        try:
            is_bug = False
            for label in issue.labels:
                if label.name in bug_labels:
                    is_bug = True
                    break
            if is_bug:
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
    issues_count = pd.DataFrame()
    issues_count['created_at'] = pd.to_datetime(issues['created_at']).copy()
    plt.rcParams["figure.autolayout"] = True
    ax = issues_count["created_at"].hist(bins=20)
    ax.set_title("Issues Labeled as Bugs Opened Over Time")
    ax.set_ylabel("Issue/Bug Count")
    ax.set_xlabel("Created Date")
    plt.xticks(rotation=45)

    # start_date = issues['created_at'].min().date()
    # end_date = issues['created_at'].max().date()
    # date_range = pd.date_range(start=start_date, end=end_date, freq='m')

    # plt.figure(figsize=(10, 5))
    # plt.title('Issues Opened By Date Range')

    # plt.hist(issues['created_at'], bins=date_range, align="right")
    # # plt.bar(date_range, issues['created_at'], align= "right")

    # plt.xticks(rotation=45, ha='center', ticks=date_range, labels=date_range)
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

def analyze_tat(issues: pd.DataFrame):
    # TODO Consider plots with number assignees could do a bar graph by label as well
    issue_tat = issues.query("state == 'closed'").copy(deep=True)
    issue_tat['created_at'] = pd.to_datetime(issue_tat['created_at']).copy()
    issue_tat['closed_at'] = pd.to_datetime(issue_tat['closed_at']).copy()
    issue_tat['time_open'] = (issue_tat['closed_at'] - issue_tat['created_at']).astype('timedelta64[D]')
    ax = issue_tat.plot(x="comments", y="time_open", marker='o', linestyle='none')
    ax.set_xlabel("Number of Comments")
    ax.set_ylabel("Issue TaT (Days)")
    ax.set_title("Closed Issues/Bugs Turnaround vs Number of Comments")