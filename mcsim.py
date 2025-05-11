import numpy as np
import matplotlib.pyplot as plt

# Retirement Planning Parameters
retirement_age = 60
current_age = 57
partner_current_age = 51
life_expectancy = 92
annual_expense = 8500 * 12  # Monthly expense converted to annual
initial_savings = 2350000  # Initial retirement savings
annual_social_security = 3600 * 12  # Annual Social Security from age 70
partner_social_security = 2000 * 12  # Partner's annual Social Security from age 65
partner_retirement_age = retirement_age + 8  # Partner's retirement age
earnings = 325000  # Earnings
partner_earnings = 75000  # Partner's annual earnings for 8 years

# partner_earning_years = 8  # Years partner will work
partner_earning_years = partner_retirement_age -  partner_current_age # Years partner will work
social_security_start = 70
partner_social_security_start = 71
annual_expense_decrease = 0.01  # 1% nominal decrease after partner's retirement
tax_rate = 0.17  # Effective tax rate
simulations = 5000  # Number of Monte Carlo simulations
inflation_mean = 0.025  # Average inflation rate
inflation_std = 0.01  # Standard deviation for inflation
investment_mean = 0.05  # Average investment return
investment_std = 0.12  # Standard deviation for investment returns

# Monte Carlo Simulation
def monte_carlo_simulation():
    years_in_retirement = life_expectancy - retirement_age
    outcomes = []

    for _ in range(simulations):
        savings = initial_savings
        annual_exp = annual_expense
        for year in range(years_in_retirement):
            current_age = retirement_age + year

            # Adjust expenses after partner's retirement
            if current_age > partner_retirement_age:
                annual_exp *= (1 - annual_expense_decrease)

            # Income
            if year < ( retirement_age - current_age):
                income = partner_earnings * (1 - tax_rate)
            else:
                income = 0

            # Income: Partner's earnings
            if year < partner_earning_years:
                partner_income = partner_earnings * (1 - tax_rate)
            else:
                partner_income = 0

            income =+ partner_income 

            # Income: Social Security
            if current_age >= social_security_start:
                income += annual_social_security * (1 - tax_rate)
            if current_age >= partner_social_security_start:
                income += partner_social_security * (1 - tax_rate)

            # Net cash flow
            net_cash_flow = income - annual_exp

            # Inflation-adjusted expenses
            inflation_rate = np.random.normal(inflation_mean, inflation_std)
            annual_exp *= (1 + inflation_rate)

            # Investment growth
            investment_return = np.random.normal(investment_mean, investment_std)
            savings = (savings + net_cash_flow) * (1 + investment_return)

            # Check if savings are depleted
            if savings <= 0:
                outcomes.append(0)
                break
        else:
            outcomes.append(savings)

    return outcomes

# Run the simulation
results = monte_carlo_simulation()

# Calculate probabilities
success_rate = sum(1 for r in results if r > 0) / simulations * 100
failure_rate = 100 - success_rate
median_ending_balance = np.median([r for r in results if r > 0])

# Print results
print(f"Success Rate: {success_rate:.2f}%")
print(f"Failure Rate: {failure_rate:.2f}%")
print(f"Median Ending Balance if Successful: ${median_ending_balance:,.2f}")

# Plot the results
plt.hist(results, bins=50, color='skyblue', edgecolor='black')
plt.title('Monte Carlo Simulation for Retirement Savings')
plt.xlabel('Ending Savings ($)')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

