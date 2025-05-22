# Function to create a linear speed dial
def create_linear_indicator(score, label="Success Rate"):
    # Normalize the score to a range of 0 to 100

    normalized_score = round(min(max(score, 0), 100))
    #normalized_score = min(max(score, 0), 100)

    # Create HTML for the linear indicator
    indicator_html = f"""
    <style>
        .container {{
            width: 240px;  /* Reduced width for 20% smaller size */
            height: 24px;  /* Reduced height for 20% smaller size */
            position: relative;
            background: darkgrey; /* Dark grey background for the dial */
            border-radius: 5px;
            margin: 20px 0;
        }}
        .gradient {{
            position: absolute;
            width: 100%;
            height: 100%;
            background: linear-gradient(to right, rgba(255, 100, 100, 0.8), rgba(255, 255, 100, 0.8), rgba(100, 200, 100, 0.8)); /* Less washed out gradient */
            border-radius: 5px;
            z-index: 1;
        }}
        .indicator {{
            position: absolute;
            width: 5px;
            height: 24px; /* Shortened height of the indicator */
            background: blue;
            left: {normalized_score * 2.4}px; /* Scale to match the width of the container */
            transform: translateX(-50%);
            z-index: 2;
        }}
        .score {{
            position: absolute;
            top: -20px; /* Position the score above the bar */
            left: {normalized_score * 2.4}px; /* Center the score above the indicator */
            transform: translateX(-50%);
            font-size: 12px; /* Reduced font size */
            color: black; /* Grey color for the score */
        }}
        .label {{
            font-size: 24px; /* Reduced font size for the label */
            font-weight: bold; /* Made the label bold */
            color: #333333; /* black color for the label */
            margin-right: 20px; /* Space between label and indicator */ 
        }}
        .label-container {{
            display: flex;
            align-items: center; /* Center align label and indicator */
        }}
    </style>
    <div class="label-container">
        <div class="label">{label}</div>
        <div class="container">
            <div class="gradient"></div>
            <div class="indicator"></div>
            <div class="score">{normalized_score}%</div>
        </div>
    </div>
    """
    
    return indicator_html
