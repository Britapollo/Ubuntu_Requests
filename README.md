# Ubuntu Image Fetcher 🌍

> *"I am because we are"* - Ubuntu Philosophy

A Python-based image downloading tool that embodies the Ubuntu philosophy of community, respect, and sharing. This script allows you to mindfully collect and organize images from the web with built-in safety features and duplicate detection.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Architecture](#code-architecture)
- [Safety Features](#safety-features)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **Single & Batch Downloads**: Download one image or multiple images in a single session
- **Smart Directory Management**: Automatically creates and organizes images in `Fetched_Images/` directory
- **Intelligent Filename Handling**: Extracts filenames from URLs or generates appropriate names based on content type
- **Progress Tracking**: Real-time feedback with download statistics and summaries

### Safety & Security
- **Content Validation**: Verifies that URLs actually point to image files
- **File Size Limits**: Protects against accidentally downloading massive files (50MB limit)
- **Timeout Protection**: 10-second timeout prevents indefinite hanging
- **Respectful Bot Identification**: Uses proper User-Agent headers
- **Duplicate Detection**: SHA256 hashing prevents downloading the same image twice

### Error Handling
- **Graceful Failures**: Handles network errors, timeouts, and invalid URLs without crashing
- **Detailed Error Messages**: Clear feedback for different types of failures
- **Connection Resilience**: Continues batch downloads even if individual URLs fail

## 🔧 Requirements

- Python 3.6 or higher
- `requests` library

## 📦 Installation

1. **Clone or download this repository**

2. **Install required dependencies**:
```bash
pip install requests
```

Or using a requirements.txt file:
```bash
pip install -r requirements.txt
```

**requirements.txt**:
```
requests>=2.28.0
```

## 🚀 Usage

### Basic Usage

Run the script:
```bash
python ubuntu_image_fetcher.py
```

### Single Image Download

```
Welcome to the Ubuntu Image Fetcher
A tool for mindfully collecting images from the web

Download [S]ingle image or [M]ultiple images? (S/M): S

Please enter the image URL: https://example.com/image.jpg
✓ Successfully fetched: image.jpg (245.3 KB)
✓ Image saved to Fetched_Images/image.jpg

✓ Connection strengthened. Community enriched.
```

### Multiple Images Download

```
Download [S]ingle image or [M]ultiple images? (S/M): M

Enter image URLs (one per line, empty line to finish):
URL: https://example.com/photo1.jpg
URL: https://example.com/photo2.png
URL: https://example.com/photo3.webp
URL: 

Processing 3 image(s)...

[1/3] Processing: https://example.com/photo1.jpg...
✓ Successfully fetched: photo1.jpg (312.5 KB)
✓ Image saved to Fetched_Images/photo1.jpg

[2/3] Processing: https://example.com/photo2.png...
✓ Successfully fetched: photo2.png (156.8 KB)
✓ Image saved to Fetched_Images/photo2.png

[3/3] Processing: https://example.com/photo3.webp...
⚠ Image already exists as: photo1.jpg (duplicate skipped)

Summary: 2 downloaded, 1 skipped (duplicates), 0 failed

✓ Connection strengthened. Community enriched.
```

## 🏗️ Code Architecture

### Main Functions

#### `main()`
The entry point of the application that:
- Displays the welcome message and Ubuntu philosophy
- Prompts user for single or multiple URL mode
- Collects URLs from user input
- Processes each URL and displays results
- Provides download statistics summary

#### `download_image(url, directory, check_duplicates)`
Core download function that:
- Creates the destination directory if needed
- Sends HTTP request with proper headers
- Validates response headers
- Checks for duplicate content
- Saves the image to disk
- Returns success status and descriptive message

**Parameters**:
- `url` (str): The image URL to download
- `directory` (str): Destination folder (default: "Fetched_Images")
- `check_duplicates` (bool): Enable duplicate detection (default: True)

**Returns**: `(success: bool, message: str)`

#### `validate_image_headers(response)`
Security function that validates HTTP response headers:
- Checks `Content-Type` to ensure it's actually an image
- Verifies `Content-Length` to prevent oversized downloads
- Returns validation status and message

**Parameters**:
- `response` (requests.Response): HTTP response object

**Returns**: `(is_valid: bool, message: str)`

#### `is_duplicate(content, directory)`
Duplicate detection using SHA256 hashing:
- Calculates hash of new content
- Compares against existing files in directory
- Identifies duplicates even with different filenames

**Parameters**:
- `content` (bytes): Image content to check
- `directory` (str): Directory to check for duplicates

**Returns**: `(is_duplicate: bool, filename: str or None)`

#### `get_file_hash(filepath)`
Utility function that:
- Calculates SHA256 hash of a file
- Uses chunked reading for memory efficiency
- Returns hexadecimal hash string

#### `get_filename_from_url(url, content_type)`
Intelligent filename extraction:
- Parses filename from URL path
- Generates appropriate filename if not found
- Maps MIME types to correct file extensions

**Supported Extensions**: `.jpg`, `.png`, `.gif`, `.webp`, `.svg`, `.bmp`

## 🛡️ Safety Features

### 1. Content Type Validation
```python
content_type = response.headers.get('Content-Type', '').lower()
if not content_type.startswith('image/'):
    return False, f"Content-Type '{content_type}' is not an image"
```
Ensures the URL actually points to an image file, not HTML or other content.

### 2. File Size Protection
```python
if content_length:
    size_mb = int(content_length) / (1024 * 1024)
    if size_mb > 50:
        return False, f"File size ({size_mb:.1f}MB) exceeds safety limit"
```
Prevents accidentally downloading massive files that could fill up disk space.

### 3. Request Timeout
```python
response = requests.get(url, timeout=10, headers=headers)
```
10-second timeout prevents the program from hanging indefinitely on slow/unresponsive servers.

### 4. Respectful Bot Identification
```python
headers = {
    'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Educational Project)'
}
```
Properly identifies the bot to web servers, following internet etiquette.

### 5. Duplicate Prevention
```python
content_hash = hashlib.sha256(content).hexdigest()
```
Uses cryptographic hashing to detect identical images, saving bandwidth and storage.

### 6. Comprehensive Error Handling
```python
except requests.exceptions.Timeout:
    return False, "✗ Connection timeout: Server took too long to respond"
except requests.exceptions.HTTPError as e:
    return False, f"✗ HTTP error: {e.response.status_code}"
except requests.exceptions.ConnectionError:
    return False, "✗ Connection error: Could not reach the server"
```
Catches specific exception types and provides clear, actionable error messages.

## 📊 Examples

### Example 1: Successful Download
```
Please enter the image URL: https://picsum.photos/400/300
✓ Successfully fetched: 300 (78.4 KB)
✓ Image saved to Fetched_Images/300
```

### Example 2: Duplicate Detection
```
[1/2] Processing: https://example.com/photo.jpg...
✓ Successfully fetched: photo.jpg (245.3 KB)

[2/2] Processing: https://example.com/same-photo-different-name.jpg...
⚠ Image already exists as: photo.jpg (duplicate skipped)
```

### Example 3: Invalid Content Type
```
Please enter the image URL: https://example.com/page.html
✗ Validation failed: Content-Type 'text/html' is not an image
```

### Example 4: Network Error
```
Please enter the image URL: https://invalid-domain-xyz123.com/image.jpg
✗ Connection error: Could not reach the server
```

## 🎓 Learning Points

This project demonstrates several important Python programming concepts:

1. **HTTP Requests**: Using the `requests` library for web communication
2. **File I/O**: Reading and writing binary files
3. **Error Handling**: Try-except blocks with specific exception types
4. **Hashing**: Using SHA256 for content comparison
5. **URL Parsing**: Extracting components from URLs
6. **Path Management**: Using `os` module for cross-platform file operations
7. **User Input**: Interactive command-line interface
8. **Code Organization**: Modular functions with clear responsibilities

## 🤝 Contributing

Contributions are welcome! Here are some ideas for enhancements:

- [ ] Add support for downloading from image galleries
- [ ] Implement resume capability for interrupted downloads
- [ ] Add image metadata extraction (dimensions, format, etc.)
- [ ] Create a GUI version using tkinter or PyQt
- [ ] Add download history/logging
- [ ] Support for authenticated downloads
- [ ] Parallel downloads for faster batch processing
- [ ] Image format conversion options

## 📄 License

This project is created for educational purposes. Feel free to use, modify, and distribute as needed.

## 🌟 Ubuntu Philosophy

This project embodies the Ubuntu philosophy:

- **Community**: Connects to the global web community
- **Respect**: Handles servers and resources respectfully with timeouts and proper identification
- **Sharing**: Organizes downloads for community use
- **Practicality**: Solves real-world needs with elegant solutions

---

**"A person is a person through other persons."** - Your program connects you to the work of others across the web.

Made with ❤️ in the spirit of Ubuntu
