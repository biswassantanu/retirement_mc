import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
from scipy.stats import t
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Any
import copy

from simulations.historical_returns import historical_equity_returns, historical_bond_returns
from simulations.tax_master_data import contribution_limits, cathup_age_401k


# Constants
CASH_ACCOUNT_RETURN_RATE = 0.015  # 1.5%


@dataclass
class SimulationConfig:
    """Configuration parameters for the simulation"""
    current_age: int
    partner_current_age: int
    life_expectancy: int
    retirement_age: int
    partner_retirement_age: int
    
    # Initial balances
    initial_savings: float
    self_401k_balance: float
    partner_401k_balance: float
    roth_ira_balance: float
    cash_savings_balance: float
    brokerage_balance: float
    
    # Income parameters
    annual_earnings: float
    partner_earnings: float
    self_yearly_increase: float
    partner_yearly_increase: float
    annual_pension: float
    partner_pension: float
    self_pension_yearly_increase: float
    partner_pension_yearly_increase: float
    annual_social_security: float
    partner_social_security: float
    withdrawal_start_age: int
    partner_withdrawal_start_age: int
    
    # 401k parameters
    self_401k_contribution: float
    partner_401k_contribution: float
    employer_self_401k_contribution: float
    employer_partner_401k_contribution: float
    maximize_self_contribution: bool
    maximize_partner_contribution: bool
    
    # Tax Parameters 
    filing_status:str
    state_of_residence:str
    tax_rate: float

    # Expense parameters
    annual_expense: float
    mortgage_payment: float
    mortgage_years_remaining: int
    self_healthcare_cost: float
    partner_healthcare_cost: float
    self_healthcare_start_age: int
    partner_healthcare_start_age: int
    annual_expense_decrease: float
    
    # Investment parameters
    stock_percentage: float
    bond_percentage: float
    stock_return_mean: float
    bond_return_mean: float
    stock_return_std: float
    bond_return_std: float
    
    # Simulation parameters
    simulations: int
    simulation_type: str
    cola_rate: float
    inflation_mean: float
    inflation_std: float
    
    # Special events
    years_until_downsize: int
    residual_amount: float
    adjust_expense_years: List[int]
    adjust_expense_amounts: List[float]
    one_time_years: List[int]
    one_time_amounts: List[float]
    windfall_years: List[int]
    windfall_amounts: List[float]
    
    # Rental income
    rental_start: int
    rental_end: int
    rental_amt: float
    rental_yearly_increase: float


@dataclass
class AccountBalances:
    """Tracks current balances across different account types"""
    self_401k: float
    partner_401k: float
    roth_ira: float
    brokerage: float
    cash: float
    
    @property
    def total(self) -> float:
        """Calculate total account balance"""
        return self.self_401k + self.partner_401k + self.roth_ira + self.brokerage + self.cash


@dataclass
class YearlyReturns:
    """Investment returns for a given year"""
    self_401k: float
    partner_401k: float
    roth_ira: float
    brokerage: float
    cash: float
    total: float
    
    @property
    def return_rate(self) -> float:
        """Calculate overall return rate"""
        # This is simplified and should be calculated based on beginning balances
        return self.total / 100 if self.total != 0 else 0


@dataclass
class YearlyDraws:
    """Withdrawal amounts for a given year"""
    self_401k: float
    partner_401k: float
    roth_ira: float
    brokerage: float
    cash: float
    total: float


@dataclass
class YearlyIncome:
    """Income sources for a given year"""
    self_earnings: float
    partner_earnings: float
    self_social_security: float
    partner_social_security: float
    self_pension: float
    partner_pension: float
    rental: float
    
    @property
    def total(self) -> float:
        """Calculate total income"""
        return (self.self_earnings + self.partner_earnings + 
                self.self_social_security + self.partner_social_security +
                self.self_pension + self.partner_pension + self.rental)


@dataclass
class YearlyExpenses:
    """Expense categories for a given year"""
    basic: float
    mortgage: float
    self_healthcare: float
    partner_healthcare: float
    one_time: float
    
    @property
    def total(self) -> float:
        """Calculate total expenses"""
        return (self.basic + self.mortgage + 
                self.self_healthcare + self.partner_healthcare + 
                self.one_time)


