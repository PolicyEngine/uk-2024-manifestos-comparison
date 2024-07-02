import streamlit as st
from policyengine_core.charts import *
import pandas as pd
import plotly.express as px
from streamlit_js_eval import streamlit_js_eval

LABOUR = "#E4003B"
CONSERVATIVES = "#0087DC"
LIB_DEM = "#FAA61A"


def display_societal_impact(year, include_indirect_impacts):
    results_df = pd.read_csv("manifesto_impact.csv")
    results_df = results_df[
        results_df["Includes indirect impacts"] == include_indirect_impacts
    ][results_df["Year"] == year].drop(
        columns=["Year", "Includes indirect impacts"]
    )
    decile_data = pd.read_csv("decile_impact.csv")
    result_df = pd.DataFrame(results_df).copy()
    # Create a display version of the DataFrame
    display_df = result_df.copy()
    # Format the Cost, Benefits, and Taxes columns
    for column in ["Cost (£bn)", "Benefits (£bn)", "Taxes (£bn)"]:
        display_df[column] = display_df[column].apply(
            lambda x: f"{x / 1e9:,.1f}"
        )
    # Format the percentage columns
    percentage_columns = [
        "Poverty Impact (%)",
        "Child Poverty Impact (%)",
        "Adult Poverty Impact (%)",
        "Senior Poverty Impact (%)",
        "Gini Index Impact (%)",
    ]
    for column in percentage_columns:
        display_df[column] = display_df[column].apply(lambda x: f"{x:.1f}")

    display_df_year = display_df
    result_df_year = result_df

    # Measure viewport width using JS; this will evaluate to None before paint,
    # then to the actual value, so must test if value is None before using
    MOBILE_WIDTH_PX = 768
    viewport_width = streamlit_js_eval(js_expressions="window.outerWidth", key = "WOW")

    # Display comparison table using the DataFrame
    st.subheader("Societal Impacts")
    st.write(
        "The chart below shows the impact by income decile of each manifesto policy, as a percentage of prior household disposable income."
    )

    decile_data = decile_data.copy()
    decile_data = decile_data[decile_data.Year == year][
        decile_data["Includes indirect impacts"] == include_indirect_impacts
    ]

    if viewport_width is not None and viewport_width < MOBILE_WIDTH_PX:
        plotly_x = 0
        plotly_y = -0.2
        plotly_yanchor = "top"
        plotly_xanchor = "left"
        plotly_orientation = "h"
    else:
        plotly_x = 1
        plotly_y = 1
        plotly_yanchor = "middle"
        plotly_xanchor = "left"
        plotly_orientation = "v"

    # Generate and display the decile impact chart
    fig_decile = (
        px.line(
            decile_data,
            x="Decile",
            y="Relative Income Change",
            color="Reform",
            title="Relative income change by decile",
            labels={"Relative Income Change": "Relative income change (%)"},
            color_discrete_map={
                "Conservatives": CONSERVATIVES,
                "Labour Party": LABOUR,
                "Liberal Democrats": LIB_DEM,
            },
        )
        .update_traces(
            mode=f"markers+lines",
            textposition="top center",
        )
        .update_layout(
            yaxis_tickformat="+,.0f",
            xaxis_tickvals=list(range(1, 11)),
            legend={
              "x": plotly_x,
              "y": plotly_y,
              "xanchor": plotly_xanchor,
              "yanchor": plotly_yanchor,
              "orientation": plotly_orientation
            }
        )
    )
    # Update y-axis range
    min_value = decile_data["Relative Income Change"].min()
    max_value = decile_data["Relative Income Change"].max()
    abs_max_value = max(abs(min_value), abs(max_value))
    fig_decile.update_yaxes(range=[-abs_max_value, abs_max_value])
    fig = format_fig(fig_decile)
    st.plotly_chart(fig_decile, use_container_width=True)

    # Display the DataFrame in Table
    st.write(
        "The table below shows the total impact of each manifesto policy on different societal metrics."
    )
    st.dataframe(
        display_df_year.set_index("Manifesto", drop=True).T,
        use_container_width=True,
    )
    # Add a selectbox to choose a metric
    selected_metric = st.selectbox(
        "Select a metric to display:", result_df_year.columns[1:]
    )
    # Remove the word "Impact" and units in brackets if present
    selected_metric_clean = selected_metric.replace(" Impact", "").split(" (")[
        0
    ]
    # Add a button to display the selected metric
    metric_data = result_df_year.set_index("Manifesto")[selected_metric]

    if selected_metric_clean == "Cost":
        metric_data *= -1
    # Determine which party has the largest impact for the selected metric
    if (
        "Poverty" in selected_metric_clean
        or "Gini Index" in selected_metric_clean
        or "Taxes" in selected_metric_clean
        or "Cost" in selected_metric_clean
    ):
        largest_impact_party = (
            metric_data.idxmin()
        )  # Find the smallest value for poverty and Gini index
        largest_impact_value = metric_data.min()
    else:
        largest_impact_party = (
            metric_data.idxmax()
        )  # Find the largest value for other metrics
        largest_impact_value = metric_data.max()

    party_color = (
        CONSERVATIVES
        if largest_impact_party == "Conservatives"
        else (LABOUR if largest_impact_party == "Labour Party" else LIB_DEM)
    )
    largest_impact_party = (
        f'<span style="color: {party_color}">{largest_impact_party}</span>'
    )
    # Add personalized messages
    if selected_metric_clean == "Cost":
        title = f"The {largest_impact_party} would reduce the deficit the most in {year}"
    elif selected_metric_clean in ["Taxes"]:
        title = f"The {largest_impact_party} would reduce {selected_metric_clean.lower()} the most in {year}"
    elif selected_metric_clean == "Benefits":
        title = f"The {largest_impact_party} would increase benefits the most in {year}"
    elif (
        "Poverty" in selected_metric_clean
        or "Gini Index" in selected_metric_clean
    ):
        if largest_impact_value < 0:
            title = f"The {largest_impact_party} would decrease {selected_metric_clean.lower()} the most in {year}"
        else:
            title = f"The {largest_impact_party} would increase {selected_metric_clean.lower()} the least in {year}"
    else:
        title = f"The {largest_impact_party} would decrease {selected_metric_clean.lower()} the most in {year}"

    metric_data = metric_data.apply(
        lambda x: (
            np.float32(x / 1e9).round(1)
            if selected_metric_clean in ["Cost", "Taxes", "Benefits"]
            else np.float32(x / 100).round(3)
        )
    )

    text = metric_data.apply(
        lambda x: (
            f"{x:+,.1f}bn"
            if selected_metric_clean in ["Cost", "Taxes", "Benefits"]
            else f"{x:+.1%}"
        )
    )

    fig = px.bar(
        metric_data,
        color=metric_data.index,
        color_discrete_map={
            "Conservatives": CONSERVATIVES,
            "Liberal Democrats": LIB_DEM,
            "Labour Party": LABOUR,
        },
        text=text,
    ).update_layout(
        yaxis_title=f"{selected_metric_clean}",
        xaxis_title="Party",
        title=title,
        showlegend=True,
        yaxis_tickformat=(
            "+,.0f"
            if selected_metric_clean in ["Cost", "Taxes", "Benefits"]
            else "+,.0%"
        ),
    )
    fig = format_fig(fig)
    st.plotly_chart(fig, use_container_width=True)
