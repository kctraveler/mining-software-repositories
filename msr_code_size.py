def get_code_size(commit):
    tree_elements = commit.commit.tree.tree
    tree_size = 0
    for tree_element in tree_elements:
        if tree_element.size:
            tree_size += tree_element.size
    return tree_size