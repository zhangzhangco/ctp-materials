#!/usr/bin/env python3
import os
import json
import re
import argparse

def parse_metadata(dirname):
    """
    Parses metadata from the directory name.
    """
    metadata = {
        "resolution": "2K",
        "fps": 24,
        "audio": "MOS",
        "dimension": "2D",
        "standard": "SMPTE",
        "aspect_ratio": "F", # Default Flat
        "content_type": "TST",
        "territory": "XX-XX",
        "rating": "INT-TD",
        "studio": "CTP",
        "facility": "CTP",
        "package_type": "OV"
    }

    # Resolution
    if "4K" in dirname:
        metadata["resolution"] = "4K"
    
    # FPS
    fps_match = re.search(r'(\d+)\s*FPS', dirname, re.IGNORECASE)
    if fps_match:
        metadata["fps"] = int(fps_match.group(1))
    
    # Dimension
    if "3D" in dirname or "Stereoscopic" in dirname:
        metadata["dimension"] = "3D"
    
    # Aspect Ratio
    if "Scope" in dirname:
        metadata["aspect_ratio"] = "S"
    elif "Flat" in dirname:
        metadata["aspect_ratio"] = "F"
    elif "Full" in dirname:
        metadata["aspect_ratio"] = "C" # Full Container usually maps to C or F depending on usage, let's use C (Full Container) or just F/S. 
        # ISDCF: F (1.85), S (2.39), C (Full Container 1.90)
        metadata["aspect_ratio"] = "C"

    return metadata

def discover_tests(test_materials_dir):
    tests = []
    
    if not os.path.exists(test_materials_dir):
        return tests

    for item in os.listdir(test_materials_dir):
        item_path = os.path.join(test_materials_dir, item)
        
        if os.path.isdir(item_path) and not item.startswith('.'):
            # Check for content
            # Priority: ZIP > TIFF sequence > Single TIFF
            
            input_file = None
            input_type = None
            
            # Look for ZIP
            zips = [f for f in os.listdir(item_path) if f.lower().endswith('.zip')]
            image_count = 0
            
            if zips:
                input_file = os.path.join(item_path, zips[0])
                
                # Count images inside ZIP to determine if multi-reel
                import zipfile
                try:
                    with zipfile.ZipFile(input_file, 'r') as zf:
                        image_count = sum(1 for name in zf.namelist() 
                                        if name.lower().endswith(('.tiff', '.tif')) 
                                        and not name.startswith('__MACOSX') 
                                        and not os.path.basename(name).startswith('.'))
                except:
                    image_count = 1
                
                # Determine input type based on image count
                if image_count >= 2:
                    input_type = "multi_reel"
                else:
                    input_type = "zip"
            else:
                # Look for TIFFs
                tiffs = [f for f in os.listdir(item_path) if f.lower().endswith('.tiff') or f.lower().endswith('.tif')]
                if tiffs:
                    # Sort to ensure sequence order
                    tiffs.sort()
                    image_count = len(tiffs)
                    if len(tiffs) >= 2:
                        # Multiple TIFFs: treat as multi-reel (each image = 5 sec)
                        input_file = item_path  # Pass directory
                        input_type = "multi_reel"
                    else:
                        input_file = os.path.join(item_path, tiffs[0])
                        input_type = "image"
            
            if input_file:
                metadata = parse_metadata(item)
                
                # Construct Title
                # Structure: Title_ContentType_AspectRatio_Language_Territory_Rating_Audio_Resolution_Studio_Date_Facility_Standard_PackageType
                # We need to sanitize the Title part (directory name)
                clean_name = item.replace(" ", "-").upper()
                
                # We will construct the full title in the workflow or here. 
                # Let's pass the components and let the workflow or script assemble it.
                # Actually, generating the title here is easier.
                
                # Date will be generated at runtime
                
                test_info = {
                    "name": item,
                    "input_path": input_file,
                    "input_type": input_type,
                    "image_count": image_count if input_type == "multi_reel" else 1,
                    "fps": metadata["fps"],
                    "resolution": metadata["resolution"],
                    "audio": metadata["audio"],
                    "clean_name": clean_name,
                    "aspect_ratio": metadata["aspect_ratio"]
                }
                tests.append(test_info)

    return tests

def main():
    parser = argparse.ArgumentParser(description="Discover tests and generate matrix JSON")
    parser.add_argument("--dir", required=True, help="Test materials directory")
    args = parser.parse_args()
    
    tests = discover_tests(args.dir)
    
    # Output JSON to stdout
    print(json.dumps(tests))

if __name__ == "__main__":
    main()
