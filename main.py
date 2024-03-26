import pandas as pd
import numpy as np

from portfolio import Portfolio

excel_path = 'Interview Project Input.xlsx'
window = 5
top_n = 3

portfolio = Portfolio(excel_path)
df = portfolio.following_positive_df

print(df.head(30))
