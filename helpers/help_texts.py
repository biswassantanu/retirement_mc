# Simulation Type Help text
simulation_help_text = """
**Simulation Types:**

- **Normal Distribution**: Models returns using a bell curve with specified mean and standard deviation. 
  Simple but may underestimate extreme events.

- **Students-T Distribution**: Similar to normal but with "fatter tails" for better modeling of market extremes.
  More conservative for risk planning.

- **Empirical Distribution**: Uses actual historical market data rather than theoretical models.
  Reflects real market patterns but limited to past events.

- **Markov Chain**: Models market regimes (bear, normal, bull) with transition probabilities between states, capturing market cycles and persistence.

- **Collar Strategy**: Uses Normal Distribution but limits stock returns between minimum and maximum values. 
  This is implemented through buying option collars and models investments with downside protection and capped upside.
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

healthcare_bridge_text = """
<div style="background-color:#e8f4f8; padding:6px; border-radius:4px; font-size:0.75em;">
    <span style="color:#0d4c73;">
        <span style="margin-right:4px; vertical-align:middle;">ℹ️</span>
        <strong>Healthcare Bridge Costs:</strong><br> These are the expenses to cover health insurance between retirement and Medicare eligibility (age 65). For early retirees, this can be one of the largest pre-Medicare expenses.<br><br>        
        Typical monthly costs range from $800-$2,000 per person depending on coverage level, location, and health status. ACA marketplace plans with subsidies may reduce costs based on your retirement income. Remember that healthcare costs typically increase faster than general inflation (often 5-7% annually).
    </span>
</div>
"""

adjust_expense_text = """
<div style="background-color:#e8f4f8; padding:6px; border-radius:4px; font-size:0.8em;">
    <span style="color:#0d4c73;">ℹ️ <strong> About Living Expense Adjustments: </strong> <br>These <strong>recurring adjustments to yealy living expense</strong> amount get carried forward. 
You can enter both positive (e.g. kid starting college) and negative (e.g. kid finishing college) amount to reduce recurring expenses. 
<br><br>Enter upto 3 such recurring adjustments.</span>
</div>
"""

one_time_expense_text = """
<div style="background-color:#e8f4f8; padding:6px; border-radius:4px; font-size:0.8em;">
    <span style="color:#0d4c73;">ℹ️ <strong> About One Time Expenses: </strong> <br>These are <strong>one time non-recurring expenses</strong> like car purchase or kid's wedding etc.<br><br>
    Enter upto 3 such one time expenses.</span>
</div>
"""


windfall_text = """
<div style="background-color:#e8f4f8; padding:6px; border-radius:4px; font-size:0.75em;">
    <span style="color:#0d4c73;">
        <span style="margin-right:4px; vertical-align:middle;">ℹ️</span>
        <strong>About Windfalls:</strong><br> Include expected one-time financial gains such as inheritances, or other lump-sum payments. Enter the amount and year you expect to receive each windfall. These amounts will be added to your investment accounts based on your allocation settings at that time.
        <br><br>Enter upto 3 such windfall amounts.
    </span>
</div>
"""

downsize_text = """
<div style="background-color:#e8f4f8; padding:6px; border-radius:4px; font-size:0.75em;">
    <span style="color:#0d4c73;">
        <span style="margin-right:4px; vertical-align:middle;">ℹ️</span>
        <strong>About Downsizing:</strong><br> Enter details about selling your current home and purchasing a less expensive one. The net proceeds (sale price minus new purchase and transaction costs) will be added to your investment accounts based on your allocation settings at that time. This can be a significant source of retirement funding.
    </span>
</div>
"""

parameter_text = """
<div style="background-color:#e8f4f8; padding:6px; border-radius:4px; font-size:0.75em;">
    <span style="color:#0d4c73;">
        <span style="margin-right:4px; vertical-align:middle;">ℹ️</span>
        <strong>Simulation Parameters:</strong><br>        
        Parameters control how your retirement simulation behaves. The distribution type affects how market volatility is modeled:<br>       
        • <strong>Normal:</strong> Standard bell curve. May underestimate crashes.<br>         
        • <strong>Students' T:</strong> Better captures market crashes with fatter tails.<br>          
        • <strong>Empirical:</strong> Based on actual historical returns.<br>
        • <strong>Markov Chain:</strong> Models market regimes and their transitions.<br>
        • <strong>Collar Strategy:</strong> Limits stock returns between min/max values, providing downside protection with capped upside.<br><br>      
    </span>
