import argparse
import logging
import os
from github import Github
from github import enable_console_debug_logging
from dotenv import load_dotenv
from msr_commits import get_commits


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
        gh = Github(os.environ['GITHUB_TOKEN'])
        repo = gh.get_repo(args.repo)
        logging.info(
            "API connection established and repo returned with ID %d", repo.id)
    except KeyError as e:
        raise Exception(
            "Github Token not defined in .env or system enviornment variable") from None
    except Exception as e:
        logging.critical("Error returning repository: %s", e)

    # TODO Define each category of data as its own .py file. Should provide a function that takes the repo object and returns a pandas dataframe
    # EXAMPLE get_issues(repo) would be a function called from a seperate file that returns all the attributes of the issues in a dataframe.
    print(get_commits(repo, 10))
    # TODO Export datframes into excel or sheets
    # Figure out if there is a way to aggregate data into multiple tabs


if __name__ == '__main__':
    main()

