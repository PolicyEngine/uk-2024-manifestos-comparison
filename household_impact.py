import streamlit as st
from enum import Enum
import pandas as pd
import numpy as np
from reforms import conservative_reform, lib_dem_reform, labour_reform
import plotly.express as px
from policyengine_core.charts import *
from policyengine_uk import Simulation


# Define colors for the parties
LABOUR = "#E4003B"
CONSERVATIVE = "#0087DC"
LIB_DEM = "#FAA61A"

names = ["The Conservatives", "Labour", "The Liberal Democrats"]
reforms = [conservative_reform, labour_reform, lib_dem_reform]


TAX_RISES = [
    "income_tax",
    "national_insurance",
    "expected_sdlt",
    "private_school_vat",
    "capital_gains_tax",
]
BENEFIT_RISES = ["universal_credit"]


def create_situation():
    situation = {
        "people": {"you": {}},
        "households": {
            "household": {
                "members": ["you"],
            },
        },
    }

    income_source_to_variable = {
        "Employment": "employment_income",
        "Self-employment": "self_employment_income",
        "Pension": "pension_income",
    }

    age = st.number_input(
        "How old are you?", min_value=0, max_value=100, value=30, key="age"
    )
    situation["people"]["you"]["age"] = age

    income_source = st.selectbox(
        "What's your main source of income?",
        ["None", "Employment", "Self-employment", "Pensions"],
        index=1,
        help="Enter the source which makes up the largest proportion of your income.",
    )
    if income_source != "None":
        income = st.number_input(
            "What's your annual income?",
            min_value=0,
            value=20000,
            help="This is your income before tax, of your main source of income.",
        )
        situation["people"]["you"][
            income_source_to_variable[income_source]
        ] = income

    has_capital = st.checkbox("Do you have capital gains?")
    if has_capital:
        capital_gains = st.number_input(
            "What's your annual capital gains?",
            min_value=0,
            max_value=1_000_000,
            value=0,
            help="This is your capital gains before tax.",
        )
        situation["people"]["you"]["capital_gains"] = capital_gains

    joint = st.checkbox("Are you married or in a civil partnership?")
    if joint:
        situation["people"]["your partner"] = {}
        situation["households"]["household"]["members"].append("your partner")

        age_spouse = st.number_input(
            "How old is your spouse?",
            min_value=0,
            max_value=100,
            value=30,
            key="age_spouse",
        )
        situation["people"]["your partner"]["age"] = age_spouse

        income_source_spouse = st.selectbox(
            "What's your spouse's main source of income?",
            ["None", "Employment", "Self-employment", "Pension"],
            key="spouse_income_source",
            index=0,
            help="Enter the source which makes up the largest proportion of your spouse's income.",
        )

        if income_source_spouse != "None":
            income_spouse = st.number_input(
                "What's your spouse's annual income?",
                key="spouse_income",
                min_value=0,
                value=20000,
                help="This is your spouse's income before tax, of their main source of income.",
            )
            situation["people"]["your partner"][
                income_source_to_variable[income_source_spouse]
            ] = income_spouse
    else:
        income_spouse = 0

    has_children = st.checkbox("Do you have children?")
    if has_children:
        num_children = st.number_input(
            "How many children do you have?",
            min_value=0,
            value=1,
            key="num_children",
        )
        situation["households"]["household"]["members"].extend(
            [f"child {i+1}" for i in range(num_children)]
        )
        for i in range(num_children):
            situation["people"][f"child {i+1}"] = {}
            age_child = st.number_input(
                f"How old is child {i+1}?",
                min_value=0,
                max_value=100,
                value=10,
                key=f"age_child {i}",
            )
            situation["people"][f"child {i+1}"]["age"] = age_child

            private_school = st.checkbox(
                f"Does child {i+1} attend a private school?",
                help="We assume they pay average fees.",
            )
            situation["people"][f"child {i+1}"][
                "attends_private_school"
            ] = private_school

    buying_first_home = st.checkbox(
        "Will you buy your first home over the next four years?"
    )
    if buying_first_home:
        value = st.number_input(
            "What's the estimated value of the property?",
            min_value=0,
            value=200000,
            key="property_value",
        )
        situation["households"]["household"][
            "main_residential_property_purchased"
        ] = value
        situation["households"]["household"][
            "main_residential_property_purchased_is_first_home"
        ] = True

    # Shift all to 2028

    for entity_type in situation:
        for entity in situation[entity_type]:
            for key in situation[entity_type][entity]:
                if key != "members":
                    situation[entity_type][entity][key] = {
                        2028: situation[entity_type][entity][key]
                    }

    return situation


