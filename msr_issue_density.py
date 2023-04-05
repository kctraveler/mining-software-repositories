import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


def calc_open_issues(commit_date: pd.Timestamp, issues: pd.DataFrame):
    open_issues = issues.query(
        "created_at <= @commit_date & (closed_at >= @commit_date or state == 'open')")
    return len(open_issues)


def calc_issue_density(code_size: int, issue_count: int):
    return issue_count / code_size


def analyze_issue_density(issues: pd.DataFrame, commits: pd.DataFrame):
    issues['created_at'] = pd.to_datetime(issues['created_at'])
    issues['closed_at'] = pd.to_datetime(issues['closed_at'])
    commits['commit_date'] = pd.to_datetime(commits['commit_date'])
    code_sizes = commits.query("code_size > 0").copy()
    code_sizes['issue_count'] = code_sizes['commit_date'].apply(
        calc_open_issues, args=(issues,))
    code_sizes['issue_density'] = code_sizes.apply(
        lambda row: calc_issue_density(row['code_size'], row['issue_count']), axis=1)
    plt.rcParams["figure.autolayout"] = True
    ax = code_sizes.plot(x="commit_date", y=["issue_density", "code_size"],
                         marker="o", linestyle='none', secondary_y=('code_size'))
    ax.set_ylabel("Defect Density (Issues / Bytes of Code)")
    ax.right_ax.set_ylabel("Code Size (Bytes)")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax.right_ax.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2, bbox_to_anchor=(0.25, -.575))
    ax.set_title("Issue Density and Code Size Over Time")