@dataclass
class YearlyCashFlow:
    """Complete cash flow for a given year"""
    year: int
    self_age: int
    partner_age: int
    
    income: YearlyIncome
    expenses: YearlyExpenses
    tax: float
    
    beginning_balance: float
    ending_balance: float
    end_value_constant_currency: float
    
    portfolio_draw: float
    draws: YearlyDraws
    
    investment_return: YearlyReturns
    
    # contributions: Tuple[float, float]
    contributions: List[float]  # list type

    account_balances: AccountBalances
    
    # Special events
    downsize_proceeds: float
    windfall_amount: float
    expense_adjustment: float
    
    simulation_id: Optional[int] = None


def monte_carlo_simulation(config: SimulationConfig) -> Tuple[int, int, List[Dict[str, Any]]]:
    """Run Monte Carlo simulation for retirement planning
    
    Args:
        config: Simulation configuration parameters
        
    Returns:
        Tuple containing success count, failure count, and sorted simulation results
    """
    current_year = datetime.now().year
    years_in_simulation = config.life_expectancy - config.current_age + 1
    
    success_count = 0
    failure_count = 0
    all_simulation_results = []
    
    # Get the ranges of historical equity and bond returns
    equity_return_min = min(historical_equity_returns.values()) / 100.0
    equity_return_max = max(historical_equity_returns.values()) / 100.0
    bond_return_min = min(historical_bond_returns.values()) / 100.0
    bond_return_max = max(historical_bond_returns.values()) / 100.0
    
    for sim in range(config.simulations):
        # Initialize accounts for this simulation
        balances = AccountBalances(
            self_401k=config.self_401k_balance,
            partner_401k=config.partner_401k_balance,
            roth_ira=config.roth_ira_balance,
            brokerage=config.brokerage_balance,
            cash=config.cash_savings_balance
        )
        
        # Initialize simulation variables
        savings = config.initial_savings
        current_annual_expense = config.annual_expense
        cash_flows = []
        year_of_depletion = None
        
        # Preselect return values for all years in this simulation
        returns = preselect_investment_returns(
            config.simulation_type,
            years_in_simulation,
            config.stock_return_mean, config.stock_return_std,
            config.bond_return_mean, config.bond_return_std,
            equity_return_min, equity_return_max, 
            bond_return_min, bond_return_max
        )
        
        for year in range(years_in_simulation):

            # set the initial value to 0 if balance becomes negative
            if savings < 0:
                savings = -1

            # Calculate current ages
            self_age = config.current_age + year
            partner_age = config.partner_current_age + year
            
            # Calculate income streams
            income = calculate_yearly_income(
                config, self_age, partner_age, year, current_year
            )
            
            # Calculate 401k contributions
            self_contribution = calculate_401k_contribution(
                self_age, config.retirement_age, 
                config.self_401k_contribution, config.employer_self_401k_contribution,
                current_year, year, config.cola_rate, 
                config.maximize_self_contribution, config.self_yearly_increase
            )
            
            partner_contribution = calculate_401k_contribution(
                partner_age, config.partner_retirement_age,
                config.partner_401k_contribution, config.employer_partner_401k_contribution,
                current_year, year, config.cola_rate,
                config.maximize_partner_contribution, config.partner_yearly_increase
            )
                    
            # Adjust for inflation and update annual expense
            current_annual_expense = adjust_expenses(
                current_annual_expense, config.inflation_mean, config.inflation_std,
                config.annual_expense_decrease, year, self_age, config.retirement_age,
                partner_age, config.partner_retirement_age
            )

            # Calculate expenses
            expenses = calculate_yearly_expenses(
                config, self_age, partner_age, year, current_year,
                current_annual_expense
            )

            # Calculate tax and portfolio draw
            portfolio_draw, total_tax = calculate_portfolio_draw(
                expenses.total, income.total, income.total * config.tax_rate, config.tax_rate
            )
            
            # Calculate the draw-down amount proportioned among different accounts
            draws = calculate_draws(portfolio_draw, balances)
            
            # Calculate investment returns using the selected simulation method
            investment_return = calculate_investment_return(
                config, balances, savings, returns, year
            )
            
            # Special events
            downsize_proceeds = config.residual_amount if year == config.years_until_downsize else 0
            
            windfall_amount = calculate_windfall(config.windfall_years, config.windfall_amounts, 
                                                current_year + year)
            
            expense_adjustment = get_expense_adjustment(
                config.adjust_expense_years, config.adjust_expense_amounts, current_year + year)
            
            # Update account balances
            update_account_balances(
                balances, investment_return, draws, 
                self_contribution, partner_contribution,
                income.total, expenses.total, total_tax
            )
            
            # Calculate ending portfolio values
            ending_portfolio_value = savings + investment_return.total + income.total - expenses.total - total_tax
            end_value_at_current_currency = ending_portfolio_value / ((1 + config.inflation_mean) ** (year + 1))
            
            # Create cash flow entry for this year
            cash_flow_entry = YearlyCashFlow(
                year=current_year + year,
                self_age=self_age,
                partner_age=partner_age,
                income=income,
                expenses=expenses,
                tax=total_tax,
                beginning_balance=savings,
                ending_balance=ending_portfolio_value,
                end_value_constant_currency=end_value_at_current_currency,
                portfolio_draw=portfolio_draw,
                draws=draws,
                investment_return=investment_return,
                #contributions=(copy.deepcopy(self_contribution), copy.deepcopy(partner_contribution)), # fix to address variable reference vs. new isntance
                contributions=[self_contribution, partner_contribution],  # list
                account_balances=copy.deepcopy(balances),  # fix to address variable reference vs. new isntance
                downsize_proceeds=downsize_proceeds,
                windfall_amount=windfall_amount,
                expense_adjustment=expense_adjustment,
                simulation_id=sim
            )
            
            # Add to cash flows for this simulation
            cash_flows.append(cash_flow_entry)
            
            # Set next period's opening balance
            savings = ending_portfolio_value + downsize_proceeds + windfall_amount
            
            # Check for depletion - only set once per simulation
            if savings < 0 and year_of_depletion is None:
                year_of_depletion = current_year + year
        
        # If portfolio never depleted, set year_of_depletion to final year
        if year_of_depletion is None:
            year_of_depletion = current_year + years_in_simulation - 1
        
        # Create a simulation result with all cash flows and the depletion year
        simulation_result = {
            "simulation_id": sim,
            "year_of_depletion": year_of_depletion,
            "final_balance": savings,
            "success": savings >= 0,
            "cash_flows": cash_flows
        }
        
        all_simulation_results.append(simulation_result)
        
        # Update success/failure counts
        if savings >= 0:
            success_count += 1
        else:
            failure_count += 1
    
    # Sort simulations from worst to best:
    # - Earlier depletion year is worse
    # - For same depletion year, lower final balance is worse
    sorted_simulation_results = sorted(
        all_simulation_results,
        key=lambda sim: (sim["year_of_depletion"], sim["final_balance"])
    )
    
    return success_count, failure_count, sorted_simulation_results


