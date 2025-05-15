import pandas as pd

# def display_balances(end_balance_10th_millions, end_balance_50th_millions, end_balance_90th_millions):
#     balance_display = (
#         f"<span style='color:#000000; font-weight:semi-bold; font-size:20px;'>End of Plan Balances </span> "
#         f"<span style='margin-left:40px; color:#777777; font-size:16px;'>10th Percentile:</span> "
#         f"<span style='margin-left:5px; color:#CC5555; font-size:24px;'>{end_balance_10th_millions:.2f}M</span> "
#         f"<span style='color:#777777; font-size:16px; margin-left:40px;'>50th Percentile:</span> "
#         f"<span style='margin-left:5px; color:#5555CC; font-size:24px;'>{end_balance_50th_millions:.2f}M</span> "
#         f"<span style='color:#777777; font-size:16px; margin-left:40px;'>90th Percentile:</span> "
#         f"<span style='margin-left:5px; color:#33AA33; font-size:24px;'>{end_balance_90th_millions:.2f}M</span>"
#     )
#     return balance_display

def display_balances(end_balance_10th, end_balance_50th, end_balance_90th):
    # Function to convert to numeric if necessary
    def convert_to_numeric(value):
        if isinstance(value, str):
            return pd.to_numeric(value.replace(',', '').replace('M', ''), errors='coerce')
        return float(value)  # If it's already a number, just return it as float

    # Convert values to numeric, handling any formatting issues
    end_balance_10th_millions = convert_to_numeric(end_balance_10th)
    end_balance_50th_millions = convert_to_numeric(end_balance_50th)
    end_balance_90th_millions = convert_to_numeric(end_balance_90th)

    # Update the green color to a darker shade
    color_10th = "#CC5555" if end_balance_10th_millions < 0 else "#228B22"  # Darker green
    color_50th = "#CC5555" if end_balance_50th_millions < 0 else "#228B22"  # Darker green
    color_90th = "#CC5555" if end_balance_90th_millions < 0 else "#228B22"  # Darker green

    balance_display = (
        f"<span style='color:#000000; font-weight:semi-bold; font-size:20px;'>End of Plan Balances </span> "
        f"<span style='margin-left:40px; color:#555555; font-size:18px;'>10th Percentile:</span> "
        f"<span style='margin-left:5px; color:{color_10th}; font-size:24px;'>{end_balance_10th_millions:.2f}M</span> "
        f"<span style='color:#555555; font-size:18px; margin-left:40px;'>50th Percentile:</span> "
        f"<span style='margin-left:5px; color:{color_50th}; font-size:24px;'>{end_balance_50th_millions:.2f}M</span> "
        f"<span style='color:#555555; font-size:18px; margin-left:40px;'>90th Percentile:</span> "
        f"<span style='margin-left:5px; color:{color_90th}; font-size:24px;'>{end_balance_90th_millions:.2f}M</span>"
    )
    return balance_display