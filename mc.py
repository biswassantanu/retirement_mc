import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime

# Set Streamlit to use full-width layout
st.set_page_config(layout="wide")

# Streamlit Display
st.title("Retirement Cash Flow Analysis")
st.subheader("Monte Carlo Simulation")

# Put the tabs inside a container with fixed height
with st.container(height=360, border=None):
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Personal Details", "Investment and Savings", "Income and Expense", "Social Security", "Healthcare Costs", "Market Returns", "Downsize"])

    # Tab 1: Personal Details
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            current_age = st.number_input("Current Age", value=55)
            partner_current_age = st.number_input("Partner's Current Age", value=50)
            life_expectancy = st.number_input("Life Expectancy", value=92)
        with col2:
            retirement_age = st.number_input("Retirement Age", value=60)
            partner_retirement_age = st.number_input("Partner's Retirement Age", value=60)

    # Tab 2: Investment and Savings
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            initial_savings = st.number_input("Current Savings", value=2000000, step=100000)
            stock_percentage = st.slider("Percentage of Stock Investment (%)", min_value=0, max_value=100, value=60)
            bond_percentage = 100 - stock_percentage  # Calculate bond percentage

    # Tab 3: Income and Expense
    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            annual_earnings = st.number_input("Annual Earnings", value=200000, step=5000)
            annual_expense = st.number_input("Annual Expense", value=8000 * 12, step=2000)
            mortgage_payment = st.number_input("Yearly Mortgage", value=36000, step=2000)
        with col2:
            partner_earnings = st.number_input("Partner's Annual Earnings", value=200000, step=5000)
            annual_expense_decrease = st.number_input("Annual Expense Decrease Rate (%)", value=0.5, step=0.05) / 100  # Convert to decimal
            mortgage_years_remaining = st.number_input("Mortgage Years Remaining", value=25)
        with col3:
            inflation_mean = st.number_input("Inflation Mean (%)", value=2.5) / 100  # Convert to decimal
            inflation_std = st.number_input("Inflation Std Dev (%)", value=1.0) / 100  # Convert to decimal
            tax_rate = st.number_input("Tax Rate (%)", value=15.0, step=1.0) / 100  # Convert to decimal

    # Tab 4: Social Security 
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            annual_social_security = st.number_input("Social Security", value=3000 * 12, step=1000)
            withdrawal_start_age = st.number_input("Withdrawal Start Age (Self)", value=67)
            cola_rate = st.number_input("COLA Rate (%)", value=1.50) / 100  # Convert to decimal
        with col2:
            partner_social_security = st.number_input("Partner's Social Security", value=1500 * 12, step=1000)
            partner_withdrawal_start_age = st.number_input("Partner's Withdrawal Start Age", value=65)

    # Tab 5: Healthcare Costs
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            self_healthcare_cost = st.number_input("Self Healthcare Cost (Annual)", value=5000, step=1000)
            self_healthcare_start_age = st.number_input("Self Healthcare Start Age", value=retirement_age)
        with col2:
            partner_healthcare_cost = st.number_input("Partner Healthcare Cost (Annual)", value=5000, step=1000)
            partner_healthcare_start_age = st.number_input("Partner Healthcare Start Age", value=partner_retirement_age)

    # Tab 6: Market Returns
    with tab6:
        col1, col2 = st.columns(2)
        with col1:
            stock_return_mean = st.number_input("Stock Return Mean (%)", value=10.10, step=0.25) / 100  # Convert to decimal
            bond_return_mean = st.number_input("Bond Return Mean (%)", value=3.9, step=0.25) / 100  # Convert to decimal
            simulations = st.number_input("Number of Simulations", value=1000, step=1000)
        with col2:
            stock_return_std = st.number_input("Stock Return Std Dev (%)", value=19.60, step=0.25) / 100  # Convert to decimal
            bond_return_std = st.number_input("Bond Return Std Dev (%)", value=1.166, step=0.05) / 100  # Convert to decimal

    # Tab 7: Downsize
    with tab7:
        col1, col2 = st.columns(2)
        with col1:
            years_until_downsize = st.number_input("After how many years", value=0)
        with col2:
            residual_amount = st.number_input("Residual Amount", value=0, step=100000)

# Calculate earning years
earning_years = retirement_age - current_age
partner_earning_years = partner_retirement_age - partner_current_age

# Get the current year
current_year = datetime.now().year

