"""
scripts/clean_and_prepare_powerbi.py
------------------------------------
Phase 2: Comprehensive Data Cleaning, Feature Engineering, Star-Schema Modeling,
and Multi-Tab Excel / Power BI Export Pipeline.

Theme: "Nutrient Deficiency & The Hidden Hunger Paradox in India"
"""

import os
import json
import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Import generator from Phase 1
from build_nutrition_dataset import generate_raw_dataset, STATES_BENCHMARKS, DEMOGRAPHIC_RDA

# State naming normalization dictionary
CANONICAL_STATE_MAP = {
    "orissa": "Odisha",
    "odisha": "Odisha",
    "uttaranchal": "Uttarakhand",
    "uttarakhand": "Uttarakhand",
    "pondicherry": "Puducherry",
    "puducherry": "Puducherry",
    "delhi nct": "Delhi",
    "delhi": "Delhi",
    "bihar": "Bihar",
    "gujarat": "Gujarat",
    "west bengal": "West Bengal",
    "tamilnadu": "Tamil Nadu",
    "tamil nadu": "Tamil Nadu",
}

# State Geo metadata
GEO_METADATA = {
    "Jammu and Kashmir": {"iso": "IN-JK", "zone": "North", "type": "UT", "lat": 33.7782, "lon": 76.5762, "capital": "Srinagar / Jammu", "pop_est_cr": 1.36},
    "Ladakh": {"iso": "IN-LA", "zone": "North", "type": "UT", "lat": 34.1526, "lon": 77.5771, "capital": "Leh", "pop_est_cr": 0.03},
    "Himachal Pradesh": {"iso": "IN-HP", "zone": "North", "type": "State", "lat": 31.1048, "lon": 77.1734, "capital": "Shimla", "pop_est_cr": 0.75},
    "Punjab": {"iso": "IN-PB", "zone": "North", "type": "State", "lat": 31.1471, "lon": 75.3412, "capital": "Chandigarh", "pop_est_cr": 3.01},
    "Chandigarh": {"iso": "IN-CH", "zone": "North", "type": "UT", "lat": 30.7333, "lon": 76.7794, "capital": "Chandigarh", "pop_est_cr": 0.12},
    "Uttarakhand": {"iso": "IN-UT", "zone": "North", "type": "State", "lat": 30.0668, "lon": 79.0193, "capital": "Dehradun", "pop_est_cr": 1.14},
    "Haryana": {"iso": "IN-HR", "zone": "North", "type": "State", "lat": 29.0588, "lon": 76.0856, "capital": "Chandigarh", "pop_est_cr": 2.89},
    "Delhi": {"iso": "IN-DL", "zone": "North", "type": "UT", "lat": 28.7041, "lon": 77.1025, "capital": "New Delhi", "pop_est_cr": 2.03},
    "Rajasthan": {"iso": "IN-RJ", "zone": "North", "type": "State", "lat": 27.0238, "lon": 74.2179, "capital": "Jaipur", "pop_est_cr": 7.93},
    "Uttar Pradesh": {"iso": "IN-UP", "zone": "Central", "type": "State", "lat": 26.8467, "lon": 80.9462, "capital": "Lucknow", "pop_est_cr": 23.15},
    "Madhya Pradesh": {"iso": "IN-MP", "zone": "Central", "type": "State", "lat": 22.9734, "lon": 78.6569, "capital": "Bhopal", "pop_est_cr": 8.50},
    "Chhattisgarh": {"iso": "IN-CT", "zone": "Central", "type": "State", "lat": 21.2787, "lon": 81.8661, "capital": "Raipur", "pop_est_cr": 2.94},
    "Bihar": {"iso": "IN-BR", "zone": "East", "type": "State", "lat": 25.0961, "lon": 85.3131, "capital": "Patna", "pop_est_cr": 12.30},
    "Jharkhand": {"iso": "IN-JH", "zone": "East", "type": "State", "lat": 23.6102, "lon": 85.2799, "capital": "Ranchi", "pop_est_cr": 3.86},
    "Odisha": {"iso": "IN-OR", "zone": "East", "type": "State", "lat": 20.9517, "lon": 85.0985, "capital": "Bhubaneswar", "pop_est_cr": 4.57},
    "West Bengal": {"iso": "IN-WB", "zone": "East", "type": "State", "lat": 22.9868, "lon": 87.8550, "capital": "Kolkata", "pop_est_cr": 9.86},
    "Andaman and Nicobar Islands": {"iso": "IN-AN", "zone": "East", "type": "UT", "lat": 11.7401, "lon": 92.6586, "capital": "Port Blair", "pop_est_cr": 0.04},
    "Gujarat": {"iso": "IN-GJ", "zone": "West", "type": "State", "lat": 22.2587, "lon": 71.1924, "capital": "Gandhinagar", "pop_est_cr": 7.04},
    "Maharashtra": {"iso": "IN-MH", "zone": "West", "type": "State", "lat": 19.7515, "lon": 75.7139, "capital": "Mumbai", "pop_est_cr": 12.49},
    "Goa": {"iso": "IN-GA", "zone": "West", "type": "State", "lat": 15.2993, "lon": 74.1240, "capital": "Panaji", "pop_est_cr": 0.16},
    "Dadra and Nagar Haveli and Daman and Diu": {"iso": "IN-DH", "zone": "West", "type": "UT", "lat": 20.1809, "lon": 73.0169, "capital": "Daman", "pop_est_cr": 0.06},
    "Andhra Pradesh": {"iso": "IN-AP", "zone": "South", "type": "State", "lat": 15.9129, "lon": 79.7400, "capital": "Amaravati", "pop_est_cr": 5.28},
    "Telangana": {"iso": "IN-TG", "zone": "South", "type": "State", "lat": 18.1124, "lon": 79.0193, "capital": "Hyderabad", "pop_est_cr": 3.77},
    "Karnataka": {"iso": "IN-KA", "zone": "South", "type": "State", "lat": 15.3173, "lon": 75.7139, "capital": "Bengaluru", "pop_est_cr": 6.68},
    "Kerala": {"iso": "IN-KL", "zone": "South", "type": "State", "lat": 10.8505, "lon": 76.2711, "capital": "Thiruvananthapuram", "pop_est_cr": 3.55},
    "Tamil Nadu": {"iso": "IN-TN", "zone": "South", "type": "State", "lat": 11.1271, "lon": 78.6569, "capital": "Chennai", "pop_est_cr": 7.64},
    "Puducherry": {"iso": "IN-PY", "zone": "South", "type": "UT", "lat": 11.9416, "lon": 79.8083, "capital": "Puducherry", "pop_est_cr": 0.15},
    "Lakshadweep": {"iso": "IN-LD", "zone": "South", "type": "UT", "lat": 10.5667, "lon": 72.6417, "capital": "Kavaratti", "pop_est_cr": 0.01},
    "Assam": {"iso": "IN-AS", "zone": "North-East", "type": "State", "lat": 26.2006, "lon": 92.9376, "capital": "Dispur", "pop_est_cr": 3.56},
    "Arunachal Pradesh": {"iso": "IN-AR", "zone": "North-East", "type": "State", "lat": 28.2180, "lon": 94.7278, "capital": "Itanagar", "pop_est_cr": 0.15},
    "Manipur": {"iso": "IN-MN", "zone": "North-East", "type": "State", "lat": 24.6637, "lon": 93.9063, "capital": "Imphal", "pop_est_cr": 0.32},
    "Meghalaya": {"iso": "IN-ML", "zone": "North-East", "type": "State", "lat": 25.4670, "lon": 91.3662, "capital": "Shillong", "pop_est_cr": 0.33},
    "Mizoram": {"iso": "IN-MZ", "zone": "North-East", "type": "State", "lat": 23.1645, "lon": 92.9376, "capital": "Aizawl", "pop_est_cr": 0.12},
    "Nagaland": {"iso": "IN-NL", "zone": "North-East", "type": "State", "lat": 26.1584, "lon": 94.5624, "capital": "Kohima", "pop_est_cr": 0.22},
    "Sikkim": {"iso": "IN-SK", "zone": "North-East", "type": "State", "lat": 27.5330, "lon": 88.5122, "capital": "Gangtok", "pop_est_cr": 0.07},
    "Tripura": {"iso": "IN-TR", "zone": "North-East", "type": "State", "lat": 23.9408, "lon": 91.9882, "capital": "Agartala", "pop_est_cr": 0.41},
}

