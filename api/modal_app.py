import modal

app = modal.App("uk-manifestos-comparison")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("policyengine-uk==2.22.0", "numpy<2")
)


@app.function(image=image, timeout=300)
@modal.web_endpoint(method="POST")
def household(data: dict) -> list[dict]:
    """Calculate household-level impacts of each manifesto."""
    import numpy as np
    from policyengine_uk import Simulation
    from policyengine_core.reforms import Reform

    year = data.get("year", 2028)
    include_indirect = data.get("includeIndirect", True)

    # Build the situation dict from input
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

    situation["people"]["you"]["age"] = {year: data.get("age", 30)}
    situation["people"]["you"]["attends_private_school"] = {year: False}

    income_source = data.get("incomeSource", "Employment")
    if income_source != "None":
        income = data.get("income", 20000)
        situation["people"]["you"][income_source_to_variable[income_source]] = {
            year: income
        }

    if data.get("hasCapitalGains"):
        situation["people"]["you"]["capital_gains"] = {
            year: data.get("capitalGains", 0)
        }

    if data.get("hasPartner"):
        situation["people"]["your partner"] = {
            "age": {year: data.get("partnerAge", 30)},
            "attends_private_school": {year: False},
        }
        situation["households"]["household"]["members"].append("your partner")
        partner_source = data.get("partnerIncomeSource", "None")
        if partner_source and partner_source != "None":
            partner_income = data.get("partnerIncome", 20000)
            situation["people"]["your partner"][
                income_source_to_variable[partner_source]
            ] = {year: partner_income}

    children = data.get("children", [])
    if data.get("hasChildren") and children:
        for i, child in enumerate(children):
            name = f"child {i + 1}"
            situation["people"][name] = {
                "age": {year: child.get("age", 10)},
                "attends_private_school": {
                    year: child.get("attendsPrivateSchool", False)
                },
            }
            situation["households"]["household"]["members"].append(name)

    if data.get("buyingFirstHome"):
        situation["households"]["household"][
            "main_residential_property_purchased"
        ] = {year: data.get("propertyValue", 200000)}
        situation["households"]["household"][
            "main_residential_property_purchased_is_first_home"
        ] = {year: True}

    if data.get("isRenter"):
        if data.get("isPrivateRenter"):
            situation["households"]["household"]["tenure_type"] = {
                year: "RENT_FROM_COUNCIL"
            }
        else:
            situation["households"]["household"]["tenure_type"] = {
                year: "RENT_PRIVATELY"
            }
        situation["households"]["household"]["rent"] = {
            year: data.get("rent", 20000)
        }
    else:
        situation["households"]["household"]["tenure_type"] = {
            year: "OWNED_WITH_MORTGAGE"
        }

    # Define reforms (same as reforms.py)
    conservative_reform = Reform.from_dict(
        {
            "gov.contrib.conservatives.cb_hitc_household": {
                "2026-01-01.2039-12-31": True
            },
            "gov.contrib.conservatives.pensioner_personal_allowance": {
                "2025-01-01.2025-12-31": 13040,
                "2026-01-01.2026-12-31": 13370,
                "2027-01-01.2027-12-31": 13710,
                "2028-01-01.2028-12-31": 14060,
                "2029-01-01.2030-12-31": 14450,
            },
            "gov.contrib.policyengine.budget.corporate_incident_tax_change": {
                "2025-01-01.2025-12-31": 1.98,
                "2026-01-01.2026-12-31": 2.98,
                "2027-01-01.2027-12-31": 4,
                "2028-01-01.2028-12-31": 5,
                "2029-01-01.2030-12-31": 6,
            },
            "gov.contrib.policyengine.budget.education": {
                "2025-01-01.2027-12-31": 0.3,
                "2028-01-01.2028-12-31": 0.5,
                "2029-01-01.2029-12-31": 1,
            },
            "gov.contrib.policyengine.budget.nhs": {
                "2025-01-01.2025-12-31": 0.274,
                "2026-01-01.2026-12-31": 0.281,
                "2027-01-01.2027-12-31": 0.535,
                "2028-01-01.2028-12-31": 0.588,
                "2029-01-01.2029-12-31": 0.609,
            },
            "gov.contrib.policyengine.budget.other_public_spending": {
                "2025-01-01.2025-12-31": -3.745,
                "2026-01-01.2026-12-31": -7.945,
                "2027-01-01.2027-12-31": -11.35,
                "2028-01-01.2028-12-31": -12.474,
                "2029-01-01.2029-12-31": -13.104,
            },
            "gov.hmrc.income_tax.charges.CB_HITC.phase_out_end": {
                "2026-01-01.2039-12-31": 160000
            },
            "gov.hmrc.income_tax.charges.CB_HITC.phase_out_start": {
                "2026-01-01.2039-12-31": 120000
            },
            "gov.hmrc.national_insurance.class_1.rates.employee.main": {
                "2025-01-01.2026-12-31": 0.07,
                "2027-01-01.2030-12-31": 0.06,
            },
            "gov.hmrc.national_insurance.class_4.rates.main": {
                "2025-01-01.2025-12-31": 0.05,
                "2026-01-01.2026-12-31": 0.04,
                "2027-01-01.2027-12-31": 0.03,
                "2028-01-01.2028-12-31": 0.02,
                "2029-01-01.2030-12-31": 0,
            },
            "gov.hmrc.stamp_duty.residential.purchase.main.first.max": {
                "2025-01-01.2039-12-31": float("inf")
            },
            "gov.hmrc.stamp_duty.residential.purchase.main.first.rate[1].rate": {
                "2025-01-01.2039-12-31": 0
            },
        },
        country_id="uk",
    )

    conservative_reform_direct = Reform.from_dict(
        {
            "gov.contrib.conservatives.cb_hitc_household": {
                "2026-01-01.2039-12-31": True
            },
            "gov.contrib.conservatives.pensioner_personal_allowance": {
                "2025-01-01.2025-12-31": 13040,
                "2026-01-01.2026-12-31": 13370,
                "2027-01-01.2027-12-31": 13710,
                "2028-01-01.2028-12-31": 14060,
                "2029-01-01.2030-12-31": 14450,
            },
            "gov.hmrc.income_tax.charges.CB_HITC.phase_out_end": {
                "2026-01-01.2039-12-31": 160000
            },
            "gov.hmrc.income_tax.charges.CB_HITC.phase_out_start": {
                "2026-01-01.2039-12-31": 120000
            },
            "gov.hmrc.national_insurance.class_1.rates.employee.main": {
                "2025-01-01.2026-12-31": 0.07,
                "2027-01-01.2030-12-31": 0.06,
            },
            "gov.hmrc.national_insurance.class_4.rates.main": {
                "2025-01-01.2025-12-31": 0.05,
                "2026-01-01.2026-12-31": 0.04,
                "2027-01-01.2027-12-31": 0.03,
                "2028-01-01.2028-12-31": 0.02,
                "2029-01-01.2030-12-31": 0,
            },
            "gov.hmrc.stamp_duty.residential.purchase.main.first.max": {
                "2025-01-01.2039-12-31": float("inf")
            },
            "gov.hmrc.stamp_duty.residential.purchase.main.first.rate[1].rate": {
                "2025-01-01.2039-12-31": 0
            },
        },
        country_id="uk",
    )

    labour_reform = Reform.from_dict(
        {
            "gov.contrib.labour.private_school_vat": {
                "2025-01-01.2039-12-31": 0.2
            },
            "gov.contrib.policyengine.budget.corporate_incident_tax_change": {
                "2024-01-01.2100-12-31": 2.6
            },
            "gov.contrib.policyengine.budget.education": {
                "2024-01-01.2100-12-31": 1.3
            },
            "gov.contrib.policyengine.budget.high_income_incident_tax_change": {
                "2024-01-01.2100-12-31": 3.2
            },
            "gov.contrib.policyengine.budget.nhs": {
                "2024-01-01.2100-12-31": 2
            },
            "gov.contrib.policyengine.budget.other_public_spending": {
                "2024-01-01.2100-12-31": 0.9
            },
        },
        country_id="uk",
    )

    labour_reform_direct = Reform.from_dict({}, country_id="uk")

    lib_dem_reform = Reform.from_dict(
        {
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
            "gov.hmrc.cgt.additional_rate": {"2024-01-01.2100-12-31": 0.25},
            "gov.hmrc.cgt.annual_exempt_amount": {
                "2024-01-01.2100-12-31": 5000
            },
            "gov.hmrc.cgt.basic_rate": {"2024-01-01.2100-12-31": 0.15},
            "gov.hmrc.cgt.higher_rate": {"2024-01-01.2100-12-31": 0.25},
        },
        country_id="uk",
    )

    lib_dem_reform_direct = Reform.from_dict(
        {
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
            "gov.hmrc.cgt.additional_rate": {"2024-01-01.2100-12-31": 0.25},
            "gov.hmrc.cgt.annual_exempt_amount": {
                "2024-01-01.2100-12-31": 5000
            },
            "gov.hmrc.cgt.basic_rate": {"2024-01-01.2100-12-31": 0.15},
            "gov.hmrc.cgt.higher_rate": {"2024-01-01.2100-12-31": 0.25},
        },
        country_id="uk",
    )

    names = ["Conservatives", "Labour", "Liberal Democrats"]
    if include_indirect:
        reforms = [conservative_reform, labour_reform, lib_dem_reform]
    else:
        reforms = [
            conservative_reform_direct,
            labour_reform_direct,
            lib_dem_reform_direct,
        ]

    baseline = Simulation(situation=situation)
    baseline.default_calculation_period = year

    results = []
    for name, reform in zip(names, reforms):
        simulation = Simulation(situation=situation, reform=reform)
        simulation.default_calculation_period = year

        diff = (
            lambda variable, sim=simulation: sim.calculate(variable, year).sum()
            - baseline.calculate(variable, year).sum()
        )

        metrics = []
        values = []

        metrics.append("Child Benefit tax charge")
        values.append(float(-diff("CB_HITC")))

        metrics.append("Triple Lock Plus")
        values.append(float(-(diff("income_tax") - diff("CB_HITC"))))

        metrics.append("National Insurance")
        values.append(float(-diff("national_insurance")))

        metrics.append("Stamp Duty")
        values.append(float(-diff("expected_sdlt")))

        metrics.append("Private School VAT")
        values.append(float(-diff("private_school_vat")))

        metrics.append("Capital Gains Tax")
        values.append(float(-diff("capital_gains_tax")))

        metrics.append("Universal Credit")
        values.append(float(diff("universal_credit")))

        metrics.append("Indirect impacts")
        values.append(float(diff("household_net_income")) - sum(values))

        metrics.append("Net change")
        values.append(float(diff("household_net_income")))

        for metric, value in zip(metrics, values):
            results.append(
                {
                    "metric": metric,
                    "value": round(value, 2),
                    "party": name,
                }
            )

    return results
