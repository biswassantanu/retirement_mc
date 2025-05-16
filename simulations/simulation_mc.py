import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime

def monte_carlo_simulation(current_age, partner_current_age, life_expectancy, initial_savings, 
                            annual_earnings, partner_earnings, self_yearly_increase, partner_yearly_increase,
                            annual_expense, mortgage_payment,
                            mortgage_years_remaining, retirement_age, partner_retirement_age, 
                            annual_social_security, withdrawal_start_age, partner_social_security, 
                            partner_withdrawal_start_age, self_healthcare_cost, self_healthcare_start_age, 
                            partner_healthcare_start_age, partner_healthcare_cost, stock_percentage, 
                            bond_percentage, stock_return_mean, bond_return_mean, stock_return_std, 
                            bond_return_std, simulations, tax_rate, cola_rate, inflation_mean, 
                            inflation_std, annual_expense_decrease, years_until_downsize, residual_amount,  
                            adjust_expense_years, adjust_expense_amounts, 
                            one_time_years, one_time_amounts,            
                            windfall_years, windfall_amounts): 

    # Get the current year
    current_year = datetime.now().year
    years_in_simulation = life_expectancy - current_age  # This should be 37 years
    success_count = 0
    failure_count = 0

    # Prepare lists to store cash flow data for each percentile simulation
    cash_flows = []
    all_cash_flows = []  
    cash_flow_10th = []
    cash_flow_50th = []
    cash_flow_90th = []

    # Unpack adjustments
    adjust_expense_year_1, adjust_expense_year_2, adjust_expense_year_3 = adjust_expense_years
    adjust_expense_amount_1, adjust_expense_amount_2, adjust_expense_amount_3 = adjust_expense_amounts

    # Unpack one-time expenses
    one_time_year_1, one_time_year_2, one_time_year_3 = one_time_years
    one_time_amount_1, one_time_amount_2, one_time_amount_3 = one_time_amounts

    # Unpack windfalls
    windfall_year_1, windfall_year_2, windfall_year_3 = windfall_years
    windfall_amount_1, windfall_amount_2, windfall_amount_3 = windfall_amounts


    for sim in range(simulations):
        savings = initial_savings
        starting_annual_earnings = annual_earnings 
        starting_partner_earnings = partner_earnings
        previous_annual_expense = annual_expense

        cash_flows = []

        for year in range(years_in_simulation):
            current_age_in_loop = current_age + year
            partner_current_age_in_loop = partner_current_age + year

            # Calculate income streams
            current_annual_earnings = calculate_earnings(starting_annual_earnings, self_yearly_increase, year, retirement_age, current_age_in_loop)
            current_partner_earnings = calculate_earnings(starting_partner_earnings, partner_yearly_increase, year, partner_retirement_age, partner_current_age_in_loop)

            self_ss = calculate_social_security(annual_social_security, cola_rate, withdrawal_start_age, current_age_in_loop)
            partner_ss = calculate_social_security(partner_social_security, cola_rate, partner_withdrawal_start_age, partner_current_age_in_loop)

            # Calculate expenses
            mortgage = calculate_mortgage(mortgage_payment, year, mortgage_years_remaining)
            healthcare_costs, self_health_expense, partner_health_expense = calculate_healthcare_costs(current_age_in_loop, self_healthcare_cost, self_healthcare_start_age, partner_current_age_in_loop, partner_healthcare_cost, partner_healthcare_start_age, inflation_mean)


            # Adjusting expenses based on hardcoded variables
            yearly_expense_adjustment = 0
            if year + current_year == adjust_expense_year_1:
                yearly_expense_adjustment = adjust_expense_amount_1

            if year + current_year == adjust_expense_year_2:
                yearly_expense_adjustment = adjust_expense_amount_2

            if year + current_year == adjust_expense_year_3:
                yearly_expense_adjustment = adjust_expense_amount_3

            previous_annual_expense += yearly_expense_adjustment
            current_annual_expense = adjust_expenses(previous_annual_expense, inflation_mean, inflation_std, annual_expense_decrease, year, current_age_in_loop, retirement_age, partner_current_age_in_loop, partner_retirement_age)
            previous_annual_expense = current_annual_expense

            # Incorporate one-time expenses 
            one_time_expense = 0
            if year + current_year == one_time_year_1:
                one_time_expense += one_time_amount_1
            
            if year + current_year == one_time_year_2:
                one_time_expense += one_time_amount_2

            if year + current_year == one_time_year_3:
                    one_time_expense += one_time_amount_3

            # Calculate total income and expenses
            gross_income = current_annual_earnings + current_partner_earnings + self_ss + partner_ss
            total_expense = current_annual_expense + mortgage + healthcare_costs + one_time_expense
            estimated_tax = gross_income * tax_rate

            # Determine portfolio draw
            portfolio_draw, total_tax = calculate_portfolio_draw(total_expense, gross_income, estimated_tax, tax_rate)

            # Calculate investment returns
            investment_return = calculate_investment_return(savings, stock_percentage, bond_percentage, stock_return_mean, stock_return_std, bond_return_mean, bond_return_std)
            return_rate = investment_return / savings

            # End of year balance
            ending_portfolio_value = savings + investment_return + gross_income - total_expense - total_tax
            end_value_at_current_currency = ending_portfolio_value / ((1 + inflation_mean ) ** (year + 1) ) 

            # Draw down rate 
            draw_rate = portfolio_draw / ending_portfolio_value

            # Check if it's time to downsize
            if year == years_until_downsize:
                downsize_proceeds = residual_amount  # Add the residual amount to the savings
            else: 
                downsize_proceeds = 0

            # Incorporate windfalls
            windfall_amount = 0 
            if year + current_year == windfall_year_1:
                windfall_amount += windfall_amount_1

            if year + current_year == windfall_year_2:
                windfall_amount += windfall_amount_2

            if year + current_year == windfall_year_3:
                windfall_amount += windfall_amount_3


            # Create cash flow entry
            cash_flow_entry = create_cash_flow_entry(
                current_year,
                year,
                current_age_in_loop,
                partner_current_age_in_loop,
                savings,  
                ending_portfolio_value,
                end_value_at_current_currency, 
                gross_income,
                total_expense,
                total_tax,
                portfolio_draw,
                draw_rate, 
                investment_return,
                return_rate, 
                self_ss,
                partner_ss,
                downsize_proceeds, 
                mortgage,
                healthcare_costs,
                current_annual_earnings,  
                current_partner_earnings,  
                self_health_expense,     
                partner_health_expense, 
                yearly_expense_adjustment, 
                one_time_expense, 
                windfall_amount
            )

            # Set the next period's opening balance - incorporating downsizing and windfall 
            savings = ending_portfolio_value + downsize_proceeds + windfall_amount

            # Add the simulation ID to the cash flow entry
            cash_flow_entry['Simulation ID'] = sim  # Add the simulation ID

            # Check if the cash flow entry is valid (not empty)
            if cash_flow_entry:  # Ensure the entry is not empty
                cash_flows.append(cash_flow_entry)

        # Append the cash flow entry to the list of all cash flows
        if cash_flows:
            all_cash_flows.append(cash_flows)

        # Check if the simulation is successful (savings do not run out before the end)
        if savings >= 0:
            success_count += 1
        else:
            failure_count += 1

    # After all simulations, sort the cash flows based on the ending portfolio value of the last year
    sorted_cash_flows = sorted(all_cash_flows, key=lambda x: x[-1]['Ending Portfolio Value'])

    return (success_count, failure_count, sorted_cash_flows)