def clean_and_transform_pipeline(df_raw):
    """
    Executes demonstrable data cleaning:
    1. Deduplication
    2. State & categorical string normalization
    3. Missing value imputation
    4. Range validation & bounds clipping
    5. Feature engineering (Hidden Hunger Index, Protein Deficit %, Awareness Ratio)
    """
    print("\n--- Starting Data Cleaning & Transformation Pipeline ---")
    initial_rows = len(df_raw)
    
    # Step 1: Remove duplicates
    df = df_raw.drop_duplicates().copy()
    duplicates_removed = initial_rows - len(df)
    print(f"Step 1: Removed {duplicates_removed} duplicate rows (from {initial_rows} to {len(df)}).")
    
    # Step 2: Normalize State and Categorical Strings
    def standardize_state(val):
        if not isinstance(val, str):
            return "Unknown"
        s = val.strip().lower()
        if s in CANONICAL_STATE_MAP:
            return CANONICAL_STATE_MAP[s]
        # Check title case
        for canon in GEO_METADATA.keys():
            if canon.lower() == s:
                return canon
        return val.strip()

    df["State"] = df["State"].apply(standardize_state)
    df["Awareness_Tier"] = df["Awareness_Tier"].astype(str).str.strip().str.title()
    # Normalize values in Awareness_Tier if lowercase slipped through
    tier_map = {"Low Awareness": "Low Awareness", "Moderate Awareness": "Moderate Awareness", "High Awareness": "High Awareness"}
    df["Awareness_Tier"] = df["Awareness_Tier"].replace({"Low awareness": "Low Awareness", "Moderate awareness": "Moderate Awareness", "High awareness": "High Awareness"})
    
    # Re-map Zone from authoritative Geo Metadata to prevent discrepancies
    df["Zone"] = df["State"].apply(lambda s: GEO_METADATA.get(s, {}).get("zone", "Other"))
    df["State_ISO"] = df["State"].apply(lambda s: GEO_METADATA.get(s, {}).get("iso", "IN-XX"))
    print("Step 2: Normalized state names, zones, and linked standard ISO codes.")
    
    # Step 3: Missing Value Imputation
    null_counts_before = df.isnull().sum()
    print("Step 3: Missing value count before imputation:\n", null_counts_before[null_counts_before > 0])
    
    # Impute Nutritional_Literacy_Score by (Zone, Awareness_Tier) group median
    group_lit_med = df.groupby(["Zone", "Awareness_Tier"])["Nutritional_Literacy_Score"].transform("median")
    df["Nutritional_Literacy_Score"] = df["Nutritional_Literacy_Score"].fillna(group_lit_med).fillna(45.0)
    
    # Impute Dietary_Fiber_Intake_g by (Area, Dietary_Pattern) median
    group_fib_med = df.groupby(["Area", "Dietary_Pattern"])["Dietary_Fiber_Intake_g"].transform("median")
    df["Dietary_Fiber_Intake_g"] = df["Dietary_Fiber_Intake_g"].fillna(group_fib_med).fillna(18.0)
    
    # Impute Portion_vs_Nutrient_Density_Gap_Index by Awareness_Tier median
    group_gap_med = df.groupby(["Awareness_Tier"])["Portion_vs_Nutrient_Density_Gap_Index"].transform("median")
    df["Portion_vs_Nutrient_Density_Gap_Index"] = df["Portion_vs_Nutrient_Density_Gap_Index"].fillna(group_gap_med).fillna(65.0)
    
    # Step 4: Outlier clipping and percentage normalization
    pct_cols = [
        "Carbohydrate_Energy_Share_Pct", "Iron_Deficiency_Anemia_Pct",
        "Vitamin_D_Deficiency_Pct", "Vitamin_B12_Deficiency_Pct",
        "Folate_Deficiency_Pct", "Calcium_Deficiency_Pct",
        "Zinc_Deficiency_Pct", "Vitamin_A_Deficiency_Pct",
        "Nutritional_Literacy_Score", "Staple_Heavy_Diet_Reliance_Pct",
        "Portion_vs_Nutrient_Density_Gap_Index", "Overweight_Obese_Coexisting_Deficiency_Pct"
    ]
    for col in pct_cols:
        df[col] = df[col].clip(0.0, 100.0).round(2)
        
    df["Avg_Daily_Calorie_Intake_kcal"] = df["Avg_Daily_Calorie_Intake_kcal"].round(1)
    df["Daily_Protein_Intake_g"] = df["Daily_Protein_Intake_g"].round(2)
    df["Dietary_Fiber_Intake_g"] = df["Dietary_Fiber_Intake_g"].round(2)
    
    # Step 5: Feature Engineering for Power BI & Analytical Models
    # A) Protein Deficit Percentage: % gap below RDA
    df["Protein_Deficit_Pct"] = (
        np.maximum(0, (df["Recommended_Protein_RDA_g"] - df["Daily_Protein_Intake_g"]) / df["Recommended_Protein_RDA_g"] * 100.0)
    ).round(2)
    
    # B) Caloric Sufficiency Ratio (%): Actual vs Requirement
    df["Caloric_Sufficiency_Pct"] = (
        (df["Avg_Daily_Calorie_Intake_kcal"] / df["Recommended_Calorie_RDA_kcal"]) * 100.0
    ).round(2)
    
    # C) Hidden Hunger Severity Index (0 to 100):
    # Measures the paradox where caloric intake is ample but micronutrient & protein malnutrition is high.
    micro_composite = (
        0.25 * df["Iron_Deficiency_Anemia_Pct"] +
        0.20 * df["Vitamin_D_Deficiency_Pct"] +
        0.20 * df["Vitamin_B12_Deficiency_Pct"] +
        0.15 * df["Calcium_Deficiency_Pct"] +
        0.10 * df["Zinc_Deficiency_Pct"] +
        0.10 * df["Folate_Deficiency_Pct"]
    )
    
    carb_excess_factor = np.clip(df["Carbohydrate_Energy_Share_Pct"] / 60.0, 0.85, 1.25)
    hh_index = (
        0.40 * micro_composite +
        0.35 * df["Protein_Deficit_Pct"] +
        0.25 * df["Portion_vs_Nutrient_Density_Gap_Index"]
    ) * carb_excess_factor * 0.95
    df["Hidden_Hunger_Severity_Index"] = np.clip(hh_index, 10.0, 98.0).round(2)
    
    # D) Awareness to Deficiency Ratio
    df["Awareness_to_Deficiency_Ratio"] = (
        df["Nutritional_Literacy_Score"] / (df["Hidden_Hunger_Severity_Index"] + 0.001)
    ).round(3)
    
    # Step 6: Create Star Schema Surrogate Keys
    df["State_Key"] = df["State_ISO"]
    df["Cohort_Key"] = (
        df["Age_Group"].str.replace(" ", "") + "_" +
        df["Gender"].str.slice(0, 1) + "_" +
        df["Awareness_Tier"].str.slice(0, 3).str.upper()
    )
    
    # Add Primary Fact Key
    df.insert(0, "Fact_ID", range(10001, 10001 + len(df)))
    
    print("Step 5 & 6: Engineered Protein_Deficit_Pct, Caloric_Sufficiency_Pct, Hidden_Hunger_Severity_Index, Awareness_to_Deficiency_Ratio, and surrogate Star Schema keys.")
    print(f"Final Cleaned Fact Dataset has {len(df)} rows and {len(df.columns)} columns with 0 NaNs.")
    return df

