import streamlit as st
from policyengine_core.charts import *
from household_impact import display_household_impact
from societal_impact import display_societal_impact
from streamlit_float import *

# Initialize float feature/capability
float_init()

# Custom CSS to ensure the floating header is positioned correctly
st.markdown("""
    <style>
        .floating-header {
            position: fixed;
            top: 46px; 
            width: 100%;
            background-color: white;
            z-index: 9999 !important;
            padding: 10px 0;
        }
        .spacer {
            height: 100px; /* Adjust this value to create enough space */
        }
    </style>
    """, unsafe_allow_html=True)

# Create a container for the floating header
header_container = st.container()
with header_container:
    st.header("UK 2024 Election Manifestos")
header_container.markdown('<div class="floating-header"></div>', unsafe_allow_html=True)
header_container.float("top:50px; background-color: white; z-index: 9999;")

st.markdown(
    "This interactive app compares the societal and household-level impacts of the Conservative, Labour and Liberal Democrat manifestos."
)

year = st.selectbox(
    "Select a year", options=[2025, 2026, 2027, 2028], index=3, key="year"
)

include_indirect_impacts = st.checkbox(
    "Include indirect impacts",
    help="Include estimates of indirect impacts through public spending or non-household taxes.",
    value=True,
)

# Create tabs
tab1, tab2 = st.tabs(["Societal Impacts", "Household Impacts"])

with tab1:
    display_societal_impact(year, include_indirect_impacts)

with tab2:
    display_household_impact(year, include_indirect_impacts)
