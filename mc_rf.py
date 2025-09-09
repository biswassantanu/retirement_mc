import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import math 
import plotly.graph_objs as go
import altair as alt
import time 
from typing import Dict, List, Tuple, Union, Any
import base64

# Import helpers
from helpers.linear_indicator import create_linear_indicator
from helpers.balance_display import display_balances
from helpers.inputs_to_df import create_parameters_dataframe
from helpers.styling import (tab_style_css, button_style_css, 
                           download_button_style_css, 
                           remove_top_white_space,
                           file_uploader_style_css)

# Import help texts 
from helpers.help_texts import (simulation_help_text, smile_help_text, 
                                living_expense_help_text, 
                                bridge_healthcare_help_text, healthcare_bridge_text,
                                tax_rate_both_working_help, tax_rate_one_retired_help, tax_rate_both_retired_help,
                                tax_calculation_disclaimer, 
                                adjust_expense_text, one_time_expense_text, windfall_text,
                                downsize_text, parameter_text,
                                auto_run_help_text,
                                stock_return_mean_help, stock_return_std_help, 
                                bond_return_mean_help, bond_return_std_help,
                                market_returns_note, 
                                stress_test_text, enable_sequence_risk_help,
                                seq_risk_years_help, seq_risk_returns_help, 
                                interpretation_guide_md,
                                disclaimer_text, help_document)

# Import simulation module with our new refactored function
from simulations.simulation_mc_rf import SimulationConfig, monte_carlo_simulation
from simulations.tax_master_data import contribution_limits


def main():
    """Main function to run the Streamlit app"""

    # Setup app configuration
    setup_app()

    st.write("###### Enter your financial information in the tabs below or upload a previously saved parameter file. Once uploaded, click <b><u>Run Simulation</u><b> to proceed.",
    unsafe_allow_html=True)

    # Load parameters from uploaded file if available
    parameters = load_parameters_from_upload()

    # Create input form with tabs
    config = create_input_form(parameters)
    
    # Show download and run buttons
    params_df = create_parameters_dataframe_from_config(config)
    run_button, auto_run = display_action_buttons(params_df)
    
    # Show spinner 
    with st.spinner("Simulating..."):

        # Run simulation if triggered
        if should_run_simulation(run_button, auto_run):
            run_simulation(config)
            time.sleep(1)
        
        # Display results if simulation has been run
    display_results()
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)


def setup_app():
    """Configure Streamlit app settings"""

    st.set_page_config(
    page_title="Retirement Planning Tool",
    page_icon="./assets/beach_access_2T.png",
    layout="wide"
    )
    
    # Apply CSS styling
    st.markdown(button_style_css, unsafe_allow_html=True)
    st.markdown(download_button_style_css, unsafe_allow_html=True)
    st.markdown(remove_top_white_space, unsafe_allow_html=True)
    
    # Create columns for title and help link
    col1, col2 = st.columns([5, 1])
    
    # App title in first column
    with col1:
        st.write("### Retirement Analysis with Monte Carlo Simulation")
    
    # Help hyperlink in second column with tooltip
    with col2:
        st.markdown("<div style='text-align: right; margin-top: 8px;'>", unsafe_allow_html=True)

        st.button("Help Guide", key="help_button", type="secondary", icon=":material/menu_book:",
                 help=help_document)  # Using the full help document as tooltip
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Add disclaimer using imported text
    st.markdown(disclaimer_text, unsafe_allow_html=True)

def load_parameters_from_upload() -> Dict[str, Any]:
    """Load parameters from uploaded CSV file"""
    uploaded_file = st.file_uploader("Upload previously downloaded simulation parameters", type=["csv"], key="param_file_uploader")
    
    if uploaded_file is None:
        return None
        
    try:
        params_df = pd.read_csv(uploaded_file)
        
        # Validate the DataFrame
        required_columns = get_required_columns()
        
        if not all(col in params_df.columns for col in required_columns):
            st.error("Uploaded file is missing one or more required columns.")
            return None
            
        # Convert DataFrame to dictionary
        return params_df.iloc[0].to_dict()
        
    except Exception as e:
        st.error(f"Error loading parameters: {e}")
        return None


