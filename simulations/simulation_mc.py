import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import math 

# Monte Carlo Simulation
def monte_carlo_simulation(current_age, partner_current_age, life_expectancy, initial_savings, annual_earnings, partner_earnings, annual_expense, mortgage_payment,
                           mortgage_years_remaining, retirement_age, partner_retirement_age, 
                           annual_social_security, withdrawal_start_age, partner_social_security, 
                           partner_withdrawal_start_age, self_healthcare_cost, self_healthcare_start_age, partner_healthcare_start_age,
                           partner_healthcare_cost, stock_percentage, bond_percentage, 
                           stock_return_mean, bond_return_mean, stock_return_std, bond_return_std, 
                           simulations, tax_rate, cola_rate, inflation_mean, inflation_std, annual_expense_decrease):

    # Get the current year
    current_year = datetime.now().year

    years_in_simulation = life_expectancy - current_age
    all_simulations = []  # To store all simulation results
    success_count = 0
    failure_count = 0

    # Prepare lists to store cash flow data for each percentile simulation
    cash_flow_10th = []
    cash_flow_50th = []
    cash_flow_90th = []

    for sim in range(simulations):
        savings = initial_savings
        simulation_results = []

        # Initialize yearly expenses and earnings
        current_annual_expense = annual_expense
        current_annual_earnings = annual_earnings 
        current_partner_earnings = partner_earnings
        current_self_healthcare_cost = self_healthcare_cost
        current_partner_healthcare_cost = partner_healthcare_cost

        starting_annual_earnings = annual_earnings 
        starting_partner_earnings = partner_earnings

        for year in range(years_in_simulation):
           
            current_age_in_loop = current_age + year
            partner_current_age_in_loop = partner_current_age + year

            # Adjust earning for yearly increase 
            current_annual_earnings = starting_annual_earnings * (1 + inflation_mean) ** year
            current_partner_earnings = starting_partner_earnings * (1 + inflation_mean) ** year          

            # Adjust expenses for inflation
            if year > 0:  # Skip the first year as we want to adjust from the second year onward
                if current_age_in_loop >= retirement_age and partner_current_age_in_loop >= partner_retirement_age:
                    current_annual_expense *= (1 + inflation_mean - annual_expense_decrease)  # Apply inflation and decrease
                else:
                    current_annual_expense *= (1 + inflation_mean)  # Apply inflation

            # Set earnings to 0 if retired
            self_income = current_annual_earnings * (1 - tax_rate) if current_age_in_loop < retirement_age else 0
            partner_income = current_partner_earnings * (1 - tax_rate) if partner_current_age_in_loop < partner_retirement_age else 0

            # Calculate mortgage payment
            mortgage = mortgage_payment if year < mortgage_years_remaining else 0


            # Calculate healthcare costs
            healthcare_costs = 0
            if current_age_in_loop >= self_healthcare_start_age:
                if current_age_in_loop < 65:
                    current_self_healthcare_cost *= (1 + inflation_mean)  # Adjust for inflation each year
                else: 
                    current_self_healthcare_cost = 0 
                healthcare_costs += current_self_healthcare_cost  # Add to total healthcare costs

            if partner_current_age_in_loop >= partner_healthcare_start_age:
                if partner_current_age_in_loop < 65:
                    current_partner_healthcare_cost *= (1 + inflation_mean)  # Adjust for inflation each year
                else: 
                    current_partner_healthcare_cost = 0
                healthcare_costs += current_partner_healthcare_cost  # Add to total healthcare costs


            # Apply COLA to Social Security benefits based on withdrawal start ages
            self_ss = annual_social_security * (1 + cola_rate) ** (current_age_in_loop - withdrawal_start_age) if current_age_in_loop >= withdrawal_start_age else 0
            partner_ss = partner_social_security * (1 + cola_rate) ** (partner_current_age_in_loop - partner_withdrawal_start_age) if partner_current_age_in_loop >= partner_withdrawal_start_age else 0

            self_income += self_ss
            partner_income += partner_ss

            # Calculate total earnings before tax
            total_earnings_before_tax = self_income / (1 - tax_rate) + partner_income / (1 - tax_rate) + self_ss + partner_ss

            annual_exp_with_mortgage = current_annual_expense + mortgage + healthcare_costs
            net_cash_flow = self_income + partner_income - annual_exp_with_mortgage

            # Calculate investment returns for stocks and bonds
            stock_investment = savings * (stock_percentage / 100)
            bond_investment = savings * (bond_percentage / 100)

            stock_return_rate = np.random.normal(stock_return_mean, stock_return_std)
            bond_return_rate = np.random.normal(bond_return_mean, bond_return_std)

            investment_return = (stock_investment * stock_return_rate) + (bond_investment * bond_return_rate)

            # # Calculate tax
            tax = max(net_cash_flow, 0) * tax_rate

            # Portfolio draw
            portfolio_draw = max(annual_exp_with_mortgage + tax - (self_income + partner_income), 0)

            # Calculate income taxes based on earnings before tax
            self_income_tax = self_income / (1 - tax_rate) * tax_rate if current_age_in_loop < retirement_age else 0
            partner_income_tax = partner_income / (1 - tax_rate) * tax_rate if partner_current_age_in_loop < partner_retirement_age else 0
 
            # Calculate total tax
            tax = self_income_tax + partner_income_tax + max(portfolio_draw, 0) * tax_rate

            # End of year balance
            savings = savings + investment_return + net_cash_flow - tax

            # Store values for each year
            simulation_results.append(savings)

            # Store cash flow data for this year
            cash_flow_entry = {
                'Year': current_year + year,
                'Self Age': current_age_in_loop,
                'Partner Age': partner_current_age_in_loop,
                'Beginning Portfolio Value': savings - investment_return - net_cash_flow + tax,
                'Total Earnings (before tax)': total_earnings_before_tax,
                'Combined Social Security': self_ss + partner_ss,
                'Investment Return': investment_return,
                'Total Expense': annual_exp_with_mortgage,
                'Yearly Expense': current_annual_expense,
                'Tax': tax,
                'Portfolio Draw': portfolio_draw,
                'Ending Portfolio Value': savings,
                'Self Earnings (before tax)': self_income / (1 - tax_rate) ,
                'Partner Earnings (before tax)': partner_income / (1 - tax_rate),
                'Self Social Security': self_ss,
                'Partner Social Security': partner_ss,
                'Mortgage': mortgage,
                'Healthcare Expense': healthcare_costs
            }

            # Append to the appropriate cash flow list based on the simulation index
            if sim == int(0.1 * simulations):  # 10th percentile
                cash_flow_10th.append(cash_flow_entry)
            elif sim == int(0.5 * simulations):  # 50th percentile
                cash_flow_50th.append(cash_flow_entry)
            elif sim == int(0.9 * simulations):  # 90th percentile
                cash_flow_90th.append(cash_flow_entry)

        all_simulations.append(simulation_results)  # Store the results of this simulation

        # Check if the simulation is successful (savings do not run out before the end)
        if savings >= 0:
            success_count += 1
        else:
            failure_count += 1

    return (success_count, failure_count, cash_flow_10th, cash_flow_50th, cash_flow_90th)
