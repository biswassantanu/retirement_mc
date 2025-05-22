import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import math 
import plotly.graph_objs as go
import altair as alt

from helpers.linear_indicator import create_linear_indicator
from helpers.balance_display import display_balances
from helpers.inputs_to_df import create_parameters_dataframe

from helpers.styling import tab_style_css
from helpers.styling import button_style_css
from helpers.styling import download_button_style_css
from helpers.styling import remove_top_white_space
from helpers.styling import file_uploader_style_css

from simulations.simulation_mc import monte_carlo_simulation


# Set Streamlit to use full-width layout
st.set_page_config(layout="wide")

# set button styles 
st.markdown(button_style_css, unsafe_allow_html=True)
st.markdown(download_button_style_css, unsafe_allow_html=True)
st.markdown(remove_top_white_space, unsafe_allow_html=True)
st.markdown(file_uploader_style_css, unsafe_allow_html=True)


current_year = datetime.now().year

# Streamlit Display
st.write("#### Retirement Analysis with Monte Carlo Simulation")

# Function to load parameters from a CSV file
def load_parameters_from_csv(uploaded_file):
    try:
        # Read the CSV file into a DataFrame
        params_df = pd.read_csv(uploaded_file)

        # Validate the DataFrame (check if all required columns are present)
        required_columns = [
            "current_age", "partner_current_age", "life_expectancy", "retirement_age",
            "partner_retirement_age", "initial_savings", "stock_percentage", "bond_percentage",
            "annual_earnings", "self_yearly_increase", "tax_rate", "partner_earnings", "partner_yearly_increase", 
            "annual_pension", "partner_pension", "self_pension_yearly_increase","partner_pension_yearly_increase", 
            "rental_start", "rental_end", "rental_amt", "rental_yearly_increase",           
            "annual_expense", "mortgage_payment", "inflation_mean",
            "annual_expense_decrease", "mortgage_years_remaining", "inflation_std",
            "annual_social_security", "withdrawal_start_age", "cola_rate",
            "partner_social_security", "partner_withdrawal_start_age",
            "self_healthcare_cost", "self_healthcare_start_age",
            "partner_healthcare_cost", "partner_healthcare_start_age",
            "stock_return_mean", "bond_return_mean", "simulations",
            "stock_return_std", "bond_return_std", "years_until_downsize",
            "residual_amount", "adjust_expense_year_1", "adjust_expense_amount_1",
            "adjust_expense_year_2", "adjust_expense_amount_2",
            "adjust_expense_year_3", "adjust_expense_amount_3",
            "one_time_year_1", "one_time_amount_1",
            "one_time_year_2", "one_time_amount_2",
            "one_time_year_3", "one_time_amount_3",
            "windfall_year_1", "windfall_amount_1",
            "windfall_year_2", "windfall_amount_2",
            "windfall_year_3", "windfall_amount_3", 
            "simulation_type"
        ]

        # Check if all required columns are present
        if not all(col in params_df.columns for col in required_columns):
            st.error("Uploaded file is missing one or more required columns.")
            return

        # Set the values in the form fields directly
        current_age = params_df["current_age"].iloc[0]
        partner_current_age = params_df["partner_current_age"].iloc[0]
        life_expectancy = params_df["life_expectancy"].iloc[0]
        retirement_age = params_df["retirement_age"].iloc[0]
        partner_retirement_age = params_df["partner_retirement_age"].iloc[0]
        initial_savings = params_df["initial_savings"].iloc[0]
        stock_percentage = params_df["stock_percentage"].iloc[0]
        bond_percentage = params_df["bond_percentage"].iloc[0]
        annual_earnings = params_df["annual_earnings"].iloc[0]
        self_yearly_increase = params_df["self_yearly_increase"].iloc[0]
        tax_rate = params_df["tax_rate"].iloc[0]
        partner_earnings = params_df["partner_earnings"].iloc[0]
        partner_yearly_increase = params_df["partner_yearly_increase"].iloc[0]
        annual_pension = params_df["annual_pension"].iloc[0]
        partner_pension = params_df["partner_pension"].iloc[0]
        self_pension_yearly_increase = params_df["self_pension_yearly_increase"].iloc[0]
        partner_pension_yearly_increase = params_df["partner_pension_yearly_increase"].iloc[0]
        rental_start = params_df["rental_start"].iloc[0]
        rental_end = params_df["rental_end"].iloc[0]
        rental_amt = params_df["rental_amt"].iloc[0]
        rental_yearly_increase = params_df["rental_yearly_increase"].iloc[0]
        annual_expense = params_df["annual_expense"].iloc[0]
        mortgage_payment = params_df["mortgage_payment"].iloc[0]
        inflation_mean = params_df["inflation_mean"].iloc[0]
        annual_expense_decrease = params_df["annual_expense_decrease"].iloc[0]
        mortgage_years_remaining = params_df["mortgage_years_remaining"].iloc[0]
        inflation_std = params_df["inflation_std"].iloc[0]
        annual_social_security = params_df["annual_social_security"].iloc[0]
        withdrawal_start_age = params_df["withdrawal_start_age"].iloc[0]
        cola_rate = params_df["cola_rate"].iloc[0]
        partner_social_security = params_df["partner_social_security"].iloc[0]
        partner_withdrawal_start_age = params_df["partner_withdrawal_start_age"].iloc[0]
        self_healthcare_cost = params_df["self_healthcare_cost"].iloc[0]
        self_healthcare_start_age = params_df["self_healthcare_start_age"].iloc[0]
        partner_healthcare_cost = params_df["partner_healthcare_cost"].iloc[0]
        partner_healthcare_start_age = params_df["partner_healthcare_start_age"].iloc[0]
        stock_return_mean = params_df["stock_return_mean"].iloc[0]
        bond_return_mean = params_df["bond_return_mean"].iloc[0]
        simulations = params_df["simulations"].iloc[0]
        stock_return_std = params_df["stock_return_std"].iloc[0]
        bond_return_std = params_df["bond_return_std"].iloc[0]
        years_until_downsize = params_df["years_until_downsize"].iloc[0]
        residual_amount = params_df["residual_amount"].iloc[0]
        adjust_expense_year_1 = params_df["adjust_expense_year_1"].iloc[0]
        adjust_expense_amount_1 = params_df["adjust_expense_amount_1"].iloc[0]
        adjust_expense_year_2 = params_df["adjust_expense_year_2"].iloc[0]
        adjust_expense_amount_2 = params_df["adjust_expense_amount_2"].iloc[0]
        adjust_expense_year_3 = params_df["adjust_expense_year_3"].iloc[0]
        adjust_expense_amount_3 = params_df["adjust_expense_amount_3"].iloc[0]
        one_time_year_1 = params_df["one_time_year_1"].iloc[0]
        one_time_amount_1 = params_df["one_time_amount_1"].iloc[0]
        one_time_year_2 = params_df["one_time_year_2"].iloc[0]
        one_time_amount_2 = params_df["one_time_amount_2"].iloc[0]
        one_time_year_3 = params_df["one_time_year_3"].iloc[0]
        one_time_amount_3 = params_df["one_time_amount_3"].iloc[0]
        windfall_year_1 = params_df["windfall_year_1"].iloc[0]
        windfall_amount_1 = params_df["windfall_amount_1"].iloc[0]
        windfall_year_2 = params_df["windfall_year_2"].iloc[0]
        windfall_amount_2 = params_df["windfall_amount_2"].iloc[0]
        windfall_year_3 = params_df["windfall_year_3"].iloc[0]
        windfall_amount_3 = params_df["windfall_amount_3"].iloc[0]
        simulation_type = params_df["simulation_type"].iloc[0]

        # Set the values in the form fields directly
        return {
            "current_age": current_age,
            "partner_current_age": partner_current_age,
            "life_expectancy": life_expectancy,
            "retirement_age": retirement_age,
            "partner_retirement_age": partner_retirement_age,
            "initial_savings": initial_savings,
            "stock_percentage": stock_percentage,
            "bond_percentage": bond_percentage,
            "annual_earnings": annual_earnings,
            "self_yearly_increase": self_yearly_increase,
            "tax_rate": tax_rate,
            "partner_earnings": partner_earnings,
            "partner_yearly_increase": partner_yearly_increase,
            "annual_pension": annual_pension,
            "partner_pension": partner_pension,
            "self_pension_yearly_increase": self_pension_yearly_increase,
            "partner_pension_yearly_increase": partner_pension_yearly_increase,
            "rental_start": rental_start,
            "rental_end": rental_end,
            "rental_amt": rental_amt,
            "rental_yearly_increase": rental_yearly_increase,
            "annual_expense": annual_expense,
            "mortgage_payment": mortgage_payment,
            "inflation_mean": inflation_mean,
            "annual_expense_decrease": annual_expense_decrease,
            "mortgage_years_remaining": mortgage_years_remaining,
            "inflation_std": inflation_std,
            "annual_social_security": annual_social_security,
            "withdrawal_start_age": withdrawal_start_age,
            "cola_rate": cola_rate,
            "partner_social_security": partner_social_security,
            "partner_withdrawal_start_age": partner_withdrawal_start_age,
            "self_healthcare_cost": self_healthcare_cost,
            "self_healthcare_start_age": self_healthcare_start_age,
            "partner_healthcare_cost": partner_healthcare_cost,
            "partner_healthcare_start_age": partner_healthcare_start_age,
            "stock_return_mean": stock_return_mean,
            "bond_return_mean": bond_return_mean,
            "simulations": simulations,
            "stock_return_std": stock_return_std,
            "bond_return_std": bond_return_std,
            "years_until_downsize": years_until_downsize,
            "residual_amount": residual_amount,
            "adjust_expense_year_1": adjust_expense_year_1,
            "adjust_expense_amount_1": adjust_expense_amount_1,
            "adjust_expense_year_2": adjust_expense_year_2,
            "adjust_expense_amount_2": adjust_expense_amount_2,
            "adjust_expense_year_3": adjust_expense_year_3,
            "adjust_expense_amount_3": adjust_expense_amount_3,
            "one_time_year_1": one_time_year_1,
            "one_time_amount_1": one_time_amount_1,
            "one_time_year_2": one_time_year_2,
            "one_time_amount_2": one_time_amount_2,
            "one_time_year_3": one_time_year_3,
            "one_time_amount_3": one_time_amount_3,
            "windfall_year_1": windfall_year_1,
            "windfall_amount_1": windfall_amount_1,
            "windfall_year_2": windfall_year_2,
            "windfall_amount_2": windfall_amount_2,
            "windfall_year_3": windfall_year_3,
            "windfall_amount_3": windfall_amount_3,
            "simulation_type" : simulation_type
        }

    except Exception as e:
        st.error(f"Error loading parameters: {e}")


