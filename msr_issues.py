import logging
from github import RateLimitExceededException
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pyplot as figure
import utils 
import matplotlib.dates as mdates

def get_issues(repo,lookback_date, cache=True):
    issues = repo.get_issues(since=lookback_date)
    logging.info("getting %d issues since %s", issues.totalCount, lookback_date)
    issue_list=[]

    for issue in issues: 
        issue_list.append(
            {"state": issue.state,
             "labels": issue.labels,
             "assignees": issue.assignees,
             "comments": issue.comments,
             "closed_at": issue.closed_at,
             "created_at": issue.created_at,
             "locked": issue.locked
             })
    return utils.convert_df(issue_list,repo.name,cache)

def analyze_issues(issues:pd.DataFrame):
    pd.to_datetime(issues['created_at'])
    
    start_date = issues['created_at'].min().date()
    end_date = issues['created_at'].max().date()
    date_range = pd.date_range(start=start_date, end=end_date, freq='m')

    plt.figure(figsize=(10, 5))
    plt.title('Issues Opened By Date Range')

    plt.hist(issues['created_at'], bins=date_range, align = "right")
    #plt.bar(date_range, issues['created_at'], align= "right")
    
    plt.xticks(rotation=45, ha='center', ticks=date_range, labels = date_range)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

    plt.show()
