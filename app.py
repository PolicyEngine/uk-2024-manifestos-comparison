import streamlit as st
from policyengine_core.charts import *
from household_impact import display_household_impact
from societal_impact import display_societal_impact
from streamlit_js_eval import streamlit_js_eval


# Measure viewport width using JS; this will evaluate to None before paint,
# then to the actual value, so must test if value is None before using
MOBILE_WIDTH_PX = 768
viewport_width = streamlit_js_eval(js_expressions="window.outerWidth", key = "WOW")

# Streamlit code for displaying the data
st.title("UK 2024 Election Manifestos")
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
    display_societal_impact(year, include_indirect_impacts, viewport_width)

with tab2:
    display_household_impact(year, include_indirect_impacts, viewport_width)
