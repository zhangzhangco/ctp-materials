#!/usr/bin/env python3
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
    xml_str = minidom.parseString(tostring(root_element)).toprettyxml(indent="  ")
    with open(output_path, "w") as f:
        f.write(xml_str)

def main():
    parser = argparse.ArgumentParser(description="Generate a simple DCP from a single TIFF image.")
    parser.add_argument("--image", required=True, help="Path to the source TIFF image")
    parser.add_argument("--output", required=True, help="Output directory for the DCP")
    parser.add_argument("--duration", type=int, default=24, help="Duration in frames (default: 24)")
    parser.add_argument("--fps", type=int, default=24, help="Frame rate (default: 24)")
    parser.add_argument("--title", default="TEST_DCP", help="Title of the DCP (CPL annotation text)")
    parser.add_argument("--annotation", default="Created by CTP Tools", help="Annotation text")
    parser.add_argument("--issuer", default="CTP Tools", help="Issuer text")

    args = parser.parse_args()

    # Ensure output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Paths
    j2k_dir = os.path.join(args.output, "j2k_frames")
    if os.path.exists(j2k_dir):
        shutil.rmtree(j2k_dir)
    os.makedirs(j2k_dir)

    # 1. Convert TIFF to J2K
    print("Converting TIFF to J2K...")
    base_j2k = os.path.join(j2k_dir, "frame.j2c")
    # Cinema 2K profile: -p cinema2k
    # Explicitly set progression order to CPRL to avoid "Unrecognized progression order" error
    cmd_convert = ["image_to_j2k", "-p", "cinema2k", "-r", "CPRL", "-i", args.image, "-o", base_j2k] 
    
    print(f"Running: {' '.join(cmd_convert)}")
    try:
        subprocess.check_call(cmd_convert)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print("Attempting to print image_to_j2k help for debugging:")
        try:
            subprocess.call(["image_to_j2k", "-h"])
        except Exception as ex:
            print(f"Could not print help: {ex}")
        sys.exit(1)

    # 2. Create Frame Sequence
    print(f"Creating {args.duration} frames...")
    for i in range(args.duration):
        dst = os.path.join(j2k_dir, f"frame_{i:06d}.j2c")
        shutil.copy(base_j2k, dst)
    
    os.remove(base_j2k)

    # 3. Wrap into MXF
    print("Wrapping J2K frames into MXF...")
    video_mxf_uuid = uuid.uuid4()
    video_mxf_name = f"{video_mxf_uuid}.mxf"
    video_mxf_path = os.path.join(args.output, video_mxf_name)
    
    frame_files = sorted([os.path.join(j2k_dir, f) for f in os.listdir(j2k_dir) if f.endswith(".j2c")])
    
    cmd_wrap = ["asdcp-test", "-c", video_mxf_path] + frame_files
    run_command(cmd_wrap)

    shutil.rmtree(j2k_dir)

    # 4. Generate XMLs
    print("Generating XML files...")
    
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
    reel = SubElement(reel_list, "Reel")
    SubElement(reel, "Id").text = generate_uuid()
    
    asset_list = SubElement(reel, "AssetList")
    
    main_picture = SubElement(asset_list, "MainPicture")
    SubElement(main_picture, "Id").text = f"urn:uuid:{video_mxf_uuid}"
    SubElement(main_picture, "AnnotationText").text = video_mxf_name
    SubElement(main_picture, "EditRate").text = f"{args.fps} 1"
    SubElement(main_picture, "IntrinsicDuration").text = str(args.duration)
    SubElement(main_picture, "EntryPoint").text = "0"
    SubElement(main_picture, "Duration").text = str(args.duration)
    SubElement(main_picture, "Hash").text = get_file_hash_b64(video_mxf_path)
    SubElement(main_picture, "FrameRate").text = f"{args.fps} 1"
    SubElement(main_picture, "ScreenAspectRatio").text = "1.85"

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
    
    asset_cpl = SubElement(asset_list_pkl, "Asset")
    SubElement(asset_cpl, "Id").text = cpl_uuid
    SubElement(asset_cpl, "AnnotationText").text = cpl_name
    SubElement(asset_cpl, "Hash").text = get_file_hash_b64(cpl_path)
    SubElement(asset_cpl, "Size").text = str(get_file_size(cpl_path))
    SubElement(asset_cpl, "Type").text = "text/xml"
    
    asset_vid = SubElement(asset_list_pkl, "Asset")
    SubElement(asset_vid, "Id").text = f"urn:uuid:{video_mxf_uuid}"
    SubElement(asset_vid, "AnnotationText").text = video_mxf_name
    SubElement(asset_vid, "Hash").text = get_file_hash_b64(video_mxf_path)
    SubElement(asset_vid, "Size").text = str(get_file_size(video_mxf_path))
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
    
    asset_pkl_am = SubElement(asset_list_am, "Asset")
    SubElement(asset_pkl_am, "Id").text = pkl_uuid
    chunk_list_pkl = SubElement(asset_pkl_am, "ChunkList")
    chunk_pkl = SubElement(chunk_list_pkl, "Chunk")
    SubElement(chunk_pkl, "Path").text = pkl_name
    SubElement(chunk_pkl, "VolumeIndex").text = "1"
    
    asset_cpl_am = SubElement(asset_list_am, "Asset")
    SubElement(asset_cpl_am, "Id").text = cpl_uuid
    chunk_list_cpl = SubElement(asset_cpl_am, "ChunkList")
    chunk_cpl = SubElement(chunk_list_cpl, "Chunk")
    SubElement(chunk_cpl, "Path").text = cpl_name
    SubElement(chunk_cpl, "VolumeIndex").text = "1"
    
    asset_vid_am = SubElement(asset_list_am, "Asset")
    SubElement(asset_vid_am, "Id").text = f"urn:uuid:{video_mxf_uuid}"
    chunk_list_vid = SubElement(asset_vid_am, "ChunkList")
    chunk_vid = SubElement(chunk_list_vid, "Chunk")
    SubElement(chunk_vid, "Path").text = video_mxf_name
    SubElement(chunk_vid, "VolumeIndex").text = "1"

    am_path = os.path.join(args.output, "ASSETMAP.xml")
    create_xml_file(am, am_path)

    # --- VOLINDEX ---
    vi = Element("VolumeIndex", {"xmlns": am_ns})
    SubElement(vi, "Index").text = "1"
    vi_path = os.path.join(args.output, "VOLINDEX.xml")
    create_xml_file(vi, vi_path)

    print(f"DCP generated successfully at: {args.output}")

if __name__ == "__main__":
    main()