def preselect_investment_returns(simulation_type, years, 
                                stock_mean, stock_std, bond_mean, bond_std,
                                equity_min, equity_max, bond_min, bond_max):
    """Preselect investment returns for the entire simulation"""
    
    # For empirical distribution - get historical data
    replace_option = True if simulation_type == "Empirical Distribution" else False
    selected_years = np.random.choice(list(historical_equity_returns.keys()), 
                                    size=years, replace=replace_option)
    
    empirical_equity_returns = [historical_equity_returns[int(year)] / 100 for year in selected_years]
    empirical_bond_returns = [historical_bond_returns[int(year)] / 100 for year in selected_years]
    
    # Shuffle the empirical returns
    np.random.shuffle(empirical_equity_returns)
    np.random.shuffle(empirical_bond_returns)
    
    # Normal distribution returns
    normal_stock_returns = np.random.normal(stock_mean, stock_std, years)
    normal_bond_returns = np.random.normal(bond_mean, bond_std, years)
    
    # Clip values to reasonable bounds
    normal_stock_returns = np.clip(normal_stock_returns, equity_min, equity_max)
    normal_bond_returns = np.clip(normal_bond_returns, bond_min, bond_max)
    
    # Student-t distribution returns
    df = 5  # degrees of freedom
    t_stock_returns = t.rvs(df, loc=stock_mean, scale=stock_std, size=years)
    t_bond_returns = t.rvs(df, loc=bond_mean, scale=bond_std, size=years)
    
    # Lognormal returns (not currently used but included for completeness)
    lognormal_stock_returns = np.random.lognormal(mean=np.log(stock_mean), 
                                                sigma=stock_std, size=years)
    lognormal_bond_returns = np.random.lognormal(mean=np.log(bond_mean), 
                                                sigma=bond_std, size=years)
    
    return {
        "empirical": (empirical_equity_returns, empirical_bond_returns),
        "normal": (normal_stock_returns, normal_bond_returns),
        "t": (t_stock_returns, t_bond_returns),
        "lognormal": (lognormal_stock_returns, lognormal_bond_returns)
    }