def calculate_earnings(starting_earnings, yearly_increment, year, retirement_age, current_age):
    if current_age < retirement_age:
        return starting_earnings * (1 + yearly_increment) ** year
    return 0

def calculate_social_security(annual_ss, cola_rate, withdrawal_start_age, current_age):
    if current_age >= withdrawal_start_age:
        return annual_ss * (1 + cola_rate) ** (current_age - withdrawal_start_age)
    return 0

def calculate_mortgage(mortgage_payment, year, mortgage_years_remaining):
    return mortgage_payment if year < mortgage_years_remaining else 0

def calculate_healthcare_costs(current_age, self_healthcare_cost, self_healthcare_start_age, partner_current_age, partner_healthcare_cost, partner_healthcare_start_age, inflation_mean):
    healthcare_costs = 0
    if current_age >= self_healthcare_start_age:
        if current_age < 65:
            self_healthcare_cost *= (1 + inflation_mean)**(current_age - self_healthcare_start_age)
        else:
            self_healthcare_cost = 0
        healthcare_costs += self_healthcare_cost
    else:
        self_healthcare_cost = 0

    if partner_current_age >= partner_healthcare_start_age:
        if partner_current_age < 65:
            partner_healthcare_cost *= (1 + inflation_mean)**(partner_current_age - partner_healthcare_start_age)
        else:
            partner_healthcare_cost = 0
        healthcare_costs += partner_healthcare_cost
    else: 
        partner_healthcare_cost = 0 

    return healthcare_costs, self_healthcare_cost, partner_healthcare_cost