def get_required_columns() -> List[str]:
    """Get list of required columns for parameter file"""
    return [
        "current_age", "partner_current_age", "life_expectancy", "retirement_age",
        "partner_retirement_age", "initial_savings", "stock_percentage", "bond_percentage",
        "annual_earnings", "self_yearly_increase", "partner_earnings", "partner_yearly_increase", 
        "annual_pension", "partner_pension", "self_pension_yearly_increase","partner_pension_yearly_increase", 
        "rental_start", "rental_end", "rental_amt", "rental_yearly_increase",      
        "self_401k_balance", "partner_401k_balance",
        "roth_ira_balance", "cash_savings_balance", "brokerage_balance",
        "self_401k_contribution", "partner_401k_contribution", "employer_self_401k_contribution",
        "employer_partner_401k_contribution", "maximize_self_contribution", "maximize_partner_contribution",
        # Tax columns ...
        "filing_status", "state_of_residence", "tax_rate",
        "tax_rate_both_working", "tax_rate_one_retired", "tax_rate_both_retired",
        #
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


def create_input_form(parameters: Dict[str, Any]) -> SimulationConfig:
    """Create the tabbed input form and return the simulation configuration"""
    current_year = datetime.now().year

    
    # Set up the tabbed container
    with st.container(height=310, border=None):
        # Set the tab styles 
        st.markdown(tab_style_css, unsafe_allow_html=True)
        
        # Create tabs for different parameter categories
        tabs = create_tabs()
        
        # Get the valid range of years for selections
        years_range = []
        # We'll populate years_range once we have life_expectancy and current_age
        
        # Tab 1: Personal Details
        current_age, partner_current_age, retirement_age, partner_retirement_age, life_expectancy = create_profile_tab(
            tabs[0], parameters)
            
        # Now we can set the valid years range
        years_range = list(range(current_year, current_year + (life_expectancy - current_age) + 1))
        
        # Tab 2: Savings & Investments
        (self_401k_balance, partner_401k_balance, roth_ira_balance, cash_savings_balance, 
         brokerage_balance, stock_percentage, bond_percentage, initial_savings) = create_savings_tab(
            tabs[1], parameters)
        
        # Tab 3: Income
        income_params = create_income_tab(tabs[2], parameters, years_range)
        (annual_earnings, partner_earnings, self_yearly_increase, partner_yearly_increase,
         annual_pension, partner_pension, self_pension_yearly_increase, partner_pension_yearly_increase,
         rental_start, rental_end, rental_amt, rental_yearly_increase) = income_params

        # Tab 4a: Contributions
        contribution_params = create_contribution_tab(tabs[3], parameters, current_age, partner_current_age)
        (self_401k_contribution, partner_401k_contribution, employer_self_401k_contribution,
         employer_partner_401k_contribution, maximize_self_contribution, maximize_partner_contribution) = contribution_params

        # Tab 4b: Taxes 
        tax_params = create_taxes_tab(tabs[4], parameters)
        # (filing_status, state_of_residence, tax_rate) = tax_params
        (filing_status, state_of_residence, tax_rate, tax_rate_both_working, tax_rate_one_retired, tax_rate_both_retired) = tax_params
        
        # Tab 5: Expenses
        expense_params = create_expenses_tab(tabs[5], parameters)
        (annual_expense, mortgage_payment, annual_expense_decrease, mortgage_years_remaining,
         inflation_mean, inflation_std) = expense_params
        
        # Tab 6: Social Security
        ss_params = create_social_security_tab(tabs[6], parameters)
        (annual_social_security, partner_social_security, withdrawal_start_age, 
         partner_withdrawal_start_age, cola_rate) = ss_params
        
        # Tab 7: Healthcare
        healthcare_params = create_healthcare_tab(tabs[7], parameters, retirement_age, partner_retirement_age)
        (self_healthcare_cost, self_healthcare_start_age, 
         partner_healthcare_cost, partner_healthcare_start_age) = healthcare_params
        
        # Tab 8: Market Returns
        market_params = create_market_returns_tab(tabs[8], parameters)
        (stock_return_mean, bond_return_mean, stock_return_std, bond_return_std)= market_params
        
        # Tab 9: Downsize
        downsize_params = create_downsize_tab(tabs[9], parameters)
        (years_until_downsize, residual_amount) = downsize_params
        
        # Tab 10: Adjust Recurring Expenses
        adjust_expense_params = create_adjust_expense_tab(tabs[10], parameters, years_range)
        (adjust_expense_year_1, adjust_expense_amount_1, 
         adjust_expense_year_2, adjust_expense_amount_2,
         adjust_expense_year_3, adjust_expense_amount_3) = adjust_expense_params
        
        # Tab 11: One-Time Expenses
        one_time_params = create_one_time_tab(tabs[11], parameters, years_range)
        (one_time_year_1, one_time_amount_1, one_time_year_2, one_time_amount_2,
         one_time_year_3, one_time_amount_3) = one_time_params
        
        # Tab 12: Windfalls
        windfall_params = create_windfall_tab(tabs[12], parameters, years_range)
        (windfall_year_1, windfall_amount_1, windfall_year_2, windfall_amount_2,
         windfall_year_3, windfall_amount_3) = windfall_params

        # Tab 13
        simulation_params = create_simulation_parameters_tab(tabs[13], parameters, years_range)
        (simulations, simulation_type, collar_min_return, collar_max_return, collar_start_year, collar_end_year)= simulation_params

        # Tab 15: Stress Tests
        stress_test_params = create_stress_tests_tab(tabs[14], parameters, years_range)
        (enable_sequence_risk, seq_risk_years, seq_risk_returns) = stress_test_params
    
    
    # Create lists for special events
    adjust_expense_years = [adjust_expense_year_1, adjust_expense_year_2, adjust_expense_year_3]
    adjust_expense_amounts = [adjust_expense_amount_1, adjust_expense_amount_2, adjust_expense_amount_3]
    one_time_years = [one_time_year_1, one_time_year_2, one_time_year_3]
    one_time_amounts = [one_time_amount_1, one_time_amount_2, one_time_amount_3]
    windfall_years = [windfall_year_1, windfall_year_2, windfall_year_3]
    windfall_amounts = [windfall_amount_1, windfall_amount_2, windfall_amount_3]
    
    # Create and return the SimulationConfig object
    return SimulationConfig(
        current_age=current_age,
        partner_current_age=partner_current_age,
        life_expectancy=life_expectancy,
        retirement_age=retirement_age,
        partner_retirement_age=partner_retirement_age,
        
        initial_savings=initial_savings,
        self_401k_balance=self_401k_balance,
        partner_401k_balance=partner_401k_balance,
        roth_ira_balance=roth_ira_balance,
        cash_savings_balance=cash_savings_balance,
        brokerage_balance=brokerage_balance,
        
        annual_earnings=annual_earnings,
        partner_earnings=partner_earnings,
        self_yearly_increase=self_yearly_increase,
        partner_yearly_increase=partner_yearly_increase,
        annual_pension=annual_pension,
        partner_pension=partner_pension,
        self_pension_yearly_increase=self_pension_yearly_increase,
        partner_pension_yearly_increase=partner_pension_yearly_increase,
        annual_social_security=annual_social_security,
        partner_social_security=partner_social_security,
        withdrawal_start_age=withdrawal_start_age,
        partner_withdrawal_start_age=partner_withdrawal_start_age,
        
        self_401k_contribution=self_401k_contribution,
        partner_401k_contribution=partner_401k_contribution,
        employer_self_401k_contribution=employer_self_401k_contribution,
        employer_partner_401k_contribution=employer_partner_401k_contribution,
        maximize_self_contribution=maximize_self_contribution,
        maximize_partner_contribution=maximize_partner_contribution,
        
        filing_status=filing_status, 
        state_of_residence=state_of_residence,
        tax_rate=tax_rate,
        # 3 tax rates 
        tax_rate_both_working=tax_rate_both_working,
        tax_rate_one_retired=tax_rate_one_retired,
        tax_rate_both_retired=tax_rate_both_retired,

        annual_expense=annual_expense,
        mortgage_payment=mortgage_payment,
        mortgage_years_remaining=mortgage_years_remaining,
        self_healthcare_cost=self_healthcare_cost,
        partner_healthcare_cost=partner_healthcare_cost,
        self_healthcare_start_age=self_healthcare_start_age,
        partner_healthcare_start_age=partner_healthcare_start_age,
        annual_expense_decrease=annual_expense_decrease,
        
        stock_percentage=stock_percentage,
        bond_percentage=bond_percentage,
        stock_return_mean=stock_return_mean,
        bond_return_mean=bond_return_mean,
        stock_return_std=stock_return_std,
        bond_return_std=bond_return_std,
        
        simulations=simulations,
        simulation_type=simulation_type,
        cola_rate=cola_rate,
        inflation_mean=inflation_mean,
        inflation_std=inflation_std,
        
        years_until_downsize=years_until_downsize,
        residual_amount=residual_amount,
        adjust_expense_years=adjust_expense_years,
        adjust_expense_amounts=adjust_expense_amounts,
        one_time_years=one_time_years,
        one_time_amounts=one_time_amounts,
        windfall_years=windfall_years,
        windfall_amounts=windfall_amounts,
        
        rental_start=rental_start,
        rental_end=rental_end,
        rental_amt=rental_amt,
        rental_yearly_increase=rental_yearly_increase,

        # Stress test parameters
        enable_sequence_risk=enable_sequence_risk,
        seq_risk_years=seq_risk_years,
        seq_risk_returns=seq_risk_returns,

        # Collar Strategy 
        collar_min_return=collar_min_return,
        collar_max_return=collar_max_return, 
        collar_start_year=collar_start_year, 
        collar_end_year=collar_end_year 

    )


def create_tabs():
    """Create the tabbed UI structure"""
    return st.tabs([
        ":material/group: Profile", 
        ":material/attach_money: Balances", 
        ":material/payments: Income", 
        ":material/savings: 401K", 
        ":material/account_balance: Taxes", 
        ":material/shopping_cart: Expense", 
        ":material/verified_user: SS", 
        ":material/local_hospital: Health",   
        ":material/bar_chart: Market", 
        ":material/house: Downsize", 
        ":material/tune: Adjust", 
        ":material/checkbook: One Time", 
        ":material/money_bag: Windfall",
        ":material/settings: Params",   
        ":material/exercise: Stress Tests"      
    ])


def create_profile_tab(tab, parameters):
    """Create the Profile tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            current_age = st.number_input("Your Current Age", 
                value=parameters["current_age"] if parameters else 50)
            partner_current_age = st.number_input("Partner's Current Age", 
                value=parameters["partner_current_age"] if parameters else 50)
        with col2:
            retirement_age = st.number_input("Your Retirement Age", 
                value=parameters["retirement_age"] if parameters else 60)
            partner_retirement_age = st.number_input("Partner's Retirement Age", 
                value=parameters["partner_retirement_age"] if parameters else 58)
        with col3:
            life_expectancy = st.number_input("Life Expectancy", 
                value=parameters["life_expectancy"] if parameters else 92)
                
    return current_age, partner_current_age, retirement_age, partner_retirement_age, life_expectancy


def create_savings_tab(tab, parameters):
    """Create the Savings and Investments tab inputs"""
    with tab:
        col1, col2, col3, col4, col5 = st.columns([2,2,2,1,2])
        with col1:
            self_401k_balance = st.number_input("Your 401(k)/ IRA Balance", 
                value=parameters["self_401k_balance"] if parameters else 200000, 
                step=25000)
            partner_401k_balance = st.number_input("Partner's 401(k) / IRA Balance", 
                value=parameters["partner_401k_balance"] if parameters else 200000, 
                step=25000)
        with col2:
            roth_ira_balance = st.number_input("Combined Roth IRA Balance", 
                value=parameters["roth_ira_balance"] if parameters else 30000, 
                step=10000)
            cash_savings_balance = st.number_input("Combined Cash/Savings Balance", 
                value=parameters["cash_savings_balance"] if parameters else 30000, 
                step=5000)
        with col3:
            brokerage_balance = st.number_input("Total Combined Investment Acct(s) Balances", 
                value=parameters["brokerage_balance"] if parameters else 100000, 
                step=25000)
            stock_percentage = st.slider("Percentage of Stock Investment (%)", 
                min_value=0, max_value=100, 
                value=parameters["stock_percentage"] if parameters else 60)
            bond_percentage = 100 - stock_percentage
        with col5:
            # Calculate total investments
            total_investment = (self_401k_balance + roth_ira_balance +
                             partner_401k_balance + brokerage_balance)
            stock_amount = total_investment * (stock_percentage / 100)
            bond_amount = total_investment * (bond_percentage / 100)

            # Display totals
            st.write(f"Investments : {total_investment:,.0f}")
            st.write(f"Cash : {cash_savings_balance:,.0f}")
            st.markdown(f"###### **Total Portfolio Balance:  {total_investment + cash_savings_balance:,.0f}**")

        initial_savings = total_investment + cash_savings_balance
        
    return (self_401k_balance, partner_401k_balance, roth_ira_balance, 
            cash_savings_balance, brokerage_balance, stock_percentage, 
            bond_percentage, initial_savings)


def create_income_tab(tab, parameters, years_range):
    """Create the Income tab inputs"""
    with tab:
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
        with col1:
            annual_earnings = st.number_input("Your Annual Earnings", 
                value=parameters["annual_earnings"] if parameters else 100000, step=5000)
            partner_earnings = st.number_input("Partner's Annual Earnings", 
                value=parameters["partner_earnings"] if parameters else 100000, step=5000)
        with col2:
            self_yearly_increase = st.number_input("Your Yearly Increase (%)", 
                value=parameters["self_yearly_increase"] * 100 if parameters else 3.0, step=0.5) / 100
            partner_yearly_increase = st.number_input("Partner Yearly Increase (%)", 
                value=parameters["partner_yearly_increase"] * 100 if parameters else 3.0, step=0.5) / 100
        with col3:
            annual_pension = st.number_input("Your Annual Pension", 
                value=parameters["annual_pension"] if parameters else 0, step=1000)
            partner_pension = st.number_input("Partner's Annual Pension", 
                value=parameters["partner_pension"] if parameters else 0, step=1000)
        with col4:
            self_pension_yearly_increase = st.number_input("Your Pension Yrly. Increase (%)", 
                value=parameters["self_pension_yearly_increase"] * 100 if parameters else 0.0, step=0.5) / 100
            partner_pension_yearly_increase = st.number_input("Partner Pension Yrly. Increase (%)", 
                value=parameters["partner_pension_yearly_increase"] * 100 if parameters else 0.0, step=0.5) / 100
        with col5:
            # Default to first year in range
            default_index = 0
            
            # If parameters exist, find the matching index
            if parameters and years_range:
                try:
                    rental_start_index = years_range.index(parameters["rental_start"])
                    rental_end_index = years_range.index(parameters["rental_end"])
                except ValueError:
                    rental_start_index = 0
                    rental_end_index = 0
            else:
                rental_start_index = 0
                rental_end_index = 0
                
            rental_start = st.selectbox("Rental Income Starts", years_range, index=rental_start_index)
            rental_end = st.selectbox("Rental Income Ends", years_range, index=rental_end_index)
        with col6:
            rental_amt = st.number_input("Annual Rental Amount", 
                value=parameters["rental_amt"] if parameters else 0, step=1000)
            rental_yearly_increase = st.number_input("Rental Yearly Increase (%)", 
                value=parameters["rental_yearly_increase"] * 100 if parameters else 4.0, step=0.5) / 100
    
    return (annual_earnings, partner_earnings, self_yearly_increase, partner_yearly_increase,
           annual_pension, partner_pension, self_pension_yearly_increase, partner_pension_yearly_increase,
           rental_start, rental_end, rental_amt, rental_yearly_increase)


def create_contribution_tab(tab, parameters, current_age, partner_current_age):
    """Create the Taxes tab inputs"""
    with tab:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            self_401k_contribution = st.number_input("Your 401(k) Contribution", 
                value=parameters["self_401k_contribution"] if parameters else 10000, step=1000)
            partner_401k_contribution = st.number_input("Partner's 401(k) Contribution", 
                value=parameters["partner_401k_contribution"] if parameters else 10000, step=1000)
                
        with col2:
            st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
            
            maximize_self_contribution = st.checkbox("Maximize 401(k) Self", 
                value=(parameters["maximize_self_contribution"] if parameters else False))
            
            if maximize_self_contribution:
                if current_age < 50:
                    self_401k_contribution = contribution_limits["401k"]["2025"]
                else:
                    self_401k_contribution = contribution_limits["401k"]["2025"] + contribution_limits["catch_up"]["2025"]
            
            st.write(f"Your Contribution: {self_401k_contribution:,.0f}")
            
            st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
            maximize_partner_contribution = st.checkbox("Maximize 401(k) Partner", 
                value=(parameters["maximize_partner_contribution"] if parameters else False))
            
            if maximize_partner_contribution:
                if partner_current_age < 50:
                    partner_401k_contribution = contribution_limits["401k"]["2025"]
                else:
                    partner_401k_contribution = contribution_limits["401k"]["2025"] + contribution_limits["catch_up"]["2025"]
            
            st.write(f"Partner's Contribution: {partner_401k_contribution:,.0f}")
            
        with col3:
            employer_self_401k_contribution = st.number_input("Employer 401K Contrib. (Self)", 
                value=parameters["employer_self_401k_contribution"] if parameters else 0, step=1000)
            employer_partner_401k_contribution = st.number_input("Employer 401K Contrib. (Partner)", 
                value=parameters["employer_partner_401k_contribution"] if parameters else 0, step=1000)
                                
    return (self_401k_contribution, partner_401k_contribution, employer_self_401k_contribution,
            employer_partner_401k_contribution, maximize_self_contribution, maximize_partner_contribution)



def create_taxes_tab(tab, parameters):
    """Create the Taxes tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

        with col1:
            filing_status = st.selectbox("Filing Status", 
                options=["Married Filing Jointly", "Single", "Married Filing Separately"], 
                index=0 if parameters is None else ["Married Filing Jointly", "Single", "Married Filing Separately"].index(parameters.get("filing_status", "Married Filing Jointly")))
            
            state_of_residence = st.selectbox("State of Residence", 
                options=["CA", "TX", "FL", "NY", "OR", "WA", "IL", "GA"], 
                index=0 if parameters is None else ["CA", "TX", "FL", "NY", "OR", "WA", "IL", "GA"].index(parameters.get("state_of_residence", "CA")))               

        # 3 tax rates 
        with col2:
            # Convert the original tax_rate to tax_rate_both_working if present
            default_tax_both_working = parameters["tax_rate"] * 100 if parameters and "tax_rate" in parameters else 15.0
            if parameters and "tax_rate_both_working" in parameters:
                default_tax_both_working = parameters["tax_rate_both_working"] * 100
                
            tax_rate_both_working = st.number_input(
                "Effective Tax Rate % - **When both are working**", 
                value=default_tax_both_working, 
                step=1.0,
                help=tax_rate_both_working_help
            ) / 100
                
            tax_rate_one_retired = st.number_input(
                "Effective Tax Rate % - **When one is retired**", 
                value=parameters["tax_rate_one_retired"] * 100 if parameters and "tax_rate_one_retired" in parameters else 12.0, 
                step=1.0,
                help=tax_rate_one_retired_help
            ) / 100

        with col3:
            tax_rate_both_retired = st.number_input(
                "Effective Tax Rate % - **When both are retired**", 
                value=parameters["tax_rate_both_retired"] * 100 if parameters and "tax_rate_both_retired" in parameters else 10.0, 
                step=1.0,
                help=tax_rate_both_retired_help
            ) / 100

            # tax_rate = st.number_input("Estimated Effective Tax Rate (%)", 
            #     value=parameters["tax_rate"] * 100 if parameters else 10.0, step=1.0) / 100

            # Hidden field approach - just set tax_rate to match tax_rate_both_working
            # Keep this field for backward compatibility - @todo cleanup later
            tax_rate = tax_rate_both_working

        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style="background-color:#e8f4f8; padding:6px; border-radius:4px; font-size:0.8em;">
                    <span style="color:#0d4c73;">ℹ️ <strong> Note: </strong> <br>{tax_calculation_disclaimer}</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            

    return (filing_status, state_of_residence, tax_rate, tax_rate_both_working, tax_rate_one_retired, tax_rate_both_retired)



def create_expenses_tab(tab, parameters):
    """Create the Expenses tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            annual_expense = st.number_input("Annual Living Expense", 
                help=living_expense_help_text, 
                value=parameters["annual_expense"] if parameters else 5000 * 12, step=2000)
            mortgage_payment = st.number_input("Yearly Mortgage", 
                value=parameters["mortgage_payment"] if parameters else 24000, step=2000)
                
        with col2:
            annual_expense_decrease = st.number_input("Annual Decrease post Retirement (Smile *) (%)", 
                help=smile_help_text, 
                value=parameters["annual_expense_decrease"] * 100 if parameters else 0.5, step=0.05) / 100
            mortgage_years_remaining = st.number_input("Mortgage Years Remaining", 
                value=parameters["mortgage_years_remaining"] if parameters else 25)
                
        with col3:
            inflation_mean = st.number_input("Inflation Mean (%)", 
                value=parameters["inflation_mean"] * 100 if parameters else 2.5, step=0.1) / 100
            inflation_std = st.number_input("Inflation Std Dev (%)", 
                value=parameters["inflation_std"] * 100 if parameters else 1.0, step=0.1) / 100
                
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
           
    return (annual_expense, mortgage_payment, annual_expense_decrease, 
            mortgage_years_remaining, inflation_mean, inflation_std)


def create_social_security_tab(tab, parameters):
    """Create the Social Security tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            annual_social_security = st.number_input("Your Social Security Benefit Amount", 
                value=parameters["annual_social_security"] if parameters else 2000 * 12, step=1000)
            partner_social_security = st.number_input("Partner's Social Security Benefit Amount", 
                value=parameters["partner_social_security"] if parameters else 2000 * 12, step=1000)
                
        with col2:
            withdrawal_start_age = st.number_input("Your Withdrawal Start Age", 
                value=parameters["withdrawal_start_age"] if parameters else 67)
            partner_withdrawal_start_age = st.number_input("Partner's Withdrawal Start Age", 
                value=parameters["partner_withdrawal_start_age"] if parameters else 65)
                
        with col3:
            cola_rate = st.number_input("Cost of Living Adjustment (COLA) Rate (%)", 
                value=parameters["cola_rate"] * 100 if parameters else 1.50, step=0.1) / 100
                
    return (annual_social_security, partner_social_security, withdrawal_start_age, 
            partner_withdrawal_start_age, cola_rate)


def create_healthcare_tab(tab, parameters, retirement_age, partner_retirement_age):
    """Create the Healthcare tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 4])
        
        with col1:
            self_healthcare_cost = st.number_input("Your Yearly Bridge Healthcare Cost",
                help=bridge_healthcare_help_text,  
                value=parameters["self_healthcare_cost"] if parameters else 5000, step=1000)
            self_healthcare_start_age = st.number_input("Your Healthcare Bridge Start Age", 
                value=parameters["self_healthcare_start_age"] if parameters else retirement_age)
                
        with col2:
            partner_healthcare_cost = st.number_input("Partner Yearly Bridge Healthcare Cost", 
                help=bridge_healthcare_help_text, 
                value=parameters["partner_healthcare_cost"] if parameters else 5000, step=1000)
            partner_healthcare_start_age = st.number_input("Partner's Healthcare Bridge Start Age", 

                value=parameters["partner_healthcare_start_age"] if parameters else partner_retirement_age)
        with col4:
            st.markdown(healthcare_bridge_text, unsafe_allow_html=True)

    return (self_healthcare_cost, self_healthcare_start_age, partner_healthcare_cost, partner_healthcare_start_age)


def create_market_returns_tab(tab, parameters):
    """Create the Market Returns tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 6])
        
        with col1:
            stock_return_mean = st.number_input("Expected Annual Stock Return (%)", 
                value=parameters["stock_return_mean"] * 100 if parameters else 6.5, 
                step=0.25,
                help=stock_return_mean_help) / 100
            bond_return_mean = st.number_input("Expected Annual Bond Return (%)", 
                value=parameters["bond_return_mean"] * 100 if parameters else 3.5, 
                step=0.25,
                help=bond_return_mean_help) / 100
                    
        with col2:
            stock_return_std = st.number_input("Stock Return Std Dev (%)", 
                value=parameters["stock_return_std"] * 100 if parameters else 15.50, 
                step=0.25,
                help=stock_return_std_help) / 100
            bond_return_std = st.number_input("Bond Return Std Dev (%)", 
                value=parameters["bond_return_std"] * 100 if parameters else 4.5, 
                step=0.05,
                help=bond_return_std_help) / 100

        with col4:
            st.markdown(market_returns_note, unsafe_allow_html=True)

    return (stock_return_mean, bond_return_mean, stock_return_std, bond_return_std)


