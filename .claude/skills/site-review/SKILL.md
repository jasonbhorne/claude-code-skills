# Site Review: $ARGUMENTS

## Description
Weekly site review for jasonhorne.org and all GitHub repositories. Pulls GA4 analytics and GitHub traffic data, then produces a .docx report.

## Trigger
- `/site-review` or `/site-review March 2026`
- "run a site review", "check my site traffic", "how is my site doing"

## Configuration

### GA4
- **Property ID:** 524969501
- **Service Account:** `~/.claude/credentials/ga4-service-account.json`
- **Library:** `google-analytics-data` (via Anaconda Python)
- **Python:** `/opt/anaconda3/bin/python3`

### GitHub
- **Tool:** `gh api` (GitHub CLI)
- **Repos (auto-discovered):** All repos owned by `jasonbhorne`
- **Traffic API limitation:** GitHub only retains 14 days of traffic data

### Output
- **Format:** .docx (using python-docx)
- **Location:** `~/Documents/Website Reviews/`
- **Naming:** `jasonhorne.org Review - {Month} {Year}.docx`

## Workflow

### Step 1: Determine Date Range

Default: last 7 days and prior 7 days for comparison.

If `$ARGUMENTS` specifies a month (e.g., "March 2026"), use that full month and the prior month for comparison.

Calculate:
- `current_start`, `current_end` (last 7 days or specified month)
- `prior_start`, `prior_end` (preceding 7 days or preceding month)
- `report_label` (e.g., "Mar 10-16, 2026" or "March 2026")

### Step 2: Pull GA4 Data

Run a Python script using the service account credentials and `google-analytics-data` library. Collect these reports:

**2a. Traffic Overview (current vs prior period)**
Metrics: `activeUsers`, `sessions`, `screenPageViews`, `bounceRate`, `averageSessionDuration`, `newUsers`

**2b. Top Pages (current period)**
Dimensions: `pagePath`, `pageTitle`
Metrics: `screenPageViews`, `activeUsers`, `averageSessionDuration`, `bounceRate`
Order by: `screenPageViews` desc, limit 20

**2c. Traffic Sources (current period)**
Dimension: `sessionDefaultChannelGroup`
Metrics: `sessions`, `activeUsers`, `bounceRate`

**2d. Referrers (current period)**
Dimension: `sessionSource`
Metrics: `sessions`, `activeUsers`
Limit: 15

**2e. Daily Breakdown (current period)**
Dimension: `date`
Metrics: `screenPageViews`, `activeUsers`, `sessions`

**2f. Device Breakdown (current period)**
Dimension: `deviceCategory`
Metrics: `sessions`, `activeUsers`, `bounceRate`

**2g. Geography (current period)**
Dimensions: `country`, `region`
Metrics: `activeUsers`, `sessions`
Limit: 15

Use this pattern for all GA4 queries:
```python
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/hornej/.claude/credentials/ga4-service-account.json"

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Metric, Dimension, OrderBy,
)

PROPERTY_ID = "524969501"
client = BetaAnalyticsDataClient()

response = client.run_report(RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    date_ranges=[DateRange(start_date="YYYY-MM-DD", end_date="YYYY-MM-DD")],
    metrics=[Metric(name="activeUsers"), ...],
    dimensions=[Dimension(name="pagePath"), ...],
    order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
    limit=20,
))
```

### Step 3: Pull GitHub Data

Use `gh api` to collect traffic for ALL repos owned by `jasonbhorne`.

First, discover repos:
```bash
gh api user/repos --paginate --jq '.[].name'
```

Then for each repo, pull (note: GitHub traffic API only returns last 14 days):
```bash
# Views and clones
gh api repos/jasonbhorne/{repo}/traffic/views
gh api repos/jasonbhorne/{repo}/traffic/clones

# Referrers and paths
gh api repos/jasonbhorne/{repo}/traffic/popular/referrers
gh api repos/jasonbhorne/{repo}/traffic/popular/paths

# Stars, forks, watchers
gh api repos/jasonbhorne/{repo} --jq '{stars: .stargazers_count, forks: .forks_count, watchers: .subscribers_count, open_issues: .open_issues_count}'
```

