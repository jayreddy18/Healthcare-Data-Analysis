
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

# -------------------------------
# CUSTOM STYLING
# -------------------------------

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------

st.title("🏥 Healthcare Analytics Dashboard")
st.caption("Interactive Diabetes & Health Risk Analysis")

# -------------------------------
# DATA UPLOAD
# -------------------------------

st.sidebar.header("Data Configuration")

uploaded_file = st.sidebar.file_uploader(
    "Upload Healthcare CSV Dataset",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Upload your healthcare CSV dataset to start the dashboard.")
    st.stop()

required_columns = [
    "Diabetes_binary",
    "HighBP",
    "HighChol",
    "BMI",
    "PhysActivity",
    "Age"
]

missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

# -------------------------------
# DATA PREPARATION
# -------------------------------

df = df.copy()

for col in required_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=required_columns)

df["Diabetes_Status"] = df["Diabetes_binary"].map({
    0: "No Diabetes",
    1: "Prediabetes/Diabetes"
})

df["Blood_Pressure"] = df["HighBP"].map({
    0: "Normal",
    1: "High Blood Pressure"
})

df["Cholesterol"] = df["HighChol"].map({
    0: "Normal",
    1: "High Cholesterol"
})

df["Physical_Activity"] = df["PhysActivity"].map({
    0: "Inactive",
    1: "Active"
})

df = df.dropna(subset=["Diabetes_Status"])

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------

st.sidebar.header("Dashboard Filters")

diabetes_filter = st.sidebar.multiselect(
    "Diabetes Status",
    options=df["Diabetes_Status"].unique(),
    default=df["Diabetes_Status"].unique()
)

bp_filter = st.sidebar.multiselect(
    "Blood Pressure",
    options=df["Blood_Pressure"].dropna().unique(),
    default=df["Blood_Pressure"].dropna().unique()
)

chol_filter = st.sidebar.multiselect(
    "Cholesterol",
    options=df["Cholesterol"].dropna().unique(),
    default=df["Cholesterol"].dropna().unique()
)

activity_filter = st.sidebar.multiselect(
    "Physical Activity",
    options=df["Physical_Activity"].dropna().unique(),
    default=df["Physical_Activity"].dropna().unique()
)

min_bmi = float(df["BMI"].min())
max_bmi = float(df["BMI"].max())

bmi_range = st.sidebar.slider(
    "BMI Range",
    min_value=min_bmi,
    max_value=max_bmi,
    value=(min_bmi, max_bmi)
)

filtered_df = df[
    (df["Diabetes_Status"].isin(diabetes_filter)) &
    (df["Blood_Pressure"].isin(bp_filter)) &
    (df["Cholesterol"].isin(chol_filter)) &
    (df["Physical_Activity"].isin(activity_filter)) &
    (df["BMI"].between(*bmi_range))
]

# -------------------------------
# KPI METRICS
# -------------------------------

st.subheader("Healthcare Overview")

total = len(filtered_df)

diabetes_cases = (
    filtered_df["Diabetes_binary"] == 1
).sum()

diabetes_rate = (
    diabetes_cases / total * 100 if total else 0
)

average_bmi = (
    filtered_df["BMI"].mean() if total else 0
)

high_bp_cases = (
    filtered_df["HighBP"] == 1
).sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Patients", f"{total:,}")
c2.metric("Diabetes Cases", f"{diabetes_cases:,}")
c3.metric("Diabetes Rate", f"{diabetes_rate:.2f}%")
c4.metric("Average BMI", f"{average_bmi:.2f}")

st.divider()

if total == 0:
    st.warning("No records match the selected filters.")
    st.stop()

# -------------------------------
# DIABETES DISTRIBUTION
# -------------------------------

st.subheader("1. Diabetes Distribution")

col1, col2 = st.columns(2)

with col1:
    diabetes_counts = filtered_df["Diabetes_Status"].value_counts()

    fig = px.pie(
        values=diabetes_counts.values,
        names=diabetes_counts.index,
        hole=0.55,
        title="Diabetes Status Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
        filtered_df,
        x="BMI",
        color="Diabetes_Status",
        barmode="overlay",
        opacity=0.7,
        title="BMI Distribution by Diabetes Status"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# BLOOD PRESSURE ANALYSIS
# -------------------------------

st.subheader("2. Blood Pressure Analysis")

bp_analysis = (
    pd.crosstab(
        filtered_df["Blood_Pressure"],
        filtered_df["Diabetes_Status"],
        normalize="index"
    ) * 100
).reset_index().melt(
    id_vars="Blood_Pressure",
    var_name="Diabetes Status",
    value_name="Percentage"
)

fig = px.bar(
    bp_analysis,
    x="Blood_Pressure",
    y="Percentage",
    color="Diabetes Status",
    barmode="group",
    title="Diabetes Prevalence by Blood Pressure",
    text_auto=".2f"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# CHOLESTEROL ANALYSIS
# -------------------------------

st.subheader("3. Cholesterol Analysis")

chol_analysis = (
    pd.crosstab(
        filtered_df["Cholesterol"],
        filtered_df["Diabetes_Status"],
        normalize="index"
    ) * 100
).reset_index().melt(
    id_vars="Cholesterol",
    var_name="Diabetes Status",
    value_name="Percentage"
)

fig = px.bar(
    chol_analysis,
    x="Cholesterol",
    y="Percentage",
    color="Diabetes Status",
    barmode="group",
    title="Diabetes Prevalence by Cholesterol",
    text_auto=".2f"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# PHYSICAL ACTIVITY ANALYSIS
# -------------------------------

st.subheader("4. Physical Activity Analysis")

activity_analysis = (
    pd.crosstab(
        filtered_df["Physical_Activity"],
        filtered_df["Diabetes_Status"],
        normalize="index"
    ) * 100
).reset_index().melt(
    id_vars="Physical_Activity",
    var_name="Diabetes Status",
    value_name="Percentage"
)

fig = px.bar(
    activity_analysis,
    x="Physical_Activity",
    y="Percentage",
    color="Diabetes Status",
    barmode="group",
    title="Diabetes Prevalence by Physical Activity",
    text_auto=".2f"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# AGE ANALYSIS
# -------------------------------

st.subheader("5. Age Group Analysis")

age_analysis = (
    filtered_df.groupby("Age")["Diabetes_binary"]
    .mean()
    .mul(100)
    .reset_index(name="Diabetes Percentage")
)

fig = px.line(
    age_analysis,
    x="Age",
    y="Diabetes Percentage",
    markers=True,
    title="Diabetes Prevalence Across Age Groups"
)

fig.update_traces(line=dict(width=3))

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# DATA EXPLORER
# -------------------------------

st.divider()

st.subheader("6. Healthcare Data Explorer")

st.write("Explore the filtered healthcare records.")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=350
)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="healthcare_filtered_data.csv",
    mime="text/csv"
)

# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption(
    "Healthcare Analytics Dashboard | "
    "Built with Python, Streamlit, Pandas and Plotly"
)
