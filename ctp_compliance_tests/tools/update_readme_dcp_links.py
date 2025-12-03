#!/usr/bin/env python3
"""
Script to add DCP download links to README.md tables.
This script reads the README, finds the material tables, and adds a DCP column with links to the release.
"""

import re
import sys

def update_readme_with_dcp_links(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the release tag and base URL
    release_tag = "latest-dcps"
    base_url = f"https://github.com/zhangzhangco/ctp-materials/releases/download/{release_tag}"
    
    # Function to generate DCP filename from material name
    def get_dcp_filename(material_name):
        # Convert material name to the format used in the workflow
        # e.g., "2K 2D 24 FPS Test" -> "2K-2D-24-FPS-TEST"
        clean_name = material_name.replace(" ", "-").upper()
        return f"DCP_{clean_name}.zip"
    
    # Pattern to match table rows (both English and Chinese)
    # Format: | # | Material Name | CTP Section | README | Image |
    # We want to add: | DCP |
    
    # First, update the header lines
    # English table header
    content = re.sub(
        r'(\| #  \| Material Name\s+\| CTP Section\s+\| README\s+\| Image\s+\|)',
        r'\1 DCP |',
        content
    )
    
    # Chinese table header  
    content = re.sub(
        r'(\| 序号 \| 素材名称\s+\| CTP 章节\s+\| README\s+\| 图片\s+\|)',
        r'\1 DCP |',
        content
    )
    
    # Update separator lines
    content = re.sub(
        r'(\| --+ \| --+ \| --+ \| --+ \| --+ \|)',
        r'\1 ---- |',
        content
    )
    
    # Now update each data row
    # Pattern: | number | Material Name | ... | ... | [link](path) |
    # We need to extract the material name and add DCP link
    
    def add_dcp_column(match):
        full_line = match.group(0)
        # Extract material name (2nd column)
        parts = full_line.split('|')
        if len(parts) >= 6:
            material_name = parts[2].strip()
            dcp_filename = get_dcp_filename(material_name)
            dcp_url = f"{base_url}/{dcp_filename}"
            # Add DCP column before the final |
            return full_line.rstrip() + f" [📦 DCP]({dcp_url}) |\n"
        return full_line
    
    # Match table rows (starting with | number |)
    content = re.sub(
        r'^\|(\s*\d+\s*)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|\s*$',
        add_dcp_column,
        content,
        flags=re.MULTILINE
    )
    
    # Write back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {readme_path} with DCP download links")

if __name__ == "__main__":
    readme_path = "README.md"
    if len(sys.argv) > 1:
        readme_path = sys.argv[1]
    
    update_readme_with_dcp_links(readme_path)