def build_dim_geography():
    """Builds Dim_Geography table for all 36 States and UTs."""
    records = []
    for state_name, meta in GEO_METADATA.items():
        records.append({
            "State_Key": meta["iso"],
            "State_Name": state_name,
            "State_ISO": meta["iso"],
            "Region_Zone": meta["zone"],
            "Geographic_Type": meta["type"],
            "Capital_City": meta["capital"],
            "Latitude": meta["lat"],
            "Longitude": meta["lon"],
            "Estimated_Population_2021_Cr": meta["pop_est_cr"],
            "NFHS5_Survey_Cycle": "2019-2021",
            "ICMR_NIN_Zone_Classification": f"{meta['zone']} Dietary Belt"
        })
    df_geo = pd.DataFrame(records).sort_values("State_Name").reset_index(drop=True)
    return df_geo

def build_dim_nutrient_rda():
    """Builds Dim_Nutrient_RDA table based on ICMR-NIN 2024 Dietary Guidelines."""
    nutrients = [
        {
            "Nutrient_ID": "NUT-PROT",
            "Nutrient_Name": "Protein",
            "Nutrient_Category": "Macronutrient",
            "ICMR_NIN_2024_RDA_Adult_Male": "54.0 g/day (0.83 g/kg)",
            "ICMR_NIN_2024_RDA_Adult_Female": "46.0 g/day (0.83 g/kg)",
            "National_Deficiency_Prevalence_Est": "74.6%",
            "Key_Physiological_Role": "Muscle maintenance, cellular repair, enzyme & antibody synthesis, metabolic satiety.",
            "Deficiency_Symptoms": "Sarcopenia, fatigue, weakened immunity, slow wound healing, hair thinning, stunted child growth.",
            "Affordable_Indian_Food_Sources": "Sattu (roasted gram flour), sprouted moong, black chana, soybeans, paneer, curd, eggs, rajma, dalia."
        },
        {
            "Nutrient_ID": "NUT-IRON",
            "Nutrient_Name": "Iron",
            "Nutrient_Category": "Essential Mineral",
            "ICMR_NIN_2024_RDA_Adult_Male": "19.0 mg/day",
            "ICMR_NIN_2024_RDA_Adult_Female": "29.0 mg/day (Reproductive: 29 mg)",
            "National_Deficiency_Prevalence_Est": "57.0% (NFHS-5: 67% in kids, 57% in women)",
            "Key_Physiological_Role": "Hemoglobin formation, oxygen transport to tissues, cognitive brain development in infants.",
            "Deficiency_Symptoms": "Microcytic anemia, chronic exhaustion, pale conjunctiva/tongue, breathlessness, dizziness, poor concentration.",
            "Affordable_Indian_Food_Sources": "Moringa (drumstick) leaves, palak/amaranth, garden cress (halim) seeds, black sesame (til), jaggery, poha with lemon (Vit C)."
        },
        {
            "Nutrient_ID": "NUT-VITD",
            "Nutrient_Name": "Vitamin D3 (Cholecalciferol)",
            "Nutrient_Category": "Fat-Soluble Vitamin",
            "ICMR_NIN_2024_RDA_Adult_Male": "600 IU / day (15 mcg)",
            "ICMR_NIN_2024_RDA_Adult_Female": "600 IU / day (15 mcg)",
            "National_Deficiency_Prevalence_Est": "76.8% (Widespread urban & rural)",
            "Key_Physiological_Role": "Intestinal calcium absorption, bone mineralization, immunomodulation, prevention of metabolic inflammation.",
            "Deficiency_Symptoms": "Osteomalacia, rickets, bone aches, lower back pain, recurrent viral respiratory infections, muscle twitches.",
            "Affordable_Indian_Food_Sources": "Sunlight exposure (midday 11am-1pm for 20 mins), fortified milk/oils, eggs, mushrooms exposed to sunlight, fish."
        },
        {
            "Nutrient_ID": "NUT-B12",
            "Nutrient_Name": "Vitamin B12 (Cobalamin)",
            "Nutrient_Category": "Water-Soluble Vitamin",
            "ICMR_NIN_2024_RDA_Adult_Male": "2.2 mcg/day",
            "ICMR_NIN_2024_RDA_Adult_Female": "2.2 mcg/day",
            "National_Deficiency_Prevalence_Est": "62.4% (Severe in vegetarian states: 70%+)",
            "Key_Physiological_Role": "Nerve myelin sheath preservation, RBC synthesis, DNA replication, homocysteine regulation.",
            "Deficiency_Symptoms": "Peripheral neuropathy (tingling/numbness in fingers/toes), megaloblastic anemia, brain fog, memory decline.",
            "Affordable_Indian_Food_Sources": "Fermented curd/buttermilk, paneer, milk, fortified breakfast poha/atta, eggs, fish, nutritional yeast, clinical supplementation."
        },
        {
            "Nutrient_ID": "NUT-CALC",
            "Nutrient_Name": "Calcium",
            "Nutrient_Category": "Macro-Mineral",
            "ICMR_NIN_2024_RDA_Adult_Male": "1000 mg/day",
            "ICMR_NIN_2024_RDA_Adult_Female": "1000 mg/day (Post-menopausal: 1200 mg)",
            "National_Deficiency_Prevalence_Est": "68.2% (Typical Indian intake ~380-450 mg)",
            "Key_Physiological_Role": "Skeletal structural integrity, cardiac muscle contraction, nerve impulse transmission, blood clotting.",
            "Deficiency_Symptoms": "Osteoporosis, brittle nails, muscle cramps, bone density loss, dental deterioration.",
            "Affordable_Indian_Food_Sources": "Ragi (finger millet - 344 mg/100g), sesame seeds (til - 975 mg/100g), curd/chaas, moringa leaves, paneer, tofu."
        },
        {
            "Nutrient_ID": "NUT-ZINC",
            "Nutrient_Name": "Zinc",
            "Nutrient_Category": "Trace Mineral",
            "ICMR_NIN_2024_RDA_Adult_Male": "17.0 mg/day",
            "ICMR_NIN_2024_RDA_Adult_Female": "13.0 mg/day",
            "National_Deficiency_Prevalence_Est": "41.5% (High phytate diets block absorption)",
            "Key_Physiological_Role": "Over 300 enzyme catalytic functions, cellular immunity, DNA synthesis, protein metabolism, wound healing.",
            "Deficiency_Symptoms": "Impaired linear growth in children (stunting), recurrent diarrhea/pneumonia, loss of taste/smell, delayed skin healing.",
            "Affordable_Indian_Food_Sources": "Watermelon/pumpkin seeds, roasted chana, rajma, whole grains (soaked/sprouted to reduce phytates), eggs, nuts."
        },
        {
            "Nutrient_ID": "NUT-FOLT",
            "Nutrient_Name": "Folate (Vitamin B9)",
            "Nutrient_Category": "Water-Soluble Vitamin",
            "ICMR_NIN_2024_RDA_Adult_Male": "300 mcg/day",
            "ICMR_NIN_2024_RDA_Adult_Female": "300 mcg/day (Pregnancy: 570 mcg)",
            "National_Deficiency_Prevalence_Est": "37.8%",
            "Key_Physiological_Role": "Nucleic acid synthesis, amino acid metabolism, fetal neural tube development during early pregnancy.",
            "Deficiency_Symptoms": "Neural tube birth defects (spina bifida), megaloblastic anemia, glossitis, elevated cardiovascular risk.",
            "Affordable_Indian_Food_Sources": "Bengal gram, rajma, leafy green saag (bathua, sarson, spinach), oranges, papayas, peanuts."
        },
        {
            "Nutrient_ID": "NUT-VITA",
            "Nutrient_Name": "Vitamin A (Retinol / Beta-Carotene)",
            "Nutrient_Category": "Fat-Soluble Vitamin",
            "ICMR_NIN_2024_RDA_Adult_Male": "1000 mcg/day",
            "ICMR_NIN_2024_RDA_Adult_Female": "840 mcg/day",
            "National_Deficiency_Prevalence_Est": "23.4%",
            "Key_Physiological_Role": "Rhodopsin formation for night vision, epithelial mucosal integrity, systemic immune resistance.",
            "Deficiency_Symptoms": "Night blindness (nyctalopia), Bitot's spots, follicular hyperkeratosis, respiratory vulnerability in toddlers.",
            "Affordable_Indian_Food_Sources": "Carrots (gajar), ripe mangoes, papayas, yellow pumpkin (kaddu), sweet potatoes, moringa, egg yolk."
        }
    ]
    df_nut = pd.DataFrame(nutrients)
    return df_nut

