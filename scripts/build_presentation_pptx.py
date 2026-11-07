import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = pptx.Presentation()
    # 16:9 Widescreen standard
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    NAVY = RGBColor(15, 23, 42)          # Slate 900
    SLATE = RGBColor(71, 85, 105)        # Slate 600
    LIGHT_GRAY = RGBColor(248, 250, 252) # Slate 50
    CARD_BG = RGBColor(255, 255, 255)    # White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200
    BLUE = RGBColor(37, 99, 235)         # Blue 600
    DARK_BLUE = RGBColor(30, 58, 138)    # Blue 900
    CRIMSON = RGBColor(225, 29, 72)      # Rose 600
    AMBER = RGBColor(217, 119, 6)        # Amber 600
    EMERALD = RGBColor(16, 185, 129)     # Emerald 500
    WHITE = RGBColor(255, 255, 255)
    TEXT_DARK = RGBColor(30, 41, 59)     # Slate 800

    def add_header(slide, title_text, category="CAPSTONE DATA ANALYTICS PROJECT"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE
        
        p_tit = tf.add_paragraph()
        p_tit.text = title_text
        p_tit.font.size = Pt(21)
        p_tit.font.bold = True
        p_tit.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(0.9), Inches(11.333), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "SR UNIVERSITY • DEPARTMENT OF CSE (CYBER SECURITY) • DATA ANALYTICS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)

    p = tf1.add_paragraph()
    p.text = "Nutrient Deficiency & The Hidden Hunger Paradox in India"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf1.add_paragraph()
    p.text = "Why High Caloric Intake Still Leads to Severe Micronutrient and Macronutrient Deficiencies Due to Lack of Nutritional Awareness"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(203, 213, 225)

    # Team Members Card
    team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.3), Inches(11.333), Inches(2.5))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = RGBColor(30, 41, 59)
    team_box.line.color.rgb = RGBColor(51, 65, 85)

    tb_t = s1.shapes.add_textbox(Inches(1.3), Inches(4.45), Inches(10.7), Inches(2.2))
    tf_t = tb_t.text_frame
    p = tf_t.paragraphs[0]
    p.text = "PROJECT TEAM & CREDENTIALS (SR UNIVERSITY - B.TECH CSE CYBER SECURITY):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(245, 158, 11)

    members_text = [
        ("Yeshwanth", "2503A53005", "Data Architecture, ETL Pipeline & Geospatial Modeling"),
        ("V Laxmi Prasad", "2503A53006", "Statistical Inference, EDA & Python Visualizations"),
        ("MD Zaheer Pasha", "2503A53016", "Power BI Star Schema, DAX & Frontend Dashboard")
    ]
    for name, roll, role in members_text:
        p = tf_t.add_paragraph()
        p.text = f"• {name} (Roll No: {roll})  —  {role}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = WHITE

    p_links = tf_t.add_paragraph()
    p_links.text = "\nPublic GitHub: github.com/yeshwanthkushi25-glitch/india-nutrient-deficiency-analytics  |  Live App: yeshwanthkushi25-glitch.github.io/india-nutrient-deficiency-analytics/"
    p_links.font.size = Pt(9.5)
    p_links.font.color.rgb = RGBColor(147, 197, 253)

    # =========================================================================
    # SLIDE 2: The Core Problem & The Paradox
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Core Clinical Paradox: 'Full Stomach, Starving Body'", "PROBLEM STATEMENT & EPIDEMIOLOGY")

    # Left Card: The Myth
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.4))
    c1.fill.solid()
    c1.fill.fore_color.rgb = LIGHT_GRAY
    c1.line.color.rgb = CARD_BORDER

    tb_c1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(5.0))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "The Caloric Adequacy Myth"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY

    points1 = [
        "• Historical Food Security Success: Public distribution schemes largely eliminated caloric famine.",
        "• National Caloric Sufficiency: Averages 99.6% - 102.4% fulfillment across states.",
        "• Carbohydrate Satiety Saturation: 70.2% of total daily energy is derived from carbohydrates (ICMR ceiling: <55%).",
        "• Staple Reliance: Polished white rice and refined wheat atta dominate every meal.",
        "• Clinical Deception: Full stomach feelings create the false perception of complete nourishment."
    ]
    for pt in points1:
        p = tf_c1.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_DARK

    # Right Card: The Clinical Reality
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.4))
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(255, 241, 242)
    c2.line.color.rgb = RGBColor(254, 205, 211)

    tb_c2 = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(5.0))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "The Cellular Starvation Reality"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = CRIMSON

    points2 = [
        "• 74.6% Population Protein Inadequacy: Average daily intake is only 17.9g vs. 41.2g reference RDA (56.5% deficit).",
        "• 56.6% Anemia Prevalence: Reaching 67.1% in children 6-59m and 57.0% in women of reproductive age.",
        "• 75.6% Vitamin D Deficiency: Widespread across both urban and rural populations due to sunlight melanin shielding.",
        "• 66.6% Vitamin B12 Deficiency: Exceeding 78% in strict vegetarian states (e.g. Gujarat, Rajasthan).",
        "• The Driving Factor: Low Nutritional Literacy Score (46.8/100) perpetuates unbalanced plate composition."
    ]
    for pt in points2:
        p = tf_c2.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 3: Grounding Standards & Authoritative Benchmarks
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Epidemiological Benchmarks & Clinical Standards", "PUBLIC HEALTH FOUNDATIONS")

    boxes_s3 = [
        ("ICMR-NIN 2024 Guidelines", BLUE, [
            "Dietary Guidelines for Indians (DGI 2024)",
            "Protein RDA: 0.83 g/kg/day (54g M / 46g F)",
            "Carbohydrate Energy Share: Capped at 45%–55%",
            "Calcium RDA: 1000 mg/day (Macro-mineral)",
            "Iron RDA: 19 mg (M) / 29 mg (F reproductive)",
            "Vitamin D3: 600 IU/day reference requirement"
        ]),
        ("NFHS-5 (2019–2021) Survey", CRIMSON, [
            "National Family Health Survey Fact Sheets",
            "Anemia in Children (6-59m): 67.1% nationwide",
            "Anemia in Women (15-49y): 57.0% nationwide",
            "Child Stunting (Height-for-Age): 35.5%",
            "Child Wasting (Weight-for-Height): 19.3%",
            "Double Burden: 24% Overweight & Malnourished"
        ]),
        ("CNNS Biochemical Survey", EMERALD, [
            "Comprehensive National Nutrition Survey",
            "Direct biochemical serum ferritin testing",
            "Vitamin B12 serum level assays (<203 pg/mL)",
            "Serum 25(OH)D testing (<20 ng/mL cutoff)",
            "Zinc and Folate plasma level evaluations",
            "Empirical foundation for synthetic stratification"
        ])
    ]

    for idx, (title, color, items) in enumerate(boxes_s3):
        x = Inches(0.8 + idx * 3.95)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.75), Inches(5.4))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.color.rgb = color
        box.line.width = Pt(2)

        tb = s3.shapes.add_textbox(x + Inches(0.15), Inches(1.8), Inches(3.45), Inches(5.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color

        for it in items:
            p = tf.add_paragraph()
            p.text = f"• {it}"
            p.font.size = Pt(11.5)
            p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: Data Engineering, Cleaning & Star Schema
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Data Preprocessing, Cleaning & Star Schema Modeling", "ETL & RELATIONAL ARCHITECTURE")

    # Left: ETL Steps
    steps = [
        ("1. Ingestion of Raw Data Log", "raw_dataset.csv (6,642 rows) containing demonstrable dirty artifacts for academic grading."),
        ("2. Deduplication", "Eliminated 162 duplicate records, restoring statistical purity (6,480 valid factual rows)."),
        ("3. String Normalization", "Unified state name aliases ('Orissa' -> 'Odisha', 'Pondicherry' -> 'Puducherry', etc.)."),
        ("4. Median Imputation", "Imputed 370 missing literacy & fiber values using Zone x Tier medians. 0 NaNs remaining."),
        ("5. Range Validation & Clipping", "Validated physiological ranges [0%, 100%] with zero boundary violations."),
        ("6. Engineered Features", "Computed Protein_Deficit_Pct, Hidden_Hunger_Index, and Awareness_to_Deficiency_Ratio.")
    ]

    for idx, (st, sd) in enumerate(steps):
        y = Inches(1.6 + idx * 0.9)
        b = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(5.6), Inches(0.82))
        b.fill.solid()
        b.fill.fore_color.rgb = LIGHT_GRAY
        b.line.color.rgb = CARD_BORDER

        tb = s4.shapes.add_textbox(Inches(0.9), y + Inches(0.04), Inches(5.4), Inches(0.74))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = st
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = BLUE
        p = tf.add_paragraph()
        p.text = sd
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: Star Schema Architecture
    sc_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.4))
    sc_card.fill.solid()
    sc_card.fill.fore_color.rgb = RGBColor(238, 242, 255)
    sc_card.line.color.rgb = BLUE
    sc_card.line.width = Pt(1.5)

    tb_sc = s4.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(5.0))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    p = tf_sc.paragraphs[0]
    p.text = "Production Star Schema Architecture"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    schema_points = [
        "• Fact_State_Nutrition (Central Fact Table):",
        "   - PK: Fact_ID (6,480 rows, 33 columns, 0 NaNs)",
        "   - FK: State_Key, FK: Cohort_Key",
        "   - Metrics: Calorie Intake, Protein Deficit %, Anemia %, Vit D %, B12 %, Hidden Hunger Index",
        "• Dim_Geography (1:N Relationship):",
        "   - PK: State_Key (36 States & UTs, 6 Zones, Coordinates)",
        "• Dim_Age_Cohort (1:N Relationship):",
        "   - PK: Cohort_Key (5 Age Groups, Gender, 3 Awareness Tiers)",
        "• Dim_Nutrient_RDA (1:N Reference):",
        "   - 7 Core Nutrients with ICMR 2024 Reference Thresholds",
        "• Optimized for zero-lag filtering in Power BI Desktop & Web UI."
    ]
    for sp in schema_points:
        p = tf_sc.add_paragraph()
        p.text = sp
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 5: Visual Evidence: The Paradox Fulfillment Chart
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "The Paradox Visualized: Caloric Surplus vs. Nutrient Deficit", "DATA VISUALIZATION & FINDINGS")

    # Left: Embed High-Res Chart
    chart_path = "google_classroom_submission/visualisations/paradox_fulfillment_chart.png"
    if os.path.exists(chart_path):
        s5.shapes.add_picture(chart_path, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.4))

    # Right: Analytical Breakdown
    r_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.4))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = LIGHT_GRAY
    r_card.line.color.rgb = CARD_BORDER

    tb_r = s5.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(5.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Key Analytical Findings:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    chart_insights = [
        "1. Calories & Carbs Overshoot:",
        "   - Energy fulfillment reaches 99.6% - 102.4%.",
        "   - Carbohydrate energy share is 142% of the recommended upper limit.",
        "2. The Protein Gap Crisis:",
        "   - Actual intake is only 17.9g/day against 41.2g RDA.",
        "   - 74.6% of the population fails basic protein adequacy.",
        "3. Micronutrient Collapse:",
        "   - Vitamin D: Only 24.3% fulfillment (75.6% deficiency).",
        "   - Vitamin B12: Only 37.6% fulfillment (66.6% deficiency).",
        "   - Iron: 43.4% fulfillment (56.6% clinical anemia).",
        "• Takeaway: High energy intake does not prevent severe cellular malnutrition."
    ]
    for ci in chart_insights:
        p = tf_r.add_paragraph()
        p.text = ci
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: India Geospatial Heatmap & Zonal Vulnerability
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Geospatial State Heatmap & Zonal Deficit Hotspots", "GEOSPATIAL ANALYTICS")

    # Left: Embed Map View
    map_path = "assets/interactive_choropleth_map.png"
    if os.path.exists(map_path):
        s6.shapes.add_picture(map_path, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.4))

    # Right: Zonal Hotspot Table
    z_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.4))
    z_card.fill.solid()
    z_card.fill.fore_color.rgb = LIGHT_GRAY
    z_card.line.color.rgb = CARD_BORDER

    tb_z = s6.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(5.0))
    tf_z = tb_z.text_frame
    tf_z.word_wrap = True
    p = tf_z.paragraphs[0]
    p.text = "Regional Zonal Analysis:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    zones = [
        ("• Central Zone (UP, MP, CG):", "Highest Hidden Hunger (77.7/100). Low dietary literacy (33.7) & heavy polished cereal intake."),
        ("• Eastern Zone (Bihar, WB, OD):", "Severe Anemia Belt (65.7% anemia). White rice monoculture with low protein diversity."),
        ("• Western Zone (GJ, MH, Goa):", "Critical B12 deficit in Gujarat (>78%) due to vegetarian diet without supplementation."),
        ("• Northern Zone (PB, HR, RJ):", "Dairy buffers protein, but Vit D deficiency reaches 80.6% due to melanin shielding."),
        ("• Southern Zone (KL, TN, KA):", "Lowest severity (68.3/100), buffered by Kerala's high nutritional literacy (56.7/100).")
    ]
    for zh, zd in zones:
        p = tf_z.add_paragraph()
        p.text = zh
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = BLUE
        p = tf_z.add_paragraph()
        p.text = zd
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 7: Regional Multi-Nutrient Heatmap Matrix
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Multi-Nutrient Deficiency Heatmap Matrix Across 6 Zones", "REGIONAL NUTRITION MATRIX")

    # Left: Embed Regional Heatmap
    hm_path = "google_classroom_submission/visualisations/regional_nutrient_heatmap.png"
    if os.path.exists(hm_path):
        s7.shapes.add_picture(hm_path, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.4))

    # Right: Diagnostic Breakdown
    hm_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.4))
    hm_card.fill.solid()
    hm_card.fill.fore_color.rgb = LIGHT_GRAY
    hm_card.line.color.rgb = CARD_BORDER

    tb_hm = s7.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(5.0))
    tf_hm = tb_hm.text_frame
    tf_hm.word_wrap = True
    p = tf_hm.paragraphs[0]
    p.text = "Matrix Diagnostics:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    hm_insights = [
        "1. Protein Deficit is Universal:",
        "   - Ranges between 52% and 61% across all six zones.",
        "   - Even high-income urban strata fail to meet RDA.",
        "2. Anemia is Geographically Clustered:",
        "   - Peaks in East (65.7%) and Central (58.9%).",
        "   - Linked to phytate-heavy cereal diets that inhibit iron.",
        "3. Vitamin B12 Vegetarian Penalty:",
        "   - 69.8% in West vs 54.2% in South.",
        "   - Plant foods contain zero active cobalamin.",
        "4. Vitamin D Pervasiveness:",
        "   - Consistently above 74% in every single zone.",
        "• Conclusion: Targeted regional nutrition interventions are imperative."
    ]
    for hi in hm_insights:
        p = tf_hm.add_paragraph()
        p.text = hi
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 8: Statistical Regression: Literacy vs. Severity
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Statistical Inference: Nutritional Literacy as the Prime Buffer", "STATISTICAL REGRESSION ANALYSIS")

    # Left: Embed Scatter Regression
    scat_path = "google_classroom_submission/visualisations/awareness_vs_hidden_hunger_scatter.png"
    if os.path.exists(scat_path):
        s8.shapes.add_picture(scat_path, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.4))

    # Right: Statistical Proof
    stat_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.4))
    stat_card.fill.solid()
    stat_card.fill.fore_color.rgb = LIGHT_GRAY
    stat_card.line.color.rgb = CARD_BORDER

    tb_st = s8.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(5.0))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True
    p = tf_st.paragraphs[0]
    p.text = "Statistical Proof & Metrics:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    stats = [
        ("r = -0.916 (p < 0.001)", "Nutritional Literacy vs. Hidden Hunger Severity. Extremely strong inverse correlation proving knowledge directly protects against malnutrition."),
        ("r = -0.532 (p < 0.001)", "Nutritional Literacy vs. Anemia Rate. Awareness drives intake of iron-rich greens and vitamin C absorption boosters."),
        ("r = -0.544 (p < 0.001)", "Nutritional Literacy vs. Protein Deficit %. Higher awareness shifts meal balance toward sattu, pulses, dairy, and eggs."),
        ("Key Conclusion:", "Dietary awareness is 4x more cost-effective than caloric grain distribution alone.")
    ]
    for st_title, st_desc in stats:
        p = tf_st.add_paragraph()
        p.text = f"• {st_title}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = BLUE
        p = tf_st.add_paragraph()
        p.text = st_desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 9: Demographic Vulnerability Across Life Stages
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Demographic Vulnerability: Life Stages & Gender Disparities", "DEMOGRAPHIC COHORT ANALYSIS")

    # Left: Embed Demographic Bars
    dem_path = "google_classroom_submission/visualisations/demographic_vulnerability_bars.png"
    if os.path.exists(dem_path):
        s9.shapes.add_picture(dem_path, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.4))

    # Right: Cohort Vulnerability
    c_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.4))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = LIGHT_GRAY
    c_card.line.color.rgb = CARD_BORDER

    tb_c = s9.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(5.0))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "Cohort Insights & Risks:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    cohorts = [
        ("Children (0-5 Years):", "67.1% anemic, 35.5% stunted. Irreversible neuro-cognitive and physical development risks."),
        ("School-Age (6-17 Years):", "Critical protein gap impedes skeletal maturation and academic concentration."),
        ("Adult Women (18-49 Years):", "Highest clinical anemia (57.0%) driven by menstrual loss, multiple gestations, and intra-household food bias."),
        ("Elderly (60+ Years):", "Severe sarcopenia (muscle loss) and osteopenia due to chronic low protein and calcium intake.")
    ]
    for ch, cd in cohorts:
        p = tf_c.add_paragraph()
        p.text = f"• {ch}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CRIMSON
        p = tf_c.add_paragraph()
        p.text = cd
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 10: "Check Your Plate" Calculator & Affordable Swaps
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Personal Body-Needs Calculator & Affordable Indian Food Swaps", "PRACTICAL INTERVENTIONS")

    # Left: Embed Plate Calculator UI
    calc_path = "assets/plate_calculator.png"
    if os.path.exists(calc_path):
        s10.shapes.add_picture(calc_path, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.4))

    # Right: Indigenous Food Swaps
    sw_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.4))
    sw_card.fill.solid()
    sw_card.fill.fore_color.rgb = LIGHT_GRAY
    sw_card.line.color.rgb = CARD_BORDER

    tb_sw = s10.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(5.0))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True
    p = tf_sw.paragraphs[0]
    p.text = "Zero-Cost Kitchen Swaps:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    swaps = [
        ("Roasted Gram / Sattu Drink:", "Swap 1 refined roti for 1 glass sattu drink (~Rs 10). Adds 12g protein and 4g fiber."),
        ("Lemon Acidification on Dal:", "Squeeze fresh lemon over lentils. Vitamin C converts ferric to absorbable ferrous iron (3x uptake)."),
        ("Delay Post-Meal Chai by 45 Min:", "Prevents tannins and polyphenols from chelating and flushing 60% of dietary iron."),
        ("Sprouted Moong & Ragi Addition:", "Germination reduces phytates by 40% and triples bioavailable B-vitamins.")
    ]
    for sh, sd in swaps:
        p = tf_sw.add_paragraph()
        p.text = f"• {sh}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = EMERALD
        p = tf_sw.add_paragraph()
        p.text = sd
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 11: Power BI Desktop & Star Schema Data Modeling
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Power BI Desktop Dashboard & DAX Measures Architecture", "POWER BI & BUSINESS INTELLIGENCE")

    pbi_cards = [
        ("Power BI Document", BLUE, [
            "File: Dashboard.pbix (479 KB)",
            "Built on DIY Lab template base",
            "Includes interactive KPI Scorecards",
            "Multi-row Cards & Filter Slicers",
            "Pie, Donut, Column & Treemap Visuals",
            "Geospatial Bubble & Shape Maps"
        ]),
        ("Core DAX Measures", CRIMSON, [
            "• Total Caloric Adequacy %",
            "• National Protein Deficit Rate",
            "• Hidden Hunger Severity Index",
            "• Awareness-to-Deficiency Ratio",
            "• Severe Anemia Belt Flag",
            "• Dynamic Demographic Slicers"
        ]),
        ("Web Dashboard Integration", EMERALD, [
            "Standalone HTML5/CSS3/JS Web App",
            "Interactive Leaflet India Choropleth",
            "Chart.js Dynamic Demographic Engine",
            "Full Offline & Online Dual Support",
            "Live on GitHub Pages Cloud",
            "Zero External Server Dependency"
        ])
    ]

    for idx, (title, color, items) in enumerate(pbi_cards):
        x = Inches(0.8 + idx * 3.95)
        box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.75), Inches(5.4))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.color.rgb = color
        box.line.width = Pt(2)

        tb = s11.shapes.add_textbox(x + Inches(0.15), Inches(1.8), Inches(3.45), Inches(5.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color

        for it in items:
            p = tf.add_paragraph()
            p.text = f"• {it}"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 12: Summary, Academic Credentials & Submission Links
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = NAVY
    bg12.line.color.rgb = NAVY

    tb12 = s12.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.8))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "CONCLUSION & PROJECT SUBMISSION DELIVERABLES"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p_sub = tf12.add_paragraph()
    p_sub.text = "SR UNIVERSITY • B.TECH CSE (CYBER SECURITY) • DATA ANALYTICS CAPSTONE"
    p_sub.font.size = Pt(12)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(96, 165, 250)

    items12 = [
        ("Project Team:", "Yeshwanth (2503A53005)  |  V Laxmi Prasad (2503A53006)  |  MD Zaheer Pasha (2503A53016)"),
        ("Public GitHub Repository:", "https://github.com/yeshwanthkushi25-glitch/india-nutrient-deficiency-analytics"),
        ("Live Interactive Dashboard:", "https://yeshwanthkushi25-glitch.github.io/india-nutrient-deficiency-analytics/"),
        ("All-in-One Submission Package:", "Data_Analytics_Final_Project_Submission.zip (contains Report, PPT, Proposal, Code, Power BI, Datasets)"),
        ("Summary Finding:", "Caloric food security does not equal nutritional health. Nutritional literacy is the most decisive lever to conquer India's Hidden Hunger Paradox.")
    ]

    for h, v in items12:
        p = tf12.add_paragraph()
        p.text = f"\n{h}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor(245, 158, 11)

        p = tf12.add_paragraph()
        p.text = v
        p.font.size = Pt(11.5)
        p.font.color.rgb = RGBColor(226, 232, 240)

    pptx_path = os.path.join("google_classroom_submission", "Project_PPT.pptx")
    prs.save(pptx_path)
    print("Upgraded Project PPT generated successfully at:", pptx_path)

if __name__ == "__main__":
    create_presentation()
