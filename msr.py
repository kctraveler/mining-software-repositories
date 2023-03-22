import argparse
import logging
import os
from github import Github
from github import enable_console_debug_logging
from dotenv import load_dotenv
from msr_commits import get_commits
from datetime import datetime


def main():
    # Handle command line arguments
    parser = argparse.ArgumentParser(
        description="Extracts data about a GitHub repository",
        prog="Mining Software Repositories")
    parser.add_argument('--repo',
                        action='store',
                        default="scikit-learn/scikit-learn",
                        help="Full repository name: owner/repo")
    parser.add_argument('--loglevel',
                        action='store',
                        default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=getattr(logging, args.loglevel.upper()),
                        format='%(asctime)s %(levelname)s: %(message)s')
    if logging.root.level <= 10:
        enable_console_debug_logging()
        logging.debug("PyGithub logging enabled.")

    # Establish API connection and get Repo
    try:
        load_dotenv()
        gh = Github(os.environ['GITHUB_TOKEN'], per_page=100)
        repo = gh.get_repo(args.repo)
        logging.info(
            "API connection established and repo returned with ID %d", repo.id)
    except KeyError as e:
        raise Exception(
            "Github Token not defined in .env or system enviornment variable") from None
    except Exception as e:
        logging.critical("Error returning repository: %s", e)

    # WARNING limiting on date range during testing to reduce request count and speed up runs
    commits = get_commits(repo, lookback_date=datetime(2023,3,1,0,0)) 
    logging.info("Finished Gathering Commits")
    logging.debug(commits)
    
    # TODO Determine if there is a better way to manage the data coming fromm multiple sources. Potentially look at matplot lib for making visualizations. 


if __name__ == '__main__':
    main()
