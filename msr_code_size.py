import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

def get_code_size(commit):
    tree_elements = commit.commit.tree.tree
    tree_size = 0
    for tree_element in tree_elements:
        if tree_element.size:
            tree_size += tree_element.size
    return tree_size

def analyze(commits:pd.DataFrame):
    commits['commit_date'] = pd.to_datetime(commits['commit_date'])
    code_sizes = commits.query("code_size > 0").copy()
    plt.rcParams["figure.autolayout"] = True
    ax = code_sizes.plot(x="commit_date", y="code_size",
                         marker="o", linestyle='none')
    ax.set_ylabel("Code Size kb")
    ax.set_title("Code size over time")


    