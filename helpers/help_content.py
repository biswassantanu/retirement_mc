# helpers/help_content.py

HELP_DOCUMENT = """
# Retirement Planning Tool Help

## Overview
This tool uses Monte Carlo simulation to model your retirement finances across thousands of possible market scenarios. It helps you determine if your retirement savings plan is likely to succeed under various market conditions.

## Key Features

### 1. Profile Settings
- **Current Age & Life Expectancy**: Define the timespan of your retirement plan
- **Retirement Age**: When you and your partner plan to stop working

### 2. Account Balances
- Input current balances across different account types (401(k), IRA, Roth, Brokerage, Cash)
- Set your investment allocation between stocks and bonds

### 3. Income Sources
- **Employment Income**: Pre-retirement earnings with annual growth rates
- **Pension Income**: Fixed income streams with optional growth rates
- **Social Security**: Benefits that start at specified ages
- **Rental Income**: Optional additional income stream with growth rate

### 4. 401(k) Contributions
- Set contribution amounts for you and your partner
- Option to maximize contributions automatically
- Include employer contributions/matching

### 5. Tax Modeling
- Three-tier tax rate system:
  - **Both Working**: Higher rate applied when both partners are employed
  - **One Retired**: Medium rate when one partner is retired
  - **Both Retired**: Lower rate when both partners are retired

### 6. Expenses
- **Living Expenses**: Regular annual expenses
- **Mortgage**: Payments that end after specified years
- **Expense Reduction**: "Retirement Smile" decrease after retirement
- **Inflation**: Modeled with both average rate and variability

### 7. Healthcare Costs
- Bridge healthcare costs before Medicare eligibility
- Automatically ends at age 65

### 8. Investment Returns
- Set expected returns and volatility for stocks and bonds
- Three simulation methods:
  - **Normal Distribution**: Standard bell curve of returns
  - **Student's t-Distribution**: More extreme market events
  - **Empirical Distribution**: Based on historical market data

### 9. Special Events
- **Downsizing**: Model home sale proceeds
- **Recurring Expense Adjustments**: Increase/decrease future expenses
- **One-Time Expenses**: Large purchases or expenses
- **Windfalls**: Inheritance, property sales, or other lump sums

## Understanding the Results

### Success Rate
The percentage of simulations where your portfolio lasted throughout your lifetime.

### Scenario Analysis
Results are shown for different market return scenarios:
- **Significantly Below Average**: 10th percentile outcome
- **Below Average**: 25th percentile outcome
- **Average Returns**: 50th percentile (median) outcome
- **Above Average**: 75th percentile outcome

### Key Metrics
- **Ending Balance**: Final portfolio value at end of plan
- **Ending Balance @ Today's $**: Inflation-adjusted final value
- **Year of Depletion**: When funds run out (or "Lasts lifetime")
- **Effective Rate of Return**: Geometric mean of returns
- **Years with Negative Return**: Count of years with losses

## Tips for Using This Tool

1. **Start with realistic assumptions** rather than best-case scenarios
2. **Run multiple simulations** with different parameters
3. **Save parameter sets** to compare different strategies
4. Use the **Auto-Update** feature to see results change as you adjust inputs
5. **Revisit and update** your plan annually as circumstances change

## Limitations

- This tool provides **estimates only** based on the parameters you enter
- Actual market returns, inflation rates, and expenses will differ
- Tax calculations are simplified and don't include brackets or deductions
- Consult with a certified financial advisor for personalized advice

## Saving and Sharing

Use the "Save Parameters" button to download your inputs as a CSV file. You can reload this file later using the upload feature.
"""