</div>
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
        <strong>Return Assumptions:</strong><br> While historical US stock returns have averaged 7-10% annually, major firms (J.P. Morgan, Schwab, Morningstar, BlackRock etc.) have lowered their 10-year forecasts to 3-7% CAGR (equivalent to 5-8% Aritmatic Mean) for US stocks and 4-5% for bonds. According to <a href='https://global.morningstar.com/en-eu/markets/experts-forecast-us-stock-bond-returns-2025-edition' target='_blank' rel='noopener noreferrer'>Morningstar's 2025</a> outlook, non-US stocks are expected to outperform US stocks over the next decade.
        <br><br>   
        <strong>Default values used in this tool </strong>(assuming a diversified equity portfolio):
        <ul style="margin: 4px 0 4px 15px; padding: 0;">
            <li><strong>Stocks:</strong> 6.5% return <strong>(arithmetic mean)</strong>, 15.5% volatility</li>
            <li><strong>Bonds:</strong> 3.5% return <strong>(arithmetic mean)</strong>, 4.5% volatility</li>
        </ul>
    </span>
</div>
"""

stress_test_text = """
<div style="background-color:#fae8e8; padding:6px; border-radius:4px; font-size:0.75em;">
    <span style="color:#0d4c73;">
        <span style="margin-right:4px; vertical-align:middle;">ℹ️</span>
        <strong>Sequence of Returns Risk:</strong><br> Tests how your plan performs if you experience poor market returns in early retirement years while also making withdrawals. This can have a significant impact on portfolio longevity.
    </span>
</div>
"""
enable_sequence_risk_help = """
When enabled, the simulation will test how your plan performs with poor returns in early retirement
"""

seq_risk_years_help="""
Number of consecutive years with poor returns at the beginning of retirement
"""

seq_risk_returns_help="""
Market return percentage during the stress period
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


interpretation_guide_md_old = """

##### Core Metrics & Success Rate Thresholds - use them to evaluate your plan

| Metric | What it means | Robust Plan | Adequate Plan | Fragile Plan |
|--------|---------------|-------------|--------------|--------------|
| **Success Rate** | Plan viability. Target value depends on the simulation type used. | Normal ≥85%<br>Student's T ≥80-85%<br>Collar ≥ 90%<br>Markov ≥75-80% | Normal 80-84%<br>Student's T 75-79%<br>Markov 70-74%<br>Collar ≥ 85-89% | Normal < 80%<br>Student's T <75%<br>Markov < 70%<br>Collar < 85% |
| **End of Plan Cushion** | Years of expenses left - use values from below historical return scenario | ≥5 yrs | 3-4 yrs | ≤2 yrs |
| **Withdrawal Rates** | Spending stress on portfolio (portfolio draw + starting balance - use values from below historical return scenario) | Avg ≤5%, Max ≤9% | Avg 6-7%, Max ≤12% | Avg > 7%, Max >12% |
| **Market Assumptions** | Equity, bond, inflation, COLA (all nominal values i.e. not adjusted for inflation) | Conservative<br>· Equity 6.5%<br>· Bonds 3.4%<br>· CPI 2.5-3.5%<br>· COLA 1.5% | Moderate<br>· Equity 7.5%<br>· Bonds 3.4%<br>· CPI 2.25%<br>· COLA 2% | Rosy<br>Equity ≥9%<br>· CPI ≤2%<br>· COLA = CPI |

##### Tolerance Rules (Trade-offs)

| Rule | When It's Acceptable | When It's Not |
|------|---------------------|--------------|
| **One weak link allowed** | At most ONE metric may be "Fragile" if other three are "Good" | Two (or more) metrics in "Fragile" at once |
| **High Success <> Thin Cushion** | If Success ≥90% (per sim type), Cushion can be 2-3 yrs | If Success < thresholds, Cushion must be ≥5 yrs |
| **Strong Cushion <> Higher Withdrawals** | If Cushion ≥5 yrs, avg withdrawals up to 6-7% tolerable | If Cushion ≤2 yrs, withdrawals should be ≤5% |
| **Conservative Assumptions <> Other Stress** | If assumptions are conservative, allow one other Adequate | If assumptions are rosy, Success + Cushion must be "Good" |
| **High Withdrawals <> Safety Backstops** | Avg 7-8% only if Success ≥90% + Cushion ≥4 yrs + conservative assumptions | Avg > 7% with low Success or thin Cushion |
"""