# Add upload button for the CSV file
uploaded_file = st.file_uploader("Upload previously downloaded simulation parameters", type=["csv"])

parameters = None
if uploaded_file is not None:
    parameters = load_parameters_from_csv(uploaded_file)

# Put the tabs inside a container with fixed height
with st.container(height=260, border=None):

    # Set the tab styles 
    st.markdown(tab_style_css, unsafe_allow_html=True)

    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs([
            ":material/group: Profile", 
            ":material/savings: Savings", 
            ":material/paid: Income", 
            ":material/account_balance: Taxes", 
            ":material/shopping_cart: Expense", 
            ":material/verified_user: Social Security", 
            ":material/local_hospital: Healthcare", 
            ":material/finance_mode: Market Returns", 
            ":material/house: Downsize", 
            ":material/tune: Adjust Exp.", 
            ":material/checkbook: One Time", 
            ":material/money_bag: Windfall"])  

    # Tab 1: Personal Details
    with tab1:
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            current_age = st.number_input("Current Age", value=parameters["current_age"] if parameters else 50)
            partner_current_age = st.number_input("Partner's Current Age", value=parameters["partner_current_age"] if parameters else 50)
        with col2:
            retirement_age = st.number_input("Retirement Age", value=parameters["retirement_age"] if parameters else 60)
            partner_retirement_age = st.number_input("Partner's Retirement Age", value=parameters["partner_retirement_age"] if parameters else 58)
        with col3:
            life_expectancy = st.number_input("Life Expectancy", value=parameters["life_expectancy"] if parameters else 92)

        # Calculate the range of valid years based on current age and life expectancy
        start_year = current_year 
        end_year = current_year + (life_expectancy - current_age)
        # Create a list of years for drops downs 
        years = list(range(start_year, end_year + 1))

    # Tab 2: Investment and Savings
    with tab2:
        col1, col2, col3, col4 = st.columns([3,1,3,4])
        with col1:
            initial_savings = st.number_input("Current Total Portfolio", value=parameters["initial_savings"] if parameters else 500000, step=100000)
        with col3:
            stock_percentage = st.slider("Percentage of Stock Investment (%)", min_value=0, max_value=100, value=parameters["stock_percentage"] if parameters else 60)
            bond_percentage = 100 - stock_percentage  # Calculate bond percentage

    # Tab 3: Income
    with tab3:
        col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
        with col1:
            annual_earnings = st.number_input("Annual Earnings", value=parameters["annual_earnings"] if parameters else 100000, step=5000)
            partner_earnings = st.number_input("Partner's Annual Earnings", value=parameters["partner_earnings"] if parameters else 100000, step=5000)

        with col2:
            self_yearly_increase = st.number_input("Self Yearly Increase (%)", value=parameters["self_yearly_increase"] * 100 if parameters else 3.0, step=0.5) / 100  # Convert to decimal
            partner_yearly_increase = st.number_input("Partner Yearly Increase (%)", value=parameters["partner_yearly_increase"] * 100 if parameters else 3.0, step=0.5) / 100  # Convert to decimal

        with col3: 
            annual_pension = st.number_input("Self Annual Pension", value=parameters["annual_pension"] if parameters else 000, step=1000)
            partner_pension = st.number_input("Partner's Annual Pension", value=parameters["partner_pension"] if parameters else 000, step=1000)

        with col4: 
            self_pension_yearly_increase = st.number_input("Self Pension Increase (%)", value=parameters["self_yearly_increase"] * 100 if parameters else 0.0, step=0.5) / 100  # Convert to decimal
            partner_pension_yearly_increase = st.number_input("Partner Pension Increase (%)", value=parameters["partner_yearly_increase"] * 100 if parameters else 0.0, step=0.5) / 100  # Convert to decimal

        with col5: 
            rental_start = st.selectbox("Rental Starts", years, index=0 if parameters is None else years.index(parameters["rental_start"]))
            rental_end = st.selectbox("Rental Ends", years, index=0 if parameters is None else years.index(parameters["rental_end"]))

        with col6: 
            rental_amt = st.number_input("Annual Rental Amount", value=parameters["rental_amt"] if parameters else 000, step=1000)
            rental_yearly_increase = st.number_input("Rental Yearly Increase (%)", value=parameters["rental_yearly_increase"] * 100 if parameters else 4.0, step=0.5) / 100  # Convert to decimal

    # Tab 4: Taxes
    with tab4:
        col1, col2, col3, col4 = st.columns([3,1,3,4])
        with col1:
            tax_rate = st.number_input("Tax Rate (%)", value=parameters["tax_rate"] * 100 if parameters else 10.0, step=1.0) / 100  # Convert to decimal
 
    # Tab 5: Expense
    with tab5:
        col1, col2 , col3, col4 = st.columns([1,1,1, 1])
        with col1:
            annual_expense = st.number_input("Annual Expense", value=parameters["annual_expense"] if parameters else 5000 * 12, step=2000)
            mortgage_payment = st.number_input("Yearly Mortgage", value=parameters["mortgage_payment"] if parameters else 24000, step=2000)
        with col2:
            annual_expense_decrease = st.number_input("Annual Decrease post Retirement (Smile *) (%)", value=parameters["annual_expense_decrease"] * 100 if parameters else 0.5, step=0.05) / 100  # Convert to decimal
            mortgage_years_remaining = st.number_input("Mortgage Years Remaining", value=parameters["mortgage_years_remaining"] if parameters else 25)
        with col3: 
            inflation_mean = st.number_input("Inflation Mean (%)", value=parameters["inflation_mean"] * 100 if parameters else 2.5) / 100  # Convert to decimal
            inflation_std = st.number_input("Inflation Std Dev (%)", value=parameters["inflation_std"] * 100 if parameters else 1.0) / 100  # Convert to decimal       
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            st.write ('###### * Smile : Research shows household expenses decrease about 1% year over year in retirement and then can increase towards end of life due to healthcare cost')

    # Tab 6: Social Security 
    with tab6:
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            annual_social_security = st.number_input("Social Security", value=parameters["annual_social_security"] if parameters else 2000 * 12, step=1000)
            partner_social_security = st.number_input("Partner's Social Security", value=parameters["partner_social_security"] if parameters else 2000 * 12, step=1000)
        with col2:
            withdrawal_start_age = st.number_input("Withdrawal Start Age (Self)", value=parameters["withdrawal_start_age"] if parameters else 67)
            partner_withdrawal_start_age = st.number_input("Partner's Withdrawal Start Age", value=parameters["partner_withdrawal_start_age"] if parameters else 65)
        with col3:
            cola_rate = st.number_input("COLA Rate (%)", value=parameters["cola_rate"] * 100 if parameters else 1.50) / 100  # Convert to decimal

    # Tab 7: Healthcare Costs
    with tab7:
        col1, col2, col3, col4 = st.columns([1,1,1, 1])
        with col1:
            self_healthcare_cost = st.number_input("Self Bridge Healthcare Cost (Annual)", value=parameters["self_healthcare_cost"] if parameters else 5000, step=1000)
            self_healthcare_start_age = st.number_input("Self Healthcare Bridge Start Age", value=parameters["self_healthcare_start_age"] if parameters else retirement_age)
        with col2:
            partner_healthcare_cost = st.number_input("Partner Bridge Healthcare Cost (Annual)", value=parameters["partner_healthcare_cost"] if parameters else 5000, step=1000)
            partner_healthcare_start_age = st.number_input("Partner Healthcare Bridge Start Age", value=parameters["partner_healthcare_start_age"] if parameters else partner_retirement_age)
        with col4:
            st.write ('###### Bridge cost is amount needed to self fund medical insurance after retirement before Medicare starts at 65')

    # Tab 8: Market Returns
    with tab8:
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            stock_return_mean = st.number_input("Stock Return Mean (%)", value=parameters["stock_return_mean"] * 100 if parameters else 7.00, step=0.25) / 100  # Convert to decimal
            bond_return_mean = st.number_input("Bond Return Mean (%)", value=parameters["bond_return_mean"] * 100 if parameters else 3.5, step=0.25) / 100  # Convert to decimal
        with col2:
            stock_return_std = st.number_input("Stock Return Std Dev (%)", value=parameters["stock_return_std"] * 100 if parameters else 16.00, step=0.25) / 100  # Convert to decimal
            bond_return_std = st.number_input("Bond Return Std Dev (%)", value=parameters["bond_return_std"] * 100 if parameters else 4.5, step=0.05) / 100  # Convert to decimal
        with col3: 
            simulations = st.number_input("Number of Simulations", value=parameters["simulations"] if parameters else 1000, step=1000)
        with col4: 
            # Check if parameters is None and set default simulation type
            if parameters is None:
                default_simulation_type = "Normal Distribution"
            else:
                default_simulation_type = parameters.get("simulation_type", "Normal Distribution")  # Default to "Normal Distribution" if not found
                
                # Ensure the default is valid
                if default_simulation_type not in ["Normal Distribution", "Students-T Distribution", "Empirical Distribution"]:
                    default_simulation_type = "Normal Distribution"
            
            # Add radio buttons for Simulation Type
            simulation_type = st.radio(
                "Simulation Type", 
                options=["Normal Distribution", "Students-T Distribution", "Empirical Distribution"], 
                index=["Normal Distribution", "Students-T Distribution",  "Empirical Distribution"].index(default_simulation_type)
            )

    # Tab 9: Downsize
    with tab9:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            years_until_downsize = st.number_input("After how many years?", value=parameters["years_until_downsize"] if parameters else 0)
        with col2: 
            residual_amount = st.number_input("Net Addition to Retirement Savings", value=parameters["residual_amount"] if parameters else 0, step=100000)

    # Tab 10: Adjust Recurring Expenses
    with tab10:      
        # Entry 1
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # Adjust column widths as needed
        with col1:
            adjust_expense_year_1 = st.selectbox("Year of Adjustment 1", years, index=0 if parameters is None else years.index(parameters["adjust_expense_year_1"]))
            adjust_expense_amount_1 = st.number_input("Adjustment Amount 1 ", value=parameters["adjust_expense_amount_1"] if parameters else 0, step=2000)
        with col2:
            adjust_expense_year_2 = st.selectbox("Year of Adjustment 2", years, index=0 if parameters is None else years.index(parameters["adjust_expense_year_2"]))
            adjust_expense_amount_2 = st.number_input("Adjustment Amount 2 ", value=parameters["adjust_expense_amount_2"] if parameters else 0, step=2000)       
        with col3:
            adjust_expense_year_3 = st.selectbox("Year of Adjustment 3", years, index=0 if parameters is None else years.index(parameters["adjust_expense_year_3"]))
            adjust_expense_amount_3 = st.number_input("Adjustment Amount 3 ", value=parameters["adjust_expense_amount_3"] if parameters else 0, step=2000)
        with col4: 
            st.markdown("<br>", unsafe_allow_html=True)
            st.write ('###### These adjustments get carried forward. You can enter negative amount')
 
    # Tab 11: One-Time Expenses
    with tab11:        
        # Entry 1
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # Adjust column widths as needed
        with col1:
            one_time_year_1 = st.selectbox("Year of One-Time Expense 1", years, index=0 if parameters is None else years.index(parameters["one_time_year_1"]))
            one_time_amount_1 = st.number_input("One-Time Expense Amount 1 ", value=parameters["one_time_amount_1"] if parameters else 0, step=5000)
        with col2:
            one_time_year_2 = st.selectbox("Year of One-Time Expense 2", years, index=0 if parameters is None else years.index(parameters["one_time_year_2"]))
            one_time_amount_2 = st.number_input("One-Time Expense Amount 2 ", value=parameters["one_time_amount_2"] if parameters else 0, step=5000)
        with col3:
            one_time_year_3 = st.selectbox("Year of One-Time Expense 3", years, index=0 if parameters is None else years.index(parameters["one_time_year_3"]))
            one_time_amount_3 = st.number_input("One-Time Expense Amount 3 ", value=parameters["one_time_amount_3"] if parameters else 0, step=5000)
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            st.write ('###### You can enter negative amount')

    # Tab 12: Windfalls
    with tab12:
        col1, col2, col3, col4  = st.columns([1, 1, 1, 1])  # Adjust column widths as needed
        with col1:
            windfall_year_1 = st.selectbox("Year of Windfall 1", years, index=0 if parameters is None else years.index(parameters["windfall_year_1"]))
            windfall_amount_1 = st.number_input("Windfall Amount 1 ", value=parameters["windfall_amount_1"] if parameters else 0, step=5000)
        with col2:
            windfall_year_2 = st.selectbox("Year of Windfall 2", years, index=0 if parameters is None else years.index(parameters["windfall_year_2"]))
            windfall_amount_2 = st.number_input("Windfall Amount 2 ", value=parameters["windfall_amount_2"] if parameters else 0, step=5000)
        with col3:
            windfall_year_3 = st.selectbox("Year of Windfall 3", years, index=0 if parameters is None else years.index(parameters["windfall_year_3"]))
            windfall_amount_3 = st.number_input("Windfall Amount 3 ", value=parameters["windfall_amount_3"] if parameters else 0, step=5000)


