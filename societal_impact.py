import streamlit as st
from policyengine_core.charts import *
import pandas as pd
import plotly.express as px

LABOUR = "#E4003B"
CONSERVATIVE = "#0087DC"
LIB_DEM = "#FAA61A"

results_df = pd.read_csv('manifesto_impact.csv')

result_df = pd.DataFrame(results_df)
# Create a display version of the DataFrame
display_df = result_df.copy()
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

def display_societal_impact():
    # Display comparison table using the DataFrame
    st.subheader("Societal Impacts")
    st.write("The chart below shows the impact by income decile of each manifesto policy, as a percentage of prior household disposable income.")

    # Load the decile impact data from the CSV file
    decile_data = pd.read_csv('decile_impact.csv')

    # Generate and display the decile impact chart
    fig_decile = px.line(
        decile_data,
        x='Decile',
        y='Relative Income Change',
        color='Reform',
        title="Relative income change by decile",
        labels={"Relative Income Change": "Relative income change (%)"},
        color_discrete_map={
            "Conservative": CONSERVATIVE,
            "Labour": LABOUR,
            "Liberal Democrat": LIB_DEM,
        }
    ).update_traces(
        mode='markers+lines',
    ).update_layout(
        yaxis_tickformat="+,.0f",
        xaxis_tickvals=list(range(1, 11)),
    )
    # Update y-axis range
    min_value = decile_data['Relative Income Change'].min()
    max_value = decile_data['Relative Income Change'].max()
    abs_max_value = max(abs(min_value), abs(max_value))
    fig_decile.update_yaxes(range=[-abs_max_value, abs_max_value])
    fig = format_fig(fig_decile)
    st.plotly_chart(fig_decile, use_container_width=True)

    # Display the DataFrame in Table
    st.caption("**Total Impacts**")
    st.write("The table below shows the total impact of each manifesto policy on different societal metrics.")
    st.dataframe(display_df.set_index("Manifesto", drop=True).T, use_container_width=True)
    # Add a selectbox to choose a metric
    selected_metric = st.selectbox("Select a metric to display:", result_df.columns[1:])
    # Remove the word "Impact" and units in brackets if present
    selected_metric_clean = selected_metric.replace(" Impact", "").split(" (")[0]
    # Add a button to display the selected metric
    metric_data = result_df.set_index('Manifesto')[selected_metric]
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
            "Conservative": CONSERVATIVE,
            "Liberal Democrat": LIB_DEM,
            "Labour": LABOUR,
        }
    ).update_layout(
        yaxis_title=f"{selected_metric_clean}",
        xaxis_title="Party",
        showlegend=True,
        yaxis_tickformat="+,.0f",
    )
    fig = format_fig(fig)
    st.plotly_chart(fig, use_container_width=True)