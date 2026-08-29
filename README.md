# Telecom Revenue Analysis

## Business problem
Megaline, a telecom operator, offers two prepaid plans: Surf and Ultimate. The
commercial department wants to know which plan brings in more revenue on average,
in order to adjust the advertising budget accordingly.

## Data
Five raw usage tables for 500 Megaline users during 2018 (`datasets/`):
- `megaline_users.csv` — user demographics and assigned plan
- `megaline_calls.csv`, `megaline_messages.csv`, `megaline_internet.csv` — per-event usage logs
- `megaline_plans.csv` — plan pricing and included allowances

## Methods
1. Data cleaning: corrected data types (dates, call-duration rounding), checked
   for duplicates.
2. Aggregation: computed monthly calls, minutes, messages, and internet usage per
   user, then merged with plan pricing to compute each user's **monthly revenue**
   (allowance overages billed on top of the base fee).
3. Descriptive statistics and visualizations (bar charts, histograms, boxplots —
   see [`ima/`](ima/)) comparing usage and revenue across plans and months.
4. Hypothesis testing — two Welch's t-tests (`scipy.stats.ttest_ind`, `equal_var=False`):
   - H0: average revenue does not differ between Ultimate and Surf users
   - H0: average revenue does not differ between users in the NY-NJ metro area and users elsewhere

## Result
This is a statistical analysis project, not a model-scoring one. Both null
hypotheses were **rejected**: despite Ultimate's higher base price, Surf users
were found to generate more revenue on average, and users in the NY-NJ metro area
showed significantly different revenue than users elsewhere.

## How to run
```bash
pip install -r requirements.txt
```
The analysis script uses a literal space in its filename, so quote it:
```bash
python "Proyecto 4.py"
```
It's a Jupytext "percent-format" script and can also be opened directly in Jupyter
or VS Code to run cell by cell.
