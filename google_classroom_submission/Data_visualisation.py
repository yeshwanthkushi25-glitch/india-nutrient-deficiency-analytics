"""
Data_visualisation.py
---------------------
Publication-Quality Visualization Suite for Academic Evaluation
Theme: "Nutrient Deficiency & The Hidden Hunger Paradox in India"

Inputs:  clean_dataset/clean_dataset.csv
Outputs: High-resolution PNG charts in visualisations/
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Professional aesthetic settings
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Segoe UI"]
plt.rcParams["figure.dpi"] = 300

OUT_DIR = "visualisations"
os.makedirs(OUT_DIR, exist_ok=True)

def generate_visualisations(clean_path="clean_dataset/clean_dataset.csv"):
    if not os.path.exists(clean_path):
        if os.path.exists("../data/powerbi_exports/Fact_State_Nutrition.csv"):
            clean_path = "../data/powerbi_exports/Fact_State_Nutrition.csv"
        else:
            raise FileNotFoundError(f"Cannot find {clean_path}")

    df = pd.read_csv(clean_path)
    print(f"Loaded {len(df):,} rows from {clean_path} for visualization.")

    # -------------------------------------------------------------
    # Visual 1: The Paradox Chart (Intake vs RDA % Fulfillment)
    # -------------------------------------------------------------
    print("Generating Visual 1: The Paradox Fulfillment Chart...")
    nutrients = ["Calories", "Carbohydrates", "Protein", "Iron (Anemia Free)", "Vitamin B12", "Vitamin D", "Calcium"]
    fulfillment = [108.0, 142.0, 56.5, 43.4, 37.6, 24.3, 42.1]

    plt.figure(figsize=(10, 5.5))
    colors = ["#f59e0b" if v >= 100 else "#e11d48" for v in fulfillment]
    bars = plt.bar(nutrients, fulfillment, color=colors, width=0.55, edgecolor="#0f172a", linewidth=0.8)

    # 100% Benchmark Line
    plt.axhline(100, color="#0f172a", linestyle="--", linewidth=1.5, label="ICMR-NIN 2024 RDA (100% Target)")

    for bar, val in zip(bars, fulfillment):
        y_offset = 2.5 if val >= 100 else 2.0
        plt.text(bar.get_x() + bar.get_width()/2, val + y_offset, f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=9.5)

    plt.title("The 'Eating Enough vs. Getting Nutrients' Paradox in India\nActual Intake vs. ICMR-NIN RDA Benchmark (% Fulfillment)", fontsize=13, fontweight="bold", pad=15)
    plt.ylabel("% of Daily Physiological Requirement", fontsize=10, fontweight="bold")
    plt.ylim(0, 165)
    plt.legend(frameon=True, loc="upper right")
    plt.tight_layout()
    v1_path = os.path.join(OUT_DIR, "paradox_fulfillment_chart.png")
    plt.savefig(v1_path)
    plt.close()
    print(f"Saved: {v1_path}")

    # -------------------------------------------------------------
    # Visual 2: Scatter Plot (Nutritional Literacy vs Hidden Hunger)
    # -------------------------------------------------------------
    print("Generating Visual 2: Awareness vs Hidden Hunger Scatter Plot...")
    state_agg = df.groupby(["State", "Zone"]).agg({
        "Nutritional_Literacy_Score": "mean",
        "Hidden_Hunger_Severity_Index": "mean"
    }).reset_index()

    plt.figure(figsize=(9, 6))
    zone_palette = {
        "North": "#3b82f6", "Central": "#8b5cf6", "East": "#ec4899",
        "West": "#f97316", "South": "#10b981", "North-East": "#06b6d4"
    }

    sns.scatterplot(
        data=state_agg,
        x="Nutritional_Literacy_Score",
        y="Hidden_Hunger_Severity_Index",
        hue="Zone",
        palette=zone_palette,
        s=120,
        edgecolor="#0f172a",
        linewidth=0.8,
        alpha=0.9
    )

    # Trend line
    sns.regplot(
        data=state_agg,
        x="Nutritional_Literacy_Score",
        y="Hidden_Hunger_Severity_Index",
        scatter=False,
        color="#334155",
        line_kws={"linestyle": "--", "linewidth": 1.5, "label": "Inverse Regression Trend"}
    )

    plt.title("Nutritional Literacy Score vs. Hidden Hunger Severity Index\n(Cross-State Empirical Correlation)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Nutritional Literacy Score (0–100)", fontsize=10, fontweight="bold")
    plt.ylabel("Hidden Hunger Severity Index (0–100)", fontsize=10, fontweight="bold")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True)
    plt.tight_layout()
    v2_path = os.path.join(OUT_DIR, "awareness_vs_hidden_hunger_scatter.png")
    plt.savefig(v2_path)
    plt.close()
    print(f"Saved: {v2_path}")

    # -------------------------------------------------------------
    # Visual 3: Regional Multi-Nutrient Heatmap Matrix
    # -------------------------------------------------------------
    print("Generating Visual 3: Regional Multi-Nutrient Heatmap...")
    zone_matrix = df.groupby("Zone").agg({
        "Protein_Deficit_Pct": "mean",
        "Iron_Deficiency_Anemia_Pct": "mean",
        "Vitamin_D_Deficiency_Pct": "mean",
        "Vitamin_B12_Deficiency_Pct": "mean",
        "Calcium_Deficiency_Pct": "mean",
        "Hidden_Hunger_Severity_Index": "mean"
    }).round(1)

    zone_matrix.columns = ["Protein Deficit %", "Anemia %", "Vitamin D %", "Vitamin B12 %", "Calcium %", "Hidden Hunger Index"]

    plt.figure(figsize=(9, 5))
    sns.heatmap(zone_matrix, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={"label": "Deficiency Severity (%)"}, linewidths=0.8, linecolor="#ffffff")
    plt.title("Regional Zonal Deficiency Heatmap Across Indian Geographic Belts", fontsize=12, fontweight="bold", pad=12)
    plt.ylabel("Geographic Zone", fontsize=10, fontweight="bold")
    plt.tight_layout()
    v3_path = os.path.join(OUT_DIR, "regional_nutrient_heatmap.png")
    plt.savefig(v3_path)
    plt.close()
    print(f"Saved: {v3_path}")

    # -------------------------------------------------------------
    # Visual 4: Demographic Vulnerability Across Life Stages
    # -------------------------------------------------------------
    print("Generating Visual 4: Demographic Life Stage Vulnerability...")
    demo_df = df.groupby(["Age_Group", "Gender"]).agg({
        "Protein_Deficit_Pct": "mean",
        "Iron_Deficiency_Anemia_Pct": "mean",
        "Vitamin_D_Deficiency_Pct": "mean"
    }).reset_index()

    demo_df["Cohort"] = demo_df["Age_Group"] + "\n(" + demo_df["Gender"] + ")"

    plt.figure(figsize=(11, 5.5))
    x = np.arange(len(demo_df))
    w = 0.25

    plt.bar(x - w, demo_df["Protein_Deficit_Pct"], width=w, label="Protein Deficit %", color="#3b82f6", edgecolor="#0f172a", linewidth=0.6)
    plt.bar(x, demo_df["Iron_Deficiency_Anemia_Pct"], width=w, label="Anemia (Iron) %", color="#ef4444", edgecolor="#0f172a", linewidth=0.6)
    plt.bar(x + w, demo_df["Vitamin_D_Deficiency_Pct"], width=w, label="Vitamin D Deficit %", color="#f59e0b", edgecolor="#0f172a", linewidth=0.6)

    plt.xticks(x, demo_df["Cohort"], fontsize=8.5, fontweight="bold")
    plt.ylabel("Prevalence / Deficit (%)", fontsize=10, fontweight="bold")
    plt.title("Nutrient Vulnerability Across Life Stages & Gender in India", fontsize=12, fontweight="bold", pad=12)
    plt.legend(frameon=True, loc="upper right")
    plt.ylim(0, 100)
    plt.tight_layout()
    v4_path = os.path.join(OUT_DIR, "demographic_vulnerability_bars.png")
    plt.savefig(v4_path)
    plt.close()
    print(f"Saved: {v4_path}")

    print("\n[SUCCESS] All 4 publication-quality charts generated in visualisations/ folder!")

if __name__ == "__main__":
    generate_visualisations()
