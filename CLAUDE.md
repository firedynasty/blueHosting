# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a basketball-focused web application that consists of multiple HTML galleries for displaying basketball content (images, videos, and text resources). The project is designed to be hosted on a web server and provides an interactive interface for navigating basketball-related content.

## Architecture

The project uses a modular content management system with multiple gallery types organized under the `content/` directory:

1. **Main Link Navigation Hub** (`index.html`) - A sidebar-based navigation system that displays content from text files in `folder_w_text/`
2. **Video Galleries** - Multiple video sections for different basketball concepts:
   - `content/player_videos/` - Player demonstration videos
   - `content/create_shot/` - Shot creation tutorials  
   - `content/driving/driving_videos/` - Driving technique videos
3. **Image Galleries** - Sequential image galleries for move breakdowns:
   - `content/dribbling/spin_move1_img/` - Spin move sequences
   - `content/dribbling/counter_cross1/` - Counter crossover sequences
   - `content/driving/driving_images/` - Driving technique images
   - `content/plays/` - Basketball play diagrams
   - `content/top_of_key/` - Top of key positioning

### Key Components

- **Template System**: Uses `template_data.js` generated from text files in `folder_w_text/` to populate the main navigation
- **Content Processing**: Python scripts automatically generate JavaScript data files from content directories
- **Responsive Design**: CSS-based layouts optimized for full-screen viewing

## Development Commands

### Global Content Processing
```bash
# Process all content at once (recommended)
python 03-run_all_processors.py

# Process main text content (individual)
python 02-process_texts.py -i ./folder_w_text -o ./template_data.js

# Process flashcard sets
python 04-process_flashcards.py -i ./flashcards_text -o ./flashcards_data.js
```

### Individual Gallery Processing
```bash
# Generate video gallery data (example)
cd content/player_videos
python process_videos.py -i ./videos -o ./video_array.js

# Generate image gallery data (example)
cd content/dribbling/spin_move1_img
python process_images.py -i ./images -o ./gallery_images.js
```

### Content Management Workflow
```bash
# Step 1: Add content files to appropriate directories
# - Text files: folder_w_text/
# - Videos: content/*/videos/
# - Images: content/*/images/
# - Flashcards: flashcards_text/ (CSV format with 2-3 columns)

# Step 2: Process all content at once
python 03-run_all_processors.py

# Alternative: Process individual sections
python 02-process_texts.py -i ./folder_w_text -o ./template_data.js
python 04-process_flashcards.py -i ./flashcards_text -o ./flashcards_data.js
cd content/player_videos && python process_videos.py
cd content/dribbling/spin_move1_img && python process_images.py
```

## File Structure Logic

- **Main Hub**: `index.html` + `template_data.js` (generated from `folder_w_text/`)
- **Content Organization**: All galleries are organized under `content/` with subdirectories by category
- **Processing Scripts**: Each gallery has its own `process_*.py` script for data generation
- **Generated Data**: Each gallery produces a `.js` file with content metadata
- **Global Processing**: `03-run_all_processors.py` runs all individual processors automatically

## Content Format Requirements

### Text Files (`folder_w_text/`)
- Mixed content format supporting both links and text
- Links format: `URL, Description`
- Text content: Plain text with automatic formatting
- File naming: Descriptive names become navigation titles

### Video Files (`content/*/videos/`)
- Supported formats: `.mp4`, `.webm`, `.ogg`, `.mov`, `.avi`, `.mkv`, `.m4v`
- Automatic title generation from filenames
- Natural sorting (handles numbers correctly)
- Organized by basketball concept (player videos, shot creation, driving)

### Image Files (`content/*/images/`)
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`, `.svg`
- Automatic title generation from filenames
- Sequential naming recommended for technique sequences
- Organized by move type (dribbling, driving, plays, positioning)

## Key Features

### Navigation System
- Keyboard shortcuts for quick navigation
- Link numbering system for direct access
- Sidebar navigation with search-friendly titles
- Note-taking functionality with clipboard copy

### Content Processing Pipeline
- **Global Processor**: `03-run_all_processors.py` discovers and runs all processing scripts
- **Text Processor**: `02-process_texts.py` handles markdown, code blocks, and link extraction
- **Individual Processors**: Each gallery has dedicated `process_images.py` or `process_videos.py`
- **Auto-Discovery**: Scripts automatically find and process content files
- **Natural Sorting**: Handles numbered sequences correctly for move progressions
- **Metadata Generation**: Creates detailed JavaScript objects with titles and paths

## Common Tasks

### Adding New Basketball Content
1. **Text/Links**: Add `.txt` file to `folder_w_text/`, run `python 02-process_texts.py`
2. **Videos**: Add videos to any `content/*/videos/` directory, run `python 03-run_all_processors.py`
3. **Images**: Add images to any `content/*/images/` directory, run `python 03-run_all_processors.py`
4. **Flashcards**: Add `.txt` files to `flashcards_text/` (2-3 column CSV format), run `python 04-process_flashcards.py`
5. **New Galleries**: Create new directory under `content/`, add processing script, include in global processor

### Flashcard Applications
- **simple-table-text-to-speech.html**: Lightweight flashcard viewer with dropdown for flashcard sets
- **flashcardsIndex.html**: Advanced flashcard application with Firebase integration and flashcard set loading

### Modifying Galleries
- Each gallery has its own HTML file with embedded CSS and JavaScript
- Data is loaded from generated `.js` files
- Styling can be modified directly in the HTML files

### Content Organization
- Use descriptive filenames as they become display titles
- Sequential numbering for ordered content (moves, drills, etc.)
- Consistent naming patterns for automatic processing

## Configuration

### Environment Detection
- `config.js` handles automatic URL detection for local vs production environments
- Local development: Uses `localhost` or `127.0.0.1` detection
- Production: Configured for `https://stanleysjourney.com/basketball`

### Processing Script Features
- **Markdown Support**: Tables, code blocks with syntax highlighting
- **Link Extraction**: Automatic parsing of `URL, Description` format
- **Cross-Platform**: Clipboard integration for macOS, Linux, Windows
- **Error Handling**: Graceful failures with detailed output
- **Timeout Protection**: 60-second timeout for processing scripts