# Create download parameters feature 
params_df = create_parameters_dataframe(
    current_age, partner_current_age, life_expectancy, retirement_age,
    partner_retirement_age, initial_savings, stock_percentage, bond_percentage,
    annual_earnings, self_yearly_increase, tax_rate, partner_earnings, partner_yearly_increase, 
    annual_pension, partner_pension, self_pension_yearly_increase, partner_pension_yearly_increase,
    rental_start, rental_end, rental_amt, rental_yearly_increase, 
    annual_expense, mortgage_payment, inflation_mean,
    annual_expense_decrease, mortgage_years_remaining, inflation_std,
    annual_social_security, withdrawal_start_age, cola_rate,
    partner_social_security, partner_withdrawal_start_age,
    self_healthcare_cost, self_healthcare_start_age,
    partner_healthcare_cost, partner_healthcare_start_age,
    stock_return_mean, bond_return_mean, simulations,
    stock_return_std, bond_return_std, years_until_downsize,
    residual_amount, adjust_expense_year_1, adjust_expense_amount_1,
    adjust_expense_year_2, adjust_expense_amount_2,
    adjust_expense_year_3, adjust_expense_amount_3,
    one_time_year_1, one_time_amount_1,
    one_time_year_2, one_time_amount_2,
    one_time_year_3, one_time_amount_3,
    windfall_year_1, windfall_amount_1,
    windfall_year_2, windfall_amount_2,
    windfall_year_3, windfall_amount_3,
    simulation_type
)