**Important:** Traffic endpoints (`/traffic/views`, `/traffic/clones`, `/traffic/popular/*`) return 403 for repos where the authenticated user doesn't have push access, and return empty data for repos with zero traffic. Handle both gracefully.

Filter the daily views/clones arrays to only include dates within the report's current period.

Aggregate across all repos:
- Total views, unique viewers
- Total clones, unique cloners
- Total stars, forks across all repos
- Top repos by views, clones, and stars
- Top referrers across all repos
- Top paths across all repos
- New stargazers (if any) with usernames and dates

### Step 4: Generate .docx Report

Use `/opt/anaconda3/bin/python3` with `python-docx` to create the report. Match the existing report style in `~/Documents/Website Reviews/`.

#### Document Structure

**Title:** `jasonhorne.org Weekly Site Review`
**Subtitle (Normal):** `{report_label}`

**Heading 1: Executive Summary**
- 4-5 bullet points (List Bullet style) covering the most notable findings across both GA4 and GitHub
- Include a "Priority" paragraph with the single most important action item

**Heading 1: 1. Website Traffic (GA4)**

**Heading 2: Key Metrics**
- Table comparing current vs prior period with % change
- Brief narrative paragraph noting trends

**Heading 2: Top Pages**
- Table with rank, path, title, views, users
- Narrative noting standout pages and engagement

**Heading 2: Traffic Sources**
- Table with channel, sessions, users, bounce rate
- Narrative on source quality

**Heading 2: Referrers**
- Table with source, sessions, users
- Note any new or notable referral sources

**Heading 2: Daily Trend**
- Table with date, views, users, sessions
- Note any spikes or patterns

**Heading 2: Devices & Geography**
- Brief tables and narrative

**Heading 1: 2. GitHub Overview**

**Heading 2: Repository Summary**
- Table: repo name, stars, forks, views (14d), unique viewers, clones, unique cloners
- Only include repos with any activity (stars > 0 OR views > 0 OR clones > 0). If a repo has zero across the board, omit it.

**Heading 2: Traffic Details**
- For each repo with meaningful traffic (views > 5 or clones > 5 in the period):
  - Heading 3 with repo name
  - Views/clones breakdown
  - Top referrers and paths
  - Any new stars/forks with usernames

**Heading 2: GitHub Highlights**
- Bullet points: top-performing repo, total reach, notable referrers, cross-traffic from jasonhorne.org

**Heading 1: 3. Cross-Channel Insights**
- Bullet points connecting GA4 and GitHub data
- Blog-to-GitHub pipeline effectiveness (referrals from jasonhorne.org to GitHub)
- Social media impact on both platforms
- Content topic performance across both channels

**Heading 1: 4. Recommendations**
- 3-5 prioritized action items based on the data
- Each as a bullet point with brief rationale

#### Table Formatting
- Use python-docx Table with a grid style
- Bold header row
- Right-align numeric columns
- Include % change column where comparing periods

#### Report File
Save to: `~/Documents/Website Reviews/jasonhorne.org Review - {Month} {Year}.docx`

For weekly reviews, use: `jasonhorne.org Review - Week of {date}.docx`

### Step 5: Print Summary

After saving the .docx, print a brief terminal summary:
- Report saved location
- 3-4 headline metrics (users, page views, GitHub clones, top content)
- Any notable changes or spikes

## Error Handling

- If GA4 auth fails, check that `~/.claude/credentials/ga4-service-account.json` exists and the `google-analytics-data` package is installed
- If `gh api` returns 403 on traffic endpoints, skip that repo's traffic (stars/forks still available)
- If a repo has zero traffic, exclude it from the report rather than showing empty rows
- If python-docx is not installed: `pip install python-docx`

## Integration with Weekly Ops

When called from the weekly-ops skill, return these values for shared context:
```python
{
    "report_path": "<path to .docx>",
    "top_findings": ["...", "...", "..."],
    "blog_topics": ["...", "..."],
    "action_items": ["...", "..."]
}
```
