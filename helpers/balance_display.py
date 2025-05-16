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
        f"<span style='color:#000000; font-weight:semi-bold; font-size:24px;'>End of Plan Balances: </span> "
        f"<span style='margin-left:10px; color:#555555; font-size:16px;'>Worst Case:</span> "
        f"<span style='margin-left:5px; color:{color_10th}; font-size:20px;'>{end_balance_10th_millions:.2f}M</span> "
        f"<span style='color:#555555; font-size:16px; margin-left:20px;'>Most Likely:</span> "
        f"<span style='margin-left:5px; color:{color_50th}; font-size:20px;'>{end_balance_50th_millions:.2f}M</span> "
        f"<span style='color:#555555; font-size:16px; margin-left:20px;'>Best Case:</span> "
        f"<span style='margin-left:5px; color:{color_90th}; font-size:20px;'>{end_balance_90th_millions:.2f}M</span>"
    )
    return balance_display