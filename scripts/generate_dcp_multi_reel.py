#!/usr/bin/env python3
"""
Multi-Reel DCP Generator
Generates a DCP with multiple reels from multiple images.
Each image becomes a 5-second (120 frame) reel.
"""
import argparse
import os
import subprocess
import shutil
import uuid
import hashlib
import datetime
import sys
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def generate_uuid():
    return f"urn:uuid:{uuid.uuid4()}"

def get_file_hash(filepath):
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.digest()

import base64
def get_file_hash_b64(filepath):
    return base64.b64encode(get_file_hash(filepath)).decode('utf-8')

def get_file_size(filepath):
    return os.path.getsize(filepath)

def create_xml_file(root_element, output_path):
    xml_str = tostring(root_element, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    
    def clean_whitespace(node):
        to_remove = []
        for child in node.childNodes:
            if child.nodeType == minidom.Node.TEXT_NODE and not child.data.strip():
                to_remove.append(child)
            elif child.nodeType == minidom.Node.ELEMENT_NODE:
                clean_whitespace(child)
        for child in to_remove:
            node.removeChild(child)
            
    clean_whitespace(dom)
    
    with open(output_path, "wb") as f:
        f.write(dom.toprettyxml(indent="  ", encoding="UTF-8"))

def main():
    parser = argparse.ArgumentParser(description="Generate multi-reel DCP from multiple images")
    parser.add_argument("--image", required=True, help="Path to ZIP file or directory containing images")
    parser.add_argument("--output", required=True, help="Output directory for the DCP")
    parser.add_argument("--fps", type=int, default=24, help="Frame rate (default: 24)")
    parser.add_argument("--title", required=True, help="Title of the DCP")
    parser.add_argument("--annotation", default="Created by CTP Tools", help="Annotation text")
    parser.add_argument("--issuer", default="CTP Tools", help="Issuer text")

    args = parser.parse_args()

    # Ensure output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Handle input: ZIP or directory
    temp_extract_dir = None
    input_files = []
    
    if args.image.lower().endswith(".zip"):
        # Extract ZIP
        temp_extract_dir = os.path.join(args.output, "temp_extract")
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        
        print(f"Extracting ZIP file: {args.image}")
        os.makedirs(temp_extract_dir)
        subprocess.check_call(["unzip", "-q", args.image, "-d", temp_extract_dir])
        
        # Find all TIFFs
        for root, dirs, files in os.walk(temp_extract_dir):
            # Ignore __MACOSX directory
            if "__MACOSX" in root:
                continue
                
            for f in files:
                # Ignore hidden files (like ._*)
                if f.startswith('.'):
                    continue
                    
                if f.lower().endswith(('.tiff', '.tif')):
                    input_files.append(os.path.join(root, f))
    
    elif os.path.isdir(args.image):
        # Directory with TIFFs
        print(f"Processing directory: {args.image}")
        for f in os.listdir(args.image):
            if f.startswith('.'):
                continue
            if f.lower().endswith(('.tiff', '.tif')):
                input_files.append(os.path.join(args.image, f))
    
    else:
        print(f"Error: Input must be a ZIP file or directory, got: {args.image}")
        sys.exit(1)
    
    if not input_files:
        print("Error: No TIFF files found in ZIP.")
        sys.exit(1)
        
    input_files.sort()
    
    print(f"Found {len(input_files)} images - creating {len(input_files)} reels")
    
    # Determine J2K parameters using opj_compress DCI profiles
    j2k_params = ["-OutFor", "j2c", "-threads", "16"]
    
    if "4K" in args.title or "4k" in args.title:
        # 4K DCI
        j2k_params += ["-cinema4K"]
    else:
        # 2K DCI
        if args.fps == 48:
            j2k_params += ["-cinema2K", "48", "-GuardBits", "1"]
        else:
            j2k_params += ["-cinema2K", "24", "-GuardBits", "1"]
    
    # Process each image as a reel
    reels_info = []
    
    for reel_idx, img_path in enumerate(input_files):
        print(f"\n=== Processing Reel {reel_idx + 1}/{len(input_files)} ===")
        
        # Create reel-specific J2K directory
        reel_j2k_dir = os.path.join(args.output, f"j2k_reel_{reel_idx}")
        if os.path.exists(reel_j2k_dir):
            shutil.rmtree(reel_j2k_dir)
        os.makedirs(reel_j2k_dir)
        
        # Convert TIFF to J2K (base frame)
        base_j2k = os.path.join(reel_j2k_dir, "base_frame.j2c")
        cmd_convert = ["opj_compress", "-i", img_path, "-o", base_j2k] + j2k_params
        print(f"Converting: {os.path.basename(img_path)}")
        subprocess.check_call(cmd_convert, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Create 120 frames (5 seconds @ 24fps)
        duration = 120
        for i in range(duration):
            dst = os.path.join(reel_j2k_dir, f"frame_{i:06d}.j2c")
            shutil.copy(base_j2k, dst)
        os.remove(base_j2k)
        
        # Wrap into MXF
        video_mxf_uuid = uuid.uuid4()
        video_mxf_name = f"{video_mxf_uuid}.mxf"
        video_mxf_path = os.path.join(args.output, video_mxf_name)
        
        cmd_wrap = ["asdcp-test", "-L", "-a", str(video_mxf_uuid), "-c", video_mxf_path, reel_j2k_dir]
        run_command(cmd_wrap)
        
        # Clean up J2K files
        shutil.rmtree(reel_j2k_dir)
        
        # Store reel info
        reels_info.append({
            "mxf_uuid": video_mxf_uuid,
            "mxf_name": video_mxf_name,
            "mxf_path": video_mxf_path,
            "duration": duration,
            "annotation": os.path.basename(img_path)
        })
    
    # Clean up temp extraction dir (only if we extracted a ZIP)
    if temp_extract_dir and os.path.exists(temp_extract_dir):
        shutil.rmtree(temp_extract_dir)
    
    # Generate XML metadata
    print("\nGenerating XML files...")
    
    cpl_uuid = generate_uuid()
    pkl_uuid = generate_uuid()
    assetmap_uuid = generate_uuid()
    
    current_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    # --- CPL ---
    cpl_ns = "http://www.smpte-ra.org/schemas/429-7/2006/CPL"
    cpl = Element("CompositionPlaylist", {"xmlns": cpl_ns})
    SubElement(cpl, "Id").text = cpl_uuid
    SubElement(cpl, "AnnotationText").text = args.title
    SubElement(cpl, "IssueDate").text = current_time
    SubElement(cpl, "Issuer").text = args.issuer
    SubElement(cpl, "Creator").text = "dci-ctp-tools-gen"
    SubElement(cpl, "ContentTitleText").text = args.title
    
    content_kind = SubElement(cpl, "ContentKind")
    content_kind.text = "test"
    
    content_version = SubElement(cpl, "ContentVersion")
    SubElement(content_version, "Id").text = f"urn:uri:{cpl_uuid}"
    SubElement(content_version, "LabelText").text = f"{args.title}_v1"

    SubElement(cpl, "RatingList")
    
    reel_list = SubElement(cpl, "ReelList")
    
    # Add each reel
    for reel_info in reels_info:
        reel = SubElement(reel_list, "Reel")
        SubElement(reel, "Id").text = generate_uuid()
        
        asset_list = SubElement(reel, "AssetList")
        
        main_picture = SubElement(asset_list, "MainPicture")
        SubElement(main_picture, "Id").text = f"urn:uuid:{reel_info['mxf_uuid']}"
        SubElement(main_picture, "AnnotationText").text = reel_info["annotation"]
        SubElement(main_picture, "EditRate").text = f"{args.fps} 1"
        SubElement(main_picture, "IntrinsicDuration").text = str(reel_info["duration"])
        SubElement(main_picture, "EntryPoint").text = "0"
        SubElement(main_picture, "Duration").text = str(reel_info["duration"])
        SubElement(main_picture, "Hash").text = get_file_hash_b64(reel_info["mxf_path"])
        SubElement(main_picture, "FrameRate").text = f"{args.fps} 1"
        SubElement(main_picture, "ScreenAspectRatio").text = "190 100"

    cpl_name = f"CPL_{uuid.uuid4()}.xml"
    cpl_path = os.path.join(args.output, cpl_name)
    create_xml_file(cpl, cpl_path)

    # --- PKL ---
    pkl_ns = "http://www.smpte-ra.org/schemas/429-8/2007/PKL"
    pkl = Element("PackingList", {"xmlns": pkl_ns})
    SubElement(pkl, "Id").text = pkl_uuid
    SubElement(pkl, "AnnotationText").text = args.title
    SubElement(pkl, "IssueDate").text = current_time
    SubElement(pkl, "Issuer").text = args.issuer
    SubElement(pkl, "Creator").text = "dci-ctp-tools-gen"
    
    asset_list_pkl = SubElement(pkl, "AssetList")
    
    # CPL asset
    asset_cpl = SubElement(asset_list_pkl, "Asset")
    SubElement(asset_cpl, "Id").text = cpl_uuid
    SubElement(asset_cpl, "AnnotationText").text = cpl_name
    SubElement(asset_cpl, "Hash").text = get_file_hash_b64(cpl_path)
    SubElement(asset_cpl, "Size").text = str(get_file_size(cpl_path))
    SubElement(asset_cpl, "Type").text = "text/xml"
    
    # MXF assets
    for reel_info in reels_info:
        asset_vid = SubElement(asset_list_pkl, "Asset")
        SubElement(asset_vid, "Id").text = f"urn:uuid:{reel_info['mxf_uuid']}"
        SubElement(asset_vid, "AnnotationText").text = reel_info["mxf_name"]
        SubElement(asset_vid, "Hash").text = get_file_hash_b64(reel_info["mxf_path"])
        SubElement(asset_vid, "Size").text = str(get_file_size(reel_info["mxf_path"]))
        SubElement(asset_vid, "Type").text = "application/mxf"

    pkl_name = f"PKL_{uuid.uuid4()}.xml"
    pkl_path = os.path.join(args.output, pkl_name)
    create_xml_file(pkl, pkl_path)

    # --- ASSETMAP ---
    am_ns = "http://www.smpte-ra.org/schemas/429-9/2007/AM"
    am = Element("AssetMap", {"xmlns": am_ns})
    SubElement(am, "Id").text = assetmap_uuid
    SubElement(am, "AnnotationText").text = args.title
    SubElement(am, "Creator").text = "dci-ctp-tools-gen"
    SubElement(am, "VolumeCount").text = "1"
    SubElement(am, "IssueDate").text = current_time
    SubElement(am, "Issuer").text = args.issuer
    
    asset_list_am = SubElement(am, "AssetList")
    
    # PKL
    asset_pkl_am = SubElement(asset_list_am, "Asset")
    SubElement(asset_pkl_am, "Id").text = pkl_uuid
    SubElement(asset_pkl_am, "PackingList").text = "true"
    chunk_list_pkl = SubElement(asset_pkl_am, "ChunkList")
    chunk_pkl = SubElement(chunk_list_pkl, "Chunk")
    SubElement(chunk_pkl, "Path").text = pkl_name
    SubElement(chunk_pkl, "VolumeIndex").text = "1"
    
    # CPL
    asset_cpl_am = SubElement(asset_list_am, "Asset")
    SubElement(asset_cpl_am, "Id").text = cpl_uuid
    chunk_list_cpl = SubElement(asset_cpl_am, "ChunkList")
    chunk_cpl = SubElement(chunk_list_cpl, "Chunk")
    SubElement(chunk_cpl, "Path").text = cpl_name
    SubElement(chunk_cpl, "VolumeIndex").text = "1"
    
    # MXF files
    for reel_info in reels_info:
        asset_vid_am = SubElement(asset_list_am, "Asset")
        SubElement(asset_vid_am, "Id").text = f"urn:uuid:{reel_info['mxf_uuid']}"
        chunk_list_vid = SubElement(asset_vid_am, "ChunkList")
        chunk_vid = SubElement(chunk_list_vid, "Chunk")
        SubElement(chunk_vid, "Path").text = reel_info["mxf_name"]
        SubElement(chunk_vid, "VolumeIndex").text = "1"

    am_path = os.path.join(args.output, "ASSETMAP.xml")
    create_xml_file(am, am_path)

    # --- VOLINDEX ---
    vi = Element("VolumeIndex", {"xmlns": am_ns})
    SubElement(vi, "Index").text = "1"
    vi_path = os.path.join(args.output, "VOLINDEX.xml")
    create_xml_file(vi, vi_path)

    print(f"\n✅ Multi-reel DCP generated successfully at: {args.output}")
    print(f"   Total reels: {len(reels_info)}")
    print(f"   Total duration: {len(reels_info) * 120 / args.fps:.1f} seconds")

if __name__ == "__main__":
    main()
