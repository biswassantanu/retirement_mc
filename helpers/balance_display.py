# helpers/balance_display.py

def display_balances(end_balance_10th_millions, end_balance_50th_millions, end_balance_90th_millions):
    balance_display = (
        f"<span style='color:#000000; font-weight:semi-bold; font-size:20px;'>End of Plan Balances </span> "
        f"<span style='margin-left:40px; color:#777777; font-size:16px;'>10th Percentile:</span> "
        f"<span style='margin-left:5px; color:#CC5555; font-size:24px;'>{end_balance_10th_millions:.2f}M</span> "
        f"<span style='color:#777777; font-size:16px; margin-left:40px;'>50th Percentile:</span> "
        f"<span style='margin-left:5px; color:#5555CC; font-size:24px;'>{end_balance_50th_millions:.2f}M</span> "
        f"<span style='color:#777777; font-size:16px; margin-left:40px;'>90th Percentile:</span> "
        f"<span style='margin-left:5px; color:#33AA33; font-size:24px;'>{end_balance_90th_millions:.2f}M</span>"
    )
    return balance_display