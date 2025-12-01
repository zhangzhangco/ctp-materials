import os
import re

BASE_DIR = "/Users/zhangxin/ctp-materials/test_materials"
GITHUB_BASE_URL = "." # Relative paths work best for READMEs

def get_ctp_section(readme_path):
    if not os.path.exists(readme_path):
        return "N/A"
    with open(readme_path, 'r') as f:
        content = f.read()
    # Look for "## 1. 来源 (Location)" followed by content
    match = re.search(r"## 1\. 来源 \(Location\)\s+(.*?)\s+##", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "N/A"

def get_tiff_path(material_dir):
    # Find tiff or zip in dir
    files = os.listdir(os.path.join(BASE_DIR, material_dir))
    tiffs = [f for f in files if f.endswith('.tiff')]
    zips = [f for f in files if f.endswith('.zip')]
    
    if tiffs:
        return tiffs[0]
    if zips:
        return zips[0]
    return None

materials = []
dirs = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and d != "__pycache__"])

for i, d in enumerate(dirs):
    readme_path = os.path.join(BASE_DIR, d, "README.md")
    ctp = get_ctp_section(readme_path)
    tiff = get_tiff_path(d)
    
    # URL-encode the directory name for links
    encoded_d = d.replace(' ', '%20')

    materials.append({
        "index": i + 1,
        "name": d,
        "ctp": ctp,
        "readme_link": f"./test_materials/{encoded_d}/README.md",
        "tiff_link": f"./test_materials/{encoded_d}/{tiff}" if tiff else ""
    })

# Generate Markdown Table
print("### Material List")
print("| # | Material Name | CTP Section | README | Image |")
print("|---|---|---|---|---|")
for m in materials:
    link_text = "ZIP" if m['tiff_link'].endswith('.zip') else "TIFF"
    tiff_md = f"[{link_text}]({m['tiff_link']})" if m['tiff_link'] else "Pending"
    name = m['name'].replace("|", "\|")
    print(f"| {m['index']} | {name} | {m['ctp']} | [View]({m['readme_link']}) | {tiff_md} |")

print("\n\n")
print("### 素材列表")
print("| 序号 | 素材名称 | CTP 章节 | README | 图片 |")
print("|---|---|---|---|---|")
for m in materials:
    link_text = "ZIP" if m['tiff_link'].endswith('.zip') else "TIFF"
    tiff_md = f"[{link_text}]({m['tiff_link']})" if m['tiff_link'] else "Pending"
    name = m['name'].replace("|", "\|")
    print(f"| {m['index']} | {name} | {m['ctp']} | [查看]({m['readme_link']}) | {tiff_md} |")
