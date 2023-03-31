import logging
from github import RateLimitExceededException
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pyplot as figure
import utils 

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