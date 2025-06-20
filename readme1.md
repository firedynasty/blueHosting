# Basketball Content Management System

A modular web application for organizing and displaying basketball-related content including videos, images, and text resources with automatic content processing and navigation.

## Features

- **Multi-Gallery System**: Separate galleries for videos, images, and text-based notes
- **Automatic Content Processing**: Python scripts generate JavaScript data files from content directories
- **Smart Navigation**: Keyboard shortcuts, link numbering, and search-friendly interface
- **Syntax Highlighting**: Code blocks in text files with language-specific highlighting
- **URL Path Management**: Tools for converting local paths to web-accessible URLs

## Project Structure

```
├── index.html                    # Main navigation hub
├── template_data.js             # Generated from folder_w_text/ content
├── folder_w_text/               # Text files with notes and links
├── player_videos/               # Video gallery section
│   ├── index.html
│   ├── videos/                  # Video files directory
│   ├── process_videos.py        # Generates video_array.js
│   └── video_array.js          # Generated video metadata
├── spin_move1_img/              # Image gallery section
│   ├── index.html
│   ├── images/                  # Image files directory
│   ├── process_images.py        # Generates gallery_images.js
│   └── gallery_images.js       # Generated image metadata
├── process_texts.py             # Main text processing script
└── find_index_html_3.py         # URL path conversion utility
```

## Getting Started

### 1. Adding Content

#### Text Notes and Links
Add `.txt` files to `folder_w_text/` with mixed content:

```
Basketball Training Notes

https://example.com/dribbling-drills, Advanced Dribbling Techniques
https://youtube.com/watch?v=abc123, Stephen Curry Shooting Form

Regular text content with automatic formatting.
Lists, paragraphs, and code blocks are supported.

```javascript
function calculateFG(made, attempted) {
  return (made / attempted) * 100;
}
```

After adding files, run:
```bash
python process_texts.py -i ./folder_w_text -o ./template_data.js
```

#### Video Content
1. Add video files (`.mp4`, `.webm`, `.mov`, etc.) to `player_videos/videos/`
2. Generate the video array:
```bash
cd player_videos
python process_videos.py -i ./videos -o ./video_array.js
```

#### Image Content
1. Add image files (`.jpg`, `.png`, `.gif`, etc.) to `spin_move1_img/images/`
2. Generate the image array:
```bash
cd spin_move1_img
python process_images.py -i ./images -o ./gallery_images.js
```

### 2. Content Processing Pipeline

Each content type has an automated processing system:

- **Text Processing**: Scans `.txt` files, extracts links and content, generates navigation data
- **Video Processing**: Scans video directory, extracts metadata, creates playback array
- **Image Processing**: Scans image directory, generates gallery with sequential ordering

### 3. URL Path Management

The `find_index_html_3.py` script helps convert local file paths to web-accessible URLs:

```bash
python find_index_html_3.py --url "https://yoursite.com" 
```

**{url} Placeholder Usage**: 
- In text files, use `{url}` as a placeholder for your domain
- The script automatically converts relative paths like `./player_videos/index.html` to `https://yoursite.com/player_videos/index.html`
- Useful for generating navigation links that work both locally and on web servers

Example output:
```
./index.html → {url}/index.html
./player_videos/index.html → {url}/player_videos/index.html  
./spin_move1_img/index.html → {url}/spin_move1_img/index.html
```

## Content Formats

### Text Files Support
- **Links**: `URL, Description` format for automatic link parsing
- **Mixed Content**: Combine links with regular text, notes, and explanations
- **Syntax Highlighting**: Code blocks with language specification:
  ```
  ```javascript
  // Your JavaScript code here
  ```
  ```
- **Supported Languages**: HTML, JavaScript, CSS, Python, and more

### Media Files
- **Videos**: `.mp4`, `.webm`, `.ogg`, `.mov`, `.avi`, `.mkv`, `.m4v`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`, `.svg`

## Navigation Features

- **Keyboard Shortcuts**: Quick navigation between content sections
- **Link Numbering**: Direct access to specific links via number keys
- **Sidebar Navigation**: Organized content with search-friendly titles
- **Copy to Clipboard**: Easy sharing of notes and links

## Usage Examples

### Adding Basketball Drills
1. Create `shooting_drills.txt` in `folder_w_text/`:
```
Shooting Form Drills

https://youtube.com/watch?v=example1, Steph Curry Form Analysis  
https://youtube.com/watch?v=example2, Catch and Shoot Mechanics

Key Points:
- Keep elbow under the ball
- Follow through with wrist snap
- Use legs for power

```python
# Track shooting percentage
def track_shots(made, total):
    return f"{(made/total)*100:.1f}% accuracy"
```
```

2. Run: `python process_texts.py -i ./folder_w_text -o ./template_data.js`
3. Content automatically appears in main navigation

### Organizing Video Analysis
1. Add analysis videos to `player_videos/videos/`
2. Run processing script to generate metadata
3. Videos become accessible through the video gallery interface

## Development

The system uses a template-based approach where Python scripts scan content directories and generate JavaScript data files that power the web interfaces. Each gallery type (text, video, image) has its own processing script and display system.

For deployment, ensure all `.js` data files are regenerated after adding new content, and update any `{url}` placeholders with your actual domain.
```



 The find_index_html_3.py script is particularly useful for deployment - it finds all index.html files and can convert

  relative paths to web URLs using the {url} placeholder, making it easy to generate navigation links that work both

 locally and on web servers.