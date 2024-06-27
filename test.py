from policyengine_uk import Microsimulation
from policyengine_core.reforms import Reform

reform = Reform.from_dict({
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
    "2025-01-01.2039-12-31": 500000000
  },
  "gov.hmrc.stamp_duty.residential.purchase.main.first.rate[1].rate": {
    "2025-01-01.2039-12-31": 0
  }
}, country_id="uk")


baseline = Microsimulation()
reformed = Microsimulation(reform=reform)

print(reformed.calculate("household_net_income", 2028).sum()/1e9 - baseline.calculate("household_net_income", 2028).sum()/1e9)