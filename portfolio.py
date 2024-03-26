import pandas as pd
import numpy as np

from utils import reorder_columns

class Portfolio : 
    def __init__(self, filename, window=20, top_n=3) :
        df = self.upload_and_format(filename)
        df = self.preprocess(df, window=window)
        self.df = self.concentration_return(df, top_n=top_n)
        self.df = reorder_columns(self.df, [0, 1, 4, 2, 3])
        self.following_positive_df = self.following_positive_df()

    def upload_and_format(self, filename) :  
        """
        Loads and formats PnL and capital data from specified Excel sheets. Dates are set as the DataFrame index,
        and missing capital values are forward-filled to align with daily dates in the dataset.
    
        Parameters:
        - filename: Path to the Excel file containing the 'Interview Project Input' and 'Allocated Capital' sheets.
    
        Returns:
        - DataFrame with PnL data merged with allocated capital data, indexed by date.
        """
        df_pnl = pd.read_excel(filename, sheet_name='Interview Project Input')
        df_capital = pd.read_excel(filename, sheet_name='Allocated Capital') 
        # Convert the 'Date' column in datetime
        df_pnl['Date'] = pd.to_datetime(df_pnl['Date'])
        df_capital['Date'] = pd.to_datetime(df_capital['Date'])

        # Sort the data by Dates
        df_pnl = df_pnl.sort_values(by='Date')
        df_capital = df_capital.sort_values(by='Date')

        # Create a DataFrame of daily dates on the entire range of dates
        all_dates = pd.date_range(start=min(df_pnl['Date'].min(), df_capital['Date'].min()),
                                end=df_pnl['Date'].max(), freq='D')

        # Mix allocated capital with Date 
        df_capital = pd.DataFrame(all_dates, columns=['Date']).merge(df_capital, on='Date', how='left')

        # Use 'forward fill' fill value in allocated Capital
        df_capital.ffill(inplace=True)
        df_pnl = df_pnl.rename(columns={" PnL ": "PnL"}).reset_index(drop=True)

        # Mix the PnL Data with Capital Data
        return pd.merge(df_pnl, df_capital, on='Date', how='left')
    
    def preprocess(self, df, window=20) :
        """
        Prepares the DataFrame by calculating daily returns for each strategy and organizing data into specified window periods.
        Identifies changes in days to segment data accordingly and assigns window indices for grouping data into distinct periods.
        
        Parameters:
        - df: DataFrame containing the loaded and merged PnL and capital data.
        - window: Size of the window for grouping data, in terms of days.
        
        Returns:
        - DataFrame enriched with 'Strat Return', window indices, and start/end dates for each window.
        """
        # Calculate the daily return for each strategy
        df['Strat Return'] = df['PnL'] / df['Capital']

        # Add 1 when a different day
        df['is_different_day'] = df['Date'].diff().astype('int64')
        df['is_different_day'] = df['is_different_day'].where(df['is_different_day'] == 0, 1)
        # Make sure that first row is not counted as difference is (n + 1) - n
        df.at[0, 'is_different_day'] = np.nan

        # Increment for every different day
        idx_day = df['is_different_day'].cumsum()
        df = df.join(idx_day, rsuffix='_sum')
        df.drop(columns="is_different_day", inplace=True)
        df.rename(columns = {"is_different_day_sum" :  "idx_day"}, inplace=True) 

        # Increment for every new window 
        df['window_idx'] = df['idx_day'] // window

        # Replace first nan with 0
        df.at[0, 'window_idx'] = 0.

        # Delete idx_day
        df.drop(columns="idx_day", inplace=True)

        date_start = df.groupby('window_idx')[['Date']].head(1).reset_index(drop=True)
        date_end = df.groupby('window_idx')[['Date']].tail(1).reset_index(drop=True)
        date_start.rename(columns= {'Date' : 'Start Date'}, inplace=True)
        date_end.rename(columns= {'Date' : 'End Date'}, inplace=True)
        df = df.merge(date_start, left_on = ['window_idx'], right_index=True, how='left')
        df = df.merge(date_end, left_on = ['window_idx'], right_index=True, how='left')

        df.drop(columns='Date', inplace=True)

        return df
  
    def concentration_return(self, df, top_n = 3): 
        """
        Calculates the concentration of returns for the top N strategies within each window period. It assesses the contribution
        of the top-performing strategies to the overall returns and computes the concentration metric.
        
        Parameters:
        - df: DataFrame prepared by the preprocess function, containing strategy returns and window indices.
        - top_n: Number of top-performing strategies to consider for calculating return concentration.
        
        Returns:
        - DataFrame with additional columns for the total period return, PnL for top N strategies, and return concentration.
        """
        df_ret = df.groupby(["window_idx"]).agg({'Strat Return': 'sum', 'Capital' : 'mean'})
        # Sum inside a window idx for all strategy pnL and Start return and select only pnl and strat ret
        df = df.groupby(["window_idx", "Strategy"]).agg({'Strat Return': 'sum', 'Start Date' : 'first', 'End Date' : 'first'})
        # Select only positive return 
        df = df.loc[df['Strat Return'] > 0].rename(columns= {'Strat Return': 'Pos Strat Return'})
        # Sort first asc for window idx then desc for strat ret
        df = df.sort_values(['window_idx', 'Pos Strat Return'], ascending=[True, False])
        # Select for each window idx top_n strat 
        df_top = df.groupby(['window_idx']).head(top_n)
        # Sum all strat for every window idx in both df and top_n strat df
        df = df.groupby('window_idx').agg({'Pos Strat Return': 'sum', 'Start Date' : 'first', 'End Date' : 'first'})
        df_top = df_top.groupby('window_idx').agg({'Pos Strat Return': 'sum'})
        # change name 
        df = df.join(df_top, how='left', rsuffix=' top_n')
        df['Concentration'] = df['Pos Strat Return top_n'] / df['Pos Strat Return']
        df.drop(columns=['Pos Strat Return top_n', 'Pos Strat Return'], inplace=True)

        df= df.merge(df_ret, left_on=['window_idx'], right_on=['window_idx'], how='left')
        return df
    
    def following_positive_df(self):
        """
        Identifies periods immediately following those with positive returns. This function is instrumental in analyzing
        the hypothesis that positive return periods are likely followed by negative return periods.
        
        It filters the portfolio data to isolate subsequent periods after positive returns, facilitating further analysis
        on the transition patterns between positive and negative returns.
        
        Returns:
        - DataFrame containing only the periods that follow a positive return period, excluding the last row if it represents
        a positive return without a subsequent period to analyze.
        """
        # Check if the last value in the dataframe represents a positive return
        is_last_value_positive = self.df['Strat Return'].iloc[-1] >= 0
        # Exclude the last row if it's a positive return period since it doesn't have a subsequent period to analyze
        if is_last_value_positive :
            df = self.df.head(-1)
        else :
            df = self.df
            # Find indices where the return is positive
        pos_idx = df.index[df['Strat Return'] > 0]
        # Select rows that immediately follow the identified positive return periods
        # Reset index for cleanliness and ease of further operations
        return self.df.loc[pos_idx + 1].reset_index(drop=True)


    
    

