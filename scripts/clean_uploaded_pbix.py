import zipfile
import os

src = r"C:\Users\yeshwanth\.gemini\antigravity\brain\f4b49de3-8c46-4442-b9c2-ec1fbe7b2d3c\.user_uploaded\media_1794065998767_36f5f12c.pbix"
dst = r"C:\Users\yeshwanth\OneDrive\Desktop\Dashboard_Clean.pbix"

with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(dst, "w") as zout:
    for item in zin.infolist():
        if item.filename == "SecurityBindings":
            continue
        data = zin.read(item.filename)
        if item.filename == "[Content_Types].xml":
            text = data.decode("utf-8")
            text = text.replace('<Override PartName="/SecurityBindings" ContentType="" />', '')
            data = text.encode("utf-8")
        
        new_item = zipfile.ZipInfo(item.filename)
        if item.filename == "DataModel":
            new_item.compress_type = zipfile.ZIP_STORED
        else:
            new_item.compress_type = item.compress_type
        new_item.flag_bits = item.flag_bits
        zout.writestr(new_item, data)

size = os.path.getsize(dst)
print(f"Created: {dst} | Size: {size} bytes ({size/(1024*1024):.2f} MB)")