def calculate_yearly_income(config, self_age, partner_age, year, current_year):
    """Calculate all income sources for a given year"""
    
    # Calculate earnings (employment)
    self_earnings = calculate_earnings(
        config.annual_earnings, config.self_yearly_increase,
        year, config.retirement_age, self_age
    )
    
    partner_earnings = calculate_earnings(
        config.partner_earnings, config.partner_yearly_increase,
        year, config.partner_retirement_age, partner_age
    )
    
    # Calculate Social Security benefits
    self_ss = calculate_social_security(
        config.annual_social_security, config.cola_rate,
        config.withdrawal_start_age, self_age
    )
    
    partner_ss = calculate_social_security(
        config.partner_social_security, config.cola_rate,
        config.partner_withdrawal_start_age, partner_age
    )
    
    # Calculate pension income
    self_pension = calculate_pension(
        config.annual_pension, config.self_pension_yearly_increase,
        year, config.retirement_age, self_age
    )
    
    partner_pension = calculate_pension(
        config.partner_pension, config.partner_pension_yearly_increase,
        year, config.partner_retirement_age, partner_age
    )
    
    # Calculate rental income
    if config.rental_start <= current_year + year <= config.rental_end:
        rental_income = config.rental_amt * ((1 + config.rental_yearly_increase) ** 
                                           (current_year + year - config.rental_start))
    else:
        rental_income = 0
    
    return YearlyIncome(
        self_earnings=self_earnings,
        partner_earnings=partner_earnings,
        self_social_security=self_ss,
        partner_social_security=partner_ss,
        self_pension=self_pension,
        partner_pension=partner_pension,
        rental=rental_income
    )


def calculate_yearly_expenses(config, self_age, partner_age, year, current_year, current_expense):
    """Calculate all expense categories for a given year"""
    
    # Calculate mortgage payment
    mortgage = calculate_mortgage(config.mortgage_payment, year, config.mortgage_years_remaining)
    
    # Calculate healthcare costs
    healthcare_costs, self_health_cost, partner_health_cost = calculate_healthcare_costs(
        self_age, config.self_healthcare_cost, config.self_healthcare_start_age,
        partner_age, config.partner_healthcare_cost, config.partner_healthcare_start_age,
        config.inflation_mean
    )
    
    # Calculate one-time expenses for this year
    one_time_expense = calculate_one_time_expense(
        config.one_time_years, config.one_time_amounts, current_year + year
    )
    
    return YearlyExpenses(
        basic=current_expense,
        mortgage=mortgage,
        self_healthcare=self_health_cost,
        partner_healthcare=partner_health_cost,
        one_time=one_time_expense
    )


