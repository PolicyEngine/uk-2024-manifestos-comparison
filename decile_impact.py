import pandas as pd
from policyengine_uk import Microsimulation
from policyengine_core.reforms import Reform
import numpy as np


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


labour_reform = Reform.from_dict({
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
  }
}, country_id="uk")


baseline = Microsimulation()

def decile_impact():
    decile = baseline.calculate("household_income_decile", period=2028).clip(1, 10)
    net_income = baseline.calculate("household_net_income", period=2028)
    
    reform_types = ["Conservative", "Labour", "Liberal Democrat"]
    reform_data = []
    
    for reform_type in reform_types:
        if reform_type == "Conservative":
            sim = Microsimulation(reform=conservative_reform)
        elif reform_type == "Liberal Democrat":
            sim = Microsimulation(reform=lib_dem_reform)
        elif reform_type == "Labour":
            sim = Microsimulation(reform=labour_reform)
        
        reformed_net_income = sim.calc("household_net_income", period=2028, map_to="household")
        income_change = net_income - reformed_net_income
        rel_income_change_by_decile = income_change.groupby(decile).sum() / net_income.groupby(decile).sum()
        
        for dec, change in rel_income_change_by_decile.items():
            reform_data.append({
                "Reform": reform_type,
                "Decile": dec,
                "Relative Income Change": -change * 100  # Invert and convert to percentage
            })
    
    reform_data_df = pd.DataFrame(reform_data)
    reform_data_df.to_csv('decile_impact.csv', index=False)
    return reform_data_df


if __name__ == "__main__":
    decile_impact()