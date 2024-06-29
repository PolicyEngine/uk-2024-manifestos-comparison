import pandas as pd
from policyengine_uk import Microsimulation
from policyengine_core.reforms import Reform
import numpy as np
from reforms import *

baseline = Microsimulation()


def calculate_impacts(year, reform=None):
    if reform is None:
        sim = Microsimulation()
    else:
        sim = Microsimulation(reform=reform)

    sim.macro_cache_read = False

    # Calculate net income
    net_income = sim.calc(
        "household_net_income", period=year, map_to="household"
    )

    # Benefits
    benefits = sim.calc("household_benefits", period=year, map_to="household")

    # Taxes
    taxes = sim.calc("household_tax", period=year, map_to="household")

    # Calculate poverty impacts
    poverty = sim.calc("in_poverty", period=year, map_to="person")

    # Child poverty
    child = sim.calc("is_child", period=year, map_to="person")

    # Adult Poverty
    adult = sim.calc("is_WA_adult", period=year, map_to="person")

    # Senior poverty
    senior = sim.calc("age_over_64", period=year, map_to="person")

    # Calculate Gini index impacts
    personal_hh_equiv_income = sim.calculate(
        "equiv_household_net_income", period=year
    )
    household_count_people = sim.calculate(
        "household_count_people", period=year
    )
    personal_hh_equiv_income.weights *= household_count_people

    return pd.DataFrame(
        {
            "net_income": net_income.sum(),
            "benefits": benefits.sum(),
            "taxes": taxes.sum(),
            "poverty": poverty.mean(),
            "child_poverty": poverty[child == 1].mean(),
            "adult_poverty": poverty[adult == 1].mean(),
            "senior_poverty": poverty[senior == 1].mean(),
            "gini_index": personal_hh_equiv_income.gini(),
        },
        index=[0],
    )


def create_data(year, include_indirect=True):
    # Combine results for comparison
    stacked = pd.concat(
        [
            calculate_impacts(year),
            calculate_impacts(
                year,
                reform=(
                    conservative_reform
                    if include_indirect
                    else conservative_reform_direct
                ),
            ),
            calculate_impacts(
                year,
                reform=(
                    labour_reform if include_indirect else labour_reform_direct
                ),
            ),
            calculate_impacts(
                year,
                reform=(
                    lib_dem_reform
                    if include_indirect
                    else lib_dem_reform_direct
                ),
            ),
        ],
        keys=[
            "Baseline",
            "Conservatives",
            "Labour Party",
            "Liberal Democrats",
        ],
    )

    return stacked


reform_types = [
    "Baseline",
    "Conservatives",
    "Labour Party",
    "Liberal Democrats",
]


# Calculate percentage differences from baseline
def pct_diff(a, b):
    return (a - b) / b


def pct_diff_reform(stacked, var, reform_type):
    return pct_diff(
        stacked.xs(reform_type, level=0)[var].values[0],
        stacked.xs("Baseline", level=0)[var].values[0],
    )


reform_types = ["Conservatives", "Labour Party", "Liberal Democrats"]
rows = []


def computations():
    for include_indirect in [True, False]:
        for year in range(2025, 2029):
            stacked = create_data(year, include_indirect=include_indirect)
            for reform_type in reform_types:
                cost = (
                    stacked.xs("Baseline", level=0)["net_income"].values[0]
                    - stacked.xs(reform_type, level=0)["net_income"].values[0]
                )
                benefits = (
                    stacked.xs("Baseline", level=0)["benefits"].values[0]
                    - stacked.xs(reform_type, level=0)["benefits"].values[0]
                ) * -1
                taxes = (
                    stacked.xs("Baseline", level=0)["taxes"].values[0]
                    - stacked.xs(reform_type, level=0)["taxes"].values[0]
                ) * -1
                poverty_pct_diff = (
                    pct_diff_reform(stacked, "poverty", reform_type) * 100 * -1
                )
                child_poverty_pct_diff = (
                    pct_diff_reform(stacked, "child_poverty", reform_type)
                    * 100
                    * -1
                )
                adult_poverty_pct_diff = (
                    pct_diff_reform(stacked, "adult_poverty", reform_type)
                    * 100
                    * -1
                )
                senior_poverty_pct_diff = (
                    pct_diff_reform(stacked, "senior_poverty", reform_type)
                    * 100
                    * -1
                )
                gini_index_pct_diff = (
                    pct_diff_reform(stacked, "gini_index", reform_type)
                    * 100
                    * -1
                )

                rows.append(
                    {
                        "Manifesto": reform_type,
                        "Cost (£bn)": cost,
                        "Benefits (£bn)": benefits,
                        "Taxes (£bn)": taxes,
                        "Poverty Impact (%)": -poverty_pct_diff,
                        "Child Poverty Impact (%)": -child_poverty_pct_diff,
                        "Adult Poverty Impact (%)": -adult_poverty_pct_diff,
                        "Senior Poverty Impact (%)": -senior_poverty_pct_diff,
                        "Gini Index Impact (%)": -gini_index_pct_diff,
                        "Year": year,
                        "Includes indirect impacts": include_indirect,
                    }
                )

    result_df = pd.DataFrame(rows)
    result_df.to_csv("manifesto_impact.csv", index=False)
    return result_df


def decile_impact():
    dfs = []
    for include_indirect in [True, False]:
        for year in range(2025, 2029):
            decile = baseline.calculate(
                "household_income_decile", period=year
            ).clip(1, 10)
            net_income = baseline.calculate(
                "household_net_income", period=year
            )

            reform_types = [
                "Conservatives",
                "Labour Party",
                "Liberal Democrats",
            ]
            reform_data = []

            for reform_type in reform_types:
                if reform_type == "Conservatives":
                    sim = Microsimulation(
                        reform=(
                            conservative_reform
                            if include_indirect
                            else conservative_reform_direct
                        )
                    )
                elif reform_type == "Liberal Democrats":
                    sim = Microsimulation(
                        reform=(
                            lib_dem_reform
                            if include_indirect
                            else lib_dem_reform_direct
                        )
                    )
                elif reform_type == "Labour Party":
                    sim = Microsimulation(
                        reform=(
                            labour_reform
                            if include_indirect
                            else labour_reform_direct
                        )
                    )

                reformed_net_income = sim.calc(
                    "household_net_income", period=year, map_to="household"
                )
                income_change = net_income - reformed_net_income
                rel_income_change_by_decile = (
                    income_change.groupby(decile).sum()
                    / net_income.groupby(decile).sum()
                )

                for dec, change in rel_income_change_by_decile.items():
                    reform_data.append(
                        {
                            "Reform": reform_type,
                            "Decile": dec,
                            "Relative Income Change": -change
                            * 100,  # Invert and convert to percentage
                        }
                    )

            reform_data_df = pd.DataFrame(reform_data)
            reform_data_df["Year"] = year
            reform_data_df["Includes indirect impacts"] = include_indirect
            dfs.append(reform_data_df)

    reform_data_df = pd.concat(dfs)
    reform_data_df.to_csv("decile_impact.csv", index=False)
    return reform_data_df


if __name__ == "__main__":
    computations()
    decile_impact()
    print("Computations completed successfully.")