def create_downsize_tab(tab, parameters):
    """Create the Downsize tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            years_until_downsize = st.number_input("After how many years?", 
                value=parameters["years_until_downsize"] if parameters else 0)
                
        with col2:
            residual_amount = st.number_input("Net Addition to Retirement Savings", 
                value=parameters["residual_amount"] if parameters else 0, step=100000)
            
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(downsize_text, unsafe_allow_html=True)
                
    return (years_until_downsize, residual_amount)


def create_adjust_expense_tab(tab, parameters, years_range):
    """Create the Adjust Recurring Expenses tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        # Find indexes in years_range if parameters exist
        def get_year_index(year_value):
            if parameters and year_value in years_range:
                return years_range.index(year_value)
            return 0
        
        with col1:
            adjust_expense_year_1 = st.selectbox("Year of Adjustment 1", years_range, 
                index=get_year_index(parameters["adjust_expense_year_1"]) if parameters else 0)
            adjust_expense_amount_1 = st.number_input("Yearly Living Expense Adjustment Amount 1", 
                value=parameters["adjust_expense_amount_1"] if parameters else 0, step=2000)
                
        with col2:
            adjust_expense_year_2 = st.selectbox("Year of Adjustment 2", years_range, 
                index=get_year_index(parameters["adjust_expense_year_2"]) if parameters else 0)
            adjust_expense_amount_2 = st.number_input("Yearly Living Expense Adjustment Amount 2", 
                value=parameters["adjust_expense_amount_2"] if parameters else 0, step=2000)
                
        with col3:
            adjust_expense_year_3 = st.selectbox("Year of Adjustment 3", years_range, 
                index=get_year_index(parameters["adjust_expense_year_3"]) if parameters else 0)
            adjust_expense_amount_3 = st.number_input("Yearly Living Expense Adjustment Amount 3", 
                value=parameters["adjust_expense_amount_3"] if parameters else 0, step=2000)
                
        with col4:
            st.markdown(adjust_expense_text, unsafe_allow_html=True)
            
    return (adjust_expense_year_1, adjust_expense_amount_1, adjust_expense_year_2, 
            adjust_expense_amount_2, adjust_expense_year_3, adjust_expense_amount_3)


def create_one_time_tab(tab, parameters, years_range):
    """Create the One-Time Expenses tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        # Find indexes in years_range if parameters exist
        def get_year_index(year_value):
            if parameters and year_value in years_range:
                return years_range.index(year_value)
            return 0
        
        with col1:
            one_time_year_1 = st.selectbox("Year of One-Time Expense 1", years_range, 
                index=get_year_index(parameters["one_time_year_1"]) if parameters else 0)
            one_time_amount_1 = st.number_input("One-Time Expense Amount 1", 
                value=parameters["one_time_amount_1"] if parameters else 0, step=5000)
                
        with col2:
            one_time_year_2 = st.selectbox("Year of One-Time Expense 2", years_range, 
                index=get_year_index(parameters["one_time_year_2"]) if parameters else 0)
            one_time_amount_2 = st.number_input("One-Time Expense Amount 2", 
                value=parameters["one_time_amount_2"] if parameters else 0, step=5000)
                
        with col3:
            one_time_year_3 = st.selectbox("Year of One-Time Expense 3", years_range, 
                index=get_year_index(parameters["one_time_year_3"]) if parameters else 0)
            one_time_amount_3 = st.number_input("One-Time Expense Amount 3", 
                value=parameters["one_time_amount_3"] if parameters else 0, step=5000)
                
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(one_time_expense_text, unsafe_allow_html=True)
            
    return (one_time_year_1, one_time_amount_1, one_time_year_2, 
            one_time_amount_2, one_time_year_3, one_time_amount_3)


def create_windfall_tab(tab, parameters, years_range):
    """Create the Windfalls tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        # Find indexes in years_range if parameters exist
        def get_year_index(year_value):
            if parameters and year_value in years_range:
                return years_range.index(year_value)
            return 0
        
        with col1:
            windfall_year_1 = st.selectbox("Year of Windfall 1", years_range, 
                index=get_year_index(parameters["windfall_year_1"]) if parameters else 0)
            windfall_amount_1 = st.number_input("Windfall Amount 1", 
                value=parameters["windfall_amount_1"] if parameters else 0, step=20000)
                
        with col2:
            windfall_year_2 = st.selectbox("Year of Windfall 2", years_range, 
                index=get_year_index(parameters["windfall_year_2"]) if parameters else 0)
            windfall_amount_2 = st.number_input("Windfall Amount 2", 
                value=parameters["windfall_amount_2"] if parameters else 0, step=20000)
                
        with col3:
            windfall_year_3 = st.selectbox("Year of Windfall 3", years_range, 
                index=get_year_index(parameters["windfall_year_3"]) if parameters else 0)
            windfall_amount_3 = st.number_input("Windfall Amount 3", 
                value=parameters["windfall_amount_3"] if parameters else 0, step=20000)
               
        with col4:
            st.markdown(windfall_text, unsafe_allow_html=True)

    return (windfall_year_1, windfall_amount_1, windfall_year_2, 
            windfall_amount_2, windfall_year_3, windfall_amount_3)


