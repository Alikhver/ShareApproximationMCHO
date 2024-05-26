import numpy as np
import pandas as pd

# Function to read data from CSV file
def read_data(filename):
    data = pd.read_csv(filename, parse_dates=['Date'])
    return data

# File name
filename = 'KER.PA 25.05.2019-2025.csv'

# Read asset data
data = read_data(filename)

# Ensure data is sorted by date
data = data.sort_values('Date')

# Generate dummy market data (in practice, use real market index data)
np.random.seed(0)  # For reproducibility
data['Market_Adj_Close'] = data['Adj Close'] * (1 + 0.001 * np.random.randn(len(data)))

# Calculate daily returns
data['Asset_Returns'] = data['Adj Close'].pct_change().dropna()
data['Market_Returns'] = data['Market_Adj_Close'].pct_change().dropna()

# Drop NA values after calculating returns
data = data.dropna(subset=['Asset_Returns', 'Market_Returns'])

# Calculate the covariance matrix
cov_matrix = np.cov(data['Asset_Returns'], data['Market_Returns'])

# Extract the covariance of asset and market returns
cov_asset_market = cov_matrix[0, 1]

# Extract the variance of market returns
var_market = cov_matrix[1, 1]

# Calculate beta
beta = cov_asset_market / var_market

print(f'Beta: {beta}')
