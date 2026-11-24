
# ==========================================
# PHASE 4: EXPLORATORY DATA ANALYSIS
# Healthcare Data Analysis Project
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/healthcare_data.csv")

# Visualization settings
sns.set_theme(style="whitegrid")

print("Starting Exploratory Data Analysis...")

# ------------------------------------------
# 1. DIABETES CATEGORY DISTRIBUTION
# ------------------------------------------

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="Diabetes_binary"
)

plt.title("Distribution of Diabetes Categories")
plt.xlabel("0 = No Diabetes | 1 = Prediabetes or Diabetes")
plt.ylabel("Number of Respondents")

plt.tight_layout()
plt.savefig("visualizations/diabetes_distribution.png")
plt.close()


# ------------------------------------------
# 2. BMI DISTRIBUTION
# ------------------------------------------

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="BMI",
    bins=40,
    kde=True
)

plt.title("BMI Distribution Among Respondents")
plt.xlabel("Body Mass Index (BMI)")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig("visualizations/bmi_distribution.png")
plt.close()


# ------------------------------------------
# 3. HEALTH CATEGORY VS HIGH BLOOD PRESSURE
# ------------------------------------------

bp_analysis = (
    df.groupby("HighBP")["Diabetes_binary"]
    .mean() * 100
)

plt.figure(figsize=(8, 5))

sns.barplot(
    x=bp_analysis.index,
    y=bp_analysis.values
)

plt.title("Prediabetes or Diabetes Category by High Blood Pressure")
plt.xlabel("High Blood Pressure (0 = No, 1 = Yes)")
plt.ylabel("Percentage in Target Category (%)")

plt.tight_layout()
plt.savefig("visualizations/bp_vs_diabetes.png")
plt.close()


# ------------------------------------------
# 4. PRINT ANALYTICAL RESULTS
# ------------------------------------------

print("\nBMI SUMMARY")
print(df["BMI"].describe())

print("\nTarget Category Percentage by High BP")
print(bp_analysis.round(2))

print("\nEDA Completed Successfully!")

