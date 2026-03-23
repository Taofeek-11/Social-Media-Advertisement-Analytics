# Data Dictionary
## Social Media Advertising Dataset

**Source:** Kaggle — Social Media Advertising Dataset
**Rows:** 5,200 campaigns
**Columns:** 19 original + 3 engineered

---

## Original Columns

| Column | Data Type | Example Value | Description | Notes |
|---|---|---|---|---|
| Campaign_ID | String | C_001 | Unique identifier for each campaign | Primary key |
| Target_Audience | String | Women 25-34 | Demographic group the campaign targets | Categorical |
| Campaign_Goal | String | Product Launch | Business objective of the campaign | 5 unique values |
| Duration | Integer | 30 | Length of campaign in days | Min: 1, Max: 90 |
| Channel_Used | String | Instagram | Social media platform used | 5 unique values |
| Conversion_Rate | Float | 0.112 | Conversions divided by total impressions | Range: 0.0 – 1.0 |
| Acquisition_Cost | Float | 261.50 | Total cost to acquire one customer ($) | Always positive |
| ROI | Float | 5.81 | Revenue generated per $ spent (multiplier) | Higher = better |
| Location | String | New York | Geographic market of the campaign | City or region |
| Language | String | English | Language of campaign creative | Categorical |
| Clicks | Integer | 4200 | Total number of clicks on the campaign | Always >= 0 |
| Impressions | Integer | 82000 | Total number of times ad was shown | Always > 0 |
| Engagement_Score | Float | 5.4 | Platform-assigned engagement quality score | Scale: 0 – 10 |
| Customer_Segment | String | High-Value | Customer value classification | 4 unique values |
| Date | Date | 2024-03-15 | Date the campaign ran | Format: YYYY-MM-DD |
| Company | String | Company Alpha | Advertiser company name | Anonymised |
| hour | Integer | 14 | Hour of day the campaign was active | Range: 0 – 23 |
| day | Integer | 2 | Day of week (0 = Monday) | Range: 0 – 6 |
| month | Integer | 3 | Month of year | Range: 1 – 12 |

---

## Engineered Features

These columns are derived during the cleaning and feature engineering step.

| Column | Formula | Description | Edge Case Handling |
|---|---|---|---|
| CTR | Clicks / Impressions | Click-through rate — measures how often people who saw the ad clicked it | Impressions = 0 replaced with NaN |
| Cost_per_Click | Acquisition_Cost / Clicks | Average cost per individual click | Clicks = 0 replaced with NaN |
| ROI_per_Day | ROI / Duration | Time-adjusted return — normalises ROI across different campaign lengths | Duration = 0 replaced with NaN |

---

## Categorical Value Reference

### Channel_Used
| Value | Description |
|---|---|
| Instagram | Meta's image and video platform |
| YouTube | Google's video platform |
| Facebook | Meta's social network |
| Twitter | X (formerly Twitter) microblogging platform |
| Pinterest | Visual discovery and bookmarking platform |

### Campaign_Goal
| Value | Description |
|---|---|
| Product Launch | Campaigns aimed at introducing a new product |
| Brand Awareness | Campaigns focused on reach and recognition |
| Market Expansion | Campaigns targeting new geographic or demographic markets |
| Retention | Campaigns aimed at re-engaging existing customers |
| Website Traffic | Campaigns driving clicks to a website or landing page |

### Customer_Segment
| Value | Description | Avg Conv. Rate |
|---|---|---|
| High-Value | Top-tier customers with high lifetime value | ~13.4% |
| New Users | First-time customers acquired recently | ~9.8% |
| Returning | Customers who have purchased more than once | ~8.9% |
| Casual | Low-frequency, price-sensitive customers | ~7.2% |

### Day of Week (day column)
| Value | Day |
|---|---|
| 0 | Monday |
| 1 | Tuesday |
| 2 | Wednesday |
| 3 | Thursday |
| 4 | Friday |
| 5 | Saturday |
| 6 | Sunday |

---

## Summary Statistics

| Column | Min | Max | Mean | Median | Std Dev |
|---|---|---|---|---|---|
| ROI | ~3.0 | ~7.5 | 5.21 | 5.18 | ~0.8 |
| Conversion_Rate | ~0.05 | ~0.20 | 0.101 | 0.099 | ~0.03 |
| Acquisition_Cost | ~180 | ~320 | 249 | 248 | ~28 |
| Engagement_Score | ~2.0 | ~8.5 | 5.0 | 5.0 | ~1.2 |
| Duration | 1 | 90 | ~30 | ~28 | ~18 |
| CTR | ~0.02 | ~0.09 | 0.048 | 0.047 | ~0.01 |

*Summary statistics are approximate and based on the full unfiltered dataset.*

---

## Data Quality Notes

| Issue | Column | Resolution |
|---|---|---|
| Zero values | Clicks, Impressions | Replaced with NaN before division operations |
| Zero values | Duration | Replaced with NaN before ROI_per_Day calculation |
| No missing values | All columns | Dataset is complete with no nulls |
| Date parsing | Date | Parsed with `parse_dates=["Date"]` on load |
