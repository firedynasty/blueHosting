#!/usr/bin/env python3
"""
Script to run all image and video processing scripts in the basketball content directories.
This script will execute all process_images.py and process_videos.py files found in the project.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_processor(script_path, script_dir):
    """Run a processing script in its directory."""
    print(f"\n{'='*60}")
    print(f"Running: {script_path}")
    print(f"Directory: {script_dir}")
    print(f"{'='*60}")
    
    try:
        # Change to the script's directory and run it
        result = subprocess.run(
            [sys.executable, os.path.basename(script_path)],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.stdout:
            print("Output:")
            print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ SUCCESS")
        else:
            print(f"❌ FAILED (exit code: {result.returncode})")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT - Script took too long to execute")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Main function to find and run all processing scripts."""
    base_dir = Path(__file__).parent
    
    # Find all processing scripts
    image_processors = list(base_dir.glob("**/process_images.py"))
    video_processors = list(base_dir.glob("**/process_videos.py"))
    
    all_processors = image_processors + video_processors
    
    if not all_processors:
        print("No processing scripts found!")
        return
    
    print(f"Found {len(all_processors)} processing scripts:")
    for script in all_processors:
        print(f"  - {script.relative_to(base_dir)}")
    
    print(f"\nStarting to process all scripts...")
    
    success_count = 0
    total_count = len(all_processors)
    
    # Run each processor
    for script_path in all_processors:
        script_dir = script_path.parent
        success = run_processor(script_path, script_dir)
        if success:
            success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total scripts: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_count - success_count}")
    
    if success_count == total_count:
        print("🎉 All processing scripts completed successfully!")
    else:
        print("⚠️  Some scripts failed. Check the output above for details.")

if __name__ == "__main__":
    main()