def calculate_investment_return(config, balances, savings, returns, year):
    """Calculate investment returns across all account types"""
    
    # Select the appropriate return rates based on simulation type
    if config.simulation_type == "Normal Distribution":
        stock_return_rate, bond_return_rate = returns["normal"][0][year], returns["normal"][1][year]
    elif config.simulation_type == "Students-T Distribution":
        stock_return_rate, bond_return_rate = returns["t"][0][year], returns["t"][1][year]
    elif config.simulation_type == "Empirical Distribution":
        stock_return_rate, bond_return_rate = returns["empirical"][0][year], returns["empirical"][1][year]
    else:
        raise ValueError(f"Unknown simulation type: {config.simulation_type}")
    
    # Calculate portfolio weighted return rate
    weighted_return = (stock_return_rate * (config.stock_percentage / 100) + 
                       bond_return_rate * (config.bond_percentage / 100))
    
    # Calculate returns for each account type
    self_401k_return = balances.self_401k * weighted_return
    partner_401k_return = balances.partner_401k * weighted_return
    roth_ira_return = balances.roth_ira * weighted_return
    brokerage_return = balances.brokerage * weighted_return
    cash_return = balances.cash * CASH_ACCOUNT_RETURN_RATE
    
    # Calculate total portfolio return
    total_return = (
        savings * (stock_return_rate * (config.stock_percentage / 100) + 
                  bond_return_rate * (config.bond_percentage / 100))
    )
    
    return YearlyReturns(
        self_401k=self_401k_return,
        partner_401k=partner_401k_return,
        roth_ira=roth_ira_return,
        brokerage=brokerage_return,
        cash=cash_return,
        total=total_return
    )


def update_account_balances(balances, returns, draws, self_contribution, partner_contribution, income, expenses, tax):
    """Update all account balances based on contributions, returns, and withdrawals"""
    
    # Update 401k balances with contributions and returns, minus draws
    balances.self_401k += self_contribution + returns.self_401k - draws.self_401k
    balances.partner_401k += partner_contribution + returns.partner_401k - draws.partner_401k
    
    # Update other account balances
    balances.roth_ira += returns.roth_ira - draws.roth_ira
    balances.cash += returns.cash - draws.cash
    
    # Calculate surplus after expenses, taxes and contributions
    net_surplus = income - expenses - tax - self_contribution - partner_contribution
    
    # Add surplus to brokerage account if positive
    if net_surplus > 0:
        balances.brokerage += returns.brokerage - draws.brokerage + net_surplus
    else:
        balances.brokerage += returns.brokerage - draws.brokerage

def calculate_draws(portfolio_draw, balances):
    """Calculate withdrawal amounts from each account type"""
    
    remaining_draw = portfolio_draw
    
    # Initialize draws
    brokerage_draw = min(remaining_draw, balances.brokerage)
    remaining_draw -= brokerage_draw
    
    self_401k_draw = min(remaining_draw, balances.self_401k)
    remaining_draw -= self_401k_draw
    
    partner_401k_draw = min(remaining_draw, balances.partner_401k)
    remaining_draw -= partner_401k_draw
    
    cash_draw = min(remaining_draw, balances.cash)
    remaining_draw -= cash_draw
    
    roth_ira_draw = min(remaining_draw, balances.roth_ira)
    remaining_draw -= roth_ira_draw
    
    return YearlyDraws(
        self_401k=self_401k_draw,
        partner_401k=partner_401k_draw,
        roth_ira=roth_ira_draw,
        brokerage=brokerage_draw,
        cash=cash_draw,
        total=portfolio_draw - remaining_draw  # Actual total drawn
    )


def calculate_earnings(starting_earnings, yearly_increment, year, retirement_age, current_age):
    """Calculate earnings based on age and retirement status"""
    if current_age < retirement_age:
        return starting_earnings * (1 + yearly_increment) ** year
    return 0


def calculate_pension(annual_pension, pension_yearly_increase, year, retirement_age, current_age):
    """Calculate pension income based on retirement status"""
    if current_age >= retirement_age:
        return annual_pension * (1 + pension_yearly_increase) ** (current_age - retirement_age)
    return 0


def calculate_social_security(annual_ss, cola_rate, withdrawal_start_age, current_age):
    """Calculate social security benefits based on eligibility age"""
    if current_age >= withdrawal_start_age:
        return annual_ss * (1 + cola_rate) ** (current_age - withdrawal_start_age)
    return 0


def calculate_mortgage(mortgage_payment, year, mortgage_years_remaining):
    """Calculate mortgage payment based on remaining years"""
    return mortgage_payment if year < mortgage_years_remaining else 0


