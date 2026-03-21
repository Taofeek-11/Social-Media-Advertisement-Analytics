# ============================================================
# SOCIAL MEDIA ADVERTISING — FULL EDA
# Columns: Campaign_ID, Target_Audience, Campaign_Goal,
#          Duration, Channel_Used, Conversion_Rate,
#          Acquisition_Cost, ROI, Location, Language,
#          Clicks, Impressions, Engagement_Score,
#          Customer_Segment, Date, Company, hour, day, month
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.figsize": (12, 5), "figure.dpi": 120})

# ── Load ─────────────────────────────────────────────────────
df = pd.read_csv("social_media_ads.csv", parse_dates=["Date"])

# ── Quick sanity check ───────────────────────────────────────
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())


# ============================================================
# SECTION 1 — DERIVED METRICS
# ============================================================

df["CTR"]           = df["Clicks"] / df["Impressions"].replace(0, np.nan)
df["Cost_per_Click"] = df["Acquisition_Cost"] / df["Clicks"].replace(0, np.nan)
df["ROI_per_Day"]   = df["ROI"] / df["Duration"].replace(0, np.nan)

print("\nNew columns added:", ["CTR", "Cost_per_Click", "ROI_per_Day"])


# ============================================================
# SECTION 2 — UNIVARIATE: NUMERIC DISTRIBUTIONS
# ============================================================

numeric_cols = [
    "ROI", "Conversion_Rate", "Acquisition_Cost",
    "Clicks", "Impressions", "Engagement_Score",
    "Duration", "CTR", "Cost_per_Click", "ROI_per_Day"
]

fig, axes = plt.subplots(2, 5, figsize=(22, 9))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    axes[i].hist(df[col].dropna(), bins=30, color="steelblue", edgecolor="white")
    axes[i].set_title(col, fontsize=11)
    axes[i].set_xlabel("")
    axes[i].set_ylabel("Count")

plt.suptitle("Numeric Feature Distributions", fontsize=14, y=1.01)
plt.tight_layout()
plt.show()

# Box plots to surface outliers
fig, axes = plt.subplots(2, 5, figsize=(22, 8))
axes = axes.flatten()
for i, col in enumerate(numeric_cols):
    axes[i].boxplot(df[col].dropna(), patch_artist=True,
                    boxprops=dict(facecolor="steelblue", color="navy"),
                    medianprops=dict(color="orange", linewidth=2))
    axes[i].set_title(col, fontsize=11)
plt.suptitle("Outlier Check — Box Plots", fontsize=14, y=1.01)
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 3 — UNIVARIATE: CATEGORICAL DISTRIBUTIONS
# ============================================================

cat_cols = [
    "Channel_Used", "Campaign_Goal", "Target_Audience",
    "Customer_Segment", "Location", "Language", "Company"
]

fig, axes = plt.subplots(2, 4, figsize=(22, 10))
axes = axes.flatten()

for i, col in enumerate(cat_cols):
    order = df[col].value_counts().index
    sns.countplot(data=df, y=col, order=order, ax=axes[i], palette="Blues_r")
    axes[i].set_title(f"{col} — Count", fontsize=11)
    axes[i].set_xlabel("Count")
    axes[i].set_ylabel("")

axes[-1].set_visible(False)
plt.suptitle("Categorical Feature Distributions", fontsize=14, y=1.01)
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 4 — CORRELATION MATRIX
# ============================================================

corr_cols = [
    "ROI", "Conversion_Rate", "Acquisition_Cost",
    "Clicks", "Impressions", "Engagement_Score",
    "Duration", "CTR", "Cost_per_Click", "ROI_per_Day"
]