def create_simulation_parameters_tab(tab, parameters, years_range):
    """Create the Simulation Parameters tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([3,3,5,6])
    
        # Initialize collar strategy variables with defaults
        current_year = datetime.now().year
        collar_min_return = parameters.get("collar_min_return", -0.05) if parameters else -0.05
        collar_max_return = parameters.get("collar_max_return", 0.15) if parameters else 0.15
        collar_start_year = parameters.get("collar_start_year", current_year) if parameters else current_year
        collar_end_year = parameters.get("collar_end_year", current_year + 32) if parameters else current_year + 32         
                
        with col1:
            simulations = st.number_input("Number of Simulations", 
                value=parameters["simulations"] if parameters else 1000, step=1000)
                
        with col2:
            # Determine the default simulation type
            if parameters is None:
                default_simulation_type = "Normal Distribution"
            else:
                default_simulation_type = parameters.get("simulation_type", "Normal Distribution")
                if default_simulation_type not in ["Normal Distribution", "Students-T Distribution", "Empirical Distribution", "Markov Chain", "Collar Strategy"]:
                    default_simulation_type = "Normal Distribution"

            # Create the radio button group
            simulation_options = ["Normal Distribution", "Students-T Distribution", "Empirical Distribution", "Markov Chain", "Collar Strategy"]
            simulation_type = st.radio("Simulation Type", options=simulation_options,
                index=simulation_options.index(default_simulation_type),
                help=simulation_help_text)
            
            # These will only be shown and adjustable in the UI when Collar Strategy is selected
            collar_min_return = parameters.get("collar_min_return", -0.05) if parameters else -0.05
            collar_max_return = parameters.get("collar_max_return", 0.15) if parameters else 0.15

        with col3:

            def get_year_index(year_value, default_index=0):
                if parameters and years_range and year_value in years_range:
                    return years_range.index(year_value)
                return default_index
            
            # Determine the default simulation type
            # Only show collar strategy controls if that option is selected
            if simulation_type == "Collar Strategy":

                # # Get the range of years for the simulation
                # life_expectancy = parameters.get("life_expectancy", 92) if parameters else 92
                # current_age = parameters.get("current_age", 50) if parameters else 50
                # years_in_simulation = life_expectancy - current_age + 1

                # Add collar strategy year selectors
                st.markdown("###### Collar Strategy Details")
                cols = st.columns(2)
                with cols[0]:
                    collar_min_return = st.number_input(
                        "Min Equity Return (%)",
                        min_value=-30.0,
                        max_value=0.0,
                        value=collar_min_return * 100,  # Convert to percentage for display
                        step=1.0
                    ) / 100  # Convert back to decimal


                    # Get saved start year or default to first year in range
                    saved_start_year = parameters.get("collar_start_year", years_range[0]) if parameters else years_range[0]
                    
                    # Find the index for the start year
                    start_index = get_year_index(saved_start_year, 0)
                    
                    collar_start_year = st.selectbox(
                        "Start Year",
                        options=years_range,
                        index=start_index,
                        key="collar_start",
                        format_func=lambda x: str(x),
                        help="Year when collar strategy begins"
                    )
                
                with cols[1]:
                    collar_max_return = st.number_input(
                        "Max Equity Return (%)",
                        min_value=0.0,
                        max_value=30.0,
                        value=collar_max_return * 100,  # Convert to percentage for display
                        step=1.0
                    ) / 100  # Convert back to decimal

                    # Get saved end year or default to LAST year in range (end of life expectancy)
                    saved_end_year = parameters.get("collar_end_year", years_range[-1]) if parameters else years_range[-1]
                    
                    # Find the index for the end year, defaulting to last year in range
                    end_index = get_year_index(saved_end_year, len(years_range)-1)
                    
                    collar_end_year = st.selectbox(
                        "End Year",
                        options=years_range,
                        index=end_index,
                        key="collar_end",
                        format_func=lambda x: str(x),
                        help="Year when collar strategy ends"
                    )

                # Display the duration
                if collar_end_year >= collar_start_year:
                    collar_duration_years = collar_end_year - collar_start_year + 1
                    st.write(f"The collar will be active for {collar_duration_years} years ({collar_start_year} to {collar_end_year}).")
                else:
                    st.error("End year must be after start year.")

            else:
                # Default values when collar strategy isn't selected
                collar_start_year = years_range[0] if years_range else current_year
                collar_end_year = years_range[-1] if years_range else current_year + 30

                
        with col4:
            st.markdown(parameter_text, unsafe_allow_html=True)

    return (simulations, simulation_type, collar_min_return, collar_max_return, collar_start_year, collar_end_year)


def create_stress_tests_tab(tab, parameters, years_range=None):
    """Create the Stress Tests tab inputs"""
    with tab:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            # Add explanatory text before the toggle
            st.markdown("""
            <div style=font-size:0.9em;">
            <strong>Sequence of Returns Risk Test</strong> <br>
            Consecutive poor returns when retirement starts.
            </div>
            """, unsafe_allow_html=True)
            
            # Keep the toggle label simpler now
            enable_sequence_risk = st.toggle(
                "Enable this test",
                value=parameters["enable_sequence_risk"] if parameters and "enable_sequence_risk" in parameters else False,
                help=enable_sequence_risk_help
            )
            # # Display the effective values if enabled
            # if enable_sequence_risk:
            #     st.write(f"Return during first {seq_risk_years} years of retirement: {seq_risk_returns*100:.1f}%")
        with col2:
            seq_risk_years = st.number_input(
                "Duration (consecutive years)",
                min_value=1,
                max_value=20,
                value=parameters["seq_risk_years"] if parameters and "seq_risk_years" in parameters else 3,
                disabled=not enable_sequence_risk,
                help=seq_risk_years_help
            )
            seq_risk_returns = st.number_input(
                "Annual Return During Stress (%)",
                min_value=-40.0,
                max_value=0.0, 
                value=parameters["seq_risk_returns"] if parameters and "seq_risk_returns" in parameters else -15.0,
                step=1.0,
                disabled=not enable_sequence_risk,
                help=seq_risk_returns_help
            ) / 100
                

        with col3:
            # Placeholder for next stress test (Black Swan)
            # We'll implement this in the next step
            st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
                
        with col4:
            st.markdown(stress_test_text, unsafe_allow_html=True)
            
    return (enable_sequence_risk, seq_risk_years, seq_risk_returns)




def create_parameters_dataframe_from_config(config):
    """Convert SimulationConfig to a DataFrame for saving/sharing"""
    # Extract special events lists into individual items
    adjust_expense_year_1, adjust_expense_year_2, adjust_expense_year_3 = (config.adjust_expense_years + [0, 0, 0])[:3]
    adjust_expense_amount_1, adjust_expense_amount_2, adjust_expense_amount_3 = (config.adjust_expense_amounts + [0, 0, 0])[:3]
    
    one_time_year_1, one_time_year_2, one_time_year_3 = (config.one_time_years + [0, 0, 0])[:3]
    one_time_amount_1, one_time_amount_2, one_time_amount_3 = (config.one_time_amounts + [0, 0, 0])[:3]
    
    windfall_year_1, windfall_year_2, windfall_year_3 = (config.windfall_years + [0, 0, 0])[:3]
    windfall_amount_1, windfall_amount_2, windfall_amount_3 = (config.windfall_amounts + [0, 0, 0])[:3]
    
    # Create a dictionary with all parameters
    params_dict = {
        "current_age": config.current_age,
        "partner_current_age": config.partner_current_age,
        "life_expectancy": config.life_expectancy,
        "retirement_age": config.retirement_age,
        "partner_retirement_age": config.partner_retirement_age,
        "initial_savings": config.initial_savings,
        "stock_percentage": config.stock_percentage,
        "bond_percentage": config.bond_percentage,
        "annual_earnings": config.annual_earnings,
        "self_yearly_increase": config.self_yearly_increase,
        "partner_earnings": config.partner_earnings,
        "partner_yearly_increase": config.partner_yearly_increase,
        "annual_pension": config.annual_pension,
        "partner_pension": config.partner_pension,
        "self_pension_yearly_increase": config.self_pension_yearly_increase,
        "partner_pension_yearly_increase": config.partner_pension_yearly_increase,

        "rental_start": config.rental_start,
        "rental_end": config.rental_end,
        "rental_amt": config.rental_amt,
        "rental_yearly_increase": config.rental_yearly_increase,
        # Savings balances
        "self_401k_balance": config.self_401k_balance,
        "partner_401k_balance": config.partner_401k_balance,
        "roth_ira_balance": config.roth_ira_balance,
        "cash_savings_balance": config.cash_savings_balance,
        "brokerage_balance": config.brokerage_balance,
        # Contributions
        "self_401k_contribution": config.self_401k_contribution,
        "partner_401k_contribution": config.partner_401k_contribution,
        "employer_self_401k_contribution": config.employer_self_401k_contribution,
        "employer_partner_401k_contribution": config.employer_partner_401k_contribution,
        "maximize_self_contribution": config.maximize_self_contribution,
        "maximize_partner_contribution": config.maximize_partner_contribution,
        #Taxes
        #"tax_rate": config.tax_rate,
        "filing_status": config.filing_status, 
        "state_of_residence": config.state_of_residence,

        "tax_rate_both_working": config.tax_rate_both_working,
        "tax_rate_one_retired": config.tax_rate_one_retired,
        "tax_rate_both_retired": config.tax_rate_both_retired,
        # Include the original tax_rate for backward compatibility
        "tax_rate": config.tax_rate_both_working,

        # Expenses
        "annual_expense": config.annual_expense,
        "mortgage_payment": config.mortgage_payment,
        "inflation_mean": config.inflation_mean,
        "annual_expense_decrease": config.annual_expense_decrease,
        "mortgage_years_remaining": config.mortgage_years_remaining,
        "inflation_std": config.inflation_std,
        # Social Security
        "annual_social_security": config.annual_social_security,
        "withdrawal_start_age": config.withdrawal_start_age,
        "cola_rate": config.cola_rate,
        "partner_social_security": config.partner_social_security,
        "partner_withdrawal_start_age": config.partner_withdrawal_start_age,
        # Healthcare
        "self_healthcare_cost": config.self_healthcare_cost,
        "self_healthcare_start_age": config.self_healthcare_start_age,
        "partner_healthcare_cost": config.partner_healthcare_cost,
        "partner_healthcare_start_age": config.partner_healthcare_start_age,
        # Market returns
        "stock_return_mean": config.stock_return_mean,
        "bond_return_mean": config.bond_return_mean,
        "simulations": config.simulations,
        "stock_return_std": config.stock_return_std,
        "bond_return_std": config.bond_return_std,
        "simulation_type": config.simulation_type,
        # Downsize
        "years_until_downsize": config.years_until_downsize,
        "residual_amount": config.residual_amount,
        # Adjust expenses
        "adjust_expense_year_1": adjust_expense_year_1,
        "adjust_expense_amount_1": adjust_expense_amount_1,
        "adjust_expense_year_2": adjust_expense_year_2,
        "adjust_expense_amount_2": adjust_expense_amount_2,
        "adjust_expense_year_3": adjust_expense_year_3,
        "adjust_expense_amount_3": adjust_expense_amount_3,
        # One-time expenses
        "one_time_year_1": one_time_year_1,
        "one_time_amount_1": one_time_amount_1,
        "one_time_year_2": one_time_year_2,
        "one_time_amount_2": one_time_amount_2,
        "one_time_year_3": one_time_year_3,
        "one_time_amount_3": one_time_amount_3,
        # Windfalls
        "windfall_year_1": windfall_year_1,
        "windfall_amount_1": windfall_amount_1,
        "windfall_year_2": windfall_year_2,
        "windfall_amount_2": windfall_amount_2,
        "windfall_year_3": windfall_year_3,
        "windfall_amount_3": windfall_amount_3
    }
    
    # Return as DataFrame with one row
    return pd.DataFrame([params_dict])


def display_action_buttons(params_df):
    """Display download parameters button and run simulation button"""
    # Convert DataFrame to CSV
    csv = params_df.to_csv(index=False)
    
    # Create columns for the buttons
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 2, 2])
    
    # Download button
    with col1:
        st.download_button(
            label="Save Parameters",
            key="parameter_download",
            data=csv,
            file_name="retirement_parameters.csv",
            mime="text/csv",
            type="primary",
            icon=":material/download:"
        )
    
    # Run simulation button
    with col3:
        run_button = st.button("Run Simulation", type="primary", icon=":material/rocket_launch:")
    
    # Auto-run checkbox
    with col4:
       auto_run = st.toggle("Run Automatically", value=False, help=auto_run_help_text)

    return run_button, auto_run


def should_run_simulation(run_button, auto_run):
    """Determine if the simulation should be run"""
    # Initialize the simulation state if it doesn't exist
    if 'simulation_initialized' not in st.session_state:
        st.session_state.simulation_initialized = False
    
    # Run if button is clicked, auto-run is checked, or first time running
    return (run_button or 
            auto_run or 
            not st.session_state.simulation_initialized)


def run_simulation(config):
    """Run the Monte Carlo simulation and store results in session state"""
    # Initialize the simulation results storage
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = {
            'success_count': 0,
            'failure_count': 0,
            'sorted_simulation_results': []
        }
    
    # Run simulation with the new refactored function
    success_count, failure_count, sorted_simulation_results = monte_carlo_simulation(config)
    
    # Store the results in session state
    st.session_state.simulation_results = {
        'success_count': success_count,
        'failure_count': failure_count,
        'sorted_simulation_results': sorted_simulation_results
    }

    # Persist config so we can show parameter banner in results
    st.session_state.simulation_config = config
    
    # Mark as initialized
    st.session_state.simulation_initialized = True

# Display PDF directly in the app
def display_result_guide_pdf(file_path):

    # Create columns with 90%-10% width distribution
    center_col, right_spacer = st.columns([76, 24])
    
    # Place the expander in the center column (80% width)
    with center_col:
        with st.expander(":material/help: How to interpret simulation results?"):
            try:
                with open("./assets/Interpret_simulation_results.pdf", "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                
                # Set width to 100% to fill the expander (which is already at 80% of page width)
                # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'

                # pdf_display = f"""
                # <embed 
                #     src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0" 
                #     type="application/pdf"
                #     width="100%" 
                #     height="600px"
                # />
                # """

                pdf_display = interpretation_guide_md

                st.markdown(pdf_display, unsafe_allow_html=True)
            except FileNotFoundError:
                st.error("PDF file not found. Please make sure the file exists in the assets folder.")