# Convert DataFrame to CSV format
csv = params_df.to_csv(index=False)  # Convert DataFrame to CSV format

# # Add download button for the CSV file
# st.download_button(
#     label="Download Simulation Parameters",
#     data=csv,
#     type='primary',
#     file_name='retirement_parameters.csv',
#     mime='text/csv',
#     icon=":material/download:",
# )

# Create two columns for the buttons
col1, col2, col3, col4 = st.columns([1,1,2,3])

# Add download button for the CSV file in the first column
with col1:
    st.download_button(
        label="Download Simulation Parameters",
        data=csv,
        type='primary',
        file_name='retirement_parameters.csv',
        mime='text/csv',
        icon=":material/download:",
    )
# Create a button to run the simulation in the second column
with col3:
    run_simulation = st.button("Run Simulation", type='primary', icon=":material/rocket_launch:")

with col4: 
    auto_run_simulation = st.checkbox("Run Automatically", value=False)


# Calculate earning years
earning_years = retirement_age - current_age
partner_earning_years = partner_retirement_age - partner_current_age

# packe Adjustments
adjust_expense_years = [adjust_expense_year_1, adjust_expense_year_2, adjust_expense_year_3]
adjust_expense_amounts = [adjust_expense_amount_1, adjust_expense_amount_2, adjust_expense_amount_3]

