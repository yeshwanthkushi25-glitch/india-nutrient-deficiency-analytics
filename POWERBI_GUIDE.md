# Power BI Data Modeling & Implementation Guide
## Project: Nutrient Deficiency & The Hidden Hunger Paradox in India

This guide provides step-by-step instructions for importing, modeling, and visualizing the dataset in **Microsoft Power BI Desktop**.

---

## 1. Data Architecture: Star Schema

The dataset is structured as a normalized **Star Schema** with one centralized Fact table and three Dimension tables, plus an aggregated Executive KPI table.

```
       +-------------------------+
       |      Dim_Geography      |
       +-------------------------+
       | PK: State_Key           |
       |     State_Name          |
       |     Region_Zone         |
       |     Geographic_Type     |
       |     Latitude / Longitude|
       |     Population_Cr       |
       +-------------------------+
                    | (1)
                    |
                    | (∞)
       +------------------------------------+          +------------------------------+
       |        Fact_State_Nutrition        |  (∞)     |   Dim_Age_Awareness_Cohort   |
       +------------------------------------+----------+------------------------------+
       | PK: Fact_ID                        |      (1) | PK: Cohort_Key               |
       | FK: State_Key (State_ISO)          |          |     Age_Group                |
       | FK: Cohort_Key                     |          |     Gender                   |
       |     Area (Urban/Rural)             |          |     Awareness_Tier           |
       |     Dietary_Pattern                |          |     Life_Stage_Description   |
       |     Calorie Intake / RDA           |          |     Dietary_Literacy_Level   |
       |     Carbohydrate Share %           |          |     Intervention_Priority    |
       |     Protein Intake / RDA           |          +------------------------------+
       |     Protein_Deficit_Pct            |
       |     Caloric_Sufficiency_Pct        |
       |     Anemia / Vit D / B12 / Zinc %  |
       |     Nutritional_Literacy_Score     |
       |     Hidden_Hunger_Severity_Index   |
       +------------------------------------+
                    |
                    | (Analytical reference)
                    v
       +-------------------------+
       |     Dim_Nutrient_RDA    |
       +-------------------------+
       | PK: Nutrient_ID         |
       |     Nutrient_Name       |
       |     ICMR_NIN_2024_RDA   |
       |     Physiological_Role  |
       |     Indian_Food_Sources |
       +-------------------------+
```

---

## 2. Table Relationships Setup in Power BI

Navigate to **Model View** in Power BI Desktop and create the following relationships:

| From Table (`*` Many) | Foreign Key Column | To Table (`1` One) | Primary Key Column | Cardinality | Cross filter direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Fact_State_Nutrition` | `State_Key` | `Dim_Geography` | `State_Key` | Many to One (`*:1`) | Single |
| `Fact_State_Nutrition` | `Cohort_Key` | `Dim_Age_Awareness_Cohort` | `Cohort_Key` | Many to One (`*:1`) | Single |

> **Geocoding Tip**: Select `Dim_Geography[Latitude]` and set **Data Category** to `Latitude`. Select `Dim_Geography[Longitude]` and set **Data Category** to `Longitude`. Select `Dim_Geography[State_Name]` and set **Data Category** to `State or Province`.

---

## 3. Core DAX Measures Catalog

Create a dedicated measure table in Power BI (`_Measures`) and add the following DAX calculations:

### 1. Caloric Sufficiency Ratio (%)
```dax
Avg Caloric Sufficiency % = 
AVERAGE(Fact_State_Nutrition[Caloric_Sufficiency_Pct])
```

### 2. National Protein Deficit (%)
```dax
Avg Protein Deficit % = 
AVERAGE(Fact_State_Nutrition[Protein_Deficit_Pct])
```

### 3. Protein Intake vs RDA Gap (grams)
```dax
Daily Protein Gap (g) = 
AVERAGE(Fact_State_Nutrition[Recommended_Protein_RDA_g]) - AVERAGE(Fact_State_Nutrition[Daily_Protein_Intake_g])
```

### 4. Carbohydrate Share of Energy (%)
```dax
Carbohydrate Energy Share % = 
AVERAGE(Fact_State_Nutrition[Carbohydrate_Energy_Share_Pct])
```

### 5. Anemia Prevalence (%)
```dax
Iron Deficiency Anemia % = 
AVERAGE(Fact_State_Nutrition[Iron_Deficiency_Anemia_Pct])
```

### 6. Vitamin D Deficiency (%)
```dax
Vitamin D Deficiency % = 
AVERAGE(Fact_State_Nutrition[Vitamin_D_Deficiency_Pct])
```

### 7. Vitamin B12 Deficiency (%)
```dax
Vitamin B12 Deficiency % = 
AVERAGE(Fact_State_Nutrition[Vitamin_B12_Deficiency_Pct])
```

### 8. Hidden Hunger Severity Index (0-100)
```dax
Hidden Hunger Severity Index = 
AVERAGE(Fact_State_Nutrition[Hidden_Hunger_Severity_Index])
```

### 9. Nutritional Literacy Score (0-100)
```dax
Nutritional Literacy Score = 
AVERAGE(Fact_State_Nutrition[Nutritional_Literacy_Score])
```

### 10. Awareness-to-Deficiency Ratio
```dax
Awareness to Deficiency Ratio = 
DIVIDE([Nutritional Literacy Score], [Hidden Hunger Severity Index], 0)
```

### 11. Double Burden of Malnutrition (%)
```dax
Double Burden Malnutrition % = 
AVERAGE(Fact_State_Nutrition[Overweight_Obese_Coexisting_Deficiency_Pct])
```

### 12. Dynamic Severity Alert Status
```dax
Severity Alert Badge = 
SWITCH(
    TRUE(),
    [Hidden Hunger Severity Index] >= 75, "🚨 Critical Hidden Hunger",
    [Hidden Hunger Severity Index] >= 60, "⚠️ Severe Nutritional Deficit",
    [Hidden Hunger Severity Index] >= 45, "⚡ Moderate Nutrient Gap",
    "✅ Acceptable Nutritional Balance"
)
```

---

## 4. Suggested Dashboard Page Layouts

### Page 1: Executive Overview & The Paradox KPI Deck
- **Top Row (KPI Cards)**:
  - Card 1: `Avg Caloric Sufficiency %` (e.g., 102.4% — Shows adequate/excess energy intake)
  - Card 2: `Avg Protein Deficit %` (e.g., 74.6% — Reveals dramatic protein deficit)
  - Card 3: `Carbohydrate Energy Share %` (e.g., 70.8% — Illustrates cereal-heavy reliance)
  - Card 4: `Hidden Hunger Severity Index` (e.g., 68.2 / 100)
  - Card 5: `Double Burden Malnutrition %` (e.g., 31.8% — Obesity co-existing with micronutrient starvation)
- **Visual 1 (Choropleth Map / Filled Map)**:
  - Location: `Dim_Geography[State_Name]`
  - Tooltips: `Avg Protein Deficit %`, `Iron Deficiency Anemia %`, `Nutritional Literacy Score`
  - Color saturation gradient: Soft Green (low deficiency) to Deep Crimson (critical deficiency).
- **Visual 2 (Grouped Bar Chart - The Paradox Visual)**:
  - X-Axis: `Dim_Age_Awareness_Cohort[Age_Group]`
  - Values: `Avg Caloric Sufficiency %` vs `Avg Protein Deficit %`

### Page 2: Micronutrient Deficiency Deep-Dive
- **Visual 1 (Matrix Heatmap)**:
  - Rows: `Dim_Geography[Region_Zone]`, `Dim_Geography[State_Name]`
  - Values: `Iron Deficiency Anemia %`, `Vitamin D Deficiency %`, `Vitamin B12 Deficiency %`, `Calcium Deficiency %`, `Zinc Deficiency %`
  - Conditional formatting: Color scale background highlighting deficiency hotspots.
- **Visual 2 (Scatter Plot - Awareness vs Deficiency Correlation)**:
  - X-Axis: `Nutritional Literacy Score`
  - Y-Axis: `Hidden Hunger Severity Index`
  - Bubble Size: `Dim_Geography[Estimated_Population_2021_Cr]`
  - Legend: `Dim_Geography[Region_Zone]`
  - Trend line: Demonstrates strong negative correlation (higher dietary awareness directly suppresses hidden hunger).

### Page 3: Demographic & Dietary Pattern Segmentation
- **Visual 1 (Clustered Column Chart)**:
  - Axis: `Fact_State_Nutrition[Dietary_Pattern]` (Vegetarian, Eggetarian, Non-Vegetarian)
  - Values: `Vitamin B12 Deficiency %`, `Avg Protein Deficit %`
- **Visual 2 (Tornado / Dual Bar Chart)**:
  - Axis: `Fact_State_Nutrition[Area]` (Urban vs. Rural)
  - Values: `Double Burden Malnutrition %` vs `Staple Heavy Diet Reliance %`

---

## 5. One-Click Quick Import Instructions
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Excel Workbook** (select `data/india_nutrient_deficiency_analytics.xlsx`) OR **Folder / Text/CSV** (point to `data/powerbi_exports/`).
3. Select the 4 core tables:
   - `Fact_State_Nutrition`
   - `Dim_Geography`
   - `Dim_Nutrient_RDA`
   - `Dim_Age_Awareness_Cohort`
4. Confirm relationships match Section 2 above.
5. Create DAX measures from Section 3.
