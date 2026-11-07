import zipfile
import json
import os

src = r"C:\Users\yeshwanth\Downloads\dav lab.pbix"
dst = r"google_classroom_submission\Dashboard.pbix"

with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(dst, "w") as zout:
    for item in zin.infolist():
        if item.filename == "SecurityBindings":
            continue
        data = zin.read(item.filename)
        
        if item.filename == "[Content_Types].xml":
            text = data.decode("utf-8")
            text = text.replace('<Override PartName="/SecurityBindings" ContentType="" />', '')
            data = text.encode("utf-8")
            
        elif "page.json" in item.filename:
            # Change page displayName
            try:
                j = json.loads(data.decode("utf-8"))
                j["displayName"] = "Nutrient Deficiency Analytics"
                data = json.dumps(j).encode("utf-8")
            except:
                pass
                
        elif "6b20688bee01d411c1e5" in item.filename:
            # Main Banner Textbox
            j = json.loads(data.decode("utf-8"))
            j["visual"]["objects"]["general"][0]["properties"]["paragraphs"] = [
                {
                    "textRuns": [
                        {
                            "value": "NUTRIENT DEFICIENCY & THE HIDDEN HUNGER PARADOX IN INDIA",
                            "textStyle": {"fontSize": "26pt", "fontWeight": "bold", "color": "#1e3a8a"}
                        }
                    ],
                    "horizontalTextAlignment": "center"
                },
                {
                    "textRuns": [
                        {
                            "value": "SR UNIVERSITY • DEPT OF CSE (CYBER SECURITY) • DATA ANALYTICS CAPSTONE",
                            "textStyle": {"fontSize": "13pt", "color": "#2563eb"}
                        }
                    ],
                    "horizontalTextAlignment": "center"
                },
                {
                    "textRuns": [
                        {
                            "value": "Team: Yeshwanth (2503A53005) | V Laxmi Prasad (2503A53006) | MD Zaheer Pasha (2503A53016)",
                            "textStyle": {"fontSize": "11pt", "color": "#475569"}
                        }
                    ],
                    "horizontalTextAlignment": "center"
                }
            ]
            data = json.dumps(j).encode("utf-8")

        new_item = zipfile.ZipInfo(item.filename)
        new_item.compress_type = item.compress_type
        new_item.flag_bits = item.flag_bits
        zout.writestr(new_item, data)

size = os.path.getsize(dst)
print(f"Successfully generated project Dashboard.pbix! Size: {size} bytes ({size/1024:.1f} KB)")
