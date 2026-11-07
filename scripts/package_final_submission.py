import os
import shutil
import zipfile

desktop_pbix = r"C:\Users\yeshwanth\OneDrive\Desktop\Dashboard.pbix"
downloads_pbix = r"C:\Users\yeshwanth\Downloads\Dashboard.pbix"
gc_dir = r"c:\Users\yeshwanth\data analytics project\google_classroom_submission"

# 1. Ensure Dashboard.pbix in google_classroom_submission is updated with the clean pbix
gc_pbix = os.path.join(gc_dir, "Dashboard.pbix")
shutil.copy2(desktop_pbix, gc_pbix)
print(f"Updated gc Dashboard.pbix: {os.path.getsize(gc_pbix)} bytes")

# Also copy upgraded Report & PPT from Desktop to gc_dir
shutil.copy2(r"C:\Users\yeshwanth\OneDrive\Desktop\Project_Report.pdf", os.path.join(gc_dir, "Project_Report.pdf"))
shutil.copy2(r"C:\Users\yeshwanth\OneDrive\Desktop\Project_PPT.pptx", os.path.join(gc_dir, "Project_PPT.pptx"))

# 2. Build the final submission ZIP with EXACTLY the required files
zip_paths = [
    r"C:\Users\yeshwanth\OneDrive\Desktop\Data_Analytics_Final_Project_Submission.zip",
    r"C:\Users\yeshwanth\Downloads\Data_Analytics_Final_Project_Submission.zip"
]

files_to_pack = [
    ("Dashboard.pbix", desktop_pbix),
    ("Project_Report.pdf", os.path.join(gc_dir, "Project_Report.pdf")),
    ("Project_Report.docx", os.path.join(gc_dir, "Project_Report.docx")),
    ("Project_PPT.pptx", os.path.join(gc_dir, "Project_PPT.pptx")),
    ("Project_Proposal.docx", os.path.join(gc_dir, "Project_Proposal.docx")),
    ("Project_Proposal.pdf", os.path.join(gc_dir, "Project_Proposal.pdf")),
    ("data_cleaning.py", os.path.join(gc_dir, "data_cleaning.py")),
    ("Data_analysis.py", os.path.join(gc_dir, "Data_analysis.py")),
    ("Data_visualisation.py", os.path.join(gc_dir, "Data_visualisation.py")),
    ("analysis_report_summary.txt", os.path.join(gc_dir, "analysis_report_summary.txt")),
    ("clean_dataset/clean_dataset.csv", os.path.join(gc_dir, "clean_dataset", "clean_dataset.csv")),
    ("clean_dataset/clean_dataset.xlsx", os.path.join(gc_dir, "clean_dataset", "clean_dataset.xlsx")),
    ("Dataset/raw_dataset.csv", os.path.join(gc_dir, "Dataset", "raw_dataset.csv")),
    ("Dataset/raw_dataset.xlsx", os.path.join(gc_dir, "Dataset", "raw_dataset.xlsx")),
]

# Check if india_nutrient_deficiency_analytics.xlsx exists in clean_dataset
excel_enhanced = os.path.join(gc_dir, "clean_dataset", "india_nutrient_deficiency_analytics.xlsx")
if os.path.exists(excel_enhanced):
    files_to_pack.append(("clean_dataset/india_nutrient_deficiency_analytics.xlsx", excel_enhanced))

# Add visualisations
vis_dir = os.path.join(gc_dir, "visualisations")
if os.path.exists(vis_dir):
    for f in os.listdir(vis_dir):
        fp = os.path.join(vis_dir, f)
        if os.path.isfile(fp):
            files_to_pack.append((f"visualisations/{f}", fp))

# Add team info and powerbi instructions
team_info_content = """SR UNIVERSITY
DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (CYBER SECURITY)
COURSE: DATA ANALYTICS CAPSTONE PROJECT

PROJECT TITLE:
Nutrient Deficiency & The Hidden Hunger Paradox in India:
Why High Caloric Intake Still Leads to Severe Macronutrient and Micronutrient Deficiencies
Due to Lack of Nutritional Awareness.

PROJECT GROUP MEMBERS:
1. Yeshwanth       - Roll No: 2503A53005 (Data Architecture, ETL Pipeline & Geospatial Modeling)
2. V Laxmi Prasad  - Roll No: 2503A53006 (Statistical Inference, EDA & Python Visualizations)
3. MD Zaheer Pasha - Roll No: 2503A53016 (Power BI Star Schema, DAX & Frontend UI)

GITHUB REPOSITORY LINK (PUBLIC):
https://github.com/yeshwanthkushi25-glitch/india-nutrient-deficiency-analytics
"""

pb_info_content = """POWER BI DASHBOARD INFORMATION
========================================================================
File: Dashboard.pbix (3-Page Executive & Technical Report)

Page 1: 1. Executive Overview & Paradox
- High-level KPIs: Energy Fulfillment (99.6%), Protein Inadequacy Gap (74.6%), Anemia (56.6%), Vitamin D3 (75.6%), Vitamin B12 (66.6%)
- Caloric Fulfillment vs Protein Deficit Inversion Chart
- 70.2% Carbohydrate Energy Share Donut Breakdown
- 36 States/UTs Anemia and Protein Ranking Spectrum

Page 2: 2. Geospatial & Micronutrients
- India 36 States/UTs Geospatial Deficit Map
- Nutritional Literacy Score vs Hidden Hunger Severity Scatter Plot
- Pearson Correlation Heatmap Matrix
- Micronutrient Deficiency Breakdown (Iron, D3, B12, Zinc, Folate, Iodine)

Page 3: 3. Demographics & Kitchen Swaps
- Vulnerability Cohort Segmentation (Under-5 Children, Pregnant Women, Adolescents, Rural Laborers)
- Urban vs Rural Calorie vs Micronutrient Inversion
- ICMR-NIN RDA Food Substitution & Kitchen Swaps Table

Compatible with all standard Power BI Desktop installations (PBIR Enhanced Report Format).
"""

for target_zip in zip_paths:
    with zipfile.ZipFile(target_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for arcname, filepath in files_to_pack:
            if os.path.exists(filepath):
                z.write(filepath, arcname)
            else:
                print(f"Warning: {filepath} not found")
        z.writestr("GITHUB_REPOSITORY_LINK_AND_TEAM_INFO.txt", team_info_content)
        z.writestr("POWER_BI_DASHBOARD_INSTRUCTIONS.txt", pb_info_content)
    size = os.path.getsize(target_zip)
    print(f"Built {target_zip}: {size} bytes ({size/(1024*1024):.2f} MB)")