plt.figure(figsize=(13, 10))
corr = df[corr_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(
    corr, mask=mask, annot=True, fmt=".2f",
    cmap="coolwarm", center=0, square=True,
    linewidths=0.5, cbar_kws={"shrink": 0.8}
)
plt.title("Correlation Matrix — Numeric KPIs", fontsize=13)
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 5 — CHANNEL PERFORMANCE
# ============================================================

channel_kpis = (
    df.groupby("Channel_Used")[["ROI", "Conversion_Rate", "CTR", "Acquisition_Cost"]]
    .mean()
    .round(3)
    .sort_values("ROI", ascending=False)
)
print("\nChannel KPI Summary:\n", channel_kpis)

fig, axes = plt.subplots(1, 4, figsize=(22, 5))
kpis = ["ROI", "Conversion_Rate", "CTR", "Acquisition_Cost"]
colors = ["steelblue", "seagreen", "darkorange", "tomato"]

for ax, kpi, color in zip(axes, kpis, colors):
    data = channel_kpis[kpi].sort_values(ascending=True)
    ax.barh(data.index, data.values, color=color, edgecolor="white")
    ax.set_title(f"Mean {kpi} by Channel", fontsize=11)
    ax.set_xlabel(kpi)

plt.suptitle("Channel Performance Comparison", fontsize=14)
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 6 — CAMPAIGN GOAL ANALYSIS
# ============================================================

goal_kpis = (
    df.groupby("Campaign_Goal")[["ROI", "Conversion_Rate", "Acquisition_Cost", "Engagement_Score"]]
    .mean()
    .round(3)
    .sort_values("ROI", ascending=False)
)
print("\nCampaign Goal KPI Summary:\n", goal_kpis)

fig, axes = plt.subplots(1, 4, figsize=(22, 5))
for ax, kpi, color in zip(axes, ["ROI", "Conversion_Rate", "Acquisition_Cost", "Engagement_Score"],
                           ["steelblue", "seagreen", "tomato", "mediumpurple"]):
    data = goal_kpis[kpi].sort_values(ascending=True)
    ax.barh(data.index, data.values, color=color, edgecolor="white")
    ax.set_title(f"Mean {kpi} by Campaign Goal", fontsize=11)
    ax.set_xlabel(kpi)

plt.suptitle("Campaign Goal Performance", fontsize=14)
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 7 — TARGET AUDIENCE & CUSTOMER SEGMENT
# ============================================================

for group_col in ["Target_Audience", "Customer_Segment"]:
    grp = (
        df.groupby(group_col)[["ROI", "Conversion_Rate", "Engagement_Score", "Acquisition_Cost"]]
        .mean()
        .round(3)
        .sort_values("ROI", ascending=False)
    )
    print(f"\n{group_col} KPI Summary:\n", grp)

    fig, axes = plt.subplots(1, 4, figsize=(22, 5))
    for ax, kpi, color in zip(axes,
                               ["ROI", "Conversion_Rate", "Engagement_Score", "Acquisition_Cost"],
                               ["steelblue", "seagreen", "darkorange", "tomato"]):
        data = grp[kpi].sort_values(ascending=True)
        ax.barh(data.index, data.values, color=color, edgecolor="white")
        ax.set_title(f"Mean {kpi} by {group_col}", fontsize=10)
    plt.suptitle(f"{group_col} Performance", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# SECTION 8 — DURATION vs ROI
# ============================================================

plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x="Duration", y="ROI", hue="Channel_Used", alpha=0.6)
# Trend line
m, b, r, p, _ = stats.linregress(df["Duration"].dropna(), df["ROI"].dropna())
x_line = np.linspace(df["Duration"].min(), df["Duration"].max(), 100)
plt.plot(x_line, m * x_line + b, color="black", linewidth=1.5, linestyle="--",
         label=f"Trend (r={r:.2f}, p={p:.3f})")
plt.title("Campaign Duration vs ROI")
plt.legend(bbox_to_anchor=(1.01, 1))
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 9 — ACQUISITION COST vs ROI  (Efficiency Quadrant)
# ============================================================

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Acquisition_Cost", y="ROI",
                hue="Channel_Used", size="Engagement_Score",
                sizes=(30, 200), alpha=0.7)
plt.axhline(df["ROI"].median(), color="gray", linestyle="--", linewidth=1, label="Median ROI")
plt.axvline(df["Acquisition_Cost"].median(), color="gray", linestyle=":", linewidth=1,
            label="Median Cost")
plt.title("Acquisition Cost vs ROI — Efficiency Quadrant")
plt.legend(bbox_to_anchor=(1.01, 1))
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 10 — HEATMAPS: CHANNEL × CAMPAIGN GOAL
# ============================================================

for metric in ["ROI", "Conversion_Rate", "CTR"]:
    pivot = df.pivot_table(values=metric, index="Campaign_Goal",
                           columns="Channel_Used", aggfunc="mean")
    plt.figure(figsize=(12, 5))
    sns.heatmap(pivot, annot=True, fmt=".3f", cmap="YlGnBu", linewidths=0.5)
    plt.title(f"Mean {metric} — Channel × Campaign Goal")
    plt.tight_layout()
    plt.show()


# ============================================================
# SECTION 11 — TIME ANALYSIS
# ============================================================

# 11a. Monthly trend
monthly = df.groupby("month")[["ROI", "Conversion_Rate", "Clicks", "Engagement_Score"]].mean()

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
for ax, col, color in zip(axes.flatten(),
                           ["ROI", "Conversion_Rate", "Clicks", "Engagement_Score"],
                           ["steelblue", "seagreen", "darkorange", "mediumpurple"]):
    ax.plot(monthly.index, monthly[col], marker="o", color=color, linewidth=2)
    ax.set_title(f"Mean {col} by Month")
    ax.set_xlabel("Month")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.suptitle("Monthly Performance Trends", fontsize=14)
plt.tight_layout()
plt.show()