def calculate_healthcare_costs(current_age, self_healthcare_cost, self_healthcare_start_age, 
                               partner_current_age, partner_healthcare_cost, partner_healthcare_start_age,
                               inflation_mean):
    """Calculate healthcare costs for both self and partner"""
    self_cost = 0
    partner_cost = 0
    
    # Self healthcare costs
    if current_age >= self_healthcare_start_age:
        if current_age < 65:  # Medicare age
            self_cost = self_healthcare_cost * (1 + inflation_mean)**(current_age - self_healthcare_start_age)
        else:
            self_cost = 0
    
    # Partner healthcare costs
    if partner_current_age >= partner_healthcare_start_age:
        if partner_current_age < 65:  # Medicare age
            partner_cost = partner_healthcare_cost * (1 + inflation_mean)**(partner_current_age - partner_healthcare_start_age)
        else:
            partner_cost = 0
    
    total_cost = self_cost + partner_cost
    return total_cost, self_cost, partner_cost


def adjust_expenses(current_expense, inflation_mean, inflation_std, annual_expense_decrease, 
                    year, current_age, retirement_age, partner_current_age, partner_retirement_age):
    """Adjust expenses for inflation and retirement status"""
    if year > 0:  # Skip the first year
        inflation_rate = np.random.normal(inflation_mean, inflation_std)
        
        if current_age >= retirement_age or partner_current_age >= partner_retirement_age:
            # If one partner retired - apply expense reduction (Retirement Smile)
            return current_expense * (1 + inflation_rate - annual_expense_decrease)
        else:
            # At least one still working - only apply inflation
            return current_expense * (1 + inflation_rate)
    
    return current_expense


def calculate_portfolio_draw(total_expense, gross_income, estimated_tax, tax_rate):
    """Calculate required portfolio withdrawal and total tax"""
    if total_expense <= (gross_income - estimated_tax):
        # No withdrawal needed
        return 0, estimated_tax
    else:
        # Need to withdraw from portfolio
        portfolio_draw = total_expense - (gross_income - estimated_tax)
        portfolio_tax = portfolio_draw * tax_rate
        total_tax = portfolio_tax + estimated_tax
        
        return portfolio_draw + portfolio_tax, total_tax


def get_latest_limit(contribution_dict, current_year):
    """Get the latest available contribution limit"""
    latest_limit = 0
    for year in sorted(contribution_dict.keys(), reverse=True):
        if int(year) <= current_year:
            latest_limit = contribution_dict[year]
            break
    return latest_limit


def calculate_401k_contribution(current_age, retirement_age, yearly_contribution, employer_contribution,
                               current_year, year, cola_rate, maximize_contribution, pay_growth_rate):
    """Calculate 401k contribution including employer match and catch-up"""
    # Return 0 if already retired
    if current_age >= retirement_age:
        return 0
        
    # Get base contribution limits and adjust for COLA
    base_limit = get_latest_limit(contribution_limits["401k"], current_year)
    adjusted_limit = base_limit * ((1 + cola_rate) ** year)
    
    # Get catch-up contribution limit and adjust for COLA
    base_catch_up_limit = get_latest_limit(contribution_limits["catch_up"], current_year)
    adjusted_catch_up_limit = base_catch_up_limit * ((1 + cola_rate) ** year)
    
    # Scale contributions based on pay growth
    scaled_yearly_contribution = yearly_contribution * ((1 + pay_growth_rate) ** year)
    scaled_employer_contribution = employer_contribution * ((1 + pay_growth_rate) ** year)
    
    # Determine catch-up amount
    catch_up_amount = adjusted_catch_up_limit if current_age >= cathup_age_401k else 0
    
    # Calculate total contribution
    if maximize_contribution:
        # Maximum allowed contribution
        employee_contribution = adjusted_limit + catch_up_amount
    else:
        # Specified contribution rate, capped at maximum
        employee_contribution = min(scaled_yearly_contribution, adjusted_limit + catch_up_amount)
    
    total_contribution = employee_contribution + scaled_employer_contribution
    return total_contribution


def calculate_windfall(windfall_years, windfall_amounts, current_year):
    """Calculate windfalls for the current year"""
    windfall_amount = 0
    
    for i in range(len(windfall_years)):
        if windfall_years[i] == current_year:
            windfall_amount += windfall_amounts[i]
            
    return windfall_amount


def get_expense_adjustment(adjust_expense_years, adjust_expense_amounts, current_year):
    """Get expense adjustment for the current year"""
    expense_adjustment = 0
    
    for i in range(len(adjust_expense_years)):
        if adjust_expense_years[i] == current_year:
            expense_adjustment += adjust_expense_amounts[i]
            
    return expense_adjustment


