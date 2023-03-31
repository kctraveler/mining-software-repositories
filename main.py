import argparse
import logging
import os
from github import Github
from github import enable_console_debug_logging
from dotenv import load_dotenv
from msr_commits import get_commits
from msr_code_size import get_code_size
from datetime import datetime
from datetime import date
import msr_issues


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
    parser.add_argument("--lookback",
                        type=lambda d: datetime.strptime(
                            d, '%Y-%m-%d'),
                        default="2023-03-01",
                        help="lookback date to analyze")
    parser.add_argument('--ignoreCache',
                        action='store_false',
                        help="Ignore the cache and pull fresh data")
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=getattr(logging, args.loglevel.upper()),
                        format='%(asctime)s %(levelname)s: %(message)s')
    if logging.root.level <= 10:
        enable_console_debug_logging()
        logging.debug("PyGithub logging enabled.")

    # Save args
    lookback_date = args.lookback
    ignore_cache = args.ignoreCache
    repo_name_full = args.repo
    # Establish API connection and get Repo
    try:
        load_dotenv()
        gh = Github(os.environ['GITHUB_TOKEN'], per_page=100)
        repo = gh.get_repo(repo_name_full)
        logging.info(
            "API connection established and repo returned with ID Rate limit: %s", repo.id)
        logging.info("Rate Limit Details: %s", gh.get_rate_limit().core)
    except KeyError as e:
        raise Exception(
            "Github Token not defined in .env or system enviornment variable") from None
    except Exception as e:
        logging.critical("Error returning repository: %s", e)

    # WARNING limiting on date range during testing to reduce request count and speed up runs
    commits = get_commits(repo, lookback_date, ignore_cache)
    logging.info("Finished Gathering Commits")
    logging.debug(commits)

    # TODO Determine if there is a better way to manage the data coming fromm multiple sources. Potentially look at matplot lib for making visualizations.


if __name__ == '__main__':
    main()
