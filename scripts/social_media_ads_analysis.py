# ============================================================
# SOCIAL MEDIA ADVERTISING DATASET — ANALYTICS STRUCTURE
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ── Plotting defaults ──────────────────────────────────────
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)


# ============================================================
# 1. DATA LOADING
# ── Purpose: Bring raw data into memory and get a first look.
# ============================================================

df = pd.read_csv("social_media_ads.csv")

print(df.head())          # first 5 rows
print(df.tail())          # last 5 rows
print(df.shape)           # (rows, columns)
print(df.columns.tolist()) # column names


# ============================================================
# 2. DATA OVERVIEW & SCHEMA INSPECTION
# ── Purpose: Understand column types, memory usage, and
#    the overall structure before touching the data.
# ============================================================

print(df.info())          # dtypes + non-null counts
print(df.dtypes)          # column-by-column type summary
print(df.memory_usage(deep=True))  # memory footprint


# ============================================================
# 3. DESCRIPTIVE STATISTICS
# ── Purpose: Summarise central tendency, spread, and range
#    for every numeric (and optional categorical) column.
# ============================================================

print(df.describe())                          # numeric columns
print(df.describe(include="object"))          # categorical columns
print(df.describe(include="all"))             # everything at once

# Per-column value counts (useful for low-cardinality columns)
for col in df.select_dtypes("object").columns:
    print(f"\n{col}:\n", df[col].value_counts())


# ============================================================
# 4. MISSING VALUE ANALYSIS
# ── Purpose: Identify gaps in the data and decide on a
#    strategy (drop, impute, or flag) before modelling.
# ============================================================

missing_count = df.isnull().sum()
missing_pct   = (df.isnull().sum() / len(df)) * 100
missing_df    = pd.DataFrame({"count": missing_count, "pct": missing_pct})
print(missing_df[missing_df["count"] > 0].sort_values("pct", ascending=False))

# Heatmap for a visual overview
plt.figure(figsize=(14, 5))
sns.heatmap(df.isnull(), cbar=False, cmap="viridis", yticklabels=False)
plt.title("Missing Value Map")
plt.tight_layout()
plt.show()


# ============================================================
# 5. DATA CLEANING
# ── Purpose: Fix or remove problems found in steps 3–4 so
#    all subsequent analysis is based on reliable data.
# ============================================================

# 5a. Drop duplicate rows
df = df.drop_duplicates()

# 5b. Handle missing values
df["Age"].fillna(df["Age"].median(), inplace=True)          # numeric → median
df["Gender"].fillna(df["Gender"].mode()[0], inplace=True)   # categorical → mode
df.dropna(subset=["Clicked on Ad"], inplace=True)           # target must exist

# 5c. Correct data types
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Age"]       = df["Age"].astype(int)

# 5d. Strip / standardise string columns
df["Gender"] = df["Gender"].str.strip().str.title()

# 5e. Rename columns for convenience
df.columns = df.columns.str.lower().str.replace(" ", "_")

print("Clean shape:", df.shape)


# ============================================================
# 6. FEATURE ENGINEERING
# ── Purpose: Derive new variables that may carry predictive
#    signal not available in the raw columns.
# ============================================================

# Extract temporal features from the timestamp
df["hour"]      = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()
df["month"]     = df["timestamp"].dt.month

# Age bucketing
df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 25, 35, 45, 60, 100],
    labels=["18-25", "26-35", "36-45", "46-60", "60+"]
)

# Interaction ratio (example derived metric)
df["daily_time_per_site"] = df["daily_time_spent_on_site"] / (df["daily_internet_usage"] + 1)

print(df[["hour", "day_of_week", "age_group", "daily_time_per_site"]].head())


# ============================================================
# 7. EXPLORATORY DATA ANALYSIS (EDA)
# ── Purpose: Uncover distributions, relationships, and
#    patterns that guide modelling decisions.
# ============================================================

# 7a. Target variable distribution
df["clicked_on_ad"].value_counts(normalize=True).plot(kind="bar", color=["steelblue", "salmon"])
plt.title("Click Rate (Clicked on Ad)")
plt.ylabel("Proportion")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 7b. Numeric feature distributions
df.select_dtypes("number").hist(bins=30, figsize=(16, 10), color="steelblue", edgecolor="white")
plt.suptitle("Numeric Feature Distributions", y=1.02)
plt.tight_layout()
plt.show()

# 7c. Categorical breakdowns vs target
for col in ["gender", "age_group", "day_of_week"]:
    ct = pd.crosstab(df[col], df["clicked_on_ad"], normalize="index")
    ct.plot(kind="bar", stacked=True, figsize=(10, 4))
    plt.title(f"Click Rate by {col.title()}")
    plt.ylabel("Proportion")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# 7d. Correlation heatmap
plt.figure(figsize=(12, 8))
corr = df.select_dtypes("number").corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()

# 7e. Pairplot (sampled for speed)
sns.pairplot(df.sample(500), hue="clicked_on_ad", diag_kind="kde")
plt.suptitle("Pairplot — Key Numeric Features", y=1.02)
plt.show()


# ============================================================
# 8. GROUP-LEVEL ANALYSIS
# ── Purpose: Compute segment-level aggregates to answer
#    business questions (e.g. which audience clicks most?).
# ============================================================

# Click rate by gender and age group
click_by_segment = (
    df.groupby(["gender", "age_group"])["clicked_on_ad"]
    .agg(click_rate="mean", total="count")
    .reset_index()
    .sort_values("click_rate", ascending=False)
)
print(click_by_segment)

# Average spend metrics by click outcome
spend_summary = df.groupby("clicked_on_ad")[
    ["area_income", "daily_time_spent_on_site", "daily_internet_usage"]
].mean()
print(spend_summary)


# ============================================================
# 9. STATISTICAL TESTING
# ── Purpose: Move beyond visual hunches and confirm whether
#    observed differences are statistically significant.
# ============================================================

# 9a. T-test: is daily time spent different between clickers / non-clickers?
clicked     = df[df["clicked_on_ad"] == 1]["daily_time_spent_on_site"]
not_clicked = df[df["clicked_on_ad"] == 0]["daily_time_spent_on_site"]
t_stat, p_value = stats.ttest_ind(clicked, not_clicked)
print(f"T-test — t={t_stat:.3f}, p={p_value:.4f}")

# 9b. Chi-squared test: is click rate independent of gender?
ct = pd.crosstab(df["gender"], df["clicked_on_ad"])
chi2, p, dof, expected = stats.chi2_contingency(ct)
print(f"Chi-squared — χ²={chi2:.3f}, p={p:.4f}, dof={dof}")


# ============================================================
# 10. EXPORT CLEAN DATA
# ── Purpose: Persist the processed dataset so it can be
#    re-used by modelling notebooks without re-running this.
# ============================================================

df.to_csv("social_media_ads_clean.csv", index=False)
print("Clean dataset saved to social_media_ads_clean.csv")
