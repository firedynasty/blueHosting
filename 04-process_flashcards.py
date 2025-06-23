#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import csv
import argparse
import subprocess
import sys

def extract_title_from_file(file_path):
    """Extract a title from the file content or file name."""
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    return f"{base_name}"

def process_flashcard_file(file_path):
    """Process a flashcard file and extract its content in table format."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Parse the CSV-like content
    lines = content.split('\n')
    table_data = []
    
    # Skip header line if it exists (contains "Chinese,English" or similar)
    start_index = 0
    if lines and ('Chinese' in lines[0] and 'English' in lines[0]):
        start_index = 1
    
    for line in lines[start_index:]:
        line = line.strip()
        if not line:
            continue
            
        # Split by comma - handle both 2-column and 3-column formats
        parts = [part.strip() for part in line.split(',')]
        
        if len(parts) == 2:
            # 2-column format: Chinese,English
            chinese, english = parts
            table_data.append(['1', chinese, english])
        elif len(parts) == 3:
            # 3-column format: Active,Chinese,English
            active, chinese, english = parts
            # Ensure active is either '1' or '2'
            if active not in ['1', '2']:
                active = '1'
            table_data.append([active, chinese, english])
        elif len(parts) > 3:
            # More than 3 columns - take first 3
            active = parts[0] if parts[0] in ['1', '2'] else '1'
            chinese = parts[1] if len(parts) > 1 else ''
            english = parts[2] if len(parts) > 2 else ''
            table_data.append([active, chinese, english])
    
    return table_data

def process_directory(flashcards_dir, output_path=None):
    """Process all text files in the flashcards directory."""
    # Dictionary to store all processed files
    json_data = {}
    
    if not os.path.exists(flashcards_dir):
        print(f"Error: Directory '{flashcards_dir}' does not exist!")
        return None
    
    # Process all .txt files
    txt_files = [f for f in os.listdir(flashcards_dir) if f.endswith('.txt')]
    
    if not txt_files:
        print(f"No .txt files found in '{flashcards_dir}'")
        return None
    
    for file_name in sorted(txt_files):
        file_path = os.path.join(flashcards_dir, file_name)
        title = extract_title_from_file(file_path)
        table_data = process_flashcard_file(file_path)
        
        if table_data:  # Only add non-empty content
            json_data[title] = {
                "title": title,
                "data": table_data
            }
    
    # Generate the JavaScript data file
    output_js = f"const flashcardsData = {json.dumps(json_data, ensure_ascii=False, indent=2)};"
    
    # Determine output path
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "flashcards_data.js")
    
    # Save to a JS file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_js)
    
    print(f"Generated flashcards data with {len(json_data)} files:")
    for title, data in json_data.items():
        print(f"  - {title}: {len(data['data'])} flashcards")
    print(f"\nSaved to: {output_path}")
    
    return json_data

def copy_to_clipboard(file_path):
    """Copy the contents of the file to clipboard."""
    try:
        # For macOS
        if sys.platform == "darwin":
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            subprocess.run(['pbcopy'], input=file_content, text=True, check=True)
            print(f"✅ File copied to clipboard")
            
        # For Linux with xclip
        elif sys.platform.startswith('linux'):
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            subprocess.run(['xclip', '-selection', 'clipboard'], input=file_content, text=True, check=True)
            print(f"✅ File copied to clipboard")
            
        # For Windows with clip
        elif sys.platform == "win32":
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            subprocess.run(['clip'], input=file_content, text=True, check=True)
            print(f"✅ File copied to clipboard")
            
    except subprocess.CalledProcessError:
        print(f"❌ Failed to copy to clipboard. Manual command: cat {file_path} | pbcopy")
    except FileNotFoundError:
        print(f"❌ Clipboard utility not found. Manual command: cat {file_path} | pbcopy")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process flashcard text files into a JavaScript data structure.')
    parser.add_argument('-i', '--input', default='./flashcards_text',
                        help='Directory containing the flashcard text files (default: ./flashcards_text)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file path (default: ./flashcards_data.js)')
    parser.add_argument('--no-copy', action='store_true',
                        help='Skip copying to clipboard')
    
    args = parser.parse_args()
    
    # Process the directory
    process_directory(args.input, args.output)
    
    # Copy to clipboard unless --no-copy flag is used
    if not args.no_copy:
        output_path = args.output if args.output else os.path.join(os.path.dirname(os.path.abspath(__file__)), "flashcards_data.js")
        copy_to_clipboard(output_path)

if __name__ == "__main__":
    main()