def create_party_summary(party, situation, reform, baseline):
    simulation = Simulation(situation=situation, reform=reform)
    simulation.default_calculation_period = 2028

    metrics = []
    values = []

    diff = (
        lambda variable: simulation.calculate(variable, 2028).sum()
        - baseline.calculate(variable, 2028).sum()
    )

    metrics.append("Child Benefit tax charge")
    values.append(-diff("CB_HITC"))

    metrics.append("Triple Lock Plus")
    values.append(-(diff("income_tax") - diff("CB_HITC")))

    metrics.append("National Insurance")
    values.append(-diff("national_insurance"))

    metrics.append("Stamp Duty")
    values.append(-diff("expected_sdlt"))

    metrics.append("Private School VAT")
    values.append(-diff("private_school_vat"))

    metrics.append("Capital Gains Tax")
    values.append(-diff("capital_gains_tax"))

    metrics.append("Universal Credit")
    values.append(diff("universal_credit"))

    metrics.append("Net change excluding in-kind spending")
    values.append(np.array(values).sum())

    metrics.append("In-kind spending")
    values.append(diff("household_net_income") - values[-1])

    metrics.append("Net change")
    values.append(diff("household_net_income"))

    df = pd.DataFrame({"Metric": metrics, "Value": values})
    df["Party"] = party
    df.Value = df.Value.round(2)
    return df


def fmt(value):
    return f"+£{value:,.0f}" if value >= 0 else f"-£{abs(value):,.0f}"


def create_main_chart(df):
    df["Text"] = df["Value"].apply(fmt)
    fig = px.bar(
        df.sort_values("Value", ascending=False),
        x="Party",
        y="Value",
        text="Text",
        color="Party",
        color_discrete_map={
            "The Conservatives": CONSERVATIVE,
            "Labour": LABOUR,
            "The Liberal Democrats": LIB_DEM,
        },
        animation_frame="Metric",
    )

    # only show the net change by default
    fig.update_traces(
        visible="legendonly",
        selector=dict(name="Net change excluding in-kind spending"),
    )

    winning_party = (
        df[df.Metric == "Net change"]
        .sort_values("Value", ascending=False)
        .iloc[0]["Party"]
    )
    party_color = (
        CONSERVATIVE
        if winning_party == "The Conservatives"
        else (LABOUR if winning_party == "Labour" else LIB_DEM)
    )

    fig = format_fig(fig).update_layout(
        showlegend=True,
        title=f'The <span style="color: {party_color}">{winning_party}</span> would increase your net income the most',
        yaxis_title="Net income change",
    )

    return fig


def display_household_impact():
    st.subheader("Household impact")

    situation = create_situation()

    with st.expander("See your situation"):
        st.json(situation)

    submit = st.button("Calculate impacts")
    if submit:
        baseline = Simulation(situation=situation)
        dfs = []

        with st.spinner("Calculating impacts..."):
            for name, reform in zip(names, reforms):
                dfs.append(
                    create_party_summary(name, situation, reform, baseline)
                )

        df = pd.concat(dfs)

        with st.expander("See breakdown"):
            st.dataframe(df, use_container_width=True)

        st.plotly_chart(create_main_chart(df), use_container_width=True)
