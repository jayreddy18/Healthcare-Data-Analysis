
# ==================================================
# PHASE 5: ADVANCED HEALTHCARE DATA ANALYSIS
# ==================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/healthcare_data.csv")

sns.set_theme(style="whitegrid")

# Create output folder if needed
import os
os.makedirs("visualizations", exist_ok=True)

# Target definition:
# 0 = No diabetes
# 1 = Prediabetes or diabetes

print("=" * 55)
print("ADVANCED HEALTHCARE DATA ANALYSIS")
print("=" * 55)


# --------------------------------------------------
# 1. HIGH BLOOD PRESSURE ANALYSIS
# --------------------------------------------------

print("\n1. HIGH BLOOD PRESSURE ANALYSIS")

bp_result = pd.crosstab(
    df["HighBP"],
    df["Diabetes_binary"],
    normalize="index"
) * 100

bp_result.columns = ["No diabetes", "Prediabetes/Diabetes"]

print(bp_result.round(2))

bp_result.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Target Category by High Blood Pressure")
plt.xlabel("High Blood Pressure (0 = No, 1 = Yes)")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=0)
plt.legend(title="Target category")
plt.tight_layout()
plt.savefig("visualizations/bp_analysis.png")
plt.close()


# --------------------------------------------------
# 2. HIGH CHOLESTEROL ANALYSIS
# --------------------------------------------------

print("\n2. HIGH CHOLESTEROL ANALYSIS")

chol_result = pd.crosstab(
    df["HighChol"],
    df["Diabetes_binary"],
    normalize="index"
) * 100

chol_result.columns = ["No diabetes", "Prediabetes/Diabetes"]

print(chol_result.round(2))

chol_result.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Target Category by High Cholesterol")
plt.xlabel("High Cholesterol (0 = No, 1 = Yes)")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=0)
plt.legend(title="Target category")
plt.tight_layout()
plt.savefig("visualizations/cholesterol_analysis.png")
plt.close()


# --------------------------------------------------
# 3. BMI ANALYSIS
# --------------------------------------------------

print("\n3. BMI ANALYSIS")

bmi_result = df.groupby("Diabetes_binary")["BMI"].agg(
    ["mean", "median", "min", "max", "count"]
)

bmi_result.index = ["No diabetes", "Prediabetes/Diabetes"]

print(bmi_result.round(2))

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Diabetes_binary",
    y="BMI"
)

plt.title("BMI Comparison Across Target Categories")
plt.xlabel("0 = No diabetes, 1 = Prediabetes/Diabetes")
plt.ylabel("BMI")

plt.tight_layout()
plt.savefig("visualizations/bmi_comparison.png")
plt.close()


# --------------------------------------------------
# 4. PHYSICAL ACTIVITY ANALYSIS
# --------------------------------------------------

print("\n4. PHYSICAL ACTIVITY ANALYSIS")

activity_result = pd.crosstab(
    df["PhysActivity"],
    df["Diabetes_binary"],
    normalize="index"
) * 100

activity_result.columns = ["No diabetes", "Prediabetes/Diabetes"]

print(activity_result.round(2))

activity_result.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Target Category by Physical Activity")
plt.xlabel("Physical Activity (0 = No, 1 = Yes)")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=0)
plt.legend(title="Target category")
plt.tight_layout()
plt.savefig("visualizations/activity_analysis.png")
plt.close()


# --------------------------------------------------
# 5. AGE GROUP ANALYSIS
# --------------------------------------------------

print("\n5. AGE GROUP ANALYSIS")

age_result = (
    df.groupby("Age")["Diabetes_binary"]
    .mean() * 100
)

print(age_result.round(2))

plt.figure(figsize=(10, 5))

sns.barplot(
    x=age_result.index,
    y=age_result.values
)

plt.title("Prediabetes/Diabetes Category by Age Group")
plt.xlabel("Age Group Code")
plt.ylabel("Percentage (%)")

plt.tight_layout()
plt.savefig("visualizations/age_analysis.png")
plt.close()


# --------------------------------------------------
# FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 55)
print("ADVANCED ANALYSIS COMPLETED SUCCESSFULLY!")
print("Five analyses and five charts generated.")
print("=" * 55)