interpretation_guide_md = """
<style>
body {
  font-family: Arial, sans-serif; /* Optional: sets the font family */
  font-size: 14px; /* Base font size for the document */
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  font-size: 14px; /* Default font size for all table content */
}
th, td {
  padding: 8px;
  text-align: left;
  border: 1px solid #ddd;
  vertical-align: top;
}
th {
  background-color: #f2f2f2;
  font-weight: bold;
  font-size: 15px; /* Slightly larger font for headers */
}
h1 {
  font-size: 24px;
  color: #333;
  margin-top: 20px;
  margin-bottom: 10px;
}
h5 {
  font-size: 16px;
  color: #333;
  margin-top: 20px;
  margin-bottom: 10px;
}
/* You can also target specific elements or classes */
.small-text {
  font-size: 10px;
}
.large-text {
  font-size: 18px;
}
</style>

<h5>Core Metrics & Success Rate Thresholds - use them to evaluate your plan</h2>
<table>
  <tr>
    <th style="width:15%">Metric</th>
    <th style="width:20%">What it means</th>
    <th style="width:20%">Robust Plan</th>
    <th style="width:20%">Adequate Plan</th>
    <th style="width:20%">Fragile Plan</th>
  </tr>
  <tr>
    <td><b>Success Rate</b></td>
    <td>Plan viability. Target value depends on the simulation type used.</td>
    <td>· Normal Dist ≥85%<br>· Student's T ≥80-85%<br>· Collar ≥ 90%<br>· Markov ≥75-80%</td>
    <td>· Normal Dist 80-84%<br>· Student's T 75-79%<br>· Collar ≥ 85-89%<br>· Markov 70-74%</td>
    <td>· Normal Dist< 80%<br>· Student's T <75%<br>· Collar < 85%<br>· Markov < 70%</td>
  </tr>
  <tr>
    <td><b>End of Plan Cushion</b></td>
    <td>Years of expenses left - use values from <b>below historical return scenario</b></td>
    <td>≥5 yrs</td>
    <td>3-4 yrs</td>
    <td>≤2 yrs</td>
  </tr>
  <tr>
    <td><b>Withdrawal Rates</b></td>
    <td>Spending stress on portfolio (portfolio draw + starting balance - use values from <b>below historical return scenario</b>)</td>
    <td>Avg ≤5%, Max ≤9%</td>
    <td>Avg 6-7%, Max ≤12%</td>
    <td>Avg > 7%, Max >12%</td>
  </tr>
  <tr>
    <td><b>Market Assumptions</b></td>
    <td>Equity, bond, inflation, COLA (all nominal values i.e. not adjusted for inflation)</td>
    <td><b>Conservative</b><br>· Equity 6.5%<br>· Bonds 3.4%<br>· CPI 2.5-3.5%<br>· COLA 1.5%</td>
    <td><b>Moderate</b><br>· Equity 7.5%<br>· Bonds 3.4%<br>· CPI 2.25%<br>· COLA 2%</td>
    <td><b>Rosy</b><br>· Equity ≥8.5%<br>· CPI ≤2%<br>· COLA = CPI</td>
  </tr>
</table>

<h5>Tolerance Rules (Trade-offs)</h2>
<table>
  <tr>
    <th style="width:25%">Rule</th>
    <th style="width:37%">When It's Acceptable</th>
    <th style="width:37%">When It's Not</th>
  </tr>
  <tr>
    <td><b>One weak link allowed</b></td>
    <td>At most ONE metric may be "Fragile" if other three are "Good"</td>
    <td>Two (or more) metrics in "Fragile" at once</td>
  </tr>
  <tr>
    <td><b>High Success &lt;&gt; Thin Cushion</b></td>
    <td>If Success ≥90% (per sim type), Cushion can be 2-3 yrs</td>
    <td>If Success < thresholds, Cushion must be ≥5 yrs</td>
  </tr>
  <tr>
    <td><b>Strong Cushion &lt;&gt; Higher Withdrawals</b></td>
    <td>If Cushion ≥5 yrs, avg withdrawals up to 6-7% tolerable</td>
    <td>If Cushion ≤2 yrs, withdrawals should be ≤5%</td>
  </tr>
  <tr>
    <td><b>Conservative Assumptions &lt;&gt; Other Stress</b></td>
    <td>If assumptions are conservative, allow one other Adequate</td>
    <td>If assumptions are rosy, Success + Cushion must be "Good"</td>
  </tr>
  <tr>
    <td><b>High Withdrawals &lt;&gt; Safety Backstops</b></td>
    <td>Avg 7-8% only if Success ≥90% + Cushion ≥4 yrs + conservative assumptions</td>
    <td>Avg > 7% with low Success or thin Cushion</td>
  </tr>
</table>
<br>
"""