# Pack One-Time Expenses
one_time_years = [one_time_year_1, one_time_year_2, one_time_year_3]
one_time_amounts = [one_time_amount_1, one_time_amount_2, one_time_amount_3]

# Pack Windfalls
windfall_years = [windfall_year_1, windfall_year_2, windfall_year_3]
windfall_amounts = [windfall_amount_1, windfall_amount_2, windfall_amount_3]

# Initialize variables to store results
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = {
        'success_count': 0,
        'failure_count': 0,
        'sorted_cash_flows': []
    }
    # Set a flag to indicate if the simulation has been run
    st.session_state.simulation_initialized = False


# Run the simulation only when the button is pressed
if (not st.session_state.simulation_initialized) or auto_run_simulation or run_simulation:
    # Run the simulation
    success_count, failure_count, sorted_cash_flows = monte_carlo_simulation(
        current_age, partner_current_age, life_expectancy, initial_savings, 
        annual_earnings, partner_earnings, self_yearly_increase, partner_yearly_increase,
        annual_pension, partner_pension, self_pension_yearly_increase, partner_pension_yearly_increase,
        rental_start, rental_end, rental_amt, rental_yearly_increase, 
        annual_expense, mortgage_payment,
        mortgage_years_remaining, retirement_age, partner_retirement_age, 
        annual_social_security, withdrawal_start_age, partner_social_security, 
        partner_withdrawal_start_age, self_healthcare_cost, self_healthcare_start_age, partner_healthcare_start_age,
        partner_healthcare_cost, stock_percentage, bond_percentage, 
        stock_return_mean, bond_return_mean, stock_return_std, bond_return_std, 
        simulations, tax_rate, cola_rate, inflation_mean, inflation_std, annual_expense_decrease, 
        years_until_downsize, residual_amount, 
        adjust_expense_years, adjust_expense_amounts,  
        one_time_years, one_time_amounts,             
        windfall_years, windfall_amounts, 
        simulation_type        
    )

        # Store the results in session state
    st.session_state.simulation_results = {
        'success_count': success_count,
        'failure_count': failure_count,
        'sorted_cash_flows': sorted_cash_flows
    }

    # Set a flag to indicate if the simulation has been run
    st.session_state.simulation_initialized = True