# 11b. Day-of-week pattern
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df["day_name"] = pd.Categorical(df["day"].map(
    {0: "Monday", 1: "Tuesday", 2: "Wednesday",
     3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
), categories=day_order, ordered=True)

day_perf = df.groupby("day_name")[["ROI", "Engagement_Score", "CTR"]].mean()

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, col, color in zip(axes, ["ROI", "Engagement_Score", "CTR"],
                           ["steelblue", "seagreen", "darkorange"]):
    ax.bar(day_perf.index, day_perf[col], color=color, edgecolor="white")
    ax.set_title(f"Mean {col} by Day of Week")
    ax.set_xticklabels(day_perf.index, rotation=45, ha="right")
plt.suptitle("Day-of-Week Performance", fontsize=14)
plt.tight_layout()
plt.show()

# 11c. Hour-of-day pattern
hour_perf = df.groupby("hour")[["ROI", "Engagement_Score", "CTR", "Clicks"]].mean()

fig, axes = plt.subplots(2, 2, figsize=(16, 9))
for ax, col, color in zip(axes.flatten(),
                           ["ROI", "Engagement_Score", "CTR", "Clicks"],
                           ["steelblue", "seagreen", "darkorange", "tomato"]):
    ax.plot(hour_perf.index, hour_perf[col], marker="o", color=color, linewidth=2)
    ax.set_title(f"Mean {col} by Hour of Day")
    ax.set_xlabel("Hour")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.suptitle("Hour-of-Day Performance", fontsize=14)
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 12 — ENGAGEMENT SCORE vs CONVERSION RATE
# ── Key question: does engagement actually convert?
# ============================================================

plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x="Engagement_Score", y="Conversion_Rate",
                hue="Channel_Used", alpha=0.6)
m, b, r, p, _ = stats.linregress(
    df["Engagement_Score"].dropna(), df["Conversion_Rate"].dropna()
)
x_line = np.linspace(df["Engagement_Score"].min(), df["Engagement_Score"].max(), 100)
plt.plot(x_line, m * x_line + b, color="black", linewidth=1.5, linestyle="--",
         label=f"Trend (r={r:.2f}, p={p:.3f})")
plt.title("Engagement Score vs Conversion Rate — Does Engagement Convert?")
plt.legend(bbox_to_anchor=(1.01, 1))
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 13 — TOP COMPANY PERFORMANCE
# ============================================================

company_perf = (
    df.groupby("Company")[["ROI", "Conversion_Rate", "CTR", "Acquisition_Cost"]]
    .mean()
    .round(3)
    .sort_values("ROI", ascending=False)
    .head(15)
)
print("\nTop 15 Companies by ROI:\n", company_perf)

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
for ax, col, color in zip(axes, ["ROI", "Acquisition_Cost"], ["steelblue", "tomato"]):
    data = company_perf[col].sort_values(ascending=True)
    ax.barh(data.index, data.values, color=color, edgecolor="white")
    ax.set_title(f"Top 15 Companies — Mean {col}")
plt.suptitle("Company-Level Performance", fontsize=14)
plt.tight_layout()
plt.show()


# ============================================================
# SECTION 14 — STATISTICAL TESTS
# ============================================================

print("\n── Statistical Tests ──")

# 14a. ANOVA: does ROI differ significantly across channels?
groups = [grp["ROI"].dropna().values for _, grp in df.groupby("Channel_Used")]
f_stat, p_val = stats.f_oneway(*groups)
print(f"ANOVA (ROI ~ Channel_Used): F={f_stat:.3f}, p={p_val:.4f}")

# 14b. ANOVA: does Conversion_Rate differ across Campaign_Goals?
groups2 = [grp["Conversion_Rate"].dropna().values for _, grp in df.groupby("Campaign_Goal")]
f2, p2 = stats.f_oneway(*groups2)
print(f"ANOVA (Conversion_Rate ~ Campaign_Goal): F={f2:.3f}, p={p2:.4f}")

# 14c. Pearson correlation: Engagement_Score vs Conversion_Rate
r, p = stats.pearsonr(df["Engagement_Score"].dropna(), df["Conversion_Rate"].dropna())
print(f"Pearson (Engagement_Score vs Conversion_Rate): r={r:.3f}, p={p:.4f}")

# 14d. Pearson correlation: Duration vs ROI
r2, p2 = stats.pearsonr(df["Duration"].dropna(), df["ROI"].dropna())
print(f"Pearson (Duration vs ROI): r={r2:.3f}, p={p2:.4f}")


# ============================================================
# SECTION 15 — SUMMARY TABLE
# ── Best performing combination of Channel × Goal
# ============================================================

summary = (
    df.groupby(["Channel_Used", "Campaign_Goal"])
    .agg(
        Mean_ROI=("ROI", "mean"),
        Mean_Conversion=("Conversion_Rate", "mean"),
        Mean_CTR=("CTR", "mean"),
        Mean_Cost=("Acquisition_Cost", "mean"),
        Campaigns=("Campaign_ID", "count")
    )
    .round(3)
    .sort_values("Mean_ROI", ascending=False)
    .reset_index()
)

print("\nTop Channel × Goal Combinations by ROI:")
print(summary.head(10).to_string(index=False))

summary.to_csv("channel_goal_summary.csv", index=False)
print("\nSaved: channel_goal_summary.csv")
