# Portfolio Strategy Analysis

## Overview
This repository contains the Python code for analyzing portfolio performance, focusing on the concentration of returns from top-performing strategies within specified window periods and examining the transitions between periods of positive and negative returns-considering consitent allocated capital. This repositery contains also an "alternative research draft" of the project in the "Bonus" Part, focusing on the daily adjusted capital based on the PnL.

Here is the link of the GitHub repository:


## Available Files in the repository
"portfolio.py" : The "portfolio.py" file serves as the central module housing all the methods for portfolio performance analysis and data processing.

"notebook report.ipynb" : The "notebook report.ipynb" is an interactive Jupyter Notebook offering a detailed walkthrough and visual exploration of the portfolio analysis process and findings.

"main.py" : The main script initializes the portfolio analysis with specific parameters and displays the first 30 entries of periods following positive returns.

"utils.py" : The util file provides a utility function to reorder DataFrame columns based on a specified permutation pattern.

"DataFrame_result.xlsx" : The "Interview Project Input.xlsx" Excel file contains the foundational data for computing the DataFrame results, organized by specified window periods and top N strategy performance metrics.

"Interview Project Input.xlsx": The "Interview Project Input.xlsx" is the original input file containing the initial data set for the portfolio performance analysis.

"Bonus alternative method Research.ipynd": The "Bonus alternative method Research.ipynb" notebook investigates the impact of daily adjusted capital on cumulative returns, offering an exploratory analysis into alternative portfolio evaluation strategies. This part is not include in the rest of the project and standby itself. It has to be considered independantly.

"Bonus_Positive_Return_Period.xlsx": The "Bonus_Positive_Return_Period.xlsx" serves as the output from the "Bonus alternative method Research.ipynb" notebook, encapsulating the results of exploring daily adjusted capital and cumulative returns.

## Features
-**Data Loading and Formatting**: Automates the process of reading PnL and capital allocation data from an Excel file and prepares it for detailed analysis.
-**Preprocessing Workflow**: Calculates daily strategy returns, organizes data into user-defined window periods, and delineates each window's start and end dates for focused analysis.
-**Return Concentration Analysis**: Determines the impact of top-performing strategies on the portfolio's overall returns within each window, quantifying the concentration of returns.
-**Post-Positive Return Analysis**: Isolates periods following positive returns to scrutinize the portfolio's subsequent performance dynamics, testing the hypothesis that positive returns often precede negative ones.

## Requirements
- Python 3.8+
- Pandas
- Numpy
- An Excel workbook containing the input data in two sheets: "Strategy PnL" and "Allocated Capital".


## Getting Started
1. **Prepare Your Data**: Place your Excel workbook in a known directory. The workbook should contain:
   - A sheet named "Strategy PnL" with the P&L time series data for the strategies.
   - A sheet named "Allocated Capital" with the time series data of the portfolio's allocated capital.

2. **Running the Analysis**:
   - Update the `excel_path` variable in the script to point to your Excel workbook.
   - Run the script to perform the analysis. Adjust the `window` and `top_n` parameters as needed for different analyses.


## Class and Functions
The Portfolio class encompasses several key methods for portfolio performance analysis, focusing on return concentration and the analysis of periods following positive returns.

## Portfolio Class
- **`__init__(filename, window=20, top_n=3)`**: Initializes the portfolio analysis by loading data, preprocessing, calculating concentration returns, and identifying periods following positive returns.
Methods

## Methods
- **`upload_and_format(filename)`**: Loads PnL and capital allocation data from an Excel file, sets the date as the DataFrame index, and forward-fills missing capital data to prepare for analysis.

- **`preprocess(df, window=20)`**: Prepares the dataset by calculating daily returns for each strategy and organizing data into specified window periods based on business days, enhancing the data structure for subsequent analytical steps.

- **`concentration_return(df, top_n=3)`**: Calculates the concentration of returns for the top N strategies within each window period, quantifying the impact of top-performing strategies on the overall portfolio returns and highlighting the distribution of strategy effectiveness.

- **`following_positive_df()`**: Identifies periods immediately following a positive return window, facilitating an investigation into the behavior of the portfolio's returns in successive periods and testing the hypothesis regarding the transition from positive to negative returns.

Each function is designed to be modular, allowing for flexible application to various datasets and analytical requirements while ensuring clarity and efficiency in portfolio performance evaluation.

## Output
The output is an Excel file, Dataframe_Result.xlsx, which encapsulates the comprehensive results of the portfolio performance evaluation. This file includes detailed insights into the return concentration across different periods, and strategy performance metrics.

## Analysis
For a dive into the interpretive analysis, refer to the Jupyter Notebook 'notebook report.ipynb'. This notebook provides a step-by-step walkthrough of the analysis process, from data loading and preprocessing to detailed exploration of return concentration and the examination of return patterns following positive periods.