# Extract results from session state for display
success_count = st.session_state.simulation_results['success_count']
failure_count = st.session_state.simulation_results['failure_count']
sorted_cash_flows = st.session_state.simulation_results['sorted_cash_flows']

# Calculate the indices for the percentiles
n = len(sorted_cash_flows)
tenth_index = int(0.1 * n)
twentyfifth_index = int(0.25 * n)
fiftieth_index = int(0.5 * n)
seventyfifth_index = int(0.75 * n)

# Get the simulation IDs for the 10th, 50th, and 90th percentiles
simulation_id_10th = sorted_cash_flows[tenth_index - 1][-1]['Simulation ID']  # Last simulation in the 10th percentile
simulation_id_25th = sorted_cash_flows[twentyfifth_index - 1][-1]['Simulation ID']  # Last simulation in the 10th percentile
simulation_id_50th = sorted_cash_flows[fiftieth_index - 1][-1]['Simulation ID']  # Last simulation in the 50th percentile
simulation_id_75th = sorted_cash_flows[seventyfifth_index - 1][-1]['Simulation ID']  # Last simulation in the 90th percentile



# Filter all cash flows based on the identified simulation IDs
df_cashflow_10th = pd.DataFrame([entry for simulation in sorted_cash_flows if simulation[0]['Simulation ID'] == simulation_id_10th for entry in simulation])
df_cashflow_25th = pd.DataFrame([entry for simulation in sorted_cash_flows if simulation[0]['Simulation ID'] == simulation_id_25th for entry in simulation])
df_cashflow_50th = pd.DataFrame([entry for simulation in sorted_cash_flows if simulation[0]['Simulation ID'] == simulation_id_50th for entry in simulation])
df_cashflow_75th = pd.DataFrame([entry for simulation in sorted_cash_flows if simulation[0]['Simulation ID'] == simulation_id_75th for entry in simulation])

