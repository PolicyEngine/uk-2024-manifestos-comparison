import streamlit as st
import pandas as pd
from policyengine_uk import Microsimulation
from policyengine_core.reforms import Reform
import plotly.express as px
import os
from policyengine_core.charts import *
import numpy as np

baseline = Microsimulation()
# Function to calculate difference in metrics between baseline and reform


def calculate_impacts(reform=None):
    if reform is None:
        sim = Microsimulation()
    else:
        sim = Microsimulation(reform=reform)

    sim.macro_cache_read = False

    # Calculate net income
    net_income = sim.calc("household_net_income", period=2028, map_to="household")

    # Benefits 
    benefits = sim.calc("household_benefits", period=2028, map_to="household")

    # Taxes 
    taxes = sim.calc("household_tax", period=2028, map_to="household")

    # Calculate poverty impacts
    poverty = sim.calc("in_poverty", period=2028, map_to="person")

    # Child poverty
    child = sim.calc("is_child", period=2028, map_to="person")

    # Adult Poverty 
    adult = sim.calc("is_WA_adult", period=2028, map_to="person")

    # Senior poverty 
    senior = sim.calc("age_over_64", period=2028, map_to="person")

    # Calculate Gini index impacts
    personal_hh_equiv_income = sim.calculate("equiv_household_net_income")
    household_count_people = sim.calculate("household_count_people")
    personal_hh_equiv_income.weights *= household_count_people

    return pd.DataFrame({
        "net_income": net_income.sum(),
        "benefits": benefits.sum(),
        "taxes": taxes.sum(),
        "poverty": poverty.mean(),
        "child_poverty": poverty[child == 1].mean(),
        "adult_poverty": poverty[adult == 1].mean(),
        "senior_poverty": poverty[senior == 1].mean(),
        "gini_index": personal_hh_equiv_income.gini()
    }, index=[0])


# Conservative manifesto reform
conservative_reform = Reform.from_dict({
  "gov.contrib.conservatives.cb_hitc_household": {
    "2026-01-01.2039-12-31": True
  },
  "gov.contrib.conservatives.pensioner_personal_allowance": {
    "2025-01-01.2025-12-31": 13040,
    "2026-01-01.2026-12-31": 13370,
    "2027-01-01.2027-12-31": 13710,
    "2028-01-01.2028-12-31": 14060,
    "2029-01-01.2030-12-31": 14450
  },
  "gov.contrib.policyengine.budget.corporate_incident_tax_change": {
    "2025-01-01.2025-12-31": 1.98,
    "2026-01-01.2026-12-31": 2.98,
    "2027-01-01.2027-12-31": 4,
    "2028-01-01.2028-12-31": 5,
    "2029-01-01.2030-12-31": 6
  },
  "gov.contrib.policyengine.budget.education": {
    "2025-01-01.2027-12-31": 0.3,
    "2028-01-01.2028-12-31": 0.5,
    "2029-01-01.2029-12-31": 1
  },
  "gov.contrib.policyengine.budget.nhs": {
    "2025-01-01.2025-12-31": 0.274,
    "2026-01-01.2026-12-31": 0.281,
    "2027-01-01.2027-12-31": 0.535,
    "2028-01-01.2028-12-31": 0.588,
    "2029-01-01.2029-12-31": 0.609
  },
  "gov.contrib.policyengine.budget.other_public_spending": {
    "2025-01-01.2025-12-31": -3.745,
    "2026-01-01.2026-12-31": -7.945,
    "2027-01-01.2027-12-31": -11.35,
    "2028-01-01.2028-12-31": -12.474,
    "2029-01-01.2029-12-31": -13.104
  },
  "gov.hmrc.income_tax.charges.CB_HITC.phase_out_end": {
    "2026-01-01.2039-12-31": 160000
  },
  "gov.hmrc.income_tax.charges.CB_HITC.phase_out_start": {
    "2026-01-01.2039-12-31": 120000
  },
  "gov.hmrc.national_insurance.class_1.rates.employee.main": {
    "2025-01-01.2026-12-31": 0.07,
    "2027-01-01.2030-12-31": 0.06
  },
  "gov.hmrc.national_insurance.class_4.rates.main": {
    "2025-01-01.2025-12-31": 0.05,
    "2026-01-01.2026-12-31": 0.04,
    "2027-01-01.2027-12-31": 0.03,
    "2028-01-01.2028-12-31": 0.02,
    "2029-01-01.2030-12-31": 0
  },
  "gov.hmrc.stamp_duty.residential.purchase.main.first.max": {
    "2025-01-01.2039-12-31": np.inf
  },
  "gov.hmrc.stamp_duty.residential.purchase.main.first.rate[1].rate": {
    "2025-01-01.2039-12-31": 0
  }
}, country_id="uk")


