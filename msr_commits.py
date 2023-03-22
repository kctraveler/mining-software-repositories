import logging
from github import Github
from github import enable_console_debug_logging
from dotenv import load_dotenv
import requests

def get_commits(repo, max=None):  
    commits = repo.get_commits() 
    logging.info("Getting Commits got %d commits",commits.totalCount)  
    
    
    commit_list = []
    
    for commit in commits:
        resp = requests.get(commits[0].url)
        date = resp.json()["commit"]["committer"]["date"]
        commit_list.append(
           {"commit_ID": commit.sha,
            "commit_date": date,
            "commit_url": commit.html_url
            }
        )
        
        if len(commit_list)>=max: 
            return commit_list
    
    return commit_list