# Function to format the DataFrame
def format_cashflow_dataframe(df):
    if df.empty:
        return df

    # Format Amount Columns
    numeric_columns = [
        'Beginning Portfolio Value', 'Self Gross Earning', 'Partner Gross Earning',
        'Self Social Security', 'Partner Social Security', 'Gross Earnings', 'Combined Social Security',
        'Investment Return', 'Downsize Proceeds', 'Mortgage', 'Healthcare Expense', 'Self Health Expense',  'Partner Health Expense',
        'Self Pension', 'Partner Pension', 'Rental Income',
        'Total Expense', 'Tax', 'Portfolio Draw', 'Ending Portfolio Value', 'At Constant Currency', 'Yearly Expense Adj', 'One Time Expense', 'Windfall Amt'
    ]

    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: f"{x:,.0f}")

    # Format % Columns 
    percent_columns = [
        'Investment Return %', 
        'Drawdown %' 
    ]
    for col in percent_columns:
        df[col] = df[col].apply(lambda x: f"{x * 100:.2f}%")  # Multiply by 100 and format to 2 decimal places


    return df

# store the unformatted dfs 
df_cashflow_10th_value = df_cashflow_10th.copy()
df_cashflow_25th_value = df_cashflow_25th.copy()
df_cashflow_50th_value = df_cashflow_50th.copy()
df_cashflow_75th_value = df_cashflow_75th.copy()

# Format the DataFrames
df_cashflow_10th = format_cashflow_dataframe(df_cashflow_10th)
df_cashflow_25th = format_cashflow_dataframe(df_cashflow_25th)
df_cashflow_50th = format_cashflow_dataframe(df_cashflow_50th)
df_cashflow_75th = format_cashflow_dataframe(df_cashflow_75th)

# Display success and failure rates
total_simulations = success_count + failure_count
success_rate = (success_count / total_simulations) * 100 if total_simulations > 0 else 0
failure_rate = (failure_count / total_simulations) * 100 if total_simulations > 0 else 0

# Extract the end-of-period balances for the 10th, 50th, and 90th percentiles
end_balance_10th = df_cashflow_10th['Ending Portfolio Value'].iloc[-1]  # Last entry for 10th percentile
end_balance_25th = df_cashflow_25th['Ending Portfolio Value'].iloc[-1]  # Last entry for 10th percentile
end_balance_50th = df_cashflow_50th['Ending Portfolio Value'].iloc[-1]  # Last entry for 50th percentile
end_balance_75th = df_cashflow_75th['Ending Portfolio Value'].iloc[-1]  # Last entry for 90th percentile

# Convert balances to millions and format to 2 decimal places
end_balance_10th_millions = float(end_balance_10th.replace(',', '')) / 1_000_000
end_balance_25th_millions = float(end_balance_25th.replace(',', '')) / 1_000_000
end_balance_50th_millions = float(end_balance_50th.replace(',', '')) / 1_000_000
end_balance_75th_millions = float(end_balance_75th.replace(',', '')) / 1_000_000


# Display linear metrics indicator
st.markdown(create_linear_indicator(math.floor(success_rate), "Success Rate: "), unsafe_allow_html=True)

# Calculate the length of the plan
years = life_expectancy - current_age + 1