# Liberal Democrat manifesto reform
lib_dem_reform = Reform.from_dict({
  "gov.contrib.policyengine.budget.consumer_incident_tax_change": {
    "2024-01-01.2100-12-31": 3.64
  },
  "gov.contrib.policyengine.budget.corporate_incident_tax_change": {
    "2024-01-01.2100-12-31": 17.66
  },
  "gov.contrib.policyengine.budget.education": {
    "2024-01-01.2100-12-31": 6.63
  },
  "gov.contrib.policyengine.budget.nhs": {
    "2024-01-01.2100-12-31": 8.35
  },
  "gov.contrib.policyengine.budget.other_public_spending": {
    "2024-01-01.2100-12-31": 6.31
  },
  "gov.dwp.benefit_cap.non_single.in_london": {
    "2024-01-01.2100-12-31": 100000
  },
  "gov.dwp.benefit_cap.non_single.outside_london": {
    "2024-01-01.2100-12-31": 100000
  },
  "gov.dwp.benefit_cap.single.in_london": {
    "2024-01-01.2100-12-31": 100000
  },
  "gov.dwp.benefit_cap.single.outside_london": {
    "2024-01-01.2100-12-31": 100000
  },
  "gov.dwp.carers_allowance.rate": {
    "2024-01-01.2100-12-31": 101.9
  },
  "gov.dwp.universal_credit.elements.child.limit.child_count": {
    "2024-01-01.2100-12-31": 99
  },
  "gov.hmrc.cgt.additional_rate": {
    "2024-01-01.2100-12-31": 0.25
  },
  "gov.hmrc.cgt.annual_exempt_amount": {
    "2024-01-01.2100-12-31": 5000
  },
  "gov.hmrc.cgt.basic_rate": {
    "2024-01-01.2100-12-31": 0.15
  },
  "gov.hmrc.cgt.higher_rate": {
    "2024-01-01.2100-12-31": 0.25
  }
}, country_id="uk")

@st.cache_resource
def create_data():
    # Combine results for comparison
    stacked = pd.concat(
        [
            calculate_impacts(),
            calculate_impacts(reform=conservative_reform),
            calculate_impacts(reform=lib_dem_reform)
        ],
        keys=["Baseline", "Conservative", "Liberal Democrat"],
    )

    return stacked

stacked = create_data()

stacked = create_data()

reform_types = ["Baseline", "Conservative", "Liberal Democrat"]

# Calculate percentage differences from baseline
def pct_diff(a, b):
    return (a - b) / b

def pct_diff_reform(var, reform_type):
    return pct_diff(stacked.xs(reform_type, level=0)[var].values[0], stacked.xs("Baseline", level=0)[var].values[0])

reform_types = ["Conservative", "Liberal Democrat"]
rows = []

