
# ==========================================
# HEALTHCARE DATA ANALYSIS
# Phase 3: Data Understanding & Quality
# ==========================================

import pandas as pd
import numpy as np

# Load healthcare dataset
df = pd.read_csv("data/healthcare_data.csv")

print("=" * 50)
print("HEALTHCARE DATA QUALITY ANALYSIS")
print("=" * 50)

# 1. Dataset dimensions
print("\n1. DATASET DIMENSIONS")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Missing values
print("\n2. MISSING VALUE ANALYSIS")
missing_values = df.isnull().sum()

print(missing_values[missing_values > 0])

if missing_values.sum() == 0:
    print("No missing values found!")

# 3. Duplicate records
print("\n3. DUPLICATE ANALYSIS")
duplicates = df.duplicated().sum()

print("Duplicate records:", duplicates)

# 4. Data types
print("\n4. DATA TYPES")
print(df.dtypes)

# 5. Statistical summary
print("\n5. STATISTICAL SUMMARY")
print(df.describe().T)

# 6. Unique values
print("\n6. UNIQUE VALUES")
for column in df.columns:
    print(f"{column}: {df[column].nunique()} unique values")

# 7. Diabetes distribution
print("\n7. DIABETES DISTRIBUTION")

diabetes_counts = df["Diabetes_binary"].value_counts().sort_index()

print(diabetes_counts)

print("\nDiabetes Percentage:")
print(
    df["Diabetes_binary"]
    .value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)

print("\nAnalysis completed!")
