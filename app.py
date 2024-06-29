import streamlit as st
from policyengine_core.charts import *
from household_impact import display_household_impact
from societal_impact import display_societal_impact


# Streamlit code for displaying the data
st.title("UK 2024 Election Manifestos")
st.markdown(
    "This interactive app compares the societal and household-level impacts of the Conservative, Labour and Liberal Democrat manifestos."
)

year = st.selectbox(
    "Select a year", options=[2025, 2026, 2027, 2028], index=0, key="year"
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
