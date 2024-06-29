import streamlit as st
from enum import Enum
from policyengine_uk import Simulation
import pandas as pd
import numpy as np
from computation import conservative_reform, lib_dem_reform, labour_reform
from policyengine_uk.variables.household.demographic.household import TenureType


def display_household_impact():
    # Add a header and subheader
    st.title("UK 2024 Manifestos Household Impact")
    st.subheader("Compare the 2024 mMnifesto impacts of Conservative, Labour and Liberal Democrat party reforms on household net income, benefits, and taxes")


    def get_income_input(person):
        income_type = st.selectbox(f"Choose an income type for {person}:", ["Employment Income", "Self-Employment Income", "Pension Income", "State Pension Income"])
        if income_type == "Employment Income":
            return st.number_input(f"{person}'s Employment Income", 0, 100000, 0)
        elif income_type == "Self-Employment Income":
            return st.number_input(f"{person}'s Self-Employment Income", 0, 100000, 0)
        elif income_type == "Pension Income":
            return st.number_input(f"{person}'s Pension Income", 0, 100000, 0)
        elif income_type == "State Pension Income":
            return st.number_input(f"{person}'s State Pension Income", 0, 100000, 0)


    # Show the age input for the head of the household
    head_age = st.number_input("Age of the Head of Household", 0, 100, 0)

    # Show care hours input for the head of the household
    head_care_hours = st.number_input("Household Head's Weekly Care Hours", 0, 100, 0)

    # Show capital gains input for the head of the household
    head_capital_gains = st.number_input("Head's Capital Gains", 0, 100000, 0)

    # Inputs
    married = st.checkbox("Married")

    # Show the age input for the spouse if married is checked
    if married:
        spouse_age = st.number_input("Age of the Spouse of the Household", 0, 100, 0)
        spouse_care_hours = st.number_input("Household Spouse's Weekly Care Hours", 0, 100, 0)
        spouse_capital_gains = st.number_input("Household Spouse's Capital Gains", 0, 100000, 0)
    else:
        spouse_age = None
        spouse_care_hours = None
        spouse_capital_gains = None

    # Get income input for head and spouse
    head_income = get_income_input("Head")
    spouse_income = get_income_input("Spouse") if married else None

    num_children = st.number_input("Number of Children", 0)

    # Initialize children_ages and in_private_school dictionaries
    children_ages = {}
    children_in_private_school = {}

    # Display age input for each child based on the number of children
    for i in range(num_children):
        children_ages[i+1] = st.number_input(f"Age of Child {i+1}", 0, 100, 0)
        children_in_private_school[i+1] = st.checkbox(f"Is Child {i+1} in Private School?")


    # Define the TenureType Enum as a constant
    tenure_mapping = {
        TenureType.RENT_FROM_COUNCIL.name: "Rented from Council",
        TenureType.RENT_FROM_HA.name: "Rented from a Housing Association",
        TenureType.RENT_PRIVATELY.name: "Rented privately",
        TenureType.OWNED_OUTRIGHT.name: "Owned outright",
        TenureType.OWNED_WITH_MORTGAGE.name: "Owned with a mortgage"
    }



    tenure_type = st.selectbox("Tenure Type:", list(tenure_mapping.values()))

    property_purchased = st.checkbox("Property Purchased")

    if property_purchased:
        property_value = st.number_input("Value of Purchased Property", 0, 1000000, 0)
    else:
        property_value = None


    def create_situation(head_income, head_age, head_care_hours, head_capital_gains, property_purchased, property_value, children_in_private_school, tenure_type, spouse_income=None, spouse_age=None, spouse_care_hours=None, spouse_capital_gains=None, children_ages=None):
        """
        Create a situation dictionary for the simulation.
        """
        # Reverse mapping from description to TenureType name
        reverse_tenure_mapping = {v: k for k, v in tenure_mapping.items()}
        selected_tenure_type = reverse_tenure_mapping[tenure_type]

        if children_ages is None:
            children_ages = {}


        situation = {
            "people": {
                "you": {
                    "age": {"2028": head_age},
                    "employment_income": {"2028": head_income},
                    "care_hours": {"2028": head_care_hours},
                    "capital_gains": {"2028": head_capital_gains}
                }
            }
        }
        members = ["you"]
        if spouse_income is not None:
            situation["people"]["your partner"] = {
                "age": {"2028": spouse_age},
                "employment_income": {"2028": spouse_income},
                "care_hours": {"2028": spouse_care_hours},
                "capital_gains": {"2028": spouse_capital_gains}
            }
            members.append("your partner")
        for key, value in children_ages.items():
            situation["people"][f"child {key}"] = {
                "age": value,
                "attends_private_school": children_in_private_school[key],
            }
            members.append(f"child {key}")
        situation["benunits"] = {"your benefit unit": {"members": members}}
        situation["households"] = {
            "your household": {
                "members": members,
                "main_residential_property_purchased_is_first_home": {"2028": property_purchased},
                "main_residence_value": {"2028": property_value},
                "tenure_type": {"2028": selected_tenure_type}
            }
        }
        return situation

    def run_simulation(situation, reform=None):
        sim = Simulation(reform=reform, situation=situation)
        net_income = sim.calc("household_net_income", period=2028)
        benefits = sim.calc("household_benefits", period=2028)
        tax = sim.calc("household_tax", period=2028)
        return net_income, benefits, tax

    # Define a function to calculate differences
    def calculate_differences(base, reform):
        return {
            "Net Income Changes": reform[0].sum() - base[0].sum(),
            "Changes in Benefits": reform[1].sum() - base[1].sum(),
            "Changes in Taxes": reform[2].sum() - base[2].sum()
        }

    def format_currency(value):
        if isinstance(value, (int, float, np.integer, np.floating)):
            return f"£{value:,.1f}"
        return value

    # Function to find the party with the maximum net income difference
    def get_highest_net_income(differences):
        highest_net_income = max(differences, key=lambda x: differences[x]['Net Income Changes'])
        return highest_net_income

    # Inside the if st.button("Run Simulation") block:
    if st.button("Run Simulation"):
        situation = create_situation(head_income, head_age, head_care_hours, head_capital_gains, property_purchased, property_value, children_in_private_school, tenure_type, spouse_income=spouse_income, spouse_age=spouse_age, spouse_care_hours=spouse_care_hours, spouse_capital_gains=spouse_capital_gains, children_ages=children_ages)
        
        baseline = run_simulation(situation)
        conservative = run_simulation(situation, conservative_reform)
        labour = run_simulation(situation, labour_reform)
        lib_dem = run_simulation(situation, lib_dem_reform)


        differences = {
            "Conservative": calculate_differences(baseline, conservative),
            "Labour": calculate_differences(baseline, labour),
            "Liberal Democrat": calculate_differences(baseline, lib_dem)
        }


        party_with_highest_net_income_change = get_highest_net_income(differences)
        highest_net_income_diff = differences[party_with_highest_net_income_change]['Net Income Changes']

        if highest_net_income_diff >= 0:
            st.write(f"This household would experience the highest net income increase under the **{party_with_highest_net_income_change}** party's reform.")
        else:
            st.write(f"This household would experience the smallest net income loss under the **{party_with_highest_net_income_change}** party's reform.")

        formatted_differences = pd.DataFrame(differences).T.applymap(format_currency)
        st.write(formatted_differences)
