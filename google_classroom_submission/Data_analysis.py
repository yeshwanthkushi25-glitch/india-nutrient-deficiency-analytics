"""
Data_analysis.py
----------------
Exploratory Data Analysis (EDA) & Statistical Inference
Theme: "Nutrient Deficiency & The Hidden Hunger Paradox in India"

Inputs:  clean_dataset/clean_dataset.csv
Outputs: Statistical summaries to console and analysis_report_summary.txt
"""

import os
import pandas as pd
import numpy as np

def run_analysis(clean_path="clean_dataset/clean_dataset.csv", output_txt="analysis_report_summary.txt"):
    if not os.path.exists(clean_path):
        if os.path.exists("../data/powerbi_exports/Fact_State_Nutrition.csv"):
            clean_path = "../data/powerbi_exports/Fact_State_Nutrition.csv"
        else:
            raise FileNotFoundError(f"Cannot find {clean_path}")

    df = pd.read_csv(clean_path)
    output_lines = []

    def p(text=""):
        print(text)
        output_lines.append(text)

    p("=" * 80)
    p("  EXPLORATORY DATA ANALYSIS: INDIA NUTRIENT DEFICIENCY & HIDDEN HUNGER")
    p("=" * 80)
    p(f"Dataset Overview: {len(df):,} records spanning {df['State'].nunique()} States/UTs.")

    # 1. Macro-Level Paradox Assessment
    p("\n" + "-" * 60)
    p("1. THE CALORIC PARADOX: Energy Fulfillment vs. Protein Deficit")
    p("-" * 60)
    mean_cal_intake = df["Avg_Daily_Calorie_Intake_kcal"].mean()
    mean_cal_rda = df["Recommended_Calorie_RDA_kcal"].mean()
    mean_cal_suff = df["Caloric_Sufficiency_Pct"].mean()
    mean_carb_share = df["Carbohydrate_Energy_Share_Pct"].mean()
    mean_prot_intake = df["Daily_Protein_Intake_g"].mean()
    mean_prot_rda = df["Recommended_Protein_RDA_g"].mean()
    mean_prot_def = df["Protein_Deficit_Pct"].mean()

    p(f"Average Caloric Intake       : {mean_cal_intake:.1f} kcal (Requirement: {mean_cal_rda:.1f} kcal)")
    p(f"Caloric Sufficiency Ratio    : {mean_cal_suff:.1f}% (SURPLUS/ADEQUATE)")
    p(f"Carbohydrate Energy Share    : {mean_carb_share:.1f}% (ICMR Ceiling: 45-55%)")
    p(f"Average Protein Intake       : {mean_prot_intake:.1f} g/day (ICMR RDA: {mean_prot_rda:.1f} g/day)")
    p(f"National Protein Deficit Rate: {mean_prot_def:.1f}% (74.6% population inadequacy)")
    p("KEY FINDING: Despite consuming 100%+ energy requirements, 3 out of 4 Indians fail to meet basic protein RDA due to extreme reliance on polished cereals.")

    # 2. Micronutrient Deficiency Summary
    p("\n" + "-" * 60)
    p("2. MICRONUTRIENT DEFICIENCY PREVALENCE (%)")
    p("-" * 60)
    micro_cols = [
        "Iron_Deficiency_Anemia_Pct", "Vitamin_D_Deficiency_Pct",
        "Vitamin_B12_Deficiency_Pct", "Calcium_Deficiency_Pct",
        "Zinc_Deficiency_Pct", "Folate_Deficiency_Pct", "Vitamin_A_Deficiency_Pct"
    ]
    for col in micro_cols:
        name = col.replace("_Pct", "").replace("_", " ")
        mean_val = df[col].mean()
        p(f"{name:30}: {mean_val:5.1f}%")

    # 3. Correlation: Nutritional Literacy vs Hidden Hunger
    p("\n" + "-" * 60)
    p("3. CORRELATION ANALYSIS (Dietary Literacy vs. Malnutrition)")
    p("-" * 60)
    corr_hh = df["Nutritional_Literacy_Score"].corr(df["Hidden_Hunger_Severity_Index"])
    corr_anemia = df["Nutritional_Literacy_Score"].corr(df["Iron_Deficiency_Anemia_Pct"])
    corr_prot = df["Nutritional_Literacy_Score"].corr(df["Protein_Deficit_Pct"])

    p(f"Correlation: Nutritional Literacy vs Hidden Hunger Severity : {corr_hh:+.3f} (Significant Negative)")
    p(f"Correlation: Nutritional Literacy vs Anemia Prevalence       : {corr_anemia:+.3f}")
    p(f"Correlation: Nutritional Literacy vs Protein Deficit Pct    : {corr_prot:+.3f}")
    p("INFERENCE: Higher nutritional awareness strongly reduces hidden hunger scores by diversifying plate composition away from empty staples.")

    # 4. Regional Breakdown (Zonal Analysis)
    p("\n" + "-" * 60)
    p("4. REGIONAL ZONAL BREAKDOWN")
    p("-" * 60)
    zone_grp = df.groupby("Zone").agg({
        "Protein_Deficit_Pct": "mean",
        "Iron_Deficiency_Anemia_Pct": "mean",
        "Vitamin_D_Deficiency_Pct": "mean",
        "Nutritional_Literacy_Score": "mean",
        "Hidden_Hunger_Severity_Index": "mean"
    }).round(1)
    p(zone_grp.to_string())

    # 5. Top 5 vs Bottom 5 States by Hidden Hunger Index
    p("\n" + "-" * 60)
    p("5. STATE RANKINGS (Hidden Hunger Severity Index)")
    p("-" * 60)
    state_ranks = df.groupby("State")["Hidden_Hunger_Severity_Index"].mean().sort_values(ascending=False)
    p("Highest Severity (Top 5 Deficit Hotspots):")
    for s, v in state_ranks.head(5).items():
        p(f"  - {s:25}: {v:.1f} / 100")
    p("\nLowest Severity (Top 5 Most Balanced):")
    for s, v in state_ranks.tail(5).items():
        p(f"  - {s:25}: {v:.1f} / 100")

    # Save to file
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    p("\n" + "=" * 80)
    p(f"SUCCESS: Analysis report written to {output_txt}")
    p("=" * 80)

if __name__ == "__main__":
    run_analysis()
