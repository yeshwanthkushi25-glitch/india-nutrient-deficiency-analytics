import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Set 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    NAVY = RGBColor(15, 23, 42)      # #0f172a
    BLUE = RGBColor(37, 99, 235)     # #2563eb
    WHITE = RGBColor(255, 255, 255)
    LIGHT_GRAY = RGBColor(241, 245, 249)
    TEXT_DARK = RGBColor(30, 41, 59)
    SLATE = RGBColor(100, 116, 139)
    CRIMSON = RGBColor(225, 29, 72)
    EMERALD = RGBColor(16, 185, 129)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category="DATA ANALYTICS CAPSTONE PROJECT"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE
        
        p_tit = tf.add_paragraph()
        p_tit.text = title_text
        p_tit.font.size = Pt(22)
        p_tit.font.bold = True
        p_tit.font.color.rgb = NAVY

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(3.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "SR UNIVERSITY • DEPARTMENT OF CSE (CYBER SECURITY) • DATA ANALYTICS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p = tf1.add_paragraph()
    p.text = "Nutrient Deficiency & The Hidden Hunger Paradox in India"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf1.add_paragraph()
    p.text = "Why High Caloric Intake Still Leads to Severe Micronutrient and Macronutrient Deficiencies Due to Lack of Nutritional Awareness"
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(203, 213, 225)

    # Team Members Card
    team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(11.333), Inches(2.2))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = RGBColor(30, 41, 59)
    team_box.line.color.rgb = RGBColor(51, 65, 85)

    tb_t = s1.shapes.add_textbox(Inches(1.2), Inches(4.6), Inches(10.9), Inches(2.0))
    tf_t = tb_t.text_frame
    p = tf_t.paragraphs[0]
    p.text = "PROJECT TEAM (SR UNIVERSITY - B.TECH CSE CYBER SECURITY):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(245, 158, 11)

    members_text = [
        "• Yeshwanth (Roll No: 2503A53005) - Data Architecture, ETL Pipeline & Geospatial Modeling",
        "• V Laxmi Prasad (Roll No: 2503A53006) - Statistical Inference, EDA & Python Visualizations",
        "• MD Zaheer Pasha (Roll No: 2503A53016) - Power BI Star Schema, DAX & Frontend Dashboard"
    ]
    for m in members_text:
        p = tf_t.add_paragraph()
        p.text = m
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE

    # -------------------------------------------------------------
    # SLIDE 2: The Core Problem & The Paradox
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Core Clinical Paradox: 'Full Stomach, Starving Body'")

    # Left Card: The Paradox Reality
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = LIGHT_GRAY
    c1.line.color.rgb = RGBColor(226, 232, 240)

    tb_c1 = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "The Caloric Adequacy Myth"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY

    points1 = [
        "• Historical public health focused on caloric famine alleviation.",
        "• Today, national daily calorie intake averages 99.6% - 102.4% fulfillment.",
        "• Diets are saturated with refined carbs (white rice, maida, sugar).",
        "• 70.2% of total daily energy comes from carbohydrates (ICMR limit: <55%).",
        "• Result: The stomach is satiated, but human cells remain severely starved of essential proteins and micronutrients."
    ]
    for pt in points1:
        p = tf_c1.add_paragraph()
        p.text = pt
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_DARK

    # Right Card: The Clinical Reality
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(255, 241, 242) # soft rose
    c2.line.color.rgb = RGBColor(254, 205, 211)

    tb_c2 = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "The Severe Cellular Deficit"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = CRIMSON

    points2 = [
        "• 74.6% Population Protein Inadequacy: Average daily intake is only 17.9g vs. 41.2g reference RDA (56.5% deficit).",
        "• 56.6% Anemia Prevalence: Reaching 67.1% in children under 5 and 57.0% in women of reproductive age.",
        "• 75.6% Vitamin D Deficiency: Widespread across urban & indoor rural belts.",
        "• 66.6% Vitamin B12 Deficiency: Surpassing 78% in strict vegetarian states.",
        "• Root Cause: Low Nutritional Literacy (Score: 46.8/100) perpetuates unbalanced plate composition."
    ]
    for pt in points2:
        p = tf_c2.add_paragraph()
        p.text = pt
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 3: Data Sources & Grounding Benchmarks
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Epidemiological Benchmarks & Data Grounding")

    boxes_s3 = [
        ("ICMR-NIN 2024 Guidelines", BLUE, [
            "Dietary Guidelines for Indians (DGI) 2024",
            "Protein RDA: 0.83 g/kg/day (54g M / 46g F)",
            "Carbohydrate Energy Share Cap: 45%–55%",
            "Calcium RDA: 1000 mg/day (Macro-mineral)",
            "Iron RDA: 19 mg (M) / 29 mg (F reproductive)"
        ]),
        ("NFHS-5 (2019–2021) Survey", CRIMSON, [
            "National Family Health Survey Fact Sheets",
            "Anemia in Children (6-59m): 67.1% national",
            "Anemia in Women (15-49y): 57.0% national",
            "Stunting: 35.5% | Wasting: 19.3%",
            "Double Burden: 24% Overweight + Malnourished"
        ]),
        ("CNNS Biochemical Survey", RGBColor(16, 185, 129), [
            "Comprehensive National Nutrition Survey",
            "Serum ferritin biochemical assessments",
            "Vitamin B12 serum level assays (<203 pg/mL)",
            "Serum 25(OH)D testing (<20 ng/mL)",
            "Zinc and Folate plasma level evaluations"
        ])
    ]

    for idx, (title, color, items) in enumerate(boxes_s3):
        x = Inches(0.8 + idx * 3.95)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.75), Inches(4.8))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.color.rgb = color
        box.line.width = Pt(2)

        tb = s3.shapes.add_textbox(x + Inches(0.15), Inches(2.0), Inches(3.45), Inches(4.4))
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

    # -------------------------------------------------------------
    # SLIDE 4: Data Preprocessing & Cleaning Pipeline
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Data Preprocessing, Cleaning & Feature Engineering")

    steps = [
        ("1. Ingestion of Raw Data Log", "Dataset/raw_dataset.csv (6,642 rows) containing demonstrable real-world dirty artifacts for academic demonstration."),
        ("2. Deduplication", "Scanned and eliminated 162 exact duplicate records, restoring statistical purity (6,480 valid factual rows)."),
        ("3. String Normalization", "Resolved state naming anomalies ('Orissa' -> 'Odisha', 'Uttaranchal' -> 'Uttarakhand', 'Pondicherry' -> 'Puducherry', 'Delhi NCT' -> 'Delhi')."),
        ("4. Missing Value Imputation", "Imputed 370 missing entries in Nutritional Literacy Score and Fiber using demographic group medians (Zone × Tier). Zero NaNs."),
        ("5. Range Validation & Clipping", "Constrained all percentage indicators within valid physiological boundaries [0.0%, 100.0%]."),
        ("6. Engineered Features", "Computed Protein_Deficit_Pct, Caloric_Sufficiency_Pct, Hidden_Hunger_Severity_Index, and Awareness_to_Deficiency_Ratio.")
    ]

    for idx, (step_title, step_desc) in enumerate(steps):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.8 + row * 1.6)

        b = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(1.4))
        b.fill.solid()
        b.fill.fore_color.rgb = LIGHT_GRAY
        b.line.color.rgb = RGBColor(203, 213, 225)

        tb = s4.shapes.add_textbox(x + Inches(0.15), y + Inches(0.1), Inches(5.3), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = step_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = step_desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = SLATE

    # -------------------------------------------------------------
    # SLIDE 5: Star Schema Relational Data Architecture
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Star Schema Architecture (Power BI Ready)")

    # Fact Box
    fact = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(2.2), Inches(4.3), Inches(4.2))
    fact.fill.solid()
    fact.fill.fore_color.rgb = RGBColor(238, 242, 255)
    fact.line.color.rgb = BLUE
    fact.line.width = Pt(2)

    tb_f = s5.shapes.add_textbox(Inches(4.6), Inches(2.3), Inches(4.1), Inches(4.0))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "Fact_State_Nutrition (Fact Table)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BLUE

    fact_cols = [
        "PK: Fact_ID (6,480 rows, 33 columns)",
        "FK: State_Key (State ISO)",
        "FK: Cohort_Key (Age + Gender + Tier)",
        "• Avg_Daily_Calorie_Intake_kcal",
        "• Carbohydrate_Energy_Share_Pct (70.2%)",
        "• Protein_Deficit_Pct (56.5%)",
        "• Iron_Deficiency_Anemia_Pct (56.6%)",
        "• Vitamin_D_Deficiency_Pct (75.6%)",
        "• Vitamin_B12_Deficiency_Pct (66.6%)",
        "• Hidden_Hunger_Severity_Index (71.0)"
    ]
    for c in fact_cols:
        p = tf_f.add_paragraph()
        p.text = c
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Dim 1: Geography (Left)
    d1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.2), Inches(3.3), Inches(4.2))
    d1.fill.solid()
    d1.fill.fore_color.rgb = LIGHT_GRAY
    d1.line.color.rgb = RGBColor(16, 185, 129)
    tb_d1 = s5.shapes.add_textbox(Inches(0.9), Inches(2.3), Inches(3.1), Inches(4.0))
    tf_d1 = tb_d1.text_frame
    p = tf_d1.paragraphs[0]
    p.text = "Dim_Geography (1:N)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(5, 150, 105)
    for c in ["PK: State_Key", "• State_Name (36 States/UTs)", "• Region_Zone (6 Zones)", "• Latitude & Longitude", "• Capital_City", "• Estimated_Population_Cr"]:
        p = tf_d1.add_paragraph()
        p.text = c
        p.font.size = Pt(10)

    # Dim 2: Cohort (Right)
    d2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(2.2), Inches(3.3), Inches(4.2))
    d2.fill.solid()
    d2.fill.fore_color.rgb = LIGHT_GRAY
    d2.line.color.rgb = RGBColor(245, 158, 11)
    tb_d2 = s5.shapes.add_textbox(Inches(9.3), Inches(2.3), Inches(3.1), Inches(4.0))
    tf_d2 = tb_d2.text_frame
    p = tf_d2.paragraphs[0]
    p.text = "Dim_Age_Cohort (1:N)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(217, 119, 6)
    for c in ["PK: Cohort_Key", "• Age_Group (5 cohorts)", "• Gender (Male/Female)", "• Awareness_Tier (3 Tiers)", "• Life_Stage_Description", "• Intervention_Priority"]:
        p = tf_d2.add_paragraph()
        p.text = c
        p.font.size = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 6: Macro & Micronutrient Fulfillment Analysis
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Intake vs. Physiological RDA Benchmark (% Fulfillment)")

    table_data = [
        ("Daily Caloric Intake", "1,742.0 kcal", "1,734.7 kcal", "99.6% (Sufficient / Surplus)", "Energy satiety met through refined staples", EMERALD),
        ("Carbohydrate Energy Share", "< 55.0%", "70.2%", "142.0% (Excessive Burden)", "Refined polished rice and wheat dominance", RGBColor(245, 158, 11)),
        ("Daily Protein Intake", "41.2 g/day", "17.9 g/day", "56.5% Deficit (Severe Gap)", "Muscle wasting, sarcopenia, and stunting", CRIMSON),
        ("Iron (Anemia-Free Status)", "< 20.0%", "56.6%", "43.4% Fulfillment (Crisis)", "Microcytic anemia in 67% toddlers & 57% women", CRIMSON),
        ("Vitamin D3 (Cholecalciferol)", "600 IU/day", "145.8 IU", "24.3% Fulfillment (Severe)", "Indoor lifestyle, high melanin, lack of fortification", CRIMSON),
        ("Vitamin B12 (Cobalamin)", "2.2 mcg/day", "0.83 mcg", "37.6% Fulfillment (Severe)", "Critical in vegetarian populations (>78% deficit)", CRIMSON),
        ("Calcium (Macro-Mineral)", "1000 mg/day", "421.0 mg", "42.1% Fulfillment (Inadequate)", "Osteopenia, dental deterioration, osteoporosis", CRIMSON)
    ]

    t_s6 = s6.shapes.add_table(rows=8, cols=5, left=Inches(0.8), top=Inches(1.8), width=Inches(11.733), height=Inches(4.8))
    heads = ["Nutrient Metric", "ICMR-NIN RDA Benchmark", "Actual National Mean", "% Fulfillment Status", "Clinical Consequence"]
    for j, h in enumerate(heads):
        cell = t_s6.table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for r in cell.text_frame.paragraphs[0].runs:
            r.font.bold = True
            r.font.size = Pt(10.5)
            r.font.color.rgb = WHITE

    for i, row in enumerate(table_data, start=1):
        for j in range(5):
            cell = t_s6.table.cell(i, j)
            cell.text = row[j]
            for r in cell.text_frame.paragraphs[0].runs:
                r.font.size = Pt(9.5)
                if j == 3:
                    r.font.bold = True
                    r.font.color.rgb = row[5]

    # -------------------------------------------------------------
    # SLIDE 7: Geospatial Hotspots & Zonal Analysis
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Geospatial State Analysis & Zonal Deficit Hotspots")

    zonal_data = [
        ("Central Zone (UP, MP, Chhattisgarh)", "77.7 / 100", "78.2%", "58.9%", "33.7 / 100", "Critical Hidden Hunger: Polished cereal dependency, lowest literacy."),
        ("Eastern Zone (Bihar, WB, Odisha, Jharkhand)", "77.8 / 100", "76.2%", "65.7%", "38.4 / 100", "Severe Anemia Belt: Highest anemia (>65%) and high carbohydrate share."),
        ("Western Zone (Gujarat, Maharashtra, Goa)", "69.8 / 100", "79.0%", "58.3%", "48.1 / 100", "B12 & Protein Gap: Vegetarian belt with high B12 deficit in Gujarat."),
        ("Northern Zone (Punjab, Haryana, Rajasthan)", "69.7 / 100", "80.6%", "59.9%", "49.4 / 100", "Vitamin D Crisis: High dairy buffers protein, but Vit D remains suppressed."),
        ("Southern Zone (TN, Kerala, Karnataka, TS, AP)", "68.3 / 100", "74.3%", "53.5%", "52.0 / 100", "Higher Awareness Buffer: Kerala lowest hidden hunger (56.7/100)."),
        ("North-East Zone (Assam, Meghalaya, etc.)", "68.6 / 100", "68.3%", "48.3%", "49.0 / 100", "Dietary Diversity: Higher intake of indigenous greens and animal protein.")
    ]

    t_s7 = s7.shapes.add_table(rows=7, cols=6, left=Inches(0.8), top=Inches(1.8), width=Inches(11.733), height=Inches(4.8))
    heads7 = ["Geographic Zone", "Hidden Hunger Index", "Vit D Deficit", "Anemia Rate", "Literacy Score", "Dietary Characterization"]
    for j, h in enumerate(heads7):
        cell = t_s7.table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for r in cell.text_frame.paragraphs[0].runs:
            r.font.bold = True
            r.font.size = Pt(10)
            r.font.color.rgb = WHITE

    for i, row in enumerate(zonal_data, start=1):
        for j in range(6):
            cell = t_s7.table.cell(i, j)
            cell.text = row[j]
            for r in cell.text_frame.paragraphs[0].runs:
                r.font.size = Pt(9.5)

    # -------------------------------------------------------------
    # SLIDE 8: Statistical Correlation (Literacy vs. Deficiencies)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Statistical Inference: Nutritional Literacy as the Prime Buffer")

    # Key Metric Highlight Cards
    corr_cards = [
        ("r = -0.916", "Nutritional Literacy vs. Hidden Hunger Severity", "Extremely strong inverse correlation (p < 0.001). Demonstrates that dietary knowledge is the single strongest suppressor of the hidden hunger paradox."),
        ("r = -0.532", "Nutritional Literacy vs. Anemia Prevalence", "Significant negative correlation. Higher awareness directly drives consumption of iron-rich greens and vitamin C absorption boosters."),
        ("r = -0.544", "Nutritional Literacy vs. Protein Deficit %", "Moderates carbohydrate overconsumption by diversifying daily portions toward sattu, pulses, dairy, and eggs.")
    ]

    for idx, (stat, title, desc) in enumerate(corr_cards):
        y = Inches(1.8 + idx * 1.6)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = BLUE
        card.line.width = Pt(1.5)

        tb_s = s8.shapes.add_textbox(Inches(1.0), y + Inches(0.15), Inches(2.2), Inches(1.1))
        p = tb_s.text_frame.paragraphs[0]
        p.text = stat
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = BLUE

        tb_d = s8.shapes.add_textbox(Inches(3.3), y + Inches(0.15), Inches(9.0), Inches(1.1))
        tf = tb_d.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 9: Personal Plate Calculator & Affordable Food Swaps
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Actionable Indian Kitchen Swaps (Zero Added Cost)")

    swaps = [
        ("Roasted Gram / Sattu Drink", "Swap 1 refined wheat roti for 1 glass of sattu drink (~Rs 10). Adds 12g bioavailable plant protein, 4g dietary fiber, and natural non-heme iron."),
        ("Vitamin C Lemon Acidification", "Squeeze fresh lemon over dal and green sabzi. Ascorbic acid converts ferric iron into absorbable ferrous iron, tripling bioavailable iron uptake."),
        ("Chai / Coffee Timing Delay", "Delay tea or coffee consumption by 45 minutes after meals. Prevents tannins and polyphenols from chelating and flushing out 60% of dietary iron."),
        ("Finger Millet (Ragi) Integration", "Replace one portion of white rice with ragi roti or porridge. Delivers 344 mg calcium per 100g, eradicating skeletal mineral deficiency."),
        ("Moringa (Drumstick Leaves)", "Add local moringa leaves to lentil curries and atta dough. Provides exceptionally dense bioavailable vitamin A, vitamin C, iron, and calcium.")
    ]

    for idx, (swap_name, swap_desc) in enumerate(swaps):
        y = Inches(1.8 + idx * 1.0)
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.85))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(236, 253, 245) # Soft Emerald
        card.line.color.rgb = RGBColor(167, 243, 208)

        tb = s9.shapes.add_textbox(Inches(1.0), y + Inches(0.08), Inches(11.3), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"✔ {swap_name}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(6, 95, 70)

        run = p.add_run()
        run.text = swap_desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 10: Technical Architecture & Live Deployment
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Software Artifacts, Power BI & GitHub Deployment")

    tech_cards = [
        ("Interactive Web Application", [
            "Hosted live on GitHub Pages with zero backend dependency.",
            "Leaflet.js 5-tier India Choropleth map with metric layer toggles.",
            "Chart.js interactive visualizations and demographic decompositions.",
            "Personalized 'Check Your Plate' calculator with real-time feedback."
        ]),
        ("Power BI Desktop Model", [
            "Clean Star Schema relational CSV exports with surrogate keys.",
            "Dashboard.pbix template with 12 production DAX measures.",
            "Dynamic Severity Alert Badges and Executive KPI cards.",
            "Complete modeling manual documented in POWERBI_GUIDE.md."
        ]),
        ("Python Pipeline Suite", [
            "data_cleaning.py: 6-step automated data engineering pipeline.",
            "Data_analysis.py: Statistical inference and EDA reporting engine.",
            "Data_visualisation.py: Publication-quality matplotlib suite.",
            "Full reproducible pipeline grounded on official ICMR-NIN 2024 data."
        ])
    ]

    for idx, (title, items) in enumerate(tech_cards):
        x = Inches(0.8 + idx * 3.95)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.75), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = s10.shapes.add_textbox(x + Inches(0.15), Inches(2.0), Inches(3.45), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = BLUE

        for it in items:
            p = tf.add_paragraph()
            p.text = f"• {it}"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 11: Summary & Submission Links
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    bg11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg11.fill.solid()
    bg11.fill.fore_color.rgb = NAVY
    bg11.line.color.rgb = NAVY

    tb11 = s11.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.0))
    tf11 = tb11.text_frame
    tf11.word_wrap = True

    p = tf11.paragraphs[0]
    p.text = "CONCLUSION & PROJECT SUBMISSION LINKS"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE

    links = [
        ("Public GitHub Repository", "https://github.com/yeshwanthkushi25-glitch/india-nutrient-deficiency-analytics"),
        ("Live Interactive Dashboard", "https://yeshwanthkushi25-glitch.github.io/india-nutrient-deficiency-analytics/"),
        ("Dataset & Modeling Manual", "Available in data/ and POWERBI_GUIDE.md inside the repository"),
        ("All-in-One Submission Package", "Final_Project_Submission_Google_Classroom.zip")
    ]

    for title, url in links:
        p = tf11.add_paragraph()
        p.text = f"\n{title}:"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = RGBColor(245, 158, 11)

        p = tf11.add_paragraph()
        p.text = url
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(147, 197, 253)

    pptx_path = os.path.join("google_classroom_submission", "Project_PPT.pptx")
    prs.save(pptx_path)
    print("Project PPT generated successfully at:", pptx_path)

if __name__ == "__main__":
    create_presentation()
