# Simulation Type Help text
simulation_help_text = """
**Simulation Types:**

- **Normal Distribution**: Models returns using a bell curve with specified mean and standard deviation. 
  Simple but may underestimate extreme events.

- **Students-T Distribution**: Similar to normal but with "fatter tails" for better modeling of market extremes.
  More conservative for risk planning.

- **Empirical Distribution**: Uses actual historical market data rather than theoretical models.
  Reflects real market patterns but limited to past events.
"""

# SMILE Help Text
smile_help_text = """
**Annual Decrease of Living Expense in Retirement:**

- **The Smile Effect**: Research shows that household expenses tend to decrease by about 1% 
  each year during retirement. However, they often rise again later in life due to increased healthcare costs — 
  creating a spending pattern shaped like a smile.
"""

# Living Expense Help Text
living_expense_help_text = """
**Annual Living Expenses:**

- **Living Expenses**: Include grocery, food, utility, shopping, entertainment, travel, car, gas, car insurance

- **Medical**: Out of pocket costs e.g. co-pay, co-insurances etc. 
  Do not include medical insurance premiums if self insured thtough ACA before medicare. 
  Enter those details in the 'Healthcare' tab.

- **Housing**: Include property tax, and insurances. Do not include mortgage. 
"""

# Bridge Health Care Help Text
bridge_healthcare_help_text = """
**Self funded Health Insurance after Retirement but before Medicare start at 65:**

- **Bridge Healthcare Cost**: Include ACA Health Exchange Plan premium and 
  out-of-pocket costs like co-pay and co-insurnace

"""

# Tax Rate Help Text
tax_rate_both_working_help = """
The average tax rate applied to your combined income when **both partners are working.**
This is total tax paid divided by total income. 
Include **Payroll Taxes** like Social Security and Medicare Taxes.
"""

tax_rate_one_retired_help = """
The average tax rate when **one person is still working and the other is retired.** 
Include **Payroll Taxes** like Social Security and Medicare Taxes.
Often lower than when both are working due to different income sources and tax brackets.
"""

tax_rate_both_retired_help = """
The average tax rate when **both partners are retired.** Typically the lowest of the three rates
due to favorable tax treatment of retirement income and potentially lower overall income.
"""
tax_calculation_disclaimer = """
Basic tax modeling with three stages is implemented. 
More advanced features like state-specific rates, tax brackets, tax treatment of social security payemnts 
and RMDs etc. are not yet supported.
"""

adjust_expense_text = """
These adjustments get carried forward. 
You can enter negative amount to reduce recurring expenses.
"""

disclaimer_text_old = """
    <div style="background-color:#f0f2f6; padding:10px; border-radius:5px; margin-bottom:15px">
        <p style="font-size:0.7em; margin-bottom:0px">
            <strong>Disclaimer:</strong> This tool provides simplified simulations for educational purposes only. 
            The results are rough estimates based on the inputs provided and should not be used as the sole basis for investment decisions. 
            For personalized financial advice, please consult with a certified financial planner or investment advisor. 
            The creators of this tool accept no responsibility for decisions made based on these simulations.
        </p>
    </div>
    """

disclaimer_text = """
    <div style="background-color:#e8f4f8; padding:10px; border-radius:5px; margin-bottom:15px; border-left:3px solid #6c757d;">
        <p style="font-size:0.8em; margin-bottom:0px; color:#0d4c73;">
            <strong>Disclaimer:</strong> For educational purposes only. 
            For personalized financial advice, please consult a certified professional advisor. 
            No liability accepted for decisions based on these simulations.
        </p>
    </div>
    """

stock_return_mean_help = """
The expected average annual return for stocks (arithmetic mean).
- This is the simple average return (not compound/CAGR)
- Higher than CAGR due to volatility
- Historical US stock market average: ~7-10%
- Recent forecasts by Vanguard, JP Morgan and others trend lower: ~6% US equity and ~8% international equity
- Used to simulate year-by-year returns
"""

stock_return_std_help = """
Standard deviation measures volatility of annual stock returns.
- Higher values = more volatile performance
- Historical US stock market: ~15-20%
- Recent market standard: ~15-16%
- Impacts both upside potential and downside risk
"""

bond_return_mean_help = """
The expected average annual return for bonds (arithmetic mean).
- This is the simple average return (not compound/CAGR)
- Generally lower than stocks with less volatility
- Historical average: ~3-5%
- Recent forecasts: ~3.5-4.5%
- More stable but lower growth than stocks
"""

bond_return_std_help = """
Standard deviation measures volatility of annual bond returns.
- Lower values than stocks = more stable returns
- Historical bond market: ~3-8% (varies by type)
- Recent market standard: ~4-5%
- Higher quality bonds typically have lower volatility
"""

auto_run_help_text = "When enabled, the simulation will run automatically each time you change any parameter, without needing to click the Run Simulation button."  

market_returns_note = """
<div style="background-color:#e8f4f8; padding:6px; border-radius:4px; font-size:0.75em;">
    <span style="color:#0d4c73;">
        <span style="margin-right:4px; vertical-align:middle;">ℹ️</span>
        <strong>Return Assumptions:</strong> While historical US stock returns have averaged 7-10% annually, major firms (J.P. Morgan, Schwab, Morningstar, BlackRock etc.) have lowered their 10-year forecasts to 3-7% CAGR (equivalent to 5-8% Aritmatic Mean) for US stocks and 4-5% for bonds. According to <a href='https://global.morningstar.com/en-eu/markets/experts-forecast-us-stock-bond-returns-2025-edition' target='_blank' rel='noopener noreferrer'>Morningstar's 2025</a> outlook, non-US stocks are expected to outperform US stocks over the next decade.
        <br><br>   
        <strong>Default values used in this tool </strong>(assuming a diversified equity portfolio):
        <ul style="margin: 4px 0 4px 15px; padding: 0;">
            <li><strong>Stocks:</strong> 6.5% return <strong>(arithmetic mean)</strong>, 15.5% volatility</li>
            <li><strong>Bonds:</strong> 3.5% return <strong>(arithmetic mean)</strong>, 4.5% volatility</li>
        </ul>
    </span>
</div>
"""

# Overall help document 
help_document = """
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