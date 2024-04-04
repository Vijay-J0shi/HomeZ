import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd

dataset = "tests/tracking_sample.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(dataset)

# Remove rows with missing values from 'x' and 'y' columns
df.dropna(subset=['x', 'y'], inplace=True)

# Output the cleaned DataFrame to a new CSV file
df.to_csv('tests/sample.csv', index=False)
