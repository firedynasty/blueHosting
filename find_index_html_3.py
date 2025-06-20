#!/usr/bin/env python3
"""
Script to find and return only index.html files in a directory tree.
"""

import os
import glob
from pathlib import Path

def find_index_html_files(directory='.', recursive=True, url_replacement=None):
    """
    Find all index.html files in the specified directory.
    
    Args:
        directory (str): Starting directory to search (default: current directory)
        recursive (bool): Whether to search subdirectories (default: True)
        url_replacement (str): If provided, replace './' at the start of paths with this URL
    
    Returns:
        list: List of paths to index.html files
    """
    index_files = []
    
    if recursive:
        # Search recursively using glob
        pattern = os.path.join(directory, '**/index.html')
        index_files = glob.glob(pattern, recursive=True)
    else:
        # Search only in the specified directory
        pattern = os.path.join(directory, 'index.html')
        if os.path.exists(pattern):
            index_files = [pattern]
    
    # Apply URL replacement if specified
    if url_replacement:
        processed_files = []
        for file_path in index_files:
            if file_path.startswith('./'):
                # Replace './' with the provided URL
                new_path = url_replacement + '/' + file_path[2:]
            elif file_path.startswith('.\\'):  # Handle Windows paths
                # Replace '.\' with the provided URL
                new_path = url_replacement + '/' + file_path[2:].replace('\\', '/')
            else:
                # For absolute paths, just convert to URL format
                new_path = url_replacement + '/' + file_path.replace('\\', '/')
            processed_files.append(new_path)
        return sorted(processed_files)
    
    return sorted(index_files)

def find_index_html_pathlib(directory='.', recursive=True, url_replacement=None):
    """
    Alternative implementation using pathlib (Python 3.4+).
    
    Args:
        directory (str): Starting directory to search
        recursive (bool): Whether to search subdirectories
        url_replacement (str): If provided, replace './' at the start of paths with this URL
    
    Returns:
        list: List of Path objects for index.html files
    """
    path = Path(directory)
    
    if recursive:
        # Use rglob for recursive search
        index_files = list(path.rglob('index.html'))
    else:
        # Search only in the specified directory
        index_files = list(path.glob('index.html'))
    
    # Convert to strings and apply URL replacement if specified
    str_files = [str(f) for f in index_files]
    
    if url_replacement:
        processed_files = []
        for file_path in str_files:
            if file_path.startswith('./'):
                # Replace './' with the provided URL
                new_path = url_replacement + '/' + file_path[2:]
            elif file_path.startswith('.\\'):  # Handle Windows paths
                # Replace '.\' with the provided URL
                new_path = url_replacement + '/' + file_path[2:].replace('\\', '/')
            else:
                # For absolute paths, just convert to URL format
                new_path = url_replacement + '/' + file_path.replace('\\', '/')
            processed_files.append(new_path)
        return sorted(processed_files)
    
    return sorted(str_files)

def main():
    """Main function to demonstrate usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Find index.html files')
    parser.add_argument('directory', nargs='?', default='.', 
                       help='Directory to search (default: current directory)')
    parser.add_argument('--no-recursive', action='store_true',
                       help='Search only in the specified directory, not subdirectories')
    parser.add_argument('--method', choices=['glob', 'pathlib'], default='glob',
                       help='Method to use for searching (default: glob)')
    parser.add_argument('--url', type=str,
                       help='URL to replace "./" prefix with (e.g., "{url}" becomes the URL)')
    
    args = parser.parse_args()
    
    recursive = not args.no_recursive
    
    print(f"Searching for index.html files in: {os.path.abspath(args.directory)}")
    print(f"Recursive search: {recursive}")
    print(f"Method: {args.method}")
    if args.url:
        print(f"URL replacement: './' -> '{args.url}/'")
    print("-" * 50)
    
    if args.method == 'glob':
        files = find_index_html_files(args.directory, recursive, args.url)
    else:
        files = find_index_html_pathlib(args.directory, recursive, args.url)
    
    if files:
        print(f"Found {len(files)} index.html file(s):")
        for file in files:
            print(f"  {file}")
        
        # Example output with URL replacement using actual found files
        if not args.url:
            print("\nExample with URL replacement (using {url}):")
            for file in files:
                if file.startswith('./'):
                    converted = "{url}/" + file[2:]
                    print(converted)
    else:
        print("No index.html files found.")
    
    return files

if __name__ == '__main__':
    main()
