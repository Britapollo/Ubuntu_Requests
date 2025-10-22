import requests
import os
import hashlib
from urllib.parse import urlparse
from pathlib import Path


def get_file_hash(filepath):
    """Calculate SHA256 hash of a file to detect duplicates."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def is_duplicate(content, directory):
    """Check if content already exists in directory by comparing hashes."""
    content_hash = hashlib.sha256(content).hexdigest()
    
    if not os.path.exists(directory):
        return False, None
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            existing_hash = get_file_hash(filepath)
            if existing_hash == content_hash:
                return True, filename
    
    return False, None


def validate_image_headers(response):
    """
    Check HTTP headers to ensure we're downloading an actual image.
    Returns (is_valid, message).
    """
    content_type = response.headers.get('Content-Type', '').lower()
    content_length = response.headers.get('Content-Length')
    
    # Check if content type indicates an image
    if not content_type.startswith('image/'):
        return False, f"Content-Type '{content_type}' is not an image"
    
    # Check file size (warn if > 50MB)
    if content_length:
        size_mb = int(content_length) / (1024 * 1024)
        if size_mb > 50:
            return False, f"File size ({size_mb:.1f}MB) exceeds safety limit of 50MB"
    
    return True, "Valid image headers"


def get_filename_from_url(url, content_type=None):
    """Extract filename from URL or generate one based on content type."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If no filename in URL, generate one based on content type
    if not filename or '.' not in filename:
        extension = '.jpg'  # Default
        if content_type:
            # Map common MIME types to extensions
            mime_to_ext = {
                'image/jpeg': '.jpg',
                'image/png': '.png',
                'image/gif': '.gif',
                'image/webp': '.webp',
                'image/svg+xml': '.svg',
                'image/bmp': '.bmp'
            }
            extension = mime_to_ext.get(content_type.lower(), '.jpg')
        
        filename = f"downloaded_image_{hash(url) % 10000}{extension}"
    
    return filename


def download_image(url, directory="Fetched_Images", check_duplicates=True):
    """
    Download an image from URL with safety checks.
    
    Args:
        url: Image URL to download
        directory: Destination directory
        check_duplicates: Whether to check for duplicate images
    
    Returns:
        (success: bool, message: str)
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Fetch the image with timeout and user agent
        # User-Agent helps identify our bot respectfully
        headers = {
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Educational Project)'
        }
        
        response = requests.get(url, timeout=10, headers=headers, stream=True)
        response.raise_for_status()
        
        # Validate headers before downloading
        is_valid, validation_msg = validate_image_headers(response)
        if not is_valid:
            return False, f"✗ Validation failed: {validation_msg}"
        
        # Get the actual content
        content = response.content
        
        # Check for duplicates if enabled
        if check_duplicates:
            is_dup, dup_filename = is_duplicate(content, directory)
            if is_dup:
                return False, f"⚠ Image already exists as: {dup_filename} (duplicate skipped)"
        
        # Extract filename
        content_type = response.headers.get('Content-Type')
        filename = get_filename_from_url(url, content_type)
        filepath = os.path.join(directory, filename)
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(content)
        
        file_size = len(content) / 1024  # KB
        return True, f"✓ Successfully fetched: {filename} ({file_size:.1f} KB)\n✓ Image saved to {filepath}"
        
    except requests.exceptions.Timeout:
        return False, "✗ Connection timeout: Server took too long to respond"
    except requests.exceptions.HTTPError as e:
        return False, f"✗ HTTP error: {e.response.status_code} - {e.response.reason}"
    except requests.exceptions.ConnectionError:
        return False, "✗ Connection error: Could not reach the server"
    except requests.exceptions.RequestException as e:
        return False, f"✗ Request error: {e}"
    except IOError as e:
        return False, f"✗ File error: Could not save image - {e}"
    except Exception as e:
        return False, f"✗ Unexpected error: {e}"


def main():
    """Main function for single or multiple URL downloads."""
    print("=" * 60)
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("=" * 60)
    print("\n'I am because we are' - Ubuntu Philosophy\n")
    
    # Ask user for single or multiple URLs
    mode = input("Download [S]ingle image or [M]ultiple images? (S/M): ").strip().upper()
    
    urls = []
    if mode == 'M':
        print("\nEnter image URLs (one per line, empty line to finish):")
        while True:
            url = input("URL: ").strip()
            if not url:
                break
            urls.append(url)
    else:
        url = input("\nPlease enter the image URL: ").strip()
        urls = [url] if url else []
    
    if not urls:
        print("No URLs provided. Exiting gracefully.")
        return
    
    print(f"\n{'=' * 60}")
    print(f"Processing {len(urls)} image(s)...")
    print(f"{'=' * 60}\n")
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for i, url in enumerate(urls, 1):
        if len(urls) > 1:
            print(f"[{i}/{len(urls)}] Processing: {url[:50]}...")
        
        success, message = download_image(url, check_duplicates=True)
        print(message)
        
        if success:
            success_count += 1
        elif "duplicate" in message.lower():
            skip_count += 1
        else:
            fail_count += 1
        
        if len(urls) > 1:
            print()  # Extra line between multiple downloads
    
    # Summary
    print(f"{'=' * 60}")
    print(f"Summary: {success_count} downloaded, {skip_count} skipped (duplicates), {fail_count} failed")
    print(f"{'=' * 60}")
    
    if success_count > 0:
        print("\n✓ Connection strengthened. Community enriched.")
        print("  Images organized in: ./Fetched_Images/")
    
    print("\nThank you for using Ubuntu Image Fetcher!")


if __name__ == "__main__":
    main()