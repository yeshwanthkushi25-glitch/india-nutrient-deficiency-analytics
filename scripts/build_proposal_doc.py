import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

doc = docx.Document()

# Page Margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Color constants
PRIMARY = RGBColor(15, 23, 42)     # Slate Navy
SECONDARY = RGBColor(37, 99, 235)  # Blue Accent
DARK_GRAY = RGBColor(51, 65, 85)

# Title
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_inst = title_p.add_run("SR UNIVERSITY\nDEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (CYBER SECURITY)\nCOURSE: DATA ANALYTICS\n\n")
run_inst.font.size = Pt(11)
run_inst.font.bold = True
run_inst.font.color.rgb = SECONDARY

run = title_p.add_run("PROJECT PROPOSAL\n")
run.font.size = Pt(20)
run.font.bold = True
run.font.color.rgb = PRIMARY

run_sub = title_p.add_run("Nutrient Deficiency & The Hidden Hunger Paradox in India:\nWhy High Caloric Intake Still Leads to Severe Micronutrient and Macronutrient Deficiencies Due to Lack of Nutritional Awareness\n")
run_sub.font.size = Pt(13)
run_sub.font.bold = True
run_sub.font.color.rgb = SECONDARY

# Team Details Box
table_team = doc.add_table(rows=4, cols=3)
table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Team Member Name", "Roll Number", "Role in Project"]
for j, h in enumerate(headers):
    cell = table_team.cell(0, j)
    cell.text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.size = Pt(10)

members = [
    ("Yeshwanth", "2503A53005", "Data Architecture, ETL & Modeling"),
    ("V Laxmi Prasad", "2503A53006", "Statistical Analysis & Visualizations"),
    ("MD Zaheer Pasha", "2503A53016", "Web Dashboard & Power BI Integration")
]
for i, m in enumerate(members, start=1):
    for j, val in enumerate(m):
        cell = table_team.cell(i, j)
        cell.text = val
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)

doc.add_paragraph()

# 1. Executive Summary & Rationale
h1 = doc.add_heading("1. Executive Summary & Background", level=1)
p = doc.add_paragraph(
    "In India, public health interventions have historically centered on eradicating caloric hunger. "
    "Consequently, modern national food consumption patterns show that average daily caloric intake meets or exceeds "
    "energy requirements (averaging 99.6% - 102.4% caloric sufficiency). However, a profound epidemiological crisis "
    "persists: over 74.6% of the population fails to achieve the ICMR-NIN recommended dietary protein allowance (0.83 g/kg/day), "
    "and more than 57% suffer from iron-deficiency anemia, alongside severe vitamin D (76.8%) and vitamin B12 (62.4%) deficits. "
    "This phenomenon, known as 'The Hidden Hunger Paradox', is primarily caused by low nutritional literacy, where diets "
    "rely disproportionately on polished white rice, refined wheat atta, and oils that fulfill caloric satiety while leaving "
    "the human body physiologically malnourished."
)

# 2. Problem Statement
doc.add_heading("2. Problem Statement", level=1)
p = doc.add_paragraph(
    "Despite economic development and agricultural surplus, why does high caloric intake coexist with widespread micronutrient "
    "and protein malnutrition across Indian states? How does lack of dietary awareness drive overconsumption of empty staples, "
    "and what data-driven interventions and regional food substitutions can resolve this paradox without increasing food expenditure?"
)

# 3. Objectives
doc.add_heading("3. Project Objectives", level=1)
objectives = [
    "Compile and clean a comprehensive public health dataset across all 28 States and 8 Union Territories covering urban/rural, demographic, and dietary strata.",
    "Benchmark nutritional intake against the latest ICMR-NIN Dietary Guidelines for Indians (2024), NFHS-5, and CNNS surveys.",
    "Engineer clinical analytics indicators including the Protein Deficit Percentage, Caloric Sufficiency Ratio, and Hidden Hunger Severity Index.",
    "Build a production-grade Star Schema data model for one-click Microsoft Power BI Desktop ingestion.",
    "Develop an interactive, standalone web dashboard featuring an India Choropleth Geo-Map, multi-nutrient heatmaps, life-stage vulnerability charts, and a personalized 'Check Your Plate' calculator with affordable Indian food swaps."
]
for obj in objectives:
    doc.add_paragraph(obj, style="List Bullet")

# 4. Methodology & Data Sources
doc.add_heading("4. Data Sources & Technical Methodology", level=1)
p = doc.add_paragraph(
    "The project anchors its benchmarks on three premier public health authorities:\n"
    "• ICMR-National Institute of Nutrition (ICMR-NIN) 2024: Dietary Guidelines for Indians.\n"
    "• National Family Health Survey (NFHS-5, 2019-21): State fact sheets on anemia, stunting, wasting, and adult overweight.\n"
    "• Comprehensive National Nutrition Survey (CNNS, UNICEF/MoHFW): Biochemical assessment of vitamins B12, D, zinc, and folate."
)

doc.add_paragraph(
    "Technical Stack:\n"
    "• Data Preprocessing: Python (Pandas, NumPy, OpenPyXL)\n"
    "• Statistical Analysis & Visualization: Python (Matplotlib, Seaborn)\n"
    "• Business Intelligence: Microsoft Power BI Desktop (Star Schema with DAX measures)\n"
    "• Web Deployment: HTML5, CSS3, JavaScript (Leaflet.js, Chart.js) hosted on GitHub Pages."
)

# 5. Deliverables & Expected Outcomes
doc.add_heading("5. Key Deliverables", level=1)
delivs = [
    "Comprehensive cleaned fact and dimension tables (6,480 rows, 33 columns, 0 NaNs) in .csv and multi-tab .xlsx format.",
    "Stand-alone Python scripts for data cleaning, statistical EDA, and publication-quality visualization generation.",
    "Interactive Leaflet.js India Choropleth Map with dynamic layer toggles for 7 key nutritional metrics.",
    "Personal Plate Calculator computing real-time energy vs. nutrient fulfillment and localized budget-friendly food swaps.",
    "Power BI Modeling Guide (POWERBI_GUIDE.md) and public GitHub repository."
]
for d in delivs:
    doc.add_paragraph(d, style="List Bullet")

proposal_docx = os.path.join("google_classroom_submission", "Project_Proposal.docx")
doc.save(proposal_docx)
print("Saved Project Proposal to:", proposal_docx)
