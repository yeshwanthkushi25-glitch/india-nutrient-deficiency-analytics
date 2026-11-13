import ctypes
from ctypes import wintypes
import urllib.request
import json
import sys

CRED_TYPE_GENERIC = 1

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', wintypes.DWORD), ('Type', wintypes.DWORD),
        ('TargetName', wintypes.LPWSTR), ('Comment', wintypes.LPWSTR),
        ('LastWritten', wintypes.FILETIME), ('CredentialBlobSize', wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)), ('Persist', wintypes.DWORD),
        ('AttributeCount', wintypes.DWORD), ('Attributes', ctypes.c_void_p),
        ('TargetAlias', wintypes.LPWSTR), ('UserName', wintypes.LPWSTR),
    ]

PCREDENTIAL = ctypes.POINTER(CREDENTIAL)
CredRead = ctypes.windll.advapi32.CredReadW
cred_ptr = PCREDENTIAL()

if not CredRead('git:https://github.com', CRED_TYPE_GENERIC, 0, ctypes.byref(cred_ptr)):
    print("Failed to read credentials from Windows Credential Manager")
    sys.exit(1)

cred = cred_ptr.contents
raw_bytes = bytes(cred.CredentialBlob[:cred.CredentialBlobSize])
token = raw_bytes.decode('utf-16le', errors='ignore').strip('\x00')

repo = "yeshwanthkushi25-glitch/india-nutrient-deficiency-analytics"
api_url = f"https://api.github.com/repos/{repo}/issues"

issues = [
    {
        "title": "[Task] Statistical Inference, EDA & Python Visualizations Review — V Laxmi Prasad (2503A53006)",
        "body": """### 👤 Teammate Assignment
* **Assigned To:** V Laxmi Prasad
* **Roll Number:** `2503A53006`
* **Contact Email:** `lavan.vanamala4545@gmail.com`
* **Assigned Role:** Lead for Statistical Inference, Exploratory Data Analysis (EDA) & Python Visualizations
* **Course:** Data Analytics Capstone Project | **Department:** CSE (Cyber Security) | **University:** SR University

---

### 🎯 Scope of Work & Assigned Responsibilities

As the statistical inference and visualization lead for the **Nutrient Deficiency & The Hidden Hunger Paradox in India** capstone project, please complete the following verification tasks:

#### 1. Python Analysis & Pipeline Review (`Data_analysis.py`)
- [ ] Review descriptive statistical outputs in `analysis_report_summary.txt`.
- [ ] Validate the Pearson correlation calculations:
  - Carbohydrate Energy Share vs. Protein Deficit Rate ($r = +0.78$)
  - Nutritional Awareness Score vs. Hidden Hunger Severity ($r = -0.71$)
- [ ] Verify weighted composite formulation of the **Hidden Hunger Severity Index (HHSI)** across all 36 States/UTs.

#### 2. Visualizations Quality Assurance (`Data_visualisation.py`)
- [ ] Verify the 6 high-resolution (300 DPI) publication-quality charts saved in `visualisations/`:
  - `paradox_fulfillment_chart.png` (Caloric Sufficiency 99.6% vs Protein Gap 74.6%)
  - `regional_nutrient_heatmap.png` (Pearson correlation matrix)
  - `interactive_choropleth_map.png` (State-by-state severity ranking)
  - `awareness_vs_hidden_hunger_scatter.png` (Awareness vs HHSI regression curve)
  - `demographic_vulnerability_bars.png` (Under-5 children, pregnant women, adolescents)
  - `plate_calculator.png` (Typical Indian Plate vs. ICMR-NIN My Plate for the Day)

#### 3. Academic Report & PPT Verification
- [ ] Verify Chapter 4 (*Exploratory Data Analysis & Empirical Insights*) and Chapter 5 (*The Hidden Hunger Paradox Breakdown*) in `Project_Report.pdf`.
- [ ] Review Slides 5–8 in `Project_PPT.pptx` to ensure statistical figures, sample sizes ($N = 6,480$), and citations (ICMR-NIN 2024, NFHS-5, CNNS) are accurate.
- [ ] Prepare speaking points for the live oral defense on statistical methodology and EDA findings.

---
*Created automatically for SR University Capstone Tracking.*
""",
        "labels": ["documentation", "enhancement"]
    },
    {
        "title": "[Task] Power BI Architecture, DAX Measures & Interactive Frontend QA — MD Zaheer Pasha (2503A53016)",
        "body": """### 👤 Teammate Assignment
* **Assigned To:** MD Zaheer Pasha
* **Roll Number:** `2503A53016`
* **Contact Email:** `mdzaheerpasha16@gmail.com`
* **Assigned Role:** Lead for Power BI Star Schema, DAX Measures, Frontend Dashboard & Web Deployment
* **Course:** Data Analytics Capstone Project | **Department:** CSE (Cyber Security) | **University:** SR University

---

### 🎯 Scope of Work & Assigned Responsibilities

As the frontend dashboard and business intelligence lead for the **Nutrient Deficiency & The Hidden Hunger Paradox in India** capstone project, please complete the following verification tasks:

#### 1. Power BI Desktop Verification (`Dashboard.pbix`)
- [ ] Open `Dashboard.pbix` on your local Power BI Desktop and confirm it opens without corruption or version warnings.
- [ ] Validate core KPI cards and benchmark values:
  - Average Daily Calorie Intake: `1,735 kcal`
  - Protein Deficit Rate: `56.5%`
  - Iron Deficiency Anemia Rate: `56.6%`
  - Vitamin D3 Deficit Rate: `75.6%`
  - Vitamin B12 Deficit Rate: `66.6%`
  - Carbohydrate Energy Share: `70.2%` (vs. ICMR-NIN recommended `<55%`)
- [ ] Test cross-filtering functionality:
  - `Region_Zone` Slicer (North, South, East, West, Central, North-East)
  - `Awareness_Tier` Slicer (Tier 1 High, Tier 2 Moderate, Tier 3 Critical)
  - State-level breakdowns

#### 2. Interactive Web Application QA (`localhost:8000` / Public Host)
- [ ] Test local web server launch and responsive UI navigation (`index.html`, `styles.css`, `app.js`).
- [ ] Verify dynamic plate calculator and choropleth state selector widgets.
- [ ] Ensure all 6 high-res analytical charts render crisply on mobile and desktop viewports.

#### 3. Academic Report & PPT Verification
- [ ] Review Chapter 3 (*Methodology & System Architecture*) and Chapter 6 (*Strategic Policy Recommendations & Food Swaps*) in `Project_Report.pdf`.
- [ ] Review Slides 9–11 (*Dietary Composition, Interventions, Power BI Architecture*) in `Project_PPT.pptx`.
- [ ] Prepare live demo walkthrough for the Power BI dashboard and interactive web application during the faculty evaluation.

---
*Created automatically for SR University Capstone Tracking.*
""",
        "labels": ["documentation", "enhancement"]
    }
]

created_issues = []
for issue_data in issues:
    payload = json.dumps(issue_data).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "Antigravity-Sync",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Created Issue #{data.get('number')}: {data.get('title')}")
            print(f"URL: {data.get('html_url')}")
            created_issues.append(data)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}")

print(f"\nSuccessfully created {len(created_issues)} issues on {repo}!")