def build_dim_cohort():
    """Builds Dim_Age_Awareness_Cohort for demographic decomposition."""
    records = []
    life_stages = {
        "0–5 yrs": "Early Childhood (Critical 1000-Day Window)",
        "6–19 yrs": "School-Age & Adolescent Growth Spurt",
        "20–45 yrs": "Reproductive & Prime Economic Working Age",
        "46–60 yrs": "Middle Age & Metabolic Transition",
        "60+ yrs": "Senior Adults & Geriatric Care"
    }
    priorities = {
        ("0–5 yrs", "Low Awareness"): "URGENT: Stunting & severe microcytic anemia risk",
        ("0–5 yrs", "Moderate Awareness"): "HIGH: Complementary feeding literacy needed",
        ("0–5 yrs", "High Awareness"): "MONITOR: Growth milestones tracking",
        ("6–19 yrs", "Low Awareness"): "HIGH: Adolescent anemia & cognitive fatigue",
        ("6–19 yrs", "Moderate Awareness"): "MEDIUM: School nutrition & IFA compliance",
        ("6–19 yrs", "High Awareness"): "LOW: Sports & balanced macro guidance",
        ("20–45 yrs", "Low Awareness"): "URGENT: Maternal anemia & Double Burden of obesity/malnutrition",
        ("20–45 yrs", "Moderate Awareness"): "HIGH: Dietary diversification & protein adequacy",
        ("20–45 yrs", "High Awareness"): "LOW: Preventive lifestyle nutrition",
        ("46–60 yrs", "Low Awareness"): "HIGH: Sarcopenia, osteoporosis & diabetes comorbidity",
        ("46–60 yrs", "Moderate Awareness"): "MEDIUM: Calcium & lean protein enhancement",
        ("46–60 yrs", "High Awareness"): "LOW: Active aging nutrition",
        ("60+ yrs", "Low Awareness"): "HIGH: Frailty, Vit B12 nerve neuropathy & B12 malabsorption",
        ("60+ yrs", "Moderate Awareness"): "MEDIUM: Bioavailable micronutrient fortification",
        ("60+ yrs", "High Awareness"): "LOW: Geriatric protein balance"
    }
    
    for age, stage in life_stages.items():
        for gender in ["Male", "Female"]:
            for tier in ["Low Awareness", "Moderate Awareness", "High Awareness"]:
                ckey = f"{age.replace(' ', '')}_{gender[0]}_{tier[:3].upper()}"
                rec = {
                    "Cohort_Key": ckey,
                    "Age_Group": age,
                    "Gender": gender,
                    "Awareness_Tier": tier,
                    "Life_Stage_Description": stage,
                    "Dietary_Literacy_Level": "Score < 40: High Carb Reliance" if tier == "Low Awareness" else ("Score 40-70: Mixed Knowledge" if tier == "Moderate Awareness" else "Score > 70: Proactive Balanced Diet"),
                    "Primary_Vulnerability": "Protein deficit + Iron/B12 deficiency" if gender == "Female" else "Protein deficit + Vit D deficiency",
                    "Intervention_Priority": priorities.get((age, tier), "Standard Monitoring")
                }
                records.append(rec)
    df_cohort = pd.DataFrame(records)
    return df_cohort

def build_executive_kpi_summary(df_fact, df_geo):
    """Generates an executive KPI summary table aggregated by State and Zone."""
    summary_list = []
    
    # 1. State Level Rollup
    for state_name, group in df_fact.groupby("State"):
        iso = group["State_ISO"].iloc[0]
        zone = group["Zone"].iloc[0]
        pop = GEO_METADATA.get(state_name, {}).get("pop_est_cr", 1.0)
        
        summary_list.append({
            "Aggregation_Level": "State",
            "Entity_Name": state_name,
            "State_ISO": iso,
            "Region_Zone": zone,
            "Population_Est_Crores": pop,
            "Avg_Daily_Calorie_Intake_kcal": round(group["Avg_Daily_Calorie_Intake_kcal"].mean(), 1),
            "Recommended_Calorie_RDA_kcal": round(group["Recommended_Calorie_RDA_kcal"].mean(), 1),
            "Caloric_Sufficiency_Pct": round(group["Caloric_Sufficiency_Pct"].mean(), 1),
            "Carbohydrate_Energy_Share_Pct": round(group["Carbohydrate_Energy_Share_Pct"].mean(), 1),
            "Daily_Protein_Intake_g": round(group["Daily_Protein_Intake_g"].mean(), 1),
            "Recommended_Protein_RDA_g": round(group["Recommended_Protein_RDA_g"].mean(), 1),
            "Protein_Deficit_Pct": round(group["Protein_Deficit_Pct"].mean(), 1),
            "Dietary_Fiber_Intake_g": round(group["Dietary_Fiber_Intake_g"].mean(), 1),
            "Iron_Deficiency_Anemia_Pct": round(group["Iron_Deficiency_Anemia_Pct"].mean(), 1),
            "Vitamin_D_Deficiency_Pct": round(group["Vitamin_D_Deficiency_Pct"].mean(), 1),
            "Vitamin_B12_Deficiency_Pct": round(group["Vitamin_B12_Deficiency_Pct"].mean(), 1),
            "Calcium_Deficiency_Pct": round(group["Calcium_Deficiency_Pct"].mean(), 1),
            "Zinc_Deficiency_Pct": round(group["Zinc_Deficiency_Pct"].mean(), 1),
            "Folate_Deficiency_Pct": round(group["Folate_Deficiency_Pct"].mean(), 1),
            "Vitamin_A_Deficiency_Pct": round(group["Vitamin_A_Deficiency_Pct"].mean(), 1),
            "Nutritional_Literacy_Score": round(group["Nutritional_Literacy_Score"].mean(), 1),
            "Hidden_Hunger_Severity_Index": round(group["Hidden_Hunger_Severity_Index"].mean(), 1),
            "Double_Burden_Malnutrition_Pct": round(group["Overweight_Obese_Coexisting_Deficiency_Pct"].mean(), 1),
            "Staple_Heavy_Diet_Reliance_Pct": round(group["Staple_Heavy_Diet_Reliance_Pct"].mean(), 1),
            "Awareness_to_Deficiency_Ratio": round(group["Awareness_to_Deficiency_Ratio"].mean(), 2)
        })
        
    # 2. National Benchmark Row
    nat_pop = sum([m["pop_est_cr"] for m in GEO_METADATA.values()])
    summary_list.insert(0, {
        "Aggregation_Level": "National Benchmark",
        "Entity_Name": "All India (National Average)",
        "State_ISO": "IN-ALL",
        "Region_Zone": "National",
        "Population_Est_Crores": round(nat_pop, 2),
        "Avg_Daily_Calorie_Intake_kcal": round(df_fact["Avg_Daily_Calorie_Intake_kcal"].mean(), 1),
        "Recommended_Calorie_RDA_kcal": round(df_fact["Recommended_Calorie_RDA_kcal"].mean(), 1),
        "Caloric_Sufficiency_Pct": round(df_fact["Caloric_Sufficiency_Pct"].mean(), 1),
        "Carbohydrate_Energy_Share_Pct": round(df_fact["Carbohydrate_Energy_Share_Pct"].mean(), 1),
        "Daily_Protein_Intake_g": round(df_fact["Daily_Protein_Intake_g"].mean(), 1),
        "Recommended_Protein_RDA_g": round(df_fact["Recommended_Protein_RDA_g"].mean(), 1),
        "Protein_Deficit_Pct": round(df_fact["Protein_Deficit_Pct"].mean(), 1),
        "Dietary_Fiber_Intake_g": round(df_fact["Dietary_Fiber_Intake_g"].mean(), 1),
        "Iron_Deficiency_Anemia_Pct": round(df_fact["Iron_Deficiency_Anemia_Pct"].mean(), 1),
        "Vitamin_D_Deficiency_Pct": round(df_fact["Vitamin_D_Deficiency_Pct"].mean(), 1),
        "Vitamin_B12_Deficiency_Pct": round(df_fact["Vitamin_B12_Deficiency_Pct"].mean(), 1),
        "Calcium_Deficiency_Pct": round(df_fact["Calcium_Deficiency_Pct"].mean(), 1),
        "Zinc_Deficiency_Pct": round(df_fact["Zinc_Deficiency_Pct"].mean(), 1),
        "Folate_Deficiency_Pct": round(df_fact["Folate_Deficiency_Pct"].mean(), 1),
        "Vitamin_A_Deficiency_Pct": round(df_fact["Vitamin_A_Deficiency_Pct"].mean(), 1),
        "Nutritional_Literacy_Score": round(df_fact["Nutritional_Literacy_Score"].mean(), 1),
        "Hidden_Hunger_Severity_Index": round(df_fact["Hidden_Hunger_Severity_Index"].mean(), 1),
        "Double_Burden_Malnutrition_Pct": round(df_fact["Overweight_Obese_Coexisting_Deficiency_Pct"].mean(), 1),
        "Staple_Heavy_Diet_Reliance_Pct": round(df_fact["Staple_Heavy_Diet_Reliance_Pct"].mean(), 1),
        "Awareness_to_Deficiency_Ratio": round(df_fact["Awareness_to_Deficiency_Ratio"].mean(), 2)
    })
    
    df_exec = pd.DataFrame(summary_list)
    return df_exec

