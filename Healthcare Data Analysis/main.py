

from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np

print("Starting Healthcare Data Analysis...")

# Download CDC Diabetes Health Indicators dataset
print("\nDownloading healthcare dataset...")

dataset = fetch_ucirepo(id=891)

# Extract features and target
X = dataset.data.features
y = dataset.data.targets

# Combine features and target
df = pd.concat([X, y], axis=1)

# Save dataset locally
df.to_csv("data/healthcare_data.csv", index=False)

print("\nDataset downloaded successfully!")

# Display basic information
print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
df.info()

print("\nDataset collection completed!")