# Prepare the data for the grid
data = {
    "Ending Balance": ["Future Currency Value", "Today's Currency Value"],
    "Worst Case": [
        f"{end_balance_10th_millions:,.2f}M",
        f"{end_balance_10th_millions / ((1 + inflation_mean) ** years):,.2f}M"
    ],
    "Below Market": [  # New label for 25th percentile
        f"{end_balance_25th_millions:,.2f}M",  # Assuming you have this variable defined
        f"{end_balance_25th_millions / ((1 + inflation_mean) ** years):,.2f}M"
    ],
    "Most Likely": [
        f"{end_balance_50th_millions:,.2f}M",
        f"{end_balance_50th_millions / ((1 + inflation_mean) ** years):,.2f}M"
    ],
    "Best Case": [
        f"{end_balance_75th_millions:,.2f}M",
        f"{end_balance_75th_millions / ((1 + inflation_mean) ** years):,.2f}M"
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Function to apply conditional formatting
def color_negative_red(val):
    color = 'red' if float(val[:-1]) < 0 else 'green'  # Convert to float for comparison
    return f'color: {color}; font-weight: bold;'

# Apply conditional formatting to the DataFrame
styled_df = df.style.map(color_negative_red, subset=["Worst Case", "Below Market", "Most Likely", "Best Case"])

# Increase font size using HTML
styled_df.set_table_attributes('style="font-size: 18px; width: 60%;"')
# Hide the index
styled_df = styled_df.hide(axis="index")
# Display the DataFrame in a grid format without index
st.markdown(styled_df.to_html(index=False, escape=False), unsafe_allow_html=True)

# Function to convert formatted string to numerical value
def convert_to_numeric(value):
    return float(value.replace('$', '').replace(',', ''))

# Function to apply conditional styling
def highlight_columns(s):
    styles = []
    for value in s:
        numeric_value = convert_to_numeric(value)
        if numeric_value > 0:
            styles.append('background-color: #ECFBEC; font-weight: bold;')  # Green background for positive values
        else:
            styles.append('background-color: #F9DFDF; font-weight: bold;')    # Red background for negative values
    return styles

st.markdown("<br>", unsafe_allow_html=True)


st.write("#### Analysis Details ")
st.markdown("<br>", unsafe_allow_html=True)

####################################


def create_cash_flow_tab(df_cashflow, df_cashflow_value, title):
    # Apply the styling to specific columns
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### " + title + " details")

    styled_df = df_cashflow.style.apply(highlight_columns, subset=['Beginning Portfolio Value', 'Ending Portfolio Value'])
    tab1, tab2, tab3 = st.tabs([
            ":material/attach_money: Portfolio Balance", 
            ":material/bar_chart: Market Returns", 
            ":material/mintmark: Withdrawal Rate"])

    positive_color = "#55AA55"
    negative_color = "#DD5050"



    with tab1: 
        # Portfolio Balance
        chart = alt.Chart(df_cashflow_value).mark_bar().encode(
            x='Year:O',
            y='Ending Portfolio Value:Q',
            color=alt.condition(
                alt.datum['Ending Portfolio Value'] < 0,  # Condition for negative values
                alt.value(negative_color),                   # Color for negative values
                alt.value(positive_color)                   # Color for positive values
            )
        ).properties(
            title='Portfolio Balance Over Time'
        )
        # Display the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)

    with tab2: 
        # Chart for portfolio return
        chart = alt.Chart(df_cashflow_value).mark_bar().encode(
            x='Year:O',
            y=alt.Y('Investment Return %:Q', title='Portfolio Return %', axis=alt.Axis(format='%')),
            color=alt.condition(
                alt.datum['Investment Return %'] < 0,  # Condition for negative values
                alt.value(negative_color),              # Color for negative values
                alt.value(positive_color)              # Color for positive values
            )
        ).properties(
            title='Portfolio Return % by Year'
        ).transform_calculate(
            'ScaledDrawdown', 'datum["Investment Return %"] * 100'  # Scale the Drawdown % by 100
        )

        # Create text labels for the bars, using the transformed field
        text = chart.mark_text(
            align='center',
            baseline='middle'
        ).encode(
            text=alt.Text('ScaledDrawdown:Q', format='.2f')  # Display the scaled percentage
        )

        textAbove = text.transform_filter( alt.datum['Investment Return %'] > 0).mark_text(
            align='center',
            baseline='middle',
            fontSize=10,
            dy=-10
        )

        textBelow = text.transform_filter( alt.datum['Investment Return %'] <= 0).mark_text(
            align='center',
            baseline='middle',
            fontSize=10,
            dy=10
        )

        # Combine the bar chart and text labels
        final_chart = chart + textAbove + textBelow

        # Display the chart in Streamlit
        st.altair_chart(final_chart, use_container_width=True)

    with tab3: 
        # Create the chart with inline transformation to scale values by 100
        chart = alt.Chart(df_cashflow_value).mark_bar().encode(
            x='Year:O',
            y=alt.Y('Drawdown %:Q', title='Withdrawal Rate %', axis=alt.Axis(format='%')),
            color=alt.condition(
                alt.datum['Drawdown %'] < 0,  # Condition for negative values
                alt.value(negative_color),              # Color for negative values
                alt.value(positive_color)              # Color for positive values
            )
        ).properties(
            title='Withdrawal Rate % by Year'
        ).transform_calculate(
            'ScaledDrawdown', 'datum["Drawdown %"] * 100'  # Scale the Drawdown % by 100
        )

        # Create text labels for the bars, using the transformed field
        text = chart.mark_text(
            align='center',
            baseline='middle'
        ).encode(
            text=alt.Text('ScaledDrawdown:Q', format='.2f')  # Display the scaled percentage
        )

        textAbove = text.transform_filter( alt.datum['Drawdown %'] > 0).mark_text(
            align='center',
            baseline='middle',
            fontSize=10,
            dy=-10
        )

        textBelow = text.transform_filter( alt.datum['Drawdown %'] <= 0).mark_text(
            align='center',
            baseline='middle',
            fontSize=10,
            dy=10
        )

        # Combine the bar chart and text labels
        final_chart = chart + textAbove + textBelow

        # Display the chart in Streamlit
        st.altair_chart(final_chart, use_container_width=True)

    # Display detailed cashflow 
    st.markdown("###### Cashflow ")   
    st.dataframe(styled_df, hide_index=True, use_container_width=True)


# Create tabs for the cash flow summaries
tab_10th, tab_25th, tab_50th, tab_75th = st.tabs([
            ":material/sentiment_dissatisfied: Worst Case ", 
            ":material/avg_pace: Below Average", 
            ":material/speed: Most Likely ", 
            ":material/diamond: Best Case "])

# Tab for 10th Percentile
with tab_10th:
    create_cash_flow_tab(df_cashflow_10th, df_cashflow_10th_value, "10th Percentile")

# Tab for 25th Percentile
with tab_25th:
    create_cash_flow_tab(df_cashflow_25th, df_cashflow_25th_value, "25th Percentile")

# Tab for 50th Percentile
with tab_50th:
    create_cash_flow_tab(df_cashflow_50th, df_cashflow_50th_value, "50th Percentile")

# Tab for 75th Percentile
with tab_75th:
    create_cash_flow_tab(df_cashflow_75th, df_cashflow_75th_value, "75th Percentile")






    ######################################

