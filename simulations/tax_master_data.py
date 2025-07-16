# tax_master_data.py

# Contribution limits and tax rates
contribution_limits = {
    "401k": {
        "2025": 23500,
        "2024": 23000,
        "2023": 22500,
        "2022": 20000,
        "2021": 19500
    },
    "catch_up": {
        "2025": 7500,
        "2024": 7500,
        "2023": 7500,
        "2022": 6500,
        "2021": 6500
    }
}

# 401k Catchup age 
catchup_age_401k = 50 

# Federal tax brackets (2023)
federal_tax_brackets = [
    {"limit": 11000, "rate": 0.10},
    {"limit": 44725, "rate": 0.12},
    {"limit": 95375, "rate": 0.22},
    {"limit": 182100, "rate": 0.24},
    {"limit": 231250, "rate": 0.32},
    {"limit": 578125, "rate": 0.35},
    {"limit": float('inf'), "rate": 0.37}  # No upper limit for the highest bracket
]

# Social Security tax treatment brackets for benefits
social_security_tax_brackets = [
    {"limit": 25000, "rate": 0.0},  # Single filers
    {"limit": 34000, "rate": 0.5},  # Up to 50% taxable
    {"limit": float('inf'), "rate": 0.85}  # Up to 85% taxable
]

# Long-term capital gains tax brackets (2023)
long_term_capital_gains_brackets = [
    {"limit": 44625, "rate": 0.0},  # 0% for single filers
    {"limit": 492300, "rate": 0.15},  # 15% for single filers
    {"limit": float('inf'), "rate": 0.20}  # 20% for single filers
]

# RMD factors (based on IRS Uniform Lifetime Table)
rmd_factors = {
    73: 27.4,
    74: 26.5,
    75: 25.6,
    76: 24.7,
    77: 23.8,
    78: 22.9,
    79: 22.0,
    80: 21.1,
    81: 20.2,
    82: 19.3,
    83: 18.4,
    84: 17.5,
    85: 16.6,
    86: 15.7,
    87: 14.8,
    88: 13.9,
    89: 13.0,
    90: 12.1,
    91: 11.2,
    92: 10.3,
    93: 9.4,
    94: 8.5,
    95: 7.6,
    96: 6.7,
    97: 5.8,
    98: 4.9,
    99: 4.0,
    100: 3.1
}

# State tax brackets for various states (2023)
state_tax_brackets = {
    "CA": [
        {"limit": 8932, "rate": 0.01},
        {"limit": 21175, "rate": 0.02},
        {"limit": 33421, "rate": 0.04},
        {"limit": 46394, "rate": 0.06},
        {"limit": 58634, "rate": 0.08},
        {"limit": 299508, "rate": 0.093},
        {"limit": 359407, "rate": 0.103},
        {"limit": 599012, "rate": 0.113},
        {"limit": float('inf'), "rate": 0.123}
    ],
    "TX": [
        # Texas has no state income tax
    ],
    "FL": [
        # Florida has no state income tax
    ],
    "NY": [
        {"limit": 8500, "rate": 0.04},
        {"limit": 11700, "rate": 0.045},
        {"limit": 13900, "rate": 0.0525},
        {"limit": 21400, "rate": 0.059},
        {"limit": 80650, "rate": 0.0621},
        {"limit": 215400, "rate": 0.0649},
        {"limit": float('inf'), "rate": 0.0685}
    ],
    "OR": [
        {"limit": 3500, "rate": 0.05},
        {"limit": 9000, "rate": 0.07},
        {"limit": float('inf'), "rate": 0.09}
    ],
    "WA": [
        # Washington has no state income tax
    ],
    "IL": [
        {"limit": float('inf'), "rate": 0.0495}  # Flat rate
    ],
    "GA": [
        {"limit": 750, "rate": 0.01},
        {"limit": 2250, "rate": 0.02},
        {"limit": 3750, "rate": 0.03},
        {"limit": 5250, "rate": 0.04},
        {"limit": 7000, "rate": 0.05},
        {"limit": float('inf'), "rate": 0.06}
    ]
}

# State capital gains tax rates (if applicable)
state_capital_gains_tax_rates = {
    "CA": 0.093,  # California capital gains taxed as regular income
    "TX": 0.0,    # No state income tax
    "FL": 0.0,    # No state income tax
    "NY": 0.0621, # New York capital gains taxed as regular income
    "OR": 0.09,   # Oregon capital gains taxed as regular income
    "WA": 0.0,    # No state income tax
    "IL": 0.0495, # Illinois capital gains taxed as regular income
    "GA": 0.06    # Georgia capital gains taxed as regular income
}

# State-specific treatment of Social Security benefits
state_social_security_treatment = {
    "CA": False,  # Does not tax Social Security benefits
    "TX": False,  # Does not tax Social Security benefits
    "FL": False,  # Does not tax Social Security benefits
    "NY": True,   # Taxes Social Security benefits based on income
    "OR": True,   # Taxes Social Security benefits based on income
    "WA": False,  # Does not tax Social Security benefits
    "IL": True,   # Taxes Social Security benefits based on income
    "GA": True    # Taxes Social Security benefits based on income
}