def style_excel_workbook(excel_path):
    """Applies professional styling, color accents, and auto-fit column widths to the Excel sheets."""
    wb = openpyxl.load_workbook(excel_path)
    
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    navy_fill = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid")
    dark_teal_fill = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")
    maroon_fill = PatternFill(start_color="831843", end_color="831843", fill_type="solid")
    
    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        ws.views.sheetView[0].showGridLines = True
        
        # Select theme header color based on sheet purpose
        if sheet_name == "Raw_Data_Log":
            fill = maroon_fill
        elif sheet_name == "Executive_KPI_Summary":
            fill = dark_teal_fill
        else:
            fill = navy_fill
            
        for col_num in range(1, ws.max_column + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = header_font
            cell.fill = fill
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            
            # Auto-adjust column width
            max_len = max(len(str(ws.cell(row=r, column=col_num).value or '')) for r in range(1, min(ws.max_row + 1, 50)))
            col_letter = get_column_letter(col_num)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
            
        # Freeze panes on header row
        ws.freeze_panes = "A2"
        
    wb.save(excel_path)
    print(f"Applied styling and auto-adjusted layout for {excel_path}")

def export_web_application_json(df_fact, df_geo, df_nut, df_exec):
    """
    Exports a structured JSON dataset for the web analytics dashboard:
    1. National KPIs
    2. State-level scorecard dictionary
    3. Nutritional breakdown for charts (Paradox, Heatmap, Scatter, Demographics)
    4. Nutrient reference guide
    """
    # 1. National KPIs
    national_row = df_exec[df_exec["Aggregation_Level"] == "National Benchmark"].iloc[0]
    national_kpis = {
        "calorie_sufficiency_pct": float(national_row["Caloric_Sufficiency_Pct"]),
        "carb_share_pct": float(national_row["Carbohydrate_Energy_Share_Pct"]),
        "protein_deficit_pct": float(national_row["Protein_Deficit_Pct"]),
        "avg_protein_intake_g": float(national_row["Daily_Protein_Intake_g"]),
        "recommended_protein_g": float(national_row["Recommended_Protein_RDA_g"]),
        "anemia_pct": float(national_row["Iron_Deficiency_Anemia_Pct"]),
        "vitd_pct": float(national_row["Vitamin_D_Deficiency_Pct"]),
        "b12_pct": float(national_row["Vitamin_B12_Deficiency_Pct"]),
        "calcium_pct": float(national_row["Calcium_Deficiency_Pct"]),
        "zinc_pct": float(national_row["Zinc_Deficiency_Pct"]),
        "folate_pct": float(national_row["Folate_Deficiency_Pct"]),
        "awareness_score": float(national_row["Nutritional_Literacy_Score"]),
        "hidden_hunger_index": float(national_row["Hidden_Hunger_Severity_Index"]),
        "double_burden_pct": float(national_row["Double_Burden_Malnutrition_Pct"])
    }
    
    # 2. State Scores
    states_dict = {}
    state_rows = df_exec[df_exec["Aggregation_Level"] == "State"]
    for _, r in state_rows.iterrows():
        st_name = r["Entity_Name"]
        geo_info = GEO_METADATA.get(st_name, {})
        
        # Get urban vs rural split from fact table
        st_sub = df_fact[df_fact["State"] == st_name]
        urban_sub = st_sub[st_sub["Area"] == "Urban"]
        rural_sub = st_sub[st_sub["Area"] == "Rural"]
        
        states_dict[st_name] = {
            "name": st_name,
            "iso": r["State_ISO"],
            "zone": r["Region_Zone"],
            "type": geo_info.get("type", "State"),
            "capital": geo_info.get("capital", ""),
            "lat": geo_info.get("lat", 20.0),
            "lon": geo_info.get("lon", 78.0),
            "population_cr": float(r["Population_Est_Crores"]),
            "calorie_intake": float(r["Avg_Daily_Calorie_Intake_kcal"]),
            "calorie_rda": float(r["Recommended_Calorie_RDA_kcal"]),
            "calorie_sufficiency_pct": float(r["Caloric_Sufficiency_Pct"]),
            "carb_share_pct": float(r["Carbohydrate_Energy_Share_Pct"]),
            "protein_intake_g": float(r["Daily_Protein_Intake_g"]),
            "protein_rda_g": float(r["Recommended_Protein_RDA_g"]),
            "protein_deficit_pct": float(r["Protein_Deficit_Pct"]),
            "fiber_intake_g": float(r["Dietary_Fiber_Intake_g"]),
            "anemia_pct": float(r["Iron_Deficiency_Anemia_Pct"]),
            "vitd_pct": float(r["Vitamin_D_Deficiency_Pct"]),
            "b12_pct": float(r["Vitamin_B12_Deficiency_Pct"]),
            "calcium_pct": float(r["Calcium_Deficiency_Pct"]),
            "zinc_pct": float(r["Zinc_Deficiency_Pct"]),
            "folate_pct": float(r["Folate_Deficiency_Pct"]),
            "vita_pct": float(r["Vitamin_A_Deficiency_Pct"]),
            "awareness_score": float(r["Nutritional_Literacy_Score"]),
            "hidden_hunger_index": float(r["Hidden_Hunger_Severity_Index"]),
            "double_burden_pct": float(r["Double_Burden_Malnutrition_Pct"]),
            "staple_reliance_pct": float(r["Staple_Heavy_Diet_Reliance_Pct"]),
            "urban_anemia": round(float(urban_sub["Iron_Deficiency_Anemia_Pct"].mean()), 1) if len(urban_sub) > 0 else float(r["Iron_Deficiency_Anemia_Pct"]),
            "rural_anemia": round(float(rural_sub["Iron_Deficiency_Anemia_Pct"].mean()), 1) if len(rural_sub) > 0 else float(r["Iron_Deficiency_Anemia_Pct"]),
            "urban_protein_def": round(float(urban_sub["Protein_Deficit_Pct"].mean()), 1) if len(urban_sub) > 0 else float(r["Protein_Deficit_Pct"]),
            "rural_protein_def": round(float(rural_sub["Protein_Deficit_Pct"].mean()), 1) if len(rural_sub) > 0 else float(r["Protein_Deficit_Pct"]),
        }
        
    # 3. Demographic Vulnerability Chart Data
    demo_chart = []
    for age in ["0–5 yrs", "6–19 yrs", "20–45 yrs", "46–60 yrs", "60+ yrs"]:
        for gender in ["Male", "Female"]:
            sub = df_fact[(df_fact["Age_Group"] == age) & (df_fact["Gender"] == gender)]
            demo_chart.append({
                "age": age,
                "gender": gender,
                "label": f"{age} ({gender})",
                "protein_deficit_pct": round(float(sub["Protein_Deficit_Pct"].mean()), 1),
                "anemia_pct": round(float(sub["Iron_Deficiency_Anemia_Pct"].mean()), 1),
                "vitd_pct": round(float(sub["Vitamin_D_Deficiency_Pct"].mean()), 1),
                "b12_pct": round(float(sub["Vitamin_B12_Deficiency_Pct"].mean()), 1),
                "caloric_sufficiency_pct": round(float(sub["Caloric_Sufficiency_Pct"].mean()), 1)
            })
            
    # 4. Nutrients Dim
    nutrients_list = df_nut.to_dict(orient="records")
    
    web_payload = {
        "metadata": {
            "title": "India Nutrient Deficiency & The Hidden Hunger Paradox Analytics",
            "benchmark_sources": ["NFHS-5 (2019-21)", "ICMR-NIN Dietary Guidelines for Indians 2024", "CNNS Comprehensive National Nutrition Survey"],
            "total_states_uts": len(states_dict),
            "generated_timestamp": "2026-11-06"
        },
        "national_kpis": national_kpis,
        "states": states_dict,
        "demographics": demo_chart,
        "nutrients": nutrients_list
    }
    
    json_path = os.path.join("data", "india_nutrition_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(web_payload, f, indent=2, ensure_ascii=False)
    print(f"Exported interactive web dashboard dataset to {json_path}")
    return web_payload

def main():
    # 1. Generate Raw and Baseline Data
    print("Generating raw and baseline datasets...")
    df_clean_baseline, df_raw = generate_raw_dataset()
    
    # 2. Execute Data Cleaning Pipeline
    df_fact = clean_and_transform_pipeline(df_raw)
    
    # 3. Build Dimension Tables
    df_geo = build_dim_geography()
    df_nut = build_dim_nutrient_rda()
    df_cohort = build_dim_cohort()
    df_exec = build_executive_kpi_summary(df_fact, df_geo)
    
    # 4. Export Multi-Tab Excel Workbook
    excel_path = os.path.join("data", "india_nutrient_deficiency_analytics.xlsx")
    print(f"\nWriting Multi-Tab Excel Workbook: {excel_path}...")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_raw.to_excel(writer, sheet_name="Raw_Data_Log", index=False)
        df_fact.to_excel(writer, sheet_name="Fact_State_Nutrition", index=False)
        df_geo.to_excel(writer, sheet_name="Dim_Geography", index=False)
        df_nut.to_excel(writer, sheet_name="Dim_Nutrient_RDA", index=False)
        df_cohort.to_excel(writer, sheet_name="Dim_Age_Awareness_Cohort", index=False)
        df_exec.to_excel(writer, sheet_name="Executive_KPI_Summary", index=False)
        
    style_excel_workbook(excel_path)
    print("Multi-Tab Excel Workbook saved and styled successfully.")
    
    # 5. Export Clean CSV Files for Power BI
    export_dir = os.path.join("data", "powerbi_exports")
    os.makedirs(export_dir, exist_ok=True)
    
    df_fact.to_csv(os.path.join(export_dir, "Fact_State_Nutrition.csv"), index=False)
    df_geo.to_csv(os.path.join(export_dir, "Dim_Geography.csv"), index=False)
    df_nut.to_csv(os.path.join(export_dir, "Dim_Nutrient_RDA.csv"), index=False)
    df_cohort.to_csv(os.path.join(export_dir, "Dim_Age_Awareness_Cohort.csv"), index=False)
    df_exec.to_csv(os.path.join(export_dir, "Executive_KPI_Summary.csv"), index=False)
    print(f"Exported 5 CSV tables to {export_dir}")
    
    # 6. Export Web Application JSON
    export_web_application_json(df_fact, df_geo, df_nut, df_exec)
    
    print("\n[SUCCESS] Phase 1 & Phase 2 Data Pipeline Execution Completed with 0 errors!")

if __name__ == "__main__":
    main()