def display_results():
    """Display simulation results with visualizations"""
    # Make sure we have results to display
    if not st.session_state.simulation_initialized:
        return
    
    # Extract results
    success_count = st.session_state.simulation_results['success_count']
    failure_count = st.session_state.simulation_results['failure_count']
    sorted_simulation_results = st.session_state.simulation_results['sorted_simulation_results']
    
    # Calculate success rate
    total_simulations = success_count + failure_count
    success_rate = (success_count / total_simulations) * 100 if total_simulations > 0 else 0
    
    # Store in session for use elsewhere (e.g., parameter banner)
    st.session_state['success_rate'] = success_rate

    # Display success rate indicator
    st.markdown(create_linear_indicator(math.floor(success_rate), "Success Rate: "), unsafe_allow_html=True)
    
    # Process simulation results for percentile scenarios
    processed_results = process_percentile_scenarios(sorted_simulation_results)
    
    # Display ending balance summary
    display_ending_balance_summary(processed_results, st.session_state.get('simulation_config'))
    
    # Call the function where you want to display the PDF
        # Display detailed scenario analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("##### Learn how to interpret simulation results :material/pan_tool: ")
    display_result_guide_pdf("./assets/Interpret_simulation_results.pdf")
    
    # Display detailed scenario analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("#### Scenario Analysis ")
    
    # Create tabs for each percentile scenario
    display_percentile_tabs(processed_results)


def process_percentile_scenarios(sorted_simulation_results):
    """Process simulation results to extract percentile scenarios"""
    # Calculate indices for percentiles
    n = len(sorted_simulation_results)
    percentiles = {
        "10th": int(0.1 * n),
        "25th": int(0.25 * n),
        "50th": int(0.5 * n),
        "75th": int(0.75 * n)
    }
    
    # Extract cash flows for each percentile
    results = {}
    for percentile, index in percentiles.items():
        # Get the simulation ID for this percentile
        if index > 0 and index <= len(sorted_simulation_results):
            sim_id = sorted_simulation_results[index - 1]["simulation_id"]
            
            # Extract cash flows
            cash_flows = []
            for sim in sorted_simulation_results:
                if sim["simulation_id"] == sim_id:
                    cash_flows = sim["cash_flows"]
                    break
                    
            # Create a DataFrame from the cash flows
            df_original = pd.DataFrame(cash_flows)
            
            # Flatten the nested structure
            df_values = flatten_nested_dataframe(df_original)

            # Reorder columns for better display
            df_values = reorder_columns(df_values)

            # Calculate year of depletion
            year_of_depletion = "Surplus at plan end"
            if not df_values.empty and 'ending_balance' in df_values.columns:
                negative_years = df_values[df_values['ending_balance'] < 0]
                if not negative_years.empty:
                    year_of_depletion = str(negative_years['year'].iloc[0])
            
            # Format the data for display
            df_formatted = format_cashflow_dataframe(df_values.copy())
            
            # Get the ending balance
            ending_balance = df_values['ending_balance'].iloc[-1] if not df_values.empty else 0
            
            results[percentile] = {
                "df_values": df_values,
                "df_formatted": df_formatted,
                "ending_balance": ending_balance,
                "year_of_depletion": year_of_depletion
            }
    
    return results

def convert_to_dict_for_display(cash_flow):
    """Convert a cash flow object to a dictionary for display"""
    # Implementation will depend on the structure of your cash flow objects
    # This is a placeholder assuming cash_flow is already a dictionary
    return cash_flow


def format_cashflow_dataframe(df):
    """Format the cash flow DataFrame for display"""
    if df.empty:
        return df
    
    # List of columns that should be formatted as currency
    monetary_columns = [
        'beginning_balance', 'ending_balance', 'end_value_constant_currency', 'portfolio_draw', 
        'income_self_earnings', 'income_partner_earnings', 
        'income_self_social_security', 'income_partner_social_security',
        'income_self_pension', 'income_partner_pension', 'income_rental',
        'expenses_basic', 'expenses_mortgage', 'expenses_self_healthcare', 
        'expenses_partner_healthcare', 'expenses_one_time',
        'investment_return_self_401k', 'investment_return_partner_401k',
        'investment_return_roth_ira', 'investment_return_brokerage',
        'investment_return_cash', 'investment_return_total', 'tax', 
        'draws_self_401k', 'draws_partner_401k', 'draws_roth_ira',
        'draws_brokerage', 'draws_cash', 'draws_total',
        'account_balances_self_401k', 'account_balances_partner_401k',
        'account_balances_roth_ira', 'account_balances_brokerage',
        'account_balances_cash', 'self_contribution', 'partner_contribution',
        'downsize_proceeds', 'windfall_amount', 'expense_adjustment'
    ]
    
    # Format monetary columns
    for col in monetary_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "")
    
    # Format percentage columns
    percentage_columns = ['return_rate', 'withdrawal_rate']
    for col in percentage_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x*100:.2f}%" if pd.notnull(x) else "")
    
    return df

def generate_parameter_summary(config):
    """Generate a summary of simulation parameters for display"""

    success_rate = (st.session_state.get("success_rate", None))
    # Success Rate
    if success_rate is not None:
        summary = (
            f"<span style='font-size:16px; font-weight:700;'>"
            f"Success Rate: {math.floor(success_rate):.0f}%  |  </span>"
        )


    # Basic simulation details
    summary += f"<b>Simulation Type:</b> {config.simulation_type} ({config.simulations:,} runs), "
    
    # Add return assumptions
    summary += f"<b>Assumed Returns:</b> Equity {config.stock_return_mean*100:.1f}% (±{config.stock_return_std*100:.1f}%), " \
               f"Bonds {config.bond_return_mean*100:.1f}% (±{config.bond_return_std*100:.1f}%), "
    
    # Add allocation
    summary += f"<b>Allocation:</b> {config.stock_percentage:.0f}/{config.bond_percentage:.0f}, "
    
    # Add collar details if applicable
    if config.simulation_type == "Collar Strategy":
        summary += f"<b>Collar:</b> Min {config.collar_min_return*100:.1f}%, Max {config.collar_max_return*100:.1f}% " \
                   f"({config.collar_start_year}-{config.collar_end_year}), "
    
    # Add sequence risk details
    if config.enable_sequence_risk:
        summary += f"<b>Sequence Risk:</b> {config.seq_risk_years} years @ {config.seq_risk_returns*100:.1f}%, "
    
    # Add inflation/COLA
    summary += f"<b>Inflation:</b> {config.inflation_mean*100:.1f}%, <b>COLA:</b> {config.cola_rate*100:.1f}%"

    
    return summary


