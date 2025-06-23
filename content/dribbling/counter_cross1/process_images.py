#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import argparse
from pathlib import Path

def is_image_file(filename):
    """Check if file is a supported image format."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg'}
    return Path(filename).suffix.lower() in image_extensions

def extract_image_info(file_path):
    """Extract metadata and info from image file."""
    file_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(file_name)[0]
    
    # Try to extract meaningful title from filename
    # Remove common prefixes/suffixes and format nicely
    title = name_without_ext.replace('_', ' ').replace('-', ' ')
    title = re.sub(r'\b\w', lambda m: m.group(0).upper(), title)  # Title case
    
    # Clean up common patterns
    title = re.sub(r'\b(IMG|DSC|Photo|Picture)\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+', ' ', title).strip()
    
    if not title:
        title = f"Image {name_without_ext}"
    
    return {
        'filename': file_name,
        'title': title,
        'path': f"images/{file_name}"
    }

def natural_sort_key(filename):
    """Sort filenames naturally (handle numbers correctly)."""
    # Split filename into text and number parts
    parts = re.split(r'(\d+)', filename.lower())
    # Convert numeric parts to integers for proper sorting
    return [int(part) if part.isdigit() else part for part in parts]

def process_images_directory(images_dir, output_path=None):
    """Process all image files in the given directory."""
    if not os.path.exists(images_dir):
        print(f"Error: Directory '{images_dir}' does not exist!")
        return None
    
    # Get all image files
    all_files = os.listdir(images_dir)
    image_files = [f for f in all_files if is_image_file(f)]
    
    if not image_files:
        print(f"No image files found in '{images_dir}'")
        return None
    
    # Sort files naturally
    image_files.sort(key=natural_sort_key)
    
    # Process each image
    images_data = []
    image_paths = []
    
    for file_name in image_files:
        file_path = os.path.join(images_dir, file_name)
        image_info = extract_image_info(file_path)
        
        images_data.append(image_info)
        image_paths.append(image_info['path'])
    
    # Generate the JavaScript code
    js_code = generate_gallery_js(image_paths, images_data)
    
    # Determine output path
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "gallery_images.js")
    
    # Save to JS file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print(f"Generated image gallery data with {len(image_files)} images:")
    for i, img in enumerate(images_data, 1):
        print(f"  {i:2d}. {img['title']} ({img['filename']})")
    print(f"\nSaved to: {output_path}")
    
    return images_data

def generate_gallery_js(image_paths, images_data):
    """Generate JavaScript code for the image gallery."""
    
    # Create the images array
    images_array = json.dumps(image_paths, indent=4)
    
    # Create detailed image info (optional, for future enhancements)
    images_info = json.dumps(images_data, ensure_ascii=False, indent=4)
    
    js_code = f"""// Auto-generated image gallery data
// Images found: {len(image_paths)}

// Simple array of image paths for the gallery
const images = {images_array};

// Detailed image information (titles, filenames, etc.)
const imagesInfo = {images_info};

// Instructions for use:
// 1. Copy the 'images' array above
// 2. Replace the existing 'images' array in your HTML file
// 3. Your gallery will automatically load these images

// Example of how to use in your HTML:
/*
Replace this line in your HTML JavaScript:
const images = [
    'https://picsum.photos/800/500?random=1',
    // ... other sample images
];

With this:
const images = {json.dumps(image_paths, indent=0).replace(chr(10), chr(10) + '    ')};
*/
"""
    
    return js_code

def generate_html_file(images_data, output_dir="."):
    """Generate a complete HTML file with the images."""
    image_paths = [img['path'] for img in images_data]
    images_array_str = json.dumps(image_paths, indent=12)
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Image Gallery</title>
    <style>
        /* Include your CSS styles here */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            min-height: 100vh;
            color: white;
            margin: 0;
            padding: 0;
        }}
        
        /* Add the rest of your CSS styles here... */
    </style>
</head>
<body>
    <!-- Your HTML structure here -->
    
    <script>
        // Your images array
        const images = {images_array_str};
        
        // Your JavaScript code here...
    </script>
</body>
</html>"""
    
    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Generated complete HTML file: {html_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate image gallery data from a directory of images.')
    parser.add_argument('-i', '--input', default='./images',
                        help='Directory containing the image files (default: ./images)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output JavaScript file path (default: ./gallery_images.js)')
    parser.add_argument('--html', action='store_true',
                        help='Also generate a complete HTML file')
    parser.add_argument('--formats', action='store_true',
                        help='Show supported image formats and exit')
    
    args = parser.parse_args()
    
    if args.formats:
        print("Supported image formats:")
        formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg']
        for fmt in formats:
            print(f"  {fmt}")
        return
    
    # Process the images directory
    images_data = process_images_directory(args.input, args.output)
    
    if images_data and args.html:
        generate_html_file(images_data)

if __name__ == "__main__":
    main()
