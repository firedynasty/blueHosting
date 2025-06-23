#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import argparse
from pathlib import Path

def is_video_file(filename):
    """Check if file is a supported video format."""
    video_extensions = {'.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', '.m4v'}
    return Path(filename).suffix.lower() in video_extensions

def extract_video_info(file_path):
    """Extract metadata and info from video file."""
    file_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(file_name)[0]
    
    # Try to extract meaningful title from filename
    title = name_without_ext.replace('_', ' ').replace('-', ' ')
    title = re.sub(r'\b\w', lambda m: m.group(0).upper(), title)  # Title case
    
    # Clean up common patterns
    title = re.sub(r'\b(VID|MOV|Video|Movie)\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+', ' ', title).strip()
    
    if not title:
        title = f"Video {name_without_ext}"
    
    return {
        'filename': file_name,
        'title': title,
        'path': f"videos/{file_name}"
    }

def natural_sort_key(filename):
    """Sort filenames naturally (handle numbers correctly)."""
    parts = re.split(r'(\d+)', filename.lower())
    return [int(part) if part.isdigit() else part for part in parts]

def process_videos_directory(videos_dir, output_path=None):
    """Process all video files in the given directory."""
    if not os.path.exists(videos_dir):
        print(f"Error: Directory '{videos_dir}' does not exist!")
        return None
    
    # Get all video files
    all_files = os.listdir(videos_dir)
    video_files = [f for f in all_files if is_video_file(f)]
    
    if not video_files:
        print(f"No video files found in '{videos_dir}'")
        return None
    
    # Sort files naturally
    video_files.sort(key=natural_sort_key)
    
    # Process each video
    videos_data = []
    video_paths = []
    
    for file_name in video_files:
        file_path = os.path.join(videos_dir, file_name)
        video_info = extract_video_info(file_path)
        
        videos_data.append(video_info)
        video_paths.append(video_info['path'])
    
    # Generate the JavaScript code
    js_code = generate_video_gallery_js(video_paths, videos_data)
    
    # Determine output path
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "video_array.js")
    
    # Save to JS file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print(f"Generated video gallery data with {len(video_files)} videos:")
    for i, video in enumerate(videos_data, 1):
        print(f"  {i:2d}. {video['title']} ({video['filename']})")
    print(f"\nSaved to: {output_path}")
    
    return videos_data

def generate_video_gallery_js(video_paths, videos_data):
    """Generate JavaScript code for the video gallery."""
    
    videos_array = json.dumps(video_paths, indent=4)
    videos_info = json.dumps(videos_data, ensure_ascii=False, indent=4)
    
    js_code = f"""// Auto-generated video gallery data
// Videos found: {len(video_paths)}

// Video array for use in HTML
const videoArray = {videos_array};

// Detailed video information (titles, filenames, etc.)
const videosInfo = {videos_info};
"""
    
    return js_code

def main():
    parser = argparse.ArgumentParser(description='Generate video gallery data from a directory of videos.')
    parser.add_argument('-i', '--input', default='./videos',
                        help='Directory containing the video files (default: ./videos)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output JavaScript file path (default: ./video_array.js)')
    parser.add_argument('--formats', action='store_true',
                        help='Show supported video formats and exit')
    
    args = parser.parse_args()
    
    if args.formats:
        print("Supported video formats:")
        formats = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', '.m4v']
        for fmt in formats:
            print(f"  {fmt}")
        return
    
    # Process the videos directory
    process_videos_directory(args.input, args.output)

if __name__ == "__main__":
    main()