def display_ending_balance_summary(processed_results, config):
    """Display a summary of ending balances for each percentile"""
    # Calculate inflation adjustment for ending balances
    years = st.session_state.get('years_in_simulation', 30)
    inflation_mean = 0.025  # Default if not available

    # Calculate the return statistics for each percentile
    for percentile in ['10th', '25th', '50th', '75th']:
        df = processed_results[percentile]['df_values']
        if 'return_rate' in df.columns:
            # Calculate median return rate
            median_return = df['return_rate'].median()
            processed_results[percentile]['median_return_rate'] = f"{median_return * 100:.2f}%"

            # Calculate arithmetic mean and standard deviation
            arithmetic_mean = df['return_rate'].mean()
            std_dev = df['return_rate'].std()            

            # Calculate geometric mean using the provided formula
            geometric_mean = arithmetic_mean - (arithmetic_mean ** 2) / 2
            processed_results[percentile]['geometric_mean'] = f"{geometric_mean * 100:.2f}%"

            # Count years with positive and negative returns
            positive_years = (df['return_rate'] > 0).sum()
            negative_years = (df['return_rate'] <= 0).sum()
            total_years = positive_years + negative_years

            processed_results[percentile]['positive_return_years'] = positive_years
            processed_results[percentile]['negative_return_years'] = negative_years
            processed_results[percentile]['negative_return_formatted'] = f"{negative_years} out of {total_years} years"
        else:
            # Default values if return_rate isn't available
            processed_results[percentile]['median_return_rate'] = "N/A"
            processed_results[percentile]['geometric_mean'] = "N/A"
            processed_results[percentile]['positive_return_years'] = 0
            processed_results[percentile]['negative_return_years'] = 0
            processed_results[percentile]['negative_return_formatted'] = "N/A"

    # Compute Cushion Years and Withdrawal Rate stats (min/max/mean/median) per percentile
    def _last_year_total_expense_incl_tax(df_):
        if df_ is None or df_.empty:
            return float('nan')
        last = df_.iloc[-1]
        components = [
            'expenses_basic',
            'expenses_mortgage',
            'expenses_self_healthcare',
            'expenses_partner_healthcare',
            'expenses_one_time',
            'tax'
        ]
        total = 0.0
        for c in components:
            if c in df_.columns and pd.notnull(last[c]):
                total += float(last[c])
        return total

    def _withdrawal_rate_stats(df_):
        if df_ is None or df_.empty or 'withdrawal_rate' not in df_.columns:
            return "N/A"
        wr = df_['withdrawal_rate']
        wr = wr[pd.notnull(wr)]
        # Exclude non-draw years (optional, keeps numbers meaningful)
        wr = wr[wr > 0]
        if wr.empty:
            return "N/A"
        # return f"[ {wr.min()*100:.1f}% - {wr.max()*100:.1f}% ]   {wr.mean()*100:.1f}%"
        #return f"{wr.mean()*100:.1f}%"
        return f"{wr.mean()*100:.1f}% | {wr.max()*100:.1f}%"

    cushion_years = {}
    wr_stats = {}
    for p in ['10th', '25th', '50th', '75th']:
        dfp = processed_results[p]['df_values']
        end_bal = processed_results[p]['ending_balance']
        total_last_exp = _last_year_total_expense_incl_tax(dfp)
        cushion = (end_bal / total_last_exp) if (total_last_exp and total_last_exp > 0) else float('nan')
        cushion_years[p] = "N/A" if (pd.isna(cushion) or cushion <= 0) else f"{cushion:.1f} yrs of expense"
        wr_stats[p] = _withdrawal_rate_stats(dfp)

    # Prepare the data for the grid (added Cushion Years and Withdrawal Rate rows)
    data = {
        "Scenarios": [
            "Ending Balance", 
            "At Today's $", 
            "End-Plan Cushion",
            "Withdrawal Rate (Avg | Max)",
            "Year of Depletion",
            "Effective Rate of Return",
            # "Negative Returns", 
            "Simulation Percentile"
        ],
        "Far Below Hist. Avg. Returns": [
            f"{processed_results['10th']['ending_balance'] / 1_000_000:,.2f}M",
            f"{processed_results['10th']['ending_balance'] / ((1 + inflation_mean) ** years) / 1_000_000:,.2f}M", 
            cushion_years['10th'],
            wr_stats['10th'],
            processed_results['10th']['year_of_depletion'],
            processed_results['10th']['geometric_mean'],
            # processed_results['10th']['negative_return_formatted'],
            "Top 90% Scenarios"
        ],
        "Below Historical Average Returns": [
            f"{processed_results['25th']['ending_balance'] / 1_000_000:,.2f}M",
            f"{processed_results['25th']['ending_balance'] / ((1 + inflation_mean) ** years) / 1_000_000:,.2f}M",
            cushion_years['25th'],
            wr_stats['25th'],
            processed_results['25th']['year_of_depletion'],
            processed_results['25th']['geometric_mean'],
            # processed_results['25th']['negative_return_formatted'],
            "Top 75% Scenarios"
        ],
        "Historical Average Returns": [
            f"{processed_results['50th']['ending_balance'] / 1_000_000:,.2f}M",
            f"{processed_results['50th']['ending_balance'] / ((1 + inflation_mean) ** years) / 1_000_000:,.2f}M",
            cushion_years['50th'],
            wr_stats['50th'],
            processed_results['50th']['year_of_depletion'],
            processed_results['50th']['geometric_mean'],
            # processed_results['50th']['negative_return_formatted'],
            "Top 50% Scenarios"
        ],
        "Above Historical Average Returns": [
            f"{processed_results['75th']['ending_balance'] / 1_000_000:,.2f}M",
            f"{processed_results['75th']['ending_balance'] / ((1 + inflation_mean) ** years) / 1_000_000:,.2f}M",
            cushion_years['75th'],
            wr_stats['75th'],
            processed_results['75th']['year_of_depletion'],
            processed_results['75th']['geometric_mean'],
            # processed_results['75th']['negative_return_formatted'],
            "Top 25% Scenarios"
        ]
    }
    
    # Create a DataFrame and apply styling
    df = pd.DataFrame(data)
    
    styles = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns
    )
    
    # Apply styles based on values
    for i, row in enumerate(df.index):
        for j, col in enumerate(df.columns):
            value = df.iloc[i, j]
            
            # Skip the first column (headers)
            if j == 0:
                continue
                
            # For Year of Depletion (row index 2)
            if i == 4:
                if value == "Surplus at plan end":
                    styles.iloc[i, j] = 'color: green; font-weight: bold;'
                else:
                    styles.iloc[i, j] = 'color: red; font-weight: bold;'
            # For currency values (rows 0 and 1)
            elif i < 2:
                try:
                    if isinstance(value, str) and 'M' in value:
                        numeric_value = float(value.replace('M', ''))
                        color = 'red' if numeric_value < 0 else 'green'
                        styles.iloc[i, j] = f'color: {color}; font-weight: bold;'
                except:
                    pass
            # For Rate rows with % (row index 3 remains effective return)
            elif i == 5:
                try:
                    if isinstance(value, str) and '%' in value:
                        numeric_value = float(value.replace('%', ''))
                        color = 'red' if numeric_value < 0 else 'green'
                        styles.iloc[i, j] = f'color: {color}; font-weight: bold;'
                except:
                    pass
            # Leave Cushion Years and Withdrawal Rate rows unstyled by default

    # Apply the styles
    styled_df = df.style.apply(lambda _: styles, axis=None)
    # Set the header background color to light grey
    styled_df = styled_df.set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#F0F2F6'), ('color', '#333'), ('font-weight', 'bold')]}
    ])
    styled_df.set_table_attributes('style="font-size: 14px; width: 75%;"')
    
    # Hide the index
    styled_df = styled_df.hide(axis="index")

    # Convert to HTML
    table_html = styled_df.to_html(index=False, escape=False)

    # Inject a single parameter banner row spanning all 4 scenario columns (minimal change: HTML insert)
    try:
        param_banner = generate_parameter_summary(config) if config is not None else ""
        if param_banner:
            # Option A: full-width banner across all 5 columns (no label cell)
            banner_label = None  # set to "Parameters" to use Option B below

            if banner_label is None:
                banner_row = (
                    "<tr>"
                    "<td colspan='5' "
                    "style='background-color:#ffffff; color:#0d4c73; font-size:13px; padding:6px;'>"
                    f"{param_banner}"
                    "</td>"
                    "</tr>"
                )
            else:
                # Option B: labeled first column + banner spanning the remaining 4 columns
                banner_row = (
                    "<tr>"
                    "<td style='background-color:#ffffff; color:#0d4c73; font-size:13px; "
                    "padding:6px; font-weight:600; white-space:nowrap;'>"
                    f"{banner_label}"
                    "</td>"
                    "<td colspan='4' "
                    "style='background-color:#ffffff; color:#0d4c73; font-size:13px; padding:6px;'>"
                    f"{param_banner}"
                    "</td>"
                    "</tr>"
                )

            # display the parameter summary as the first row
            # table_html = table_html.replace("<tbody>", f"<tbody>{banner_row}", 1)

            # display the parameter summary as the last row
            table_html = table_html.replace("</tbody>", f"{banner_row}</tbody>", 1)
    except Exception:
        pass

    # Display the modified table
    st.markdown(table_html, unsafe_allow_html=True)

def display_percentile_tabs(processed_results):
    """Display tabs with detailed cash flow analysis for each percentile"""

    content_area, right_spacer = st.columns([9, 2])

    with content_area: 
        # Create tabs for the cash flow summaries
        tab_10th, tab_25th, tab_50th, tab_75th = st.tabs([
            ":material/thunderstorm: Far Below Hist. Avg. Returns", 
            ":material/rainy: Below Average Historical Returns", 
            ":material/partly_cloudy_day: Average Historical Returns", 
            ":material/sunny: Above Historical Average Returns"
        ])
        
        # Display each percentile in its tab
        with tab_10th:
            create_cash_flow_tab(processed_results["10th"]["df_formatted"], 
                            processed_results["10th"]["df_values"], 
                            ":material/thunderstorm: With Significantly Below Historical Average Returns",
                            "download_key_10th")
        
        with tab_25th:
            create_cash_flow_tab(processed_results["25th"]["df_formatted"], 
                            processed_results["25th"]["df_values"], 
                            ":material/rainy: With Below Historical Average Returns",
                            "download_key_25th"
                            )
        
        with tab_50th:
            create_cash_flow_tab(processed_results["50th"]["df_formatted"], 
                            processed_results["50th"]["df_values"], 
                            ":material/partly_cloudy_day: With Average Historical Returns",
                            "download_key_50th"
                            )
        
        with tab_75th:
            create_cash_flow_tab(processed_results["75th"]["df_formatted"], 
                            processed_results["75th"]["df_values"], 
                            ":material/sunny: With Above Historical Average Returns", 
                            "download_key_75th"
                            )

def create_cash_flow_tab(df_cashflow, df_cashflow_value, title, download_button_key):
    """Create a tab with cash flow details and visualizations"""
    # Display title
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### " + title + " details")

    # # Create columns with 10% padding on each side (10% - 80% - 10%)
    # content_area, right_spacer = st.columns([10, 0])
    # with content_area:

    # Apply styling to columns that exist
    columns_to_style = []
    target_columns = ['beginning_balance', 'ending_balance', 'investment_return_total', 'return_rate']

    # Only add columns that actually exist in the dataframe
    for col in target_columns:
        if col in df_cashflow.columns:
            columns_to_style.append(col)

    
    # Apply styling
    if columns_to_style:
        styled_df = df_cashflow.style.apply(highlight_columns, subset=columns_to_style)
    else:
        styled_df = df_cashflow.style
    
    # Create tabs for visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        ":material/attach_money: Portfolio Balance", 
        ":material/bar_chart: Market Returns", 
        ":material/mintmark: Withdrawal Rate", 
        ":material/table_view: Cash Flow Details"
    ])
    
    positive_color = "#55AA55"
    negative_color = "#DD5050"
    
    with tab1: 

        # Create portfolio balance chart
        chart = create_balance_chart(df_cashflow_value, positive_color, negative_color)
        if chart:
            st.altair_chart(chart, use_container_width=True)
    
    with tab2: 
        # Create return chart with actual column names
        chart = create_return_chart(df_cashflow_value, positive_color, negative_color)
        if chart:
            st.altair_chart(chart, use_container_width=True)
    
    with tab3: 
        # Create withdrawal chart with actual column names
        chart = create_withdrawal_chart(df_cashflow_value, positive_color, negative_color)
        if chart:
            st.altair_chart(chart, use_container_width=True)
    
    with tab4: 
        # Display the dataframe
        st.markdown("###### Cashflow ")   
        st.dataframe(styled_df, hide_index=True, use_container_width=True)

        csv1 = df_cashflow_value.to_csv(index=False)
        st.download_button(
            label="Download Cashflow Data",
            key=download_button_key, #key need to be different for each tab
            data=csv1,
            file_name="retirement_cashflow.csv",
            mime="text/csv",
            type="primary",
            icon=":material/download:"
        )           

