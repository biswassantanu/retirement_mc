import streamlit as st
import numpy as np

# Function to create a linear speed dial
def create_linear_indicator(score):
    # Normalize the score to a range of 0 to 100
    normalized_score = min(max(score, 0), 100)

    # Create HTML for the linear indicator
    indicator_html = f"""
    <style>
        .container {{
            width: 300px;
            height: 50px;
            position: relative;
            background: linear-gradient(to right, red, yellow, green);
            border-radius: 5px;
            margin: 20px 0;
        }}
        .indicator {{
            position: absolute;
            width: 5px;
            height: 100%;
            background: black;
            left: {normalized_score * 3}px; /* Scale to match the width of the container */
            transform: translateX(-50%);
        }}
        .score {{
            position: absolute;
            top: -30px; /* Position the score above the bar */
            left: {normalized_score * 3}px; /* Center the score above the indicator */
            transform: translateX(-50%);
            font-size: 24px;
            font-weight: bold;
            color: black;
        }}
    </style>
    <div class="container">
        <div class="indicator"></div>
        <div class="score">{normalized_score}%</div>
    </div>
    """
    
    return indicator_html

# Streamlit app
st.title("Monte Carlo Simulation Results")

# Example score (you can replace this with your actual score)
success_probability_score = np.random.randint(0, 101)  # Random score for demonstration

# Display the linear indicator
st.markdown(create_linear_indicator(success_probability_score), unsafe_allow_html=True)