def calculate_one_time_expense(one_time_years, one_time_amounts, current_year):
    """Calculate one-time expenses for the current year"""
    one_time_expense = 0
    
    for i in range(len(one_time_years)):
        if one_time_years[i] == current_year:
            one_time_expense += one_time_amounts[i]
            
    return one_time_expense


def convert_to_dict_for_display(cash_flow_entry):
    """Convert a YearlyCashFlow object to a dictionary for display/visualization"""
    return {
        'Year': cash_flow_entry.year,
        'Self Age': cash_flow_entry.self_age,
        'Partner Age': cash_flow_entry.partner_age,
        'Beginning Portfolio Value': cash_flow_entry.beginning_balance,
        'Gross Earnings': cash_flow_entry.income.total,
        'Total Expense': cash_flow_entry.expenses.total,
        'Tax': cash_flow_entry.tax,
        'Portfolio Draw': cash_flow_entry.portfolio_draw,
        'Investment Return': cash_flow_entry.investment_return.total,
        'Ending Portfolio Value': cash_flow_entry.ending_balance,
        'At Constant Currency': cash_flow_entry.end_value_constant_currency,
        'Downsize Proceeds': cash_flow_entry.downsize_proceeds,
        'Investment Return %': cash_flow_entry.investment_return.return_rate,
        'Drawdown %': cash_flow_entry.portfolio_draw / cash_flow_entry.ending_balance if cash_flow_entry.ending_balance > 0 else 0,
        'Self Gross Earning': cash_flow_entry.income.self_earnings,
        'Partner Gross Earning': cash_flow_entry.income.partner_earnings,
        'Self Social Security': cash_flow_entry.income.self_social_security,
        'Partner Social Security': cash_flow_entry.income.partner_social_security,
        'Combined Social Security': cash_flow_entry.income.self_social_security + cash_flow_entry.income.partner_social_security,
        'Self Pension': cash_flow_entry.income.self_pension,
        'Partner Pension': cash_flow_entry.income.partner_pension,
        'Rental Income': cash_flow_entry.income.rental,
        'Mortgage': cash_flow_entry.expenses.mortgage,
        'Healthcare Expense': cash_flow_entry.expenses.self_healthcare + cash_flow_entry.expenses.partner_healthcare,
        'Self Health Expense': cash_flow_entry.expenses.self_healthcare,
        'Partner Health Expense': cash_flow_entry.expenses.partner_healthcare,
        'Yearly Expense Adj': cash_flow_entry.expense_adjustment,
        'One Time Expense': cash_flow_entry.expenses.one_time,
        'Windfall Amt': cash_flow_entry.windfall_amount,
        'Self 401K Contribution': cash_flow_entry.contributions[0],
        'Self 401K Return': cash_flow_entry.investment_return.self_401k,
        'Self 401K Draw': cash_flow_entry.draws.self_401k,
        'Self 401K Balance': cash_flow_entry.account_balances.self_401k,
        'Partner 401K Contribution': cash_flow_entry.contributions[1],
        'Partner 401K Return': cash_flow_entry.investment_return.partner_401k,
        'Partner 401K Draw': cash_flow_entry.draws.partner_401k,
        'Partner 401K Balance': cash_flow_entry.account_balances.partner_401k,
        'Roth IRA Return': cash_flow_entry.investment_return.roth_ira,
        'Roth IRA Draw': cash_flow_entry.draws.roth_ira,
        'Roth IRA Balance': cash_flow_entry.account_balances.roth_ira,
        'Brokerage Acct Return': cash_flow_entry.investment_return.brokerage,
        'Brokerage Draw': cash_flow_entry.draws.brokerage,
        'Brokerage Acct Balance': cash_flow_entry.account_balances.brokerage,
        'Cash Return': cash_flow_entry.investment_return.cash,
        'Cash Draw': cash_flow_entry.draws.cash,
        'Cash Balance': cash_flow_entry.account_balances.cash,
        'Total Acct Balance': cash_flow_entry.account_balances.total,
        'Simulation ID': cash_flow_entry.simulation_id
    }