def flatten_nested_dataframe(df):
    """
    Flatten a DataFrame with nested dictionaries into a flat DataFrame
    with individual columns for each nested value.
    """
    df_flat = df.copy()
    
    # Process each nested dictionary column
    nested_columns = ['income', 'expenses', 'draws', 'investment_return', 'account_balances']
    
    for col in nested_columns:
        if col in df.columns:

            # Extract each nested key as its own column
            nested_data = df[col].apply(pd.Series)
            
            # Add prefix to avoid column name conflicts
            nested_data = nested_data.add_prefix(f"{col}_")
            
            # Drop the original nested column
            df_flat = df_flat.drop(columns=[col])
            
            # Join the flattened columns back to the main dataframe
            df_flat = pd.concat([df_flat, nested_data], axis=1)

    if 'contributions' in df.columns:
        try:
            df_flat['self_contribution'] = df['contributions'].apply(lambda x: x[0] if len(x) > 0 else 0)
            df_flat['partner_contribution'] = df['contributions'].apply(lambda x: x[1] if len(x) > 1 else 0)
            df_flat = df_flat.drop(columns=['contributions'])
        except Exception as e:
            st.warning(f"Error processing contributions: {e}")

    # Calculate useful derived metrics
    if 'beginning_balance' in df_flat.columns and 'investment_return_total' in df_flat.columns:
        # Handle division by zero - set return_rate to 0 when beginning_balance is 0
        df_flat['return_rate'] = np.where(
            df_flat['beginning_balance'] > 0,  # Condition
            df_flat['investment_return_total'] / df_flat['beginning_balance'],  # When balance > 0
            0  # When balance = 0
        )

    if 'portfolio_draw' in df_flat.columns and 'beginning_balance' in df_flat.columns:
        # Handle division by zero - set withdrawal_rate to 0 when beginning_balance is 0
        df_flat['withdrawal_rate'] = np.where(
            df_flat['beginning_balance'] > 0,  # Condition
            df_flat['portfolio_draw'] / df_flat['beginning_balance'],  # When balance > 0
            0  # When balance = 0
        )


    return df_flat

def reorder_columns(df):
    """
    Reorder DataFrame columns with specified columns first,
    and remaining columns in alphabetical order.
    """
    # Define the desired column order for primary columns
    # These columns will appear first in the specified order
    primary_columns = [
        'year',
        'self_age',
        'partner_age',
        'beginning_balance',
        'portfolio_draw',
        'ending_balance',
        'income_self_earnings',
        'income_partner_earnings',
        'investment_return_total',
        'expenses_basic',
        'expenses_mortgage',
        'tax',
        'draws_total',
        'income_self_social_security',
        'income_partner_social_security',
        'income_self_pension',
        'income_partner_pension',
        'income_rental',
        'expenses_one_time',
        'expenses_self_healthcare',
        'expenses_partner_healthcare',
        'return_rate',
        'withdrawal_rate',
        'end_value_constant_currency',
        'downsize_proceeds',
        'windfall_amount',
        'account_balances_self_401k',
        'self_contribution',
        'investment_return_self_401k',
        'draws_self_401k',
        'account_balances_partner_401k',
        'partner_contribution',
        'investment_return_partner_401k',
        'draws_partner_401k',
        'account_balances_brokerage',
        'investment_return_brokerage',
        'draws_brokerage',
        'account_balances_cash',
        'investment_return_cash',
        'draws_cash',
        'account_balances_roth_ira',
        'investment_return_roth_ira',
        'draws_roth_ira',
        'expense_adjustment',
        'simulation_id'
    ]
    
    # Filter the primary columns to only include those that exist in the dataframe
    ordered_columns = [col for col in primary_columns if col in df.columns]
    
    # Get any remaining columns and sort them alphabetically
    remaining_columns = [col for col in df.columns if col not in ordered_columns]
    remaining_columns.sort()  # Sort alphabetically
    
    # Combine primary columns with remaining columns
    final_column_order = ordered_columns + remaining_columns
    
    # Return a new DataFrame with reordered columns
    return df[final_column_order]


def create_balance_chart(df, positive_color, negative_color):
    """Create a chart showing portfolio balance over time in millions"""
    if 'year' not in df.columns or 'ending_balance' not in df.columns:
        st.error(f"Cannot create portfolio balance chart: Missing required columns.")
        return None
    
    # Create a copy of the dataframe to avoid modifying the original
    chart_df = df.copy()
    
    # Convert ending_balance to millions
    chart_df['ending_balance_millions'] = chart_df['ending_balance'] / 1_000_000
    
    # Create the base chart with values in millions
    chart = alt.Chart(chart_df).mark_bar().encode(
        x='year:O',
        y=alt.Y('ending_balance_millions:Q', title='Portfolio Balance (Millions $)'),
        color=alt.condition(
            'datum.ending_balance_millions < 0',
            alt.value(negative_color),
            alt.value(positive_color)
        )
    ).properties(
        title='Portfolio Balance Over Time'
    ).transform_calculate(
        # Create a formatted text field for the labels
        # FormattedValue='format(datum.ending_balance_millions, ".1f") + "M"'
        FormattedValue='format(datum.ending_balance_millions, ".1f")'
    )
    
    # Create base text marks
    text = chart.mark_text(align='center', baseline='middle').encode(
        text='FormattedValue:N'  # Use the formatted value we calculated
    )
    
    # Text above positive bars
    textAbove = text.transform_filter(
        'datum.ending_balance_millions >= 0'
    ).mark_text(
        align='center', 
        baseline='middle', 
        fontSize=10, 
        dy=-10,
        color=positive_color  # Use the same green color as the bars
    )
    
    # Text below negative bars
    textBelow = text.transform_filter(
        'datum.ending_balance_millions < 0'
    ).mark_text(
        align='center', 
        baseline='middle', 
        fontSize=10, 
        dy=10,
        color=negative_color  # Use the same red color as the bars
    )
    
    # Combine chart and text layers
    return chart + textAbove + textBelow


def create_return_chart(df, positive_color, negative_color):
    """Create a chart showing portfolio returns"""
    if 'year' not in df.columns or 'return_rate' not in df.columns:
        st.error(f"Cannot create return chart: Missing required columns.")
        return None
    
    chart = alt.Chart(df).mark_bar().encode(
        x='year:O',
        y=alt.Y('return_rate:Q', title='Portfolio Return %', axis=alt.Axis(format='%')),
        color=alt.condition(
            'datum.return_rate < 0',
            alt.value(negative_color),
            alt.value(positive_color)
        )
    ).properties(
        title='Portfolio Return % by Year'
    ).transform_calculate(
        ScaledValue='datum.return_rate * 100'
    )
    
    # Create text labels
    text = chart.mark_text(align='center', baseline='middle').encode(
        text=alt.Text('ScaledValue:Q', format='.1f')
    )
    
    textAbove = text.transform_filter(
        'datum.return_rate >= 0'
    ).mark_text(
        align='center', baseline='middle', fontSize=10, dy=-10
    )
    
    textBelow = text.transform_filter(
        'datum.return_rate < 0'
    ).mark_text(
        align='center', baseline='middle', fontSize=10, dy=10
    )
    
    return chart + textAbove + textBelow

def create_withdrawal_chart(df, positive_color, negative_color):
    """Create a chart showing withdrawal rates"""
    if 'year' not in df.columns or 'withdrawal_rate' not in df.columns:
        st.error(f"Cannot create withdrawal chart: Missing required columns.")
        return None
    
    chart = alt.Chart(df).mark_bar().encode(
        x='year:O',
        y=alt.Y('withdrawal_rate:Q', title='Withdrawal Rate %', axis=alt.Axis(format='%')),
        color=alt.condition(
            'datum.withdrawal_rate < 0',
            alt.value(negative_color),
            alt.value(positive_color)
        )
    ).properties(
        title='Withdrawal Rate % by Year'
    ).transform_calculate(
        ScaledValue='datum.withdrawal_rate * 100'
    )
    
    # Create text labels
    text = chart.mark_text(align='center', baseline='middle').encode(
        text=alt.Text('ScaledValue:Q', format='.1f')
    )
    
    textAbove = text.transform_filter(
        'datum.withdrawal_rate >= 0'
    ).mark_text(
        align='center', baseline='middle', fontSize=10, dy=-10
    )
    
    textBelow = text.transform_filter(
        'datum.withdrawal_rate < 0'
    ).mark_text(
        align='center', baseline='middle', fontSize=10, dy=10
    )
    
    return chart + textAbove + textBelow

def highlight_columns(s):
    """Apply conditional styling to specific columns"""
    styles = []
    for value in s:
        try:

            # Handle the value as string for preprocessing
            value_str = str(value)
            
            # Check if it's a percentage
            if '%' in value_str:
                # Remove % sign and convert to float
                numeric_value = float(value_str.replace('%', ''))
            else:
                # Handle monetary or regular number values
                numeric_value = float(value_str.replace('$', '').replace(',', ''))
                       
            # Apply styling based on value
            if numeric_value >= 0:
                styles.append('background-color: #ECFBEC; font-weight: bold;')  # Green background for positive
            else:
                styles.append('background-color: #F9DFDF; font-weight: bold;')  # Red background for negative
        except ValueError:
            # If conversion fails, use default styling
            styles.append('')
            
    return styles


# Run the main app
if __name__ == "__main__":
    main()
