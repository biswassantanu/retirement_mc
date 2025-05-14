# Tab styling CSS
tab_style_css ="""
        <style>
            .stTabs [data-baseweb="tab-list"] {
                gap: 5px;
            }

            .stTabs [data-baseweb="tab"] {
                height: 32px;
                white-space: pre-wrap;
                background-color: #F0F2F6; /* Background color for inactive tabs */
                border-radius: 4px 4px 0px 0px;
                gap: 1px;
                padding-top: 5px;
                padding-bottom: 5px;
                padding-right: 10px;
                padding-left: 10px;
            }

            /* Active tab styling */
            .stTabs [aria-selected="true"] {
                background-color: #FFFFFF; /* Active tab background color */
                color: inherit; /* Use default text color */
                border-bottom: 2px solid #FFFFFF; /* Optional: Change underline color to match the active tab */
            }

            /* Change the text color of inactive tabs */
            .stTabs [data-baseweb="tab"] {
                color: #333; /* Change inactive tab text color */
            }
        </style>
    """