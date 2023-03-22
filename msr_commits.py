import logging
from github import Github
from github import enable_console_debug_logging
import requests
import pandas as pd

# NOTES
# May want to populate the data frame directly for efficiency and skip the JSON style format.
# Need to refactor and find a way to get date that doesn't hit the rate limit. Doesn't seem easy with the current API client or making one request per commit.
# Already slow as is with the API client to retrieve the 30k commits. Worried about rate limit for additional portions.

# This is the public function to be called from the main file.


def get_commits(repo, max=-1):
    commit_list = generate_commit_list(repo, max)
    df = pd.json_normalize(commit_list)
    df.to_csv("./commit-data.csv")  # Move this to main function?
    return df


def generate_commit_list(repo, max=-1):
    commits = repo.get_commits()
    logging.info("Getting %d commits", commits.totalCount)

    commit_list = []
    for commit in commits:
        try:
            # TODO find better way to get dates to avoid rate limits
            # resp = requests.get(commits[0].url)
            # date = resp.json()["commit"]["committer"]["date"]
            commit_list.append(
                {"commit_ID": commit.sha,
                 #  "commit_date": date,
                 "commit_url": commit.html_url
                 }
            )
        except Exception as e:
            logging.critical(e)
            # logging.critical(resp)

        # optional max commits to improve performance
        if len(commit_list) >= max and max != -1:
            return commit_list

    return commit_list
