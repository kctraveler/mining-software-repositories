import argparse
import logging
import os
from github import Github
from github import enable_console_debug_logging
from dotenv import load_dotenv
from datetime import datetime
import msr_code_size
import msr_commits
import msr_issues
import msr_issue_density
import matplotlib.pyplot as plt


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
                        default="2000-01-01",
                        help="lookback date to analyze")
    parser.add_argument('--ignoreCache',
                        action='store_false',  # Change this back later
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

    # Gather data
    commits = msr_commits.get_commits(repo, lookback_date, ignore_cache)
    issues = msr_issues.get_issues(repo, lookback_date, ignore_cache)

    # Analyze data
    # msr_commits.analyze(commits)
    msr_issues.analyze(issues)
    msr_issue_density.analyze_issue_density(issues, commits)
    msr_code_size.analyze(commits)

    plt.show(block=False)
    while True:
        i = input("Press Enter to close all visualizations and exit...")
        if not i:
            plt.close('all')
            break


if __name__ == '__main__':
    main()
