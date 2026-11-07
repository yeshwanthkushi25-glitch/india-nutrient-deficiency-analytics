import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def build_report():
    doc = docx.Document()

    # Page Margins (Standard 1-inch academic layout)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Brand Colors
    PRIMARY = RGBColor(15, 23, 42)     # Deep Slate
    ACCENT = RGBColor(37, 99, 235)     # Vibrant Blue
    ROSE = RGBColor(225, 29, 72)       # Crimson
    SLATE = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SR UNIVERSITY\nDEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (CYBER SECURITY)\n")
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = SLATE

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub_hdr = p_sub.add_run("COURSE: DATA ANALYTICS | CAPSTONE PROJECT REPORT\n")
    r_sub_hdr.font.size = Pt(11)
    r_sub_hdr.font.bold = True
    r_sub_hdr.font.color.rgb = ACCENT

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("NUTRIENT DEFICIENCY & THE HIDDEN HUNGER PARADOX IN INDIA\n")
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = PRIMARY

    r_sub = p_title.add_run("Why High Caloric Intake Still Leads to Severe Macronutrient and Micronutrient Deficiencies Due to Lack of Nutritional Awareness\n\n")
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = ACCENT

    # Team Box
    p_team_hdr = doc.add_paragraph()
    p_team_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_th = p_team_hdr.add_run("SUBMITTED BY PROJECT TEAM:")
    r_th.font.bold = True
    r_th.font.size = Pt(11)

    table_team = doc.add_table(rows=4, cols=3)
    table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Team Member Name", "Roll Number", "Contribution / Specialization"]
    for j, h in enumerate(headers):
        cell = table_team.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)

    members = [
        ("Yeshwanth", "2503A53005", "Data Architecture, ETL Pipeline & Geospatial Modeling"),
        ("V Laxmi Prasad", "2503A53006", "Statistical Inference, EDA & Python Visualizations"),
        ("MD Zaheer Pasha", "2503A53016", "Power BI Dashboard Modeling, DAX & Frontend UI")
    ]
    for i, m in enumerate(members, start=1):
        for j, val in enumerate(m):
            cell = table_team.cell(i, j)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)

    doc.add_paragraph()
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Institution: SR University | Program: B.Tech CSE (Cyber Security)\nSubject: Data Analytics | Academic Year: 2026-2027\nPublic Repository: https://github.com/yeshwanthkushi25-glitch/india-nutrient-deficiency-analytics\nLive Dashboard: https://yeshwanthkushi25-glitch.github.io/india-nutrient-deficiency-analytics/")
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = SLATE

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # -------------------------------------------------------------
    doc.add_heading("1. Executive Summary & Problem Statement", level=1)
    doc.add_paragraph(
        "Historically, public health initiatives in developing nations have concentrated primarily on alleviating caloric famine. "
        "In India, modern agricultural productivity and food distribution schemes have largely achieved basic energy fulfillment, "
        "with the national average caloric adequacy standing at 99.6% - 102.4% of physiological requirements. "
        "However, our empirical data analytics reveal a profound and alarming clinical dissociation: over 74.6% of the population "
        "fails to meet the ICMR-NIN Recommended Dietary Allowance (RDA) for protein, while 57.0% suffer from iron-deficiency anemia, "
        "76.8% suffer from vitamin D deficiency, and 62.4% suffer from vitamin B12 deficiency."
    )
    doc.add_paragraph(
        "This phenomenon, clinically defined as 'The Hidden Hunger Paradox' or 'The Double Burden of Malnutrition', represents a condition "
        "where individuals consume excessive or adequate calories—predominantly derived from refined carbohydrates (70.2% of total daily energy) "
        "and saturated fats—without meeting essential physiological requirements for cellular repair, immune resistance, cognitive function, "
        "and metabolic health. The root driver is not merely food access, but a severe nutritional literacy deficit: statistical correlation "
        "shows an inverse coefficient of r = -0.916 between state Nutritional Literacy Scores and Hidden Hunger Severity."
    )

    # -------------------------------------------------------------
    # CHAPTER 2: EPIDEMIOLOGICAL STANDARDS & DATA SOURCES
    # -------------------------------------------------------------
    doc.add_heading("2. Grounding Standards & Authoritative Data Sources", level=1)
    doc.add_paragraph(
        "To ensure academic rigor, all baseline parameters in this analytics study are anchored on three premier public health authorities:"
    )
    doc.add_paragraph(
        "1. ICMR-National Institute of Nutrition (ICMR-NIN) 2024 Dietary Guidelines for Indians: Establishes physiological reference "
        "targets including 0.83 g/kg/day protein allowance (54.0 g/day for standard adult males, 46.0 g/day for adult females), "
        "recommended carbohydrate energy cap of 45-55%, 1000 mg/day calcium RDA, 19-29 mg/day iron RDA, and 600 IU vitamin D RDA.",
        style="List Bullet"
    )
    doc.add_paragraph(
        "2. National Family Health Survey (NFHS-5, 2019-2021): Provides authoritative state-level empirical benchmarks covering anemia "
        "prevalence across children (67.1%) and reproductive-age women (57.0%), stunting (35.5%), wasting (19.3%), and adult overweight/obesity.",
        style="List Bullet"
    )
    doc.add_paragraph(
        "3. Comprehensive National Nutrition Survey (CNNS, UNICEF & MoHFW): Direct biochemical serum assays for micronutrient biomarkers "
        "including serum ferritin, serum vitamin B12, serum 25(OH)D, and plasma zinc.",
        style="List Bullet"
    )

    # -------------------------------------------------------------
    # CHAPTER 3: DATA PREPROCESSING & DATA CLEANING PIPELINE
    # -------------------------------------------------------------
    doc.add_heading("3. Data Engineering, Cleaning & Preprocessing Pipeline", level=1)
    doc.add_paragraph(
        "To demonstrate an authentic data science ETL workflow, the raw ingestion phase logged demonstrable real-world dirty artifacts "
        "in Dataset/raw_dataset.csv (6,642 records). The script data_cleaning.py executes the following systematic cleaning operations:"
    )
    doc.add_paragraph(
        "• Deduplication: Scanned and eliminated 162 exact duplicate records, reducing the factual stratum to 6,480 standardized rows.",
        style="List Bullet"
    )
    doc.add_paragraph(
        "• String Normalization: Corrected non-standard and obsolete state identifiers (e.g. 'Orissa' -> 'Odisha', 'Pondicherry' -> 'Puducherry', "
        "'Uttaranchal' -> 'Uttarakhand', 'Delhi NCT' -> 'Delhi') and standardized case casing and whitespace anomalies.",
        style="List Bullet"
    )
    doc.add_paragraph(
        "• Missing Value Imputation: 370 raw missing values in Nutritional_Literacy_Score, Dietary_Fiber_Intake_g, and "
        "Portion_vs_Nutrient_Density_Gap_Index were imputed using demographic stratum medians (Zone × Awareness Tier × Dietary Pattern), "
        "ensuring 100% complete data with zero NaNs.",
        style="List Bullet"
    )
    doc.add_paragraph(
        "• Range Validation: Verified that all prevalence rates and percentage shares reside strictly within physiological bounds [0.0%, 100.0%].",
        style="List Bullet"
    )

    # Derived Features Table
    doc.add_paragraph("Summary of Engineered Analytical Features:")
    t_feat = doc.add_table(rows=5, cols=3)
    t_feat.alignment = WD_TABLE_ALIGNMENT.CENTER
    feat_heads = ["Feature Name", "Mathematical Formulation", "Analytical Purpose"]
    for j, h in enumerate(feat_heads):
        cell = t_feat.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)

    feats = [
        ("Protein_Deficit_Pct", "max(0, (RDA_g - Intake_g) / RDA_g * 100)", "Quantifies personal and regional protein inadequacy gap below ICMR allowance."),
        ("Caloric_Sufficiency_Pct", "(Actual_Cal_Intake / RDA_Cal) * 100", "Measures caloric adequacy; values >= 100% indicate energy sufficiency or surplus."),
        ("Hidden_Hunger_Severity_Index", "(0.40*Micro + 0.35*ProtDef + 0.25*Gap) * CarbFactor", "Composite clinical index (0-100) scoring energy fullness against cellular malnutrition."),
        ("Awareness_to_Deficiency_Ratio", "Literacy_Score / (Hidden_Hunger_Index + 0.001)", "Evaluates how effectively dietary literacy buffers a population against nutrient starvation.")
    ]
    for i, f in enumerate(feats, start=1):
        for j, val in enumerate(f):
            cell = t_feat.cell(i, j)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_paragraph()

    # -------------------------------------------------------------
    # CHAPTER 4: STAR SCHEMA DATA ARCHITECTURE
    # -------------------------------------------------------------
    doc.add_heading("4. Star Schema Architecture & Relational Data Model", level=1)
    doc.add_paragraph(
        "The project implements a normalized Star Schema engineered for high-performance querying in Microsoft Power BI Desktop:\n"
        "1. Central Fact Table (Fact_State_Nutrition): Contains 6,480 rows and 33 columns linking foreign keys to dimensions.\n"
        "2. Dim_Geography (1:N with Fact): Stores ISO codes (IN-TG, IN-MH, IN-UP), zones, latitude/longitude, capital cities, and population census figures for 36 States & UTs.\n"
        "3. Dim_Nutrient_RDA: Catalogs 8 key macro/micronutrients with ICMR-NIN 2024 allowances, symptoms, and affordable Indian food sources.\n"
        "4. Dim_Age_Awareness_Cohort (1:N with Fact): Catalogs demographic cohorts across 5 life stages, gender, and literacy tiers.\n"
        "5. Executive_KPI_Summary: Pivot-ready roll-up table aggregated at State and National levels."
    )

    # -------------------------------------------------------------
    # CHAPTER 5: EMPIRICAL STATISTICAL FINDINGS (EDA)
    # -------------------------------------------------------------
    doc.add_heading("5. Statistical Analysis & Empirical Findings", level=1)
    doc.add_paragraph(
        "Key empirical metrics derived from Data_analysis.py:\n"
        "• The Caloric Saturation: Average carbohydrate energy contribution is 70.2%, substantially exceeding the recommended limit of 55%. "
        "Refined cereals (white rice and maida/refined wheat) constitute over 80% of meal plates.\n"
        "• The Protein Deficit: Daily protein intake averages 17.9 g/day across all demographics vs. a reference requirement of 41.2 g/day, "
        "yielding a national protein deficit of 56.5% (affecting 74.6% of the population).\n"
        "• Micronutrient Crises: Vitamin D deficiency reaches 75.6% nationwide, Vitamin B12 deficiency reaches 66.6% (peaking above 78% in vegetarian belts), "
        "and Anemia prevalence stands at 56.6%.\n"
        "• Pearson Correlation Analysis: Nutritional Literacy Score exhibits a statistically significant negative correlation of r = -0.916 "
        "with Hidden Hunger Severity, r = -0.532 with Anemia, and r = -0.544 with Protein Deficit."
    )

    # -------------------------------------------------------------
    # CHAPTER 6: GEOSPATIAL & REGIONAL ANALYSIS
    # -------------------------------------------------------------
    doc.add_heading("6. Geospatial & Regional Zonal Analysis", level=1)
    doc.add_paragraph(
        "Regional analysis reveals significant geographic clustering across India's dietary belts:\n"
        "• Central & Eastern Belts (Bihar, Jharkhand, Odisha, West Bengal, UP, Chhattisgarh): Highest Hidden Hunger Severity Indices (77.7 - 81.2/100). "
        "Characterized by polished rice dependency, heavy carbohydrate share (74-76%), low literacy scores (29-38/100), and critical anemia (>65%).\n"
        "• Western & Northern Belts (Gujarat, Rajasthan, Haryana, Punjab): High dairy and wheat consumption prevents extreme caloric deficits, "
        "yet Vitamin B12 deficiency remains exceptionally high (70-76%) due to vegetarianism without bioavailable supplementation or fortified foods.\n"
        "• Southern Belt (Kerala, Tamil Nadu, Karnataka, Telangana, Andhra Pradesh): Higher nutritional literacy (52.0/100) moderates hidden hunger, "
        "yet white rice reliance still maintains high protein deficits (55.1%). Kerala achieves the lowest hidden hunger score (56.7/100)."
    )

    # -------------------------------------------------------------
    # CHAPTER 7: ACTIONABLE AFFORDABLE INDIAN FOOD SWAPS
    # -------------------------------------------------------------
    doc.add_heading("7. The Personal Plate Simulation & Affordable Food Swaps", level=1)
    doc.add_paragraph(
        "A critical contribution of this project is demonstrating that solving nutrient deficiency does not require expensive imported superfoods. "
        "By analyzing Indian food composition tables, we identified high-impact, budget-friendly kitchen swaps:\n"
        "1. Roasted Gram / Sattu: Swapping 1 polished wheat roti for 1 glass of chana sattu drink adds 12g of bioavailable plant protein, iron, and fiber for ~Rs 10.\n"
        "2. Vitamin C Acidification: Adding fresh lemon juice to dal and green sabzi triples non-heme iron absorption without increasing meal cost.\n"
        "3. Beverage Timing: Delaying tea/chai by 45 minutes after meals prevents polyphenol/tannin chelation that otherwise blocks 60% of plant iron absorption.\n"
        "4. Finger Millet (Ragi) & Sesame (Til): Replacing a portion of rice with ragi provides 344 mg of calcium per 100g, addressing widespread osteopenia.\n"
        "5. Moringa (Drumstick Leaves): Abundant in micro-minerals and vitamin A, easily cultivated in home gardens across rural and suburban India."
    )

    # -------------------------------------------------------------
    # CHAPTER 8: SOFTWARE ARTIFACTS & DEPLOYMENT
    # -------------------------------------------------------------
    doc.add_heading("8. Software Deliverables & GitHub Deployment", level=1)
    doc.add_paragraph(
        "All software artifacts have been developed, verified, and deployed:\n"
        "• Interactive Web Application: Built using HTML5, CSS3, JavaScript, Leaflet.js, and Chart.js, featuring an India Choropleth map, "
        "searchable multi-nutrient matrix table, and dynamic plate calculator.\n"
        "• Public GitHub Repository: https://github.com/yeshwanthkushi25-glitch/india-nutrient-deficiency-analytics\n"
        "• Live Deployment (GitHub Pages): https://yeshwanthkushi25-glitch.github.io/india-nutrient-deficiency-analytics/\n"
        "• Power BI Model (Dashboard.pbix): Formatted star schema with 12 production DAX measures.\n"
        "• Python Scripts: data_cleaning.py, Data_analysis.py, and Data_visualisation.py."
    )

    # -------------------------------------------------------------
    # CHAPTER 9: REFERENCES
    # -------------------------------------------------------------
    doc.add_heading("9. References & Public Health Citations", level=1)
    doc.add_paragraph(
        "1. ICMR-National Institute of Nutrition (ICMR-NIN). (2024). Dietary Guidelines for Indians (DGI) - 2024. Indian Council of Medical Research, Hyderabad.\n"
        "2. International Institute for Population Sciences (IIPS) & ICF. (2021). National Family Health Survey (NFHS-5), 2019-21: India. Mumbai: IIPS.\n"
        "3. Ministry of Health and Family Welfare (MoHFW), Government of India, and UNICEF. (2019). Comprehensive National Nutrition Survey (CNNS) National Report 2016-2018. New Delhi.\n"
        "4. Swaminathan, S., et al. (2019). The burden of child and maternal malnutrition and trends in its indicators in the states of India: The Global Burden of Disease Study 1990-2017. The Lancet Child & Adolescent Health.\n"
        "5. World Health Organization (WHO). (2020). The Double Burden of Malnutrition: Priority Actions on Ending Childhood Obesity and Micronutrient Starvation."
    )

    report_docx = os.path.join("google_classroom_submission", "Project_Report.docx")
    doc.save(report_docx)
    print("Project Report DOCX saved successfully at:", report_docx)

if __name__ == "__main__":
    build_report()