def adjust_expenses(current_expense, inflation_mean, inflation_std, annual_expense_decrease, year, current_age, retirement_age, partner_current_age, partner_retirement_age):
 
    inflation_rate = np.random.normal(inflation_mean, inflation_std)
    if year > 0:  # Skip the first year as we want to adjust from the second year onward
        if current_age >= retirement_age and partner_current_age >= partner_retirement_age:
            return current_expense * (1 + inflation_rate - annual_expense_decrease)
        else:
            return current_expense * (1 + inflation_rate)
    return current_expense 

def calculate_portfolio_draw(total_expense, gross_income, estimated_tax, tax_rate):
    if total_expense <= (gross_income - estimated_tax):
        return 0, estimated_tax  # No portfolio draw needed
    else:
        portfolio_draw = total_expense - (gross_income - estimated_tax)
        portfolio_tax = portfolio_draw * tax_rate      
        total_tax = portfolio_tax + estimated_tax
        return portfolio_draw + portfolio_tax, total_tax

def calculate_investment_return(savings, stock_percentage, bond_percentage, stock_return_mean, stock_return_std, bond_return_mean, bond_return_std):
    stock_investment = savings * (stock_percentage / 100)
    bond_investment = savings * (bond_percentage / 100)

    stock_return_rate = np.random.normal(stock_return_mean, stock_return_std)
    bond_return_rate = np.random.normal(bond_return_mean, bond_return_std)

    return (stock_investment * stock_return_rate) + (bond_investment * bond_return_rate)

def create_cash_flow_entry(current_year, year, current_age, partner_current_age, savings, ending_portfolio_value,end_value_at_current_currency,
                            gross_income, total_expense, total_tax, portfolio_draw, draw_rate, 
                            investment_return, return_rate, self_ss, partner_ss, downsize_proceeds, mortgage, healthcare_costs, 
                            self_gross_earning, partner_gross_earning, self_health_expense, partner_health_expense, 
                            yearly_expense_adjustment, one_time_expense, windfall_amount
                            ):

    return {
        'Year': current_year + year,
        'Self Age': current_age,
        'Partner Age': partner_current_age,
        'Beginning Portfolio Value': savings,
        'Gross Earnings': gross_income,
        'Total Expense': total_expense,
        'Tax': total_tax,
        'Portfolio Draw': portfolio_draw,
        'Investment Return': investment_return,
        'Ending Portfolio Value': ending_portfolio_value,
        'At Constant Currency': end_value_at_current_currency, 
        'Downsize Proceeds' : downsize_proceeds, 
        'Investment Return %' : return_rate, 
        'Drawdown %' : draw_rate, 
        'Self Gross Earning': self_gross_earning,
        'Partner Gross Earning': partner_gross_earning,
        'Self Social Security': self_ss,
        'Partner Social Security': partner_ss,
        'Combined Social Security': self_ss + partner_ss, 
        'Mortgage': mortgage,
        'Healthcare Expense': healthcare_costs,
        'Self Health Expense': self_health_expense,
        'Partner Health Expense': partner_health_expense, 
        'Yearly Expense Adj' : yearly_expense_adjustment, 
        'One Time Expense' : one_time_expense,  
        'Windfall Amt' : windfall_amount
    }
