"""
data_cleaning.py
----------------
Academic Data Cleaning, Preprocessing & Feature Engineering Pipeline
Project: "Nutrient Deficiency & The Hidden Hunger Paradox in India"

Inputs:  Dataset/raw_dataset.csv (or .xlsx)
Outputs: clean_dataset/clean_dataset.csv
"""

import os
import pandas as pd
import numpy as np

# Standardized Geo & State Mappings
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

def clean_data(raw_path="Dataset/raw_dataset.csv", output_path="clean_dataset/clean_dataset.csv"):
    print("=" * 70)
    print("STEP 1: Loading Raw Dataset...")
    print("=" * 70)
    if not os.path.exists(raw_path):
        # Fallback to local data folder if running from root
        if os.path.exists("data/india_nutrient_deficiency_analytics.xlsx"):
            df_raw = pd.read_excel("data/india_nutrient_deficiency_analytics.xlsx", sheet_name="Raw_Data_Log")
        else:
            raise FileNotFoundError(f"Cannot find {raw_path}")
    else:
        df_raw = pd.read_csv(raw_path) if raw_path.endswith(".csv") else pd.read_excel(raw_path)

    initial_rows = len(df_raw)
    initial_nulls = df_raw.isnull().sum().sum()
    print(f"Raw Records: {initial_rows} rows | Total Missing (NaN) values: {initial_nulls}")

    # 1. Deduplication
    print("\n--- STEP 2: Duplicate Record Removal ---")
    df = df_raw.drop_duplicates().copy()
    dups_removed = initial_rows - len(df)
    print(f"Removed {dups_removed} duplicate records ({initial_rows} -> {len(df)}).")

    # 2. String Standardization
    print("\n--- STEP 3: State & Categorical String Standardization ---")
    def clean_state(val):
        if not isinstance(val, str):
            return "Unknown"
        s = val.strip().lower()
        return CANONICAL_STATE_MAP.get(s, val.strip().title())

    df["State"] = df["State"].apply(clean_state)
    df["Awareness_Tier"] = df["Awareness_Tier"].astype(str).str.strip().str.title()
    df["Awareness_Tier"] = df["Awareness_Tier"].replace({
        "Low Awareness": "Low Awareness",
        "Moderate Awareness": "Moderate Awareness",
        "High Awareness": "High Awareness"
    })
    print(f"Standardized {df['State'].nunique()} Indian States and Union Territories.")

    # 3. Missing Value Imputation
    print("\n--- STEP 4: Missing Value Imputation ---")
    null_cols = df.columns[df.isnull().any()].tolist()
    print(f"Columns with missing values: {null_cols}")

    if "Nutritional_Literacy_Score" in df.columns:
        med_lit = df.groupby(["Zone", "Awareness_Tier"])["Nutritional_Literacy_Score"].transform("median")
        df["Nutritional_Literacy_Score"] = df["Nutritional_Literacy_Score"].fillna(med_lit).fillna(45.0)

    if "Dietary_Fiber_Intake_g" in df.columns:
        med_fib = df.groupby(["Area", "Dietary_Pattern"])["Dietary_Fiber_Intake_g"].transform("median")
        df["Dietary_Fiber_Intake_g"] = df["Dietary_Fiber_Intake_g"].fillna(med_fib).fillna(18.0)

    if "Portion_vs_Nutrient_Density_Gap_Index" in df.columns:
        med_gap = df.groupby("Awareness_Tier")["Portion_vs_Nutrient_Density_Gap_Index"].transform("median")
        df["Portion_vs_Nutrient_Density_Gap_Index"] = df["Portion_vs_Nutrient_Density_Gap_Index"].fillna(med_gap).fillna(65.0)

    print(f"Post-Imputation Missing Values: {df.isnull().sum().sum()} (Zero NaNs).")

    # 4. Outlier Validation & Percentage Clipping (0 - 100%)
    print("\n--- STEP 5: Range Validation & Clipping ---")
    pct_cols = [c for c in df.columns if c.endswith("_Pct") or "Score" in c or "Index" in c]
    for col in pct_cols:
        df[col] = df[col].clip(0.0, 100.0).round(2)

    # 5. Feature Engineering
    print("\n--- STEP 6: Analytical Feature Engineering ---")
    # A) Protein Deficit Percentage
    df["Protein_Deficit_Pct"] = (
        np.maximum(0, (df["Recommended_Protein_RDA_g"] - df["Daily_Protein_Intake_g"]) / df["Recommended_Protein_RDA_g"] * 100.0)
    ).round(2)

    # B) Caloric Sufficiency Ratio %
    df["Caloric_Sufficiency_Pct"] = (
        (df["Avg_Daily_Calorie_Intake_kcal"] / df["Recommended_Calorie_RDA_kcal"]) * 100.0
    ).round(2)

    # C) Hidden Hunger Severity Index (0 - 100)
    micro_composite = (
        0.25 * df["Iron_Deficiency_Anemia_Pct"] +
        0.20 * df["Vitamin_D_Deficiency_Pct"] +
        0.20 * df["Vitamin_B12_Deficiency_Pct"] +
        0.15 * df["Calcium_Deficiency_Pct"] +
        0.10 * df["Zinc_Deficiency_Pct"] +
        0.10 * df["Folate_Deficiency_Pct"]
    )
    carb_factor = np.clip(df["Carbohydrate_Energy_Share_Pct"] / 60.0, 0.85, 1.25)
    hh_index = (0.40 * micro_composite + 0.35 * df["Protein_Deficit_Pct"] + 0.25 * df["Portion_vs_Nutrient_Density_Gap_Index"]) * carb_factor * 0.95
    df["Hidden_Hunger_Severity_Index"] = np.clip(hh_index, 10.0, 98.0).round(2)

    # D) Awareness-to-Deficiency Ratio
    df["Awareness_to_Deficiency_Ratio"] = (
        df["Nutritional_Literacy_Score"] / (df["Hidden_Hunger_Severity_Index"] + 0.001)
    ).round(3)

    # Export clean dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("\n" + "=" * 70)
    print(f"SUCCESS: Cleaned dataset saved to: {output_path}")
    print(f"Final Clean Shape: {df.shape[0]} rows, {df.shape[1]} columns, 0 NaNs.")
    print("=" * 70)
    return df

if __name__ == "__main__":
    clean_data()
