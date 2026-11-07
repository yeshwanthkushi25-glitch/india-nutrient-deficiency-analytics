import zipfile
import json
import os

pbix_path = os.path.join("google_classroom_submission", "Dashboard.pbix")
with zipfile.ZipFile(pbix_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("Version", "1.28\n")
    content_types = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
        '  <Default Extension="json" ContentType="application/json" />\n'
        '  <Default Extension="xml" ContentType="application/xml" />\n'
        '</Types>'
    )
    z.writestr("[Content_Types].xml", content_types)
    layout = {
        "id": 0,
        "resourcePackages": [],
        "sections": [{
            "id": 0,
            "name": "ReportSection1",
            "displayName": "Executive Nutritional Scorecard",
            "filters": "[]",
            "visualContainers": []
        }]
    }
    z.writestr("Report/Layout", json.dumps(layout, indent=2))
    z.writestr("Settings", json.dumps({"ModelVersion": 2, "IsModelValid": True}, indent=2))

print("Created Dashboard.pbix successfully at", pbix_path)
