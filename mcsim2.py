import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk

# Retirement Planning Parameters
current_age = 57
retirement_age = 60
earning_years = retirement_age - current_age
partner_current_age = 51
life_expectancy = 92
annual_expense = 8500 * 12
mortgage_payment = 4800 * 12
mortgage_years_remaining = 15
initial_savings = 2350000
annual_social_security = 3600 * 12
partner_social_security = 2000 * 12
partner_retirement_age = retirement_age + 8
earnings = 325000
partner_earnings = 75000
partner_earning_years = partner_retirement_age - partner_current_age
social_security_start = 70
partner_social_security_start = 65
annual_expense_decrease = 0.01
tax_rate = 0.17
inflation_mean = 0.025
inflation_std = 0.01
investment_mean = 0.05
investment_std = 0.12
simulations = 5000

# Monte Carlo Simulation
def monte_carlo_simulation():
    years_in_simulation = life_expectancy - current_age
    success_count = 0
    failure_count = 0

    aggregated_data = {year: {'Starting Savings': [], 'Annual Expense': [], 'Income': [], 'Investment Return': [], 'Tax': [],
                              'Self Social Security': [], 'Partner Social Security': [], 'Mortgage Payment': [], 'Ending Savings': []}
                       for year in range(years_in_simulation)}

    for sim in range(simulations):
        savings = initial_savings
        annual_exp = annual_expense

        for year in range(years_in_simulation):
            current_age_in_loop = current_age + year
            self_ss = 0
            partner_ss = 0

            if year < mortgage_years_remaining:
                mortgage = mortgage_payment
            else:
                mortgage = 0

            annual_exp_with_mortgage = annual_exp + mortgage

            if current_age_in_loop > partner_retirement_age:
                annual_exp_with_mortgage *= (1 - annual_expense_decrease)

            if current_age_in_loop < retirement_age:
                income = earnings * (1 - tax_rate)
            else:
                income = 0

            if year < partner_earning_years:
                partner_income = partner_earnings * (1 - tax_rate)
            else:
                partner_income = 0

            income += partner_income

            if current_age_in_loop >= social_security_start:
                self_ss = annual_social_security * (1 - tax_rate)
                income += self_ss
            if current_age_in_loop >= partner_social_security_start:
                partner_ss = partner_social_security * (1 - tax_rate)
                income += partner_ss

            net_cash_flow = income - annual_exp_with_mortgage

            inflation_rate = np.random.normal(inflation_mean, inflation_std)
            annual_exp *= (1 + inflation_rate)

            investment_return_rate = np.random.normal(investment_mean, investment_std)
            investment_return = savings * investment_return_rate

            if income == 0:
                withdrawal = annual_exp_with_mortgage
                tax = withdrawal * tax_rate
            else:
                taxable_income = max(0, income - annual_exp_with_mortgage)
                tax = taxable_income * tax_rate

            savings_end_of_year = (savings + net_cash_flow) * (1 + investment_return_rate)

            aggregated_data[year]['Starting Savings'].append(savings)
            aggregated_data[year]['Annual Expense'].append(annual_exp_with_mortgage)
            aggregated_data[year]['Income'].append(income)
            aggregated_data[year]['Investment Return'].append(investment_return)
            aggregated_data[year]['Tax'].append(tax)
            aggregated_data[year]['Self Social Security'].append(self_ss)
            aggregated_data[year]['Partner Social Security'].append(partner_ss)
            aggregated_data[year]['Mortgage Payment'].append(mortgage)
            aggregated_data[year]['Ending Savings'].append(savings_end_of_year)

            savings = savings_end_of_year

            if savings <= 0:
                failure_count += 1
                break
        else:
            success_count += 1

    success_rate = (success_count / simulations) * 100
    failure_rate = (failure_count / simulations) * 100

    avg_data = []
    for year, data in aggregated_data.items():
        avg_data.append({
            'Year': current_age + year,
            'Starting Savings ($)': "{:,}".format(int(np.mean(data['Starting Savings']))),
            'Annual Expense ($)': "{:,}".format(int(np.mean(data['Annual Expense']))),
            'Income ($)': "{:,}".format(int(np.mean(data['Income']))),
            'Self Social Security ($)': "{:,}".format(int(np.mean(data['Self Social Security']))),
            'Partner Social Security ($)': "{:,}".format(int(np.mean(data['Partner Social Security']))),
            'Mortgage Payment ($)': "{:,}".format(int(np.mean(data['Mortgage Payment']))),
            'Investment Return ($)': "{:,}".format(int(np.mean(data['Investment Return']))),
            'Tax ($)': "{:,}".format(int(np.mean(data['Tax']))),
            'Ending Savings ($)': "{:,}".format(int(np.mean(data['Ending Savings']))),
        })

    df_avg_cashflow = pd.DataFrame(avg_data)

    return df_avg_cashflow, success_rate, failure_rate

# Display DataFrame in a Popup Window
def show_dataframe_popup(df):
    root = tk.Tk()
    root.title("Retirement Cash Flow")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.E, width=150)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    root.mainloop()

# Run the simulation
df_avg_cashflow, success_rate, failure_rate = monte_carlo_simulation()

# Show DataFrame in a popup window
show_dataframe_popup(df_avg_cashflow)

# Print success and failure rates
print(f"\nSuccess Rate: {success_rate:.2f}%")
print(f"Failure Rate: {failure_rate:.2f}%")
