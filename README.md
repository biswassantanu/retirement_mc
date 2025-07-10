
# Retirement Analysis with Monte Carlo Simulation

A powerful financial planning tool built with Streamlit that helps you analyze retirement scenarios using Monte Carlo simulations.

## Overview

This application provides a comprehensive retirement planning framework using Monte Carlo simulation to model the uncertainty in market returns and inflation. It helps users visualize different retirement scenarios and understand the probability of financial success in retirement.

## Features

- **Interactive Input Interface**: Easily adjust all key retirement parameters through an intuitive tabbed interface.
- **Monte Carlo Simulation**: Run thousands of simulations to model different market scenarios.
- **Multiple Scenarios**: View results for different percentiles (worst case, below average, most likely, best case).
- **Detailed Analysis**: Explore year-by-year cash flows, investment returns, and withdrawal rates.
- **Data Visualization**: Interactive charts showing portfolio balance, market returns, and withdrawal rates.
- **Parameter Management**: Save and load simulation parameters for future reference.

### Key Parameters Include:

- **Personal Profile**: Age, retirement age, life expectancy.
- **Investment Allocation**: Stock/bond percentages, initial balances across account types.
- **Income Sources**: Salary, pension, Social Security, rental income.
- **Retirement Accounts**: 401(k), IRA, Roth IRA contributions and employer matches.
- **Expenses**: Living expenses, healthcare costs, mortgage payments.
- **Market Assumptions**: Return rates, volatility, inflation.
- **Special Events**: Home downsizing, one-time expenses, windfalls.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/retirement-analysis.git
   cd retirement-analysis
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run mc_rf.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501).

3. Input your financial parameters using the tabbed interface.

4. Click "Run Simulation" to generate results.

5. Download your parameters for future use with the "Download Simulation Parameters" button.

## Technical Details

### Technology Stack

- **Streamlit**: Front-end interface and interactivity.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical computations.
- **Plotly/Altair**: Data visualization.
- **Monte Carlo Methods**: Financial simulation.

## Analysis Methodology

The application uses a sophisticated Monte Carlo simulation approach:

1. **Asset Return Modeling**: Models stock and bond returns using configurable distributions.
2. **Income Planning**: Accounts for various income sources throughout retirement.
3. **Dynamic Withdrawals**: Models portfolio withdrawals based on retirement expenses.
4. **Tax Consideration**: Incorporates basic tax impacts on withdrawals.
5. **Longevity Risk**: Models outcomes through the user's specified life expectancy.
6. **Special Events**: Handles life events like downsizing, healthcare needs, and windfalls.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This application provides financial modeling for educational purposes only. It should not be considered financial advice. Always consult with a qualified financial advisor for personalized retirement planning.
```