for reform_type in reform_types:
    cost = stacked.xs("Baseline", level=0)["net_income"].values[0] - stacked.xs(reform_type, level=0)["net_income"].values[0]
    benefits = (stacked.xs("Baseline", level=0)["benefits"].values[0] - stacked.xs(reform_type, level=0)["benefits"].values[0]) * -1
    taxes = (stacked.xs("Baseline", level=0)["taxes"].values[0] - stacked.xs(reform_type, level=0)["taxes"].values[0]) * -1
    poverty_pct_diff = pct_diff_reform("poverty", reform_type) * 100 * -1
    child_poverty_pct_diff = pct_diff_reform("child_poverty", reform_type) * 100 * -1
    adult_poverty_pct_diff = pct_diff_reform("adult_poverty", reform_type) * 100 * -1
    senior_poverty_pct_diff = pct_diff_reform("senior_poverty", reform_type) * 100 * -1
    gini_index_pct_diff = pct_diff_reform("gini_index", reform_type) * 100 * -1

    rows.append(
        {
            "Manifesto": reform_type,
            "Cost (in £B)": cost,
            "Benefits (in £B)": benefits,
            "Taxes (in £B)": taxes,
            "Poverty Impact (%)": -poverty_pct_diff,
            "Child Poverty Impact (%)": -child_poverty_pct_diff,
            "Adult Poverty Impact (%)": -adult_poverty_pct_diff,
            "Senior Poverty Impact (%)": -senior_poverty_pct_diff,
            "Gini Index Impact (%)": -gini_index_pct_diff,
        }
    )

result_df = pd.DataFrame(rows)

# Create a display version of the DataFrame
display_df = result_df.copy()

# Format the Cost, Benefits, and Taxes columns
for column in ["Cost (in £B)", "Benefits (in £B)", "Taxes (in £B)"]:
    display_df[column] = display_df[column].apply(lambda x: f'£{x / 1e9:,.1f}')

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
st.title("Comparison of the UK 2024 Manifestos")

st.markdown("We will compare the societal and household impact of the Conservative and Liberal Democrat party manifestos")

# Display comparison table using the DataFrame
st.subheader("Impact Comparison from Baseline")
st.write("Here is a comparison of the impacts of Conservative and Liberal Democrat manifestos compared to the baseline:")

def decile_impact():
    decile = baseline.calculate("household_income_decile", period=2028).clip(1, 10)
    net_income = baseline.calculate("household_net_income", period=2028)
    
    reform_data = []
    
    for reform_type in reform_types:
        if reform_type == "Conservative":
            sim = Microsimulation(reform=conservative_reform)
        elif reform_type == "Liberal Democrat":
            sim = Microsimulation(reform=lib_dem_reform)
        
        reformed_net_income = sim.calc("household_net_income", period=2028, map_to="household")
        income_change = net_income - reformed_net_income
        rel_income_change_by_decile = income_change.groupby(decile).sum() / net_income.groupby(decile).sum()
        
        for dec, change in rel_income_change_by_decile.items():
            reform_data.append({
                "Reform": reform_type,
                "Decile": dec,
                "Relative Income Change": -change * 100  # Invert and convert to percentage
            })
    
    return pd.DataFrame(reform_data)

# Generate the reform data
reform_data = decile_impact()

# Find the min and max values to set the range
min_value = reform_data['Relative Income Change'].min()
max_value = reform_data['Relative Income Change'].max()
abs_max_value = max(abs(min_value), abs(max_value))

# Create the Plotly line chart with equalized range
fig = px.line(reform_data, x='Decile', y='Relative Income Change', color='Reform',
              title="Relative Income Change by Decile for Each Reform",
              labels={"Relative Income Change": "Relative Income Change (%)"},
              color_discrete_map={
                  "Conservative": "#0087DC",
                  "Liberal Democrat": "#FAA61A"
              })

# Update y-axis range
fig.update_yaxes(range=[-abs_max_value, abs_max_value])

# Display the chart in Streamlit
st.plotly_chart(format_fig(fig), use_container_width=True)

# Display the Dataframe in Table
st.table(display_df)

# Add a selectbox to choose a metric
selected_metric = st.selectbox("Select a metric to display:", result_df.columns[1:])

# Add a button to display the selected metric
metric_data = result_df.set_index('Manifesto')[selected_metric]  

fig = px.bar(
    metric_data,
    x=metric_data.index,
    y=metric_data.values,
    color=metric_data.index,
    title=f"Impact of {selected_metric}",
    color_discrete_map={
        "Conservative": "#0087DC",
        "Liberal Democrat": "#FAA61A"
    }
).update_layout(
    yaxis_title=f"{selected_metric}",
    xaxis_title="Party",
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)
