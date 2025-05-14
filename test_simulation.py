from simulations.simulation_mc import monte_carlo_simulation

# Default values based on the calling program
current_age = 55
partner_current_age = 50
life_expectancy = 92
initial_savings = 2000000
annual_earnings = 200000
partner_earnings = 200000
self_yearly_increase = 0.03  # 3%
partner_yearly_increase = 0.03  # 3%
annual_expense = 8000 * 12  # Annual expense
mortgage_payment = 36000  # Yearly mortgage
mortgage_years_remaining = 25
retirement_age = 60
partner_retirement_age = 60
annual_social_security = 3000 * 12  # Annual social security
withdrawal_start_age = 67
cola_rate = 0.015  # 1.5%
partner_social_security = 1500 * 12  # Partner's annual social security
partner_withdrawal_start_age = 65
self_healthcare_cost = 5000  # Self healthcare cost
self_healthcare_start_age = retirement_age
partner_healthcare_cost = 5000  # Partner healthcare cost
partner_healthcare_start_age = partner_retirement_age
stock_percentage = 60
bond_percentage = 40
stock_return_mean = 0.1010  # 10.10%
bond_return_mean = 0.039  # 3.9%
stock_return_std = 0.1960  # 19.60%
bond_return_std = 0.01166  # 1.166%
simulations = 10
tax_rate = 0.15  # 15%
cola_rate = 0.015  # 1.5%
inflation_mean = 0.025  # 2.5%
inflation_std = 0.01  # 1%
annual_expense_decrease = 0.005  # 0.5%

# Call the simulation method
success_count, failure_count, cash_flow_10th, cash_flow_50th, cash_flow_90th = monte_carlo_simulation(
    current_age, partner_current_age, life_expectancy, initial_savings, 
    annual_earnings, partner_earnings, self_yearly_increase, partner_yearly_increase,
    annual_expense, mortgage_payment,
    mortgage_years_remaining, retirement_age, partner_retirement_age, 
    annual_social_security, withdrawal_start_age, partner_social_security, 
    partner_withdrawal_start_age, self_healthcare_cost, self_healthcare_start_age, 
    partner_healthcare_start_age, partner_healthcare_cost, stock_percentage, 
    bond_percentage, stock_return_mean, bond_return_mean, stock_return_std, 
    bond_return_std, simulations, tax_rate, cola_rate, inflation_mean, 
    inflation_std, annual_expense_decrease
)

# Print debugging statements
print("Debugging: Simulation Results")
print(f"Success Count: {success_count}")
print(f"Failure Count: {failure_count}")
print(f"10th Percentile Cash Flow Entries: {len(cash_flow_10th)}")
print(f"50th Percentile Cash Flow Entries: {len(cash_flow_50th)}")
print(f"90th Percentile Cash Flow Entries: {len(cash_flow_90th)}")

# Optionally, print the first few entries of the 50th percentile cash flow for inspection
print("50th Percentile Cash Flow Data (First 5 Entries):")
for entry in cash_flow_50th[:5]:  # Print the first 5 entries
    print(entry)
