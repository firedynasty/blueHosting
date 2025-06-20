# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a basketball-focused web application that consists of multiple HTML galleries for displaying basketball content (images, videos, and text resources). The project is designed to be hosted on a web server and provides an interactive interface for navigating basketball-related content.

## Architecture

The project uses a modular approach with three main content types:

1. **Main Link Navigation Hub** (`index.html`) - A sidebar-based navigation system that displays various basketball and general content from text files
2. **Video Gallery** (`player_videos/`) - A video player interface for basketball player demonstrations
3. **Image Gallery** (`spin_move1_img/`) - An image gallery focused on basketball move sequences

### Key Components

- **Template System**: Uses `template_data.js` generated from text files in `folder_w_text/` to populate the main navigation
- **Content Processing**: Python scripts automatically generate JavaScript data files from content directories
- **Responsive Design**: CSS-based layouts optimized for full-screen viewing

## Development Commands

### Content Processing
```bash
# Generate template data from text files
python process_texts.py -i ./folder_w_text -o ./template_data.js

# Generate video gallery data
cd player_videos
python process_videos.py -i ./videos -o ./video_array.js

# Generate image gallery data  
cd spin_move1_img
python process_images.py -i ./images -o ./gallery_images.js
```

### Content Management
```bash
# Add new text content (automatic processing)
# 1. Add .txt files to folder_w_text/
# 2. Run: python process_texts.py
# 3. Output automatically updates template_data.js

# Add new videos (automatic processing)
# 1. Add video files to player_videos/videos/
# 2. Run: cd player_videos && python process_videos.py
# 3. Output updates video_array.js

# Add new images (automatic processing)
# 1. Add image files to spin_move1_img/images/
# 2. Run: cd spin_move1_img && python process_images.py
# 3. Output updates gallery_images.js
```

## File Structure Logic

- **Main Hub**: `index.html` + `template_data.js` (generated from `folder_w_text/`)
- **Video Section**: `player_videos/index.html` + `video_array.js` (generated from `videos/`)
- **Image Section**: `spin_move1_img/index.html` + `gallery_images.js` (generated from `images/`)

## Content Format Requirements

### Text Files (`folder_w_text/`)
- Mixed content format supporting both links and text
- Links format: `URL, Description`
- Text content: Plain text with automatic formatting
- File naming: Descriptive names become navigation titles

### Video Files (`player_videos/videos/`)
- Supported formats: `.mp4`, `.webm`, `.ogg`, `.mov`, `.avi`, `.mkv`, `.m4v`
- Automatic title generation from filenames
- Natural sorting (handles numbers correctly)

### Image Files (`spin_move1_img/images/`)
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`, `.svg`
- Automatic title generation from filenames
- Sequential naming recommended for move sequences

## Key Features

### Navigation System
- Keyboard shortcuts for quick navigation
- Link numbering system for direct access
- Sidebar navigation with search-friendly titles
- Note-taking functionality with clipboard copy

### Content Processing Pipeline
- Python scripts automatically scan directories
- Generate JavaScript data files
- Handle file sorting and metadata extraction
- Support for both media and text content

## Common Tasks

### Adding New Basketball Content
1. **Text/Links**: Add `.txt` file to `folder_w_text/`, run `python process_texts.py`
2. **Videos**: Add video to `player_videos/videos/`, run processing script
3. **Images**: Add images to `spin_move1_img/images/`, run processing script

### Modifying Galleries
- Each gallery has its own HTML file with embedded CSS and JavaScript
- Data is loaded from generated `.js` files
- Styling can be modified directly in the HTML files

### Content Organization
- Use descriptive filenames as they become display titles
- Sequential numbering for ordered content (moves, drills, etc.)
- Consistent naming patterns for automatic processing