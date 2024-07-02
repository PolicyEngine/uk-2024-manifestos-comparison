import streamlit as st
import pandas as pd
from policyengine_uk import Microsimulation
from policyengine_core.reforms import Reform
import plotly.express as px
import os
from policyengine_core.charts import *
import numpy as np
from streamlit_js_eval import streamlit_js_eval

# Import the decile impact function from the separate file
from decile_impact import decile_impact

baseline = Microsimulation()
# Function to calculate difference in metrics between baseline and reform

# This expression returns None before paint, then refreshes
# and returns the correct val - must check if val is None before using
screen_width = streamlit_js_eval(js_expressions="window.outerWidth", key = "SCW")
MOBILE_WIDTH_PX = 768

impact_data = pd.read_csv('manifesto_impact.csv')

# Create a display version of the DataFrame
display_df = impact_data.copy()

# Format the Cost, Benefits, and Taxes columns
for column in ["Cost (£bn)", "Benefits (£bn)", "Taxes (£bn)"]:
    display_df[column] = display_df[column].apply(lambda x: f'{x / 1e9:,.1f}')

# Format the percentage columns
percentage_columns = [
    "Poverty Impact (%)",
    "Child Poverty Impact (%)",
    "Adult Poverty Impact (%)",
    "Senior Poverty Impact (%)",
    "Gini Index Impact (%)"
]
for column in percentage_columns:
    display_df[column] = display_df[column].apply(lambda x: f'{x:.1f}')


# Streamlit code for displaying the data
st.title("UK 2024 Manifestos Comparison")

st.markdown("We will compare the impacts of the Conservative, Liberal Democrat and Labour party manifestos on society and households")

# Display comparison table using the DataFrame
st.subheader("Societal Impact Comparison")
st.write("Here is a comparison of the impacts of the Conservative, Liberal Democrat and Labour party manifestos:")

# Load the decile impact data from the CSV file
reform_data = pd.read_csv('decile_impact.csv')
print(screen_width)

plotly_x = None
plotly_y = None
plotly_yanchor = None
# Generate and display the decile impact chart
if screen_width is not None and screen_width < MOBILE_WIDTH_PX:
    plotly_x = 0.5
    plotly_y = -0.2
    plotly_xanchor = "center"
    plotly_yanchor = "top"
    plotly_orientation = "h"
else:
    plotly_x = 1
    plotly_y = 1
    plotly_xanchor = "left"
    plotly_yanchor = "middle"
    plotly_orientation = "v"

print(plotly_x)
print(plotly_y)
print(plotly_yanchor)

fig_decile = px.line(
    reform_data,
    x='Decile',
    y='Relative Income Change',
    color='Reform',
    title="Relative Income Change by Decile for Each Reform",
    labels={"Relative Income Change": "Relative Income Change (%)"},
    color_discrete_map={
        "Conservative": "#0087DC",
        "Labour": "#E4003B",
        "Liberal Democrat": "#FAA61A"
    },
)

fig_decile.update_layout(
    legend={
      "x": plotly_x,
      "y": plotly_y,
      "xanchor": plotly_xanchor,
      "yanchor": plotly_yanchor,
      "orientation": plotly_orientation
    }
)
# Update y-axis range
min_value = reform_data['Relative Income Change'].min()
max_value = reform_data['Relative Income Change'].max()
abs_max_value = max(abs(min_value), abs(max_value))
fig_decile.update_yaxes(range=[-abs_max_value, abs_max_value])

st.plotly_chart(fig_decile, use_container_width=True)



# Display the Dataframe in Table
st.caption("**Total Impacts**")
st.table(display_df)
# Add a selectbox to choose a metric
selected_metric = st.selectbox("Select a metric to display:", impact_data.columns[1:])

# Remove the word "Impact" and units in brackets if present
selected_metric_clean = selected_metric.replace(" Impact", "").split(" (")[0]

# Add a button to display the selected metric
metric_data = impact_data.set_index('Manifesto')[selected_metric]

# Determine which party has the largest impact for the selected metric
if "Poverty" in selected_metric_clean or "Gini Index" in selected_metric_clean:
    largest_impact_party = metric_data.idxmin()  # Find the smallest value for poverty and Gini index
    largest_impact_value = metric_data.min()
else:
    largest_impact_party = metric_data.idxmax()  # Find the largest value for other metrics
    largest_impact_value = metric_data.max()

# Determine the year
year = 2028

# Add personalized messages
if selected_metric_clean in ["Cost", "Taxes"]:
    st.write(f"The **{largest_impact_party}** party would reduce **{selected_metric_clean.lower()}** the most in {year}.")
elif selected_metric_clean == "Benefits":
    st.write(f"The **{largest_impact_party}** party would increase benefits the most in {year}.")
elif "Poverty" in selected_metric_clean or "Gini Index" in selected_metric_clean:
    if largest_impact_value < 0:
        st.write(f"The **{largest_impact_party}** party would decrease **{selected_metric_clean.lower()}** the most in {year}.")
    else:
        st.write(f"The **{largest_impact_party}** party would increase **{selected_metric_clean.lower()}** the least in {year}.")
else:
    st.write(f"The **{largest_impact_party}** party would decrease **{selected_metric_clean.lower()}** the most in {year}.")

fig = px.bar(
    metric_data,
    x=metric_data.index,
    y=metric_data.values,
    color=metric_data.index,
    color_discrete_map={
        "Conservative": "#0087DC",
        "Labour": "#E4003B",
        "Liberal Democrat": "#FAA61A"
    }
).update_layout(
    yaxis_title=f"{selected_metric_clean}",
    xaxis_title="Party",
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)
