import pandas as pd
import sqlite3
import os

# ============================================================
# MENTAL HEALTH IN AMERICA: TRENDS & TREATMENT GAPS
# Data sourced from SAMHSA NSDUH annual reports 2008-2024
# and NIMH published statistics
# ============================================================

output_folder = r"C:\Users\bryce\Desktop\Data Projects\Medical Projects\03 - Mental Health\csv"
db_path = r"C:\Users\bryce\Desktop\Data Projects\Medical Projects\03 - Mental Health\mental_health.db"

# ============================================================
# TABLE 1: NATIONAL TREND — AMI & SMI BY YEAR (2008-2024)
# Source: SAMHSA NSDUH Annual Reports
# AMI = Any Mental Illness, SMI = Serious Mental Illness
# ============================================================

national_trend = pd.DataFrame({
    "year": [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
             2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "ami_pct": [19.5, 19.9, 19.9, 19.6, 18.6, 18.5, 18.1, 17.9,
                18.3, 18.9, 19.1, 19.9, 20.6, 22.8, 23.1, 22.8, 23.4],
    "smi_pct": [3.7,  3.7,  4.1,  3.9,  4.1,  4.2,  4.1,  4.0,
                4.2,  4.5,  4.6,  5.2,  5.6,  5.5,  5.5,  5.8,  5.6],
    "ami_millions": [45.1, 45.9, 46.0, 45.6, 43.7, 43.8, 43.6, 43.4,
                     44.7, 46.6, 47.6, 51.5, 52.9, 57.8, 59.3, 59.3, 61.5],
    "source": ["SAMHSA NSDUH"] * 17
})

# ============================================================
# TABLE 2: TREATMENT GAP BY YEAR
# % of AMI adults who received mental health treatment
# Source: SAMHSA NSDUH Annual Reports
# ============================================================

treatment_gap = pd.DataFrame({
    "year": [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
             2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "ami_pct": [19.5, 19.9, 19.9, 19.6, 18.6, 18.5, 18.1, 17.9,
                18.3, 18.9, 19.1, 19.9, 20.6, 22.8, 23.1, 22.8],
    "received_treatment_pct": [38.5, 39.2, 39.6, 40.0, 40.5, 42.7, 43.0, 43.1,
                                43.1, 42.6, 43.3, 44.8, 46.2, 47.2, 48.7, 54.9],
    "unmet_need_pct": [61.5, 60.8, 60.4, 60.0, 59.5, 57.3, 57.0, 56.9,
                       56.9, 57.4, 56.7, 55.2, 53.8, 52.8, 51.3, 45.1],
    "source": ["SAMHSA NSDUH"] * 16
})

# ============================================================
# TABLE 3: DEMOGRAPHICS — AMI BY AGE GROUP (2023)
# Source: SAMHSA NSDUH 2023 Annual Report
# ============================================================

demographics_age = pd.DataFrame({
    "age_group": ["12-17", "18-25", "26-49", "50+", "18+"],
    "ami_pct":   [16.7,    36.2,    27.9,    15.0,  22.8],
    "smi_pct":   [None,     9.7,     6.9,     3.6,   5.8],
    "received_treatment_pct": [58.0, 51.0, 55.6, 52.3, 54.9],
    "year": [2023] * 5,
    "source": ["SAMHSA NSDUH 2023"] * 5
})

# ============================================================
# TABLE 4: DEMOGRAPHICS — AMI BY SEX (2023)
# Source: SAMHSA NSDUH 2023 / NIMH Statistics
# ============================================================

demographics_sex = pd.DataFrame({
    "sex": ["Female", "Male"],
    "ami_pct": [27.2, 18.1],
    "smi_pct": [7.0,  4.4],
    "received_treatment_pct": [51.7, 40.6],
    "year": [2023, 2023],
    "source": ["SAMHSA NSDUH 2023 / NIMH"] * 2
})

# ============================================================
# TABLE 5: DEMOGRAPHICS — AMI BY RACE/ETHNICITY (2023)
# Source: SAMHSA NSDUH 2023 Annual Report
# ============================================================

demographics_race = pd.DataFrame({
    "race_ethnicity": [
        "White (Non-Hispanic)",
        "Two or More Races",
        "American Indian/Alaska Native",
        "Black (Non-Hispanic)",
        "Hispanic",
        "Asian"
    ],
    "ami_pct": [24.9, 35.8, 28.4, 18.6, 18.2, 14.5],
    "smi_pct": [5.5,  11.8,  7.3,  5.2,  4.4,  2.8],
    "year": [2023] * 6,
    "source": ["SAMHSA NSDUH 2023"] * 6
})

# ============================================================
# TABLE 6: COVID IMPACT — PRE VS POST COVID COMPARISON
# Source: SAMHSA NSDUH 2019-2023
# ============================================================

covid_impact = pd.DataFrame({
    "year": [2019, 2020, 2021, 2022, 2023],
    "ami_pct": [19.9, 20.6, 22.8, 23.1, 22.8],
    "smi_pct": [5.2,  5.6,  5.5,  5.5,  5.8],
    "depression_pct": [7.8, 8.4, 8.3, 8.3, 8.3],
    "suicidal_ideation_pct": [4.8, 4.9, 5.0, 5.1, 5.0],
    "received_treatment_pct": [44.8, 46.2, 47.2, 48.7, 54.9],
    "source": ["SAMHSA NSDUH"] * 5
})

# ============================================================
# TABLE 7: STATE-LEVEL AMI PREVALENCE (2021-2022 avg)
# Source: SAMHSA NSDUH State Estimates 2021-2022
# ============================================================

state_data = pd.DataFrame({
    "state": [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California",
        "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
        "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
        "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
        "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
        "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
        "District of Columbia"
    ],
    "ami_pct": [
        20.7, 25.4, 21.8, 22.1, 20.2,
        24.1, 21.1, 21.8, 18.7, 18.4,
        19.1, 24.2, 19.8, 22.3, 19.6,
        20.8, 23.8, 20.3, 26.2, 19.5,
        23.4, 22.7, 21.8, 20.4, 22.9,
        25.3, 20.1, 21.9, 25.5, 18.5,
        24.6, 20.1, 20.4, 21.3, 22.8,
        23.9, 26.4, 21.6, 24.8, 20.1,
        22.0, 22.1, 18.2, 22.9, 27.1,
        20.0, 25.2, 25.9, 22.6, 24.8,
        20.3
    ],
    "year": ["2021-2022"] * 51,
    "source": ["SAMHSA NSDUH State Estimates"] * 51
})

# ============================================================
# WRITE ALL TABLES TO CSV
# ============================================================

os.makedirs(output_folder, exist_ok=True)

national_trend.to_csv(os.path.join(output_folder, "mh_national_trend.csv"), index=False)
treatment_gap.to_csv(os.path.join(output_folder, "mh_treatment_gap.csv"), index=False)
demographics_age.to_csv(os.path.join(output_folder, "mh_demographics_age.csv"), index=False)
demographics_sex.to_csv(os.path.join(output_folder, "mh_demographics_sex.csv"), index=False)
demographics_race.to_csv(os.path.join(output_folder, "mh_demographics_race.csv"), index=False)
covid_impact.to_csv(os.path.join(output_folder, "mh_covid_impact.csv"), index=False)
state_data.to_csv(os.path.join(output_folder, "mh_state_data.csv"), index=False)

print("All CSV files written successfully")

# ============================================================
# WRITE ALL TABLES TO SQLITE
# ============================================================

conn = sqlite3.connect(db_path)

national_trend.to_sql("national_trend", conn, if_exists="replace", index=False)
treatment_gap.to_sql("treatment_gap", conn, if_exists="replace", index=False)
demographics_age.to_sql("demographics_age", conn, if_exists="replace", index=False)
demographics_sex.to_sql("demographics_sex", conn, if_exists="replace", index=False)
demographics_race.to_sql("demographics_race", conn, if_exists="replace", index=False)
covid_impact.to_sql("covid_impact", conn, if_exists="replace", index=False)
state_data.to_sql("state_data", conn, if_exists="replace", index=False)

conn.close()

print("All tables written to mental_health.db successfully")
print("\nTables created:")
print("  - national_trend      : AMI & SMI trend 2008-2024")
print("  - treatment_gap       : Treatment rates vs prevalence 2008-2023")
print("  - demographics_age    : AMI by age group 2023")
print("  - demographics_sex    : AMI by sex 2023")
print("  - demographics_race   : AMI by race/ethnicity 2023")
print("  - covid_impact        : Pre vs post COVID comparison 2019-2023")
print("  - state_data          : State-level AMI prevalence 2021-2022")
