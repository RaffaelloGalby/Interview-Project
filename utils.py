import pandas as pd 

def reorder_columns(df, perm):
    """Take a dataframe and permute columns elements by the permutation perm"""
    assert all(isinstance(i, int) for i in perm), "Order list permutation elements are not intergers"
    assert min(perm) == 0, "Permutation min element is different from 0"

    cols = df.columns.tolist()
    assert len(perm) == len(cols), f"Permutation length different from {len(cols)} columns in dataframe"
    assert max(perm) == len(cols) - 1, "Permutation max element is different from len(cols) - 1"

    new_cols = [''] * len(cols)
    for i, idx in enumerate(perm) :
        new_cols[idx] = cols[i]

    return df.reindex(columns = new_cols)