# Monte Carlo Simulation
def monte_carlo_simulation(initial_savings, annual_earnings, partner_earnings, annual_expense, mortgage_payment,
                           mortgage_years_remaining, retirement_age, partner_retirement_age, 
                           annual_social_security, withdrawal_start_age, partner_social_security, 
                           partner_withdrawal_start_age, self_healthcare_cost, self_healthcare_start_age,
                           partner_healthcare_cost, stock_percentage, bond_percentage, 
                           stock_return_mean, bond_return_mean, stock_return_std, bond_return_std, 
                           simulations, tax_rate, cola_rate, inflation_mean, inflation_std, annual_expense_decrease):
    
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
                'Self Earnings (before tax)': self_income / (1 - tax_rate) ,
                'Partner Earnings (before tax)': partner_income / (1 - tax_rate),
                'Self Social Security': self_ss,
                'Partner Social Security': partner_ss,
                'Total Earnings (before tax)': total_earnings_before_tax,
                'Investment Return': investment_return,
                'Yearly Expense': current_annual_expense,
                'Mortgage': mortgage,
                'Healthcare Expense': healthcare_costs,
                'Total Expense': annual_exp_with_mortgage,
                'Tax': tax,
                'Portfolio Draw': portfolio_draw,
                'Ending Portfolio Value': savings
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

# Run the simulation
success_count, failure_count, cash_flow_10th, cash_flow_50th, cash_flow_90th = monte_carlo_simulation(
    initial_savings, annual_earnings, partner_earnings, annual_expense, mortgage_payment,
    mortgage_years_remaining, retirement_age, partner_retirement_age, 
    annual_social_security, withdrawal_start_age, partner_social_security, 
    partner_withdrawal_start_age, self_healthcare_cost, self_healthcare_start_age,
    partner_healthcare_cost, stock_percentage, bond_percentage, 
    stock_return_mean, bond_return_mean, stock_return_std, bond_return_std, 
    simulations, tax_rate, cola_rate, inflation_mean, inflation_std, annual_expense_decrease
)

# Prepare data for display for each percentile
df_cashflow_10th = pd.DataFrame(cash_flow_10th)
df_cashflow_50th = pd.DataFrame(cash_flow_50th)
df_cashflow_90th = pd.DataFrame(cash_flow_90th)

# Function to format the DataFrame
def format_cashflow_dataframe(df):
    if df.empty:
        return df
    numeric_columns = [
        'Beginning Portfolio Value', 'Self Earnings (before tax)', 'Partner Earnings (before tax)',
        'Self Social Security', 'Partner Social Security', 'Total Earnings (before tax)',
        'Investment Return', 'Yearly Expense', 'Mortgage', 'Healthcare Expense',
        'Total Expense', 'Tax', 'Portfolio Draw', 'Ending Portfolio Value'
    ]
    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: f"{x:,.0f}")
    return df

# Format the DataFrames
df_cashflow_10th = format_cashflow_dataframe(df_cashflow_10th)
df_cashflow_50th = format_cashflow_dataframe(df_cashflow_50th)
df_cashflow_90th = format_cashflow_dataframe(df_cashflow_90th)

# Display success and failure rates
total_simulations = success_count + failure_count
success_rate = (success_count / total_simulations) * 100 if total_simulations > 0 else 0
failure_rate = (failure_count / total_simulations) * 100 if total_simulations > 0 else 0

st.write("# Simulation Results")
st.markdown(f"<p style='font-size: 36px; color: green; display: inline; margin-right: 50px;'>Success Rate: {success_rate:.0f}%</p>"
            f"<p style='font-size: 36px; color: red; display: inline;margin-right: 50px;'>Failure Rate: {failure_rate:.0f}%</p>", unsafe_allow_html=True)

# Display the DataFrames for each percentile
st.write("### Yearly Cash Flow Summary (10th Percentile Simulation)")
st.dataframe(df_cashflow_10th)

st.write("### Yearly Cash Flow Summary (50th Percentile Simulation)")
st.dataframe(df_cashflow_50th)

st.write("### Yearly Cash Flow Summary (90th Percentile Simulation)")
st.dataframe(df_cashflow_90th)

# Create a container for the charts
with st.container():
    st.header("Retirement Ending Savings Over Time")
    
    # Plotting the results using Streamlit's line chart for the 50th percentile
    st.line_chart(df_cashflow_50th.set_index('Year')['Ending Portfolio Value'].str.replace(',', '').astype(float))
