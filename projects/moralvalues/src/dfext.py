
import pandas as pd

def reorder_first(self: pd.DataFrame, target_cols) -> pd.DataFrame:
    self = self.loc[:,target_cols].join(other=self.drop(columns=target_cols))
    return self

def reorder_last(self: pd.DataFrame, target_cols) -> pd.DataFrame:
    self = self.drop(columns=target_cols).join(other=self.loc[:,target_cols])
    return self

def reorder_before(self: pd.DataFrame, target_cols, before_col) -> pd.DataFrame:
    cols = self.columns.tolist()[:]
    cols = [c for c in cols if c not in target_cols]
    left_cols = cols[:cols.index(before_col)]
    right_cols = cols[cols.index(before_col):]
    self = self.loc[:,left_cols + target_cols + right_cols]
    return self

def reorder_after(self: pd.DataFrame, target_cols, after_col) -> pd.DataFrame:
    cols = self.columns.tolist()[:]
    cols = [c for c in cols if c not in target_cols]
    left_cols = cols[:cols.index(after_col)+1]
    right_cols = cols[cols.index(after_col)+1:]
    self = self.loc[:,left_cols + target_cols + right_cols]
    return self

pd.DataFrame.reorder_first = reorder_first
pd.DataFrame.reorder_last = reorder_last
pd.DataFrame.reorder_before = reorder_before
pd.DataFrame.reorder_after = reorder_after