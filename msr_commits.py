import logging
from github import RateLimitExceededException
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pyplot as figure

# NOTES
# Returning full commit history requries around 1000 request. May want to build in some checking for rate limits and ways to manage that. 

def get_commits(repo, lookback_date=datetime(2000,1,1,0,0), save=True):
    """This is the public function used to get commits for the given repo.

    Args:
        repo (github.Repository.Repository): The repository to get the commits from
        lookback_date (datetime.datetime, optional): Lookback date and time to gather commits. Defaults to Jan 1, 2000.
        save (bool, optional): Whether or not the output should be saved to a csv file. Defaults to True.

    Returns:
        pandas.DataFrame: Pandas dataframe containing all of the data gathered.
    """
    commits = repo.get_commits(since=lookback_date)
    logging.info("Getting %d commits since %s", commits.totalCount, lookback_date)
    commit_list = []
    for commit in commits:
        try:
            commit_list.append(
                {"commit_ID": commit.sha,
                 "commit_date": commit.commit.author.date,
                 "commit_url": commit.html_url
                 })
        except RateLimitExceededException as rate:
            logging.critical('RATE LIMIT EXCEEDED at Commit %d\n Last Commit Date: %s\n%s', len(commit_list), commit_list[0].commit_date, rate)
        except Exception as e:
            logging.error('%s\nException while adding commit URL: %s', e, commit.url)
    
    return convert_df(commit_list, repo.name, save)


def convert_df(list, repo_name, save):
    """Private function that converts data to dataframe and saves if indicated.

    Args:
        list (dict): The dictrionary of data gathered that is being saved.
        repo_name (string): The string that will will prefix the file
        save (bool): whether or not the data should be saved to a csv or just converted to df.

    Returns:
        pandas.DataFrame: The input list of dicts converted to a DataFrame.
    """
    df = pd.DataFrame(list)
    file_name = './{name}_commit_data.csv'.format(name = repo_name)
    print(df)


    
    # if save:
    #     df.to_csv(file_name)

    plt.scatter(df.commit_date, df.commit_ID, alpha=0.25)
    #[plt.text(x=['commit_date'], y=['commit_ID'], s=['commit_url'])]

    plt.xlabel('Commit Date Timeline')
    plt.ylabel('Commit ID')
    plt.title('Commit Timeline')
    plt.show()    
    return df

    

