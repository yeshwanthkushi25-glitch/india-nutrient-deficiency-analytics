# Nutrient Deficiency & The Hidden Hunger Paradox in India
### Why High Caloric Intake Still Leads to Severe Macronutrient and Micronutrient Deficiencies Due to Lack of Nutritional Awareness

[![Public Health Standards](https://img.shields.io/badge/Standards-ICMR--NIN%202024%20%7C%20NFHS--5-blue.svg)](https://nin.res.in/)
[![Power BI Ready](https://img.shields.io/badge/Data%20Model-Star%20Schema%20(Power%20BI)-F2C811.svg)](#power-bi-star-schema--modeling)
[![Interactive Dashboard](https://img.shields.io/badge/Live%20Dashboard-GitHub%20Pages-10b981.svg)](#interactive-web-application)
[![Coverage](https://img.shields.io/badge/Geography-28%20States%20%2B%208%20UTs-darkgreen.svg)](#geographical--demographic-coverage)

---

## 📌 Executive Summary & Problem Statement

In contemporary India, millions of citizens achieve or exceed daily caloric energy needs (kcal) through diets saturated with polished white rice, refined wheat atta, added sugars, and hydrogenated fats. However, they remain in a state of **chronic cellular starvation** for bioavailable protein, iron, vitamin B12, vitamin D3, calcium, zinc, and folate. This phenomenon is known clinically as **"The Hidden Hunger Paradox"** (or *The Double Burden of Malnutrition*).

### Key Clinical & National Health Findings:
- **Caloric Sufficiency vs. Protein Gap:** While the national average daily caloric fulfillment stands at **102.4% of RDA**, over **74.6% of the population fails to achieve the ICMR-NIN recommended dietary protein allowance** (0.83 g/kg/day), consuming on average only ~36.8g/day against a 54g/day reference target.
- **Carbohydrate Saturation:** The average Indian diet derives **70.8% of daily energy from refined carbohydrates**, far exceeding the ICMR-NIN 2024 recommended ceiling of 45%–55%.
- **Micronutrient Deficiencies:**
  - **Iron-Deficiency Anemia:** 57.0% overall (peaking at 67.1% in children 6–59 months and 57.0% in women 15–49 years).
  - **Vitamin D3 Deficiency:** 76.8% prevalence due to indoor lifestyles, high melanin, and negligible dietary fortification.
  - **Vitamin B12 Deficiency:** 62.4% nationwide, escalating to 75%+ in strict vegetarian populations lacking dietary awareness or supplementation.
  - **Calcium Inadequacy:** 68.2% of diets fail the 1000 mg/day RDA benchmark (actual intake ~380–450 mg/day).
- **The Awareness Disconnect:** States and cohorts with lower nutritional literacy scores (<40/100) exhibit 30%–45% higher Hidden Hunger Severity Indices, driven by the misconception that *"feeling full from rice/roti equals proper nourishment"*.

---

## 🏛️ Grounding Standards & Public Health Sources

This project models and benchmarks data using authoritative epidemiological and dietary datasets:
1. **ICMR-National Institute of Nutrition (ICMR-NIN) 2024:** *Dietary Guidelines for Indians (DGI)*. Established reference RDA values (54g protein for 65kg male, 46g for 55kg female, 1000mg calcium, 19mg/29mg iron).
2. **NFHS-5 (2019–2021):** *National Family Health Survey*, International Institute for Population Sciences (IIPS) & MoHFW. Authoritative state-level benchmarks for anemia, stunting, wasting, and adult overweight rates.
3. **CNNS (2016–2018):** *Comprehensive National Nutrition Survey*, UNICEF and Ministry of Health and Family Welfare. Biochemical micronutrient assessment data.

---

## 🏗️ Project Architecture & Star Schema Model

The dataset is organized as a production-grade **Star Schema** designed for zero-lag filtering in **Microsoft Power BI Desktop** and web applications.

```
                  +---------------------------+
                  |       Dim_Geography       |
                  +---------------------------+
                  | PK: State_Key             |
                  |     State_Name            |
                  |     Region_Zone           |
                  |     Geographic_Type       |
                  |     Latitude / Longitude  |
                  |     Population_Cr         |
                  +---------------------------+
                                | (1)
                                |
                                | (∞)
  +-----------------------------+-----------------------------+
  |                   Fact_State_Nutrition                    |
  +-----------------------------------------------------------+
  | PK: Fact_ID                                               |
  | FK: State_Key (State_ISO)                                 |
  | FK: Cohort_Key                                            |
  |     Area (Urban / Rural)                                  |
  |     Dietary_Pattern (Veg / Egg / Non-Veg)                 |
  |     Avg_Daily_Calorie_Intake_kcal                         |
  |     Recommended_Calorie_RDA_kcal                          |
  |     Caloric_Sufficiency_Pct                               |
  |     Carbohydrate_Energy_Share_Pct                         |
  |     Daily_Protein_Intake_g                                |
  |     Recommended_Protein_RDA_g                             |
  |     Protein_Deficit_Pct                                   |
  |     Iron_Deficiency_Anemia_Pct                            |
  |     Vitamin_D_Deficiency_Pct                              |
  |     Vitamin_B12_Deficiency_Pct                            |
  |     Calcium_Deficiency_Pct                                |
  |     Zinc_Deficiency_Pct                                   |
  |     Nutritional_Literacy_Score                            |
  |     Hidden_Hunger_Severity_Index                          |
  |     Double_Burden_Malnutrition_Pct                        |
  +-----------------------------------------------------------+
            | (∞)                                     |
            |                                         | (Analytical Ref)
            | (1)                                     v
  +-------------------------------+       +-------------------------+
  |   Dim_Age_Awareness_Cohort    |       |    Dim_Nutrient_RDA     |
  +-------------------------------+       +-------------------------+
  | PK: Cohort_Key                |       | PK: Nutrient_ID         |
  |     Age_Group                 |       |     Nutrient_Name       |
  |     Gender                    |       |     ICMR_RDA_Adult_Male |
  |     Awareness_Tier            |       |     ICMR_RDA_Adult_Fem  |
  |     Life_Stage_Description    |       |     Physiological_Role  |
  |     Intervention_Priority     |       |     Indian_Food_Sources |
  +-------------------------------+       +-------------------------+
```

---

## 🧹 Demonstrable Data Cleaning & ETL Pipeline

To showcase real-world data engineering for academic review, the raw generator injects intentional real-world artifacts into the `Raw_Data_Log` sheet:
- **Dirty State Names:** Standardized `"Orissa"` ➔ `"Odisha"`, `"Pondicherry"` ➔ `"Puducherry"`, `"Uttaranchal"` ➔ `"Uttarakhand"`, and stripped erratic whitespace/case variants (`"bihar"`, `"GUJARAT "`).
- **Deduplication:** Identified and eliminated **162 exact duplicate rows** (from 6,642 raw rows to 6,480 clean rows).
- **Missing Value Imputation:** Imputed missing values across `Nutritional_Literacy_Score`, `Dietary_Fiber_Intake_g`, and `Portion_vs_Nutrient_Density_Gap_Index` using demographic stratum medians.
- **Engineered Analytical Features:**
  - `Protein_Deficit_Pct`: Percentage shortfall against ICMR-NIN RDA.
  - `Caloric_Sufficiency_Pct`: Actual caloric intake as a ratio of physiological requirement.
  - `Hidden_Hunger_Severity_Index`: Composite clinical index combining high caloric sufficiency with micronutrient (Iron, D, B12, Calcium, Zinc) and protein deficits.
  - `Awareness_to_Deficiency_Ratio`: `Literacy_Score / (Hidden_Hunger_Severity_Index + 0.001)`.

The final cleaned fact dataset has **6,480 rows, 33 columns, and zero NaN errors**.

---

## 📊 Power BI Implementation & DAX Measures

The dataset includes a dedicated [POWERBI_GUIDE.md](POWERBI_GUIDE.md) documenting table relationships, data categorization, and **12 production DAX measures**:

```dax
// National Protein Deficit Rate
Avg Protein Deficit % = AVERAGE(Fact_State_Nutrition[Protein_Deficit_Pct])

// Hidden Hunger Severity Index
Hidden Hunger Severity Index = AVERAGE(Fact_State_Nutrition[Hidden_Hunger_Severity_Index])

// Caloric Sufficiency %
Avg Caloric Sufficiency % = AVERAGE(Fact_State_Nutrition[Caloric_Sufficiency_Pct])

// Carbohydrate Energy Share %
Carbohydrate Energy Share % = AVERAGE(Fact_State_Nutrition[Carbohydrate_Energy_Share_Pct])

// Severity Alert Badge
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

## 🌐 Interactive Web Application Features

The repository includes a modern, zero-dependency, responsive single-page web application (`index.html`, `styles.css`, `app.js`):
1. **Executive KPI Dashboard:** Real-time summary cards displaying national protein gaps, calorie sufficiency, anemia prevalence, and awareness metrics.
2. **Interactive India Choropleth (Leaflet.js):** Color-swappable geospatial heatmap covering all 28 States & 8 UTs (toggle between Protein Deficit, Anemia, Vit B12, Vit D, Calcium, Hidden Hunger, and Literacy Score).
3. **State Nutritional Scorecard Panel:** Dynamic side panel updated by map clicks, showing urban vs. rural splits, calorie vs. protein gaps, and localized dietary advice.
4. **"Check Your Plate" Body-Needs Calculator:** Users input their age, gender, physical activity, and daily Indian food servings (rotis, rice bowls, dal, dairy, paneer, eggs, greens, tea after meals) to receive real-time calorie vs. nutrient fulfillment percentages and affordable kitchen swaps (sattu, lemon on dal, delayed tea, roasted chana).
5. **Multi-Nutrient Heatmap Matrix Table:** Sortable and searchable data table covering all 36 Indian territories.
6. **Download Center:** Direct download buttons for the multi-tab `.xlsx` workbook, CSV tables, and Power BI guide.

---

## 📁 Repository File Structure

```
├── data/
│   ├── india_nutrient_deficiency_analytics.xlsx  # Master 6-tab formatted workbook (1.99 MB)
│   ├── india_nutrition_data.json                 # Pre-aggregated web API dataset
│   ├── india_nutrition_data.js                   # Pre-bundled JS data bundle
│   ├── india_states.geojson                      # GeoJSON boundary file (36 States & UTs)
│   ├── india_states_geojson.js                   # Pre-bundled GeoJSON bundle
│   └── powerbi_exports/                          # Power BI Star Schema CSVs
│       ├── Fact_State_Nutrition.csv
│       ├── Dim_Geography.csv
│       ├── Dim_Nutrient_RDA.csv
│       ├── Dim_Age_Awareness_Cohort.csv
│       └── Executive_KPI_Summary.csv
├── scripts/
│   ├── build_nutrition_dataset.py                # Raw generator & dirty log creator
│   └── clean_and_prepare_powerbi.py              # ETL cleaning & Star Schema modeling
├── POWERBI_GUIDE.md                              # Complete DAX catalog & setup manual
├── index.html                                    # Web analytics frontend
├── styles.css                                    # Responsive styling & themes
├── app.js                                        # Application state, map & chart engine
└── README.md                                     # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Run Data Pipelines Locally
```bash
# Install dependencies
python -m pip install pandas openpyxl

# Generate raw and clean datasets
python scripts/clean_and_prepare_powerbi.py
```

### 2. Launch Local Web Application
```bash
# Launch preview server
python -m http.server 8080

# Open in browser:
# http://localhost:8080
```

### 3. Open in Power BI Desktop
1. Open **Power BI Desktop**.
2. Select **Get Data** > **Folder** or **Excel** pointing to `data/powerbi_exports/` or `data/india_nutrient_deficiency_analytics.xlsx`.
3. Follow the relationship setup and DAX formulas in [POWERBI_GUIDE.md](POWERBI_GUIDE.md).

---

## 📜 Citations & Academic References
- Indian Council of Medical Research - National Institute of Nutrition (ICMR-NIN). *Dietary Guidelines for Indians (DGI) - 2024*. Hyderabad, India.
- International Institute for Population Sciences (IIPS) and ICF. *National Family Health Survey (NFHS-5), 2019-21: India*. Mumbai: IIPS.
- Ministry of Health and Family Welfare (MoHFW), Government of India, and UNICEF. *Comprehensive National Nutrition Survey (CNNS) National Report 2016-2018*. New Delhi.
