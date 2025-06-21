#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import csv
import re
import argparse
import subprocess
import sys
import html

def extract_title_from_file(file_path):
    """Extract a title from the file content or file name."""
    file_name = os.path.basename(file_path)
    
    # Extract page number for elementary_chinese files
    if file_name.startswith("elementary_chinese_pg"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        # Try to find a title in the content
        lines = content.split('\n')
        for line in lines:
            if '|' in line:
                # Extract the part after the pipe which typically contains the title
                title = line.split('|', 1)[1].strip()
                return f"Elementary Chinese ({file_name}) - {title}"
        
        # If no title found, use the file name
        page_num = file_name.replace("elementary_chinese_pg", "").replace(".txt", "")
        return f"Elementary Chinese (Page {page_num})"
    
    # For other files, just use the filename without extension
    base_name = os.path.splitext(file_name)[0]
    return f"{base_name} ({os.path.splitext(file_name)[1][1:]})"

def detect_local_galleries(content, base_dir):
    """Detect local gallery references and add metadata."""
    gallery_info = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        # Look for local gallery patterns
        if any(pattern in line for pattern in ['_img/', '_videos/', '_gallery/', '/images/', '/videos/']):
            # Check if corresponding folder exists
            folder_name = None
            if '_img/' in line:
                folder_name = line.split('_img/')[0].split('/')[-1] + '_img'
            elif '_videos/' in line:
                folder_name = line.split('_videos/')[0].split('/')[-1] + '_videos'
            elif '/images/' in line:
                folder_name = line.split('/images/')[0].split('/')[-1]
            elif '/videos/' in line:
                folder_name = line.split('/videos/')[0].split('/')[-1]
            
            if folder_name:
                folder_path = os.path.join(base_dir, '..', folder_name)
                if os.path.exists(folder_path):
                    gallery_info.append({
                        'type': 'local_gallery',
                        'folder': folder_name,
                        'url_line': line
                    })
    
    return gallery_info

def parse_markdown_tables(content):
    """Parse markdown tables and convert them to HTML tables."""
    lines = content.split('\n')
    processed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this line looks like a table header (contains |)
        if '|' in line and line.count('|') >= 2:
            # Look for the separator line (next line with dashes and |)
            if i + 1 < len(lines) and re.match(r'^[\s\|\-\:]+$', lines[i + 1].strip()):
                # We found a table!
                table_lines = [line]
                table_lines.append(lines[i + 1])  # separator line
                i += 2
                
                # Collect all subsequent table rows
                while i < len(lines) and '|' in lines[i].strip() and lines[i].strip():
                    table_lines.append(lines[i].strip())
                    i += 1
                
                # Convert to HTML table
                html_table = convert_markdown_table_to_html(table_lines)
                processed_lines.append(html_table)
                continue
        
        processed_lines.append(lines[i])
        i += 1
    
    return '\n'.join(processed_lines)

def convert_markdown_table_to_html(table_lines):
    """Convert markdown table lines to HTML table."""
    if len(table_lines) < 3:  # Need at least header, separator, and one data row
        return '\n'.join(table_lines)  # Return as-is if not a valid table
    
    # Parse header
    header_line = table_lines[0].strip()
    headers = [cell.strip() for cell in header_line.split('|') if cell.strip()]
    
    # Parse data rows (skip separator line)
    data_rows = []
    for line in table_lines[2:]:
        if line.strip():
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:  # Only add non-empty rows
                data_rows.append(cells)
    
    # Generate HTML
    html_content = '<table class="markdown-table">\n'
    html_content += '  <thead>\n    <tr>\n'
    for header in headers:
        html_content += f'      <th>{html.escape(header)}</th>\n'
    html_content += '    </tr>\n  </thead>\n'
    
    html_content += '  <tbody>\n'
    for row in data_rows:
        html_content += '    <tr>\n'
        for cell in row:
            html_content += f'      <td>{html.escape(cell)}</td>\n'
        html_content += '    </tr>\n'
    html_content += '  </tbody>\n'
    html_content += '</table>'
    
    return html_content

def parse_code_blocks(content):
    """Parse markdown-style code blocks and convert them to HTML with syntax highlighting classes."""
    # Pattern to match code blocks with language specifier
    code_block_pattern = r'```(\w+)?\n(.*?)```'
    
    def replace_code_block(match):
        language = match.group(1) if match.group(1) else 'text'
        code_content = match.group(2)
        
        # Escape HTML entities in the code content
        escaped_code = html.escape(code_content)
        
        # Return HTML with Prism.js classes
        return f'<pre><code class="language-{language}">{escaped_code}</code></pre>'
    
    # Replace all code blocks
    processed_content = re.sub(code_block_pattern, replace_code_block, content, flags=re.DOTALL)
    
    return processed_content

def process_txt_file(file_path, base_dir=None):
    """Process a text file and extract its content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Detect local galleries if base_dir provided
    gallery_info = []
    if base_dir:
        gallery_info = detect_local_galleries(content, base_dir)
    
    # Parse markdown tables first
    content = parse_markdown_tables(content)
    
    # Parse code blocks for syntax highlighting
    content = parse_code_blocks(content)
    
    # Basic processing of content to make it more structured
    lines = content.split('\n')
    processed_lines = []
    
    # Simple formatting for elementary_chinese files to extract vocab
    in_vocab_section = False
    vocab_entries = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip lines with URLs or interactive elements (but not if they're in code blocks)
        if ("http" in line or "interactive" in line) and not ('<pre><code' in line):
            continue
            
        # Look for vocabulary sections
        if "Chinese" in line and "Pinyin" in line or "English" in line:
            in_vocab_section = True
            continue
            
        if in_vocab_section:
            # Try to extract vocabulary entries
            if re.match(r'^\s*\d+\s*$', line):  # Skip line numbers
                continue
                
            vocab_entries.append(line)
    
    # If we found vocab entries, format them
    if vocab_entries:
        processed_content = "\n".join(vocab_entries)
    else:
        processed_content = content
    
    # For now, just return the content as string to avoid JS errors
    # Gallery info can be added later if needed
    return processed_content

def process_csv_file(file_path):
    """Process a CSV file and extract its content."""
    content_lines = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:  # Skip empty rows
                    content_lines.append(",".join(row))
    except Exception as e:
        return f"Error reading CSV: {str(e)}"
        
    return "\n".join(content_lines)

def process_directory(texts_dir, output_path=None):
    """Process all text files in the given directory."""
    # Dictionary to store all processed files
    json_data = {}
    counter = 1
    
    # Process all .txt files
    txt_files = [f for f in os.listdir(texts_dir) if f.endswith('.txt')]
    for file_name in sorted(txt_files):
        file_path = os.path.join(texts_dir, file_name)
        title = extract_title_from_file(file_path)
        content = process_txt_file(file_path, texts_dir)
        
        if content:  # Only add non-empty content
            json_data[str(counter)] = {
                "title": title,
                "content": content
            }
            counter += 1
    
    # Process all .csv files
    csv_files = [f for f in os.listdir(texts_dir) if f.endswith('.csv')]
    for file_name in sorted(csv_files):
        file_path = os.path.join(texts_dir, file_name)
        title = extract_title_from_file(file_path)
        content = process_csv_file(file_path)
        
        if content:  # Only add non-empty content
            json_data[str(counter)] = {
                "title": title,
                "content": content
            }
            counter += 1
    
    # Output the JSON data
    output_js = f"const templates = {json.dumps(json_data, ensure_ascii=False, indent=2)}"
    
    # Determine output path
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "template_data.js")
    
    # Save to a JS file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_js)
    
    print(f"Generated template data with {len(json_data)} entries to {output_path}")
    
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
    parser = argparse.ArgumentParser(description='Process Chinese text files into a JSON structure.')
    parser.add_argument('-i', '--input', default='./folder_w_text',
                        help='Directory containing the text files (default: ./chinese_texts)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file path (default: ./template_data.js)')
    parser.add_argument('--no-copy', action='store_true',
                        help='Skip copying to clipboard')
    
    args = parser.parse_args()
    
    # Process the directory
    process_directory(args.input, args.output)
    
    # Copy to clipboard unless --no-copy flag is used
    if not args.no_copy:
        output_path = args.output if args.output else os.path.join(os.path.dirname(os.path.abspath(__file__)), "template_data.js")
        copy_to_clipboard(output_path)

if __name__ == "__main__":
    main()