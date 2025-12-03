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
    
    # Process line by line
    lines = content.split('\n')
    new_lines = []
    in_table = False
    
    for i, line in enumerate(lines):
        # Detect table header
        if re.match(r'^\|\s*#', line) or re.match(r'^\|\s*序号', line):
            in_table = True
            # Check if DCP column already exists
            if '| DCP |' not in line and '| DCP' not in line:
                # Add DCP header
                new_line = line.rstrip() + ' DCP |'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        # Detect separator line
        elif in_table and re.match(r'^\|\s*--', line):
            if '| ---- |' not in line and not line.endswith('---- |'):
                new_line = line.rstrip() + ' ---- |'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        # Detect data rows
        elif in_table and re.match(r'^\|\s*\d+', line):
            parts = line.split('|')
            if len(parts) >= 6:
                # Check if DCP link already exists
                if '[📦 DCP]' not in line:
                    material_name = parts[2].strip()
                    dcp_filename = get_dcp_filename(material_name)
                    dcp_url = f"{base_url}/{dcp_filename}"
                    
                    # Add status badge using shields.io endpoint
                    # The badge will fetch status from the JSON file in the release
                    badge_json_url = f"{base_url}/{material_name.replace(' ', '-').upper()}.json"
                    badge_url = f"https://img.shields.io/endpoint?url={badge_json_url}"
                    
                    new_line = line.rstrip() + f' ![Status]({badge_url}) [📦 DCP]({dcp_url}) |'
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        # Detect end of table (empty line or non-table content)
        elif in_table and line.strip() == '':
            in_table = False
            new_lines.append(line)
        else:
            new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # Write back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {readme_path} with DCP download links")

if __name__ == "__main__":
    readme_path = "README.md"
    if len(sys.argv) > 1:
        readme_path = sys.argv[1]
    
    update_readme_with_dcp_links(readme_path)
