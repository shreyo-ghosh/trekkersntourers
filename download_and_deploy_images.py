#!/usr/bin/env python3
"""
S3 Image Downloader and Web Deployer
Downloads all images from S3 bucket and updates HTML references.
"""

import boto3
import os
from pathlib import Path
from PIL import Image
import re

# AWS Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.getenv('S3_BUCKET', 'trekkersntourers.com')
S3_REGION = os.getenv('S3_REGION', 'ap-south-1')

# Local paths
IMAGES_DIR = Path("assets/images")
HTML_FILE = Path("index.html")

# Image extensions to download
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

def setup_s3_client():
    """Create and return boto3 S3 client."""
    return boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

def list_s3_images(s3_client):
    """List all image files in S3 bucket."""
    images = []
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        
        if 'Contents' not in response:
            print(f"❌ No objects found in bucket: {S3_BUCKET}")
            return images
        
        for obj in response['Contents']:
            key = obj['Key']
            ext = Path(key).suffix.lower()
            
            if ext in IMAGE_EXTENSIONS:
                images.append(key)
                print(f"✓ Found image: {key}")
        
        print(f"\n📊 Total images found: {len(images)}\n")
        return images
    
    except Exception as e:
        print(f"❌ Error listing S3 objects: {e}")
        return images

def download_images(s3_client, image_keys):
    """Download image files from S3 to local assets/images folder."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = []
    failed = []
    
    print(f"📥 Downloading {len(image_keys)} images from S3...")
    
    for key in image_keys:
        try:
            # Create local file path
            filename = Path(key).name
            local_path = IMAGES_DIR / filename
            
            # Download file
            s3_client.download_file(S3_BUCKET, key, str(local_path))
            
            # Verify file exists and has size > 0
            if local_path.exists() and local_path.stat().st_size > 0:
                file_size_kb = local_path.stat().st_size / 1024
                print(f"  ✓ Downloaded: {filename} ({file_size_kb:.1f} KB)")
                downloaded.append(filename)
                
                # Validate image can be opened
                try:
                    with Image.open(local_path) as img:
                        print(f"    └─ Validated: {img.format} {img.size[0]}x{img.size[1]}px")
                except Exception as e:
                    print(f"    ⚠ Warning: Could not validate image: {e}")
            else:
                print(f"  ❌ File too small or empty: {filename}")
                failed.append(filename)
        
        except Exception as e:
            print(f"  ❌ Failed to download {key}: {e}")
            failed.append(key)
    
    print(f"\n✅ Successfully downloaded: {len(downloaded)} images")
    if failed:
        print(f"❌ Failed to download: {len(failed)} images")
    
    return downloaded, failed

def get_local_images():
    """Get list of all local image files in assets/images."""
    if not IMAGES_DIR.exists():
        return []
    
    local_images = []
    for ext in IMAGE_EXTENSIONS:
        local_images.extend(IMAGES_DIR.glob(f"*{ext}"))
        local_images.extend(IMAGES_DIR.glob(f"*{ext.upper()}"))
    
    return [f.name for f in local_images]

def update_html_references(downloaded_images):
    """Update HTML file to reference downloaded images."""
    if not HTML_FILE.exists():
        print(f"❌ HTML file not found: {HTML_FILE}")
        return
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    replacements = 0
    
    # Build mapping of placeholder patterns to potential real images
    image_map = {
        'hero-trek': None,
        'trip-mountains': None,
        'trip-beach': None,
        'trip-waterfall': None,
        'why-us': None,
        'highland': None,
    }
    
    # Try to match downloaded images to these slots
    for key in image_map:
        for img in downloaded_images:
            if key.lower() in img.lower():
                image_map[key] = img
                break
    
    print(f"\n🔄 Updating HTML references...")
    
    # Replace placeholder images with actual downloads
    placeholder_patterns = [
        (r'https://via\.placeholder\.com/\d+x\d+\.jpg\?text=hero-trek\.jpg', 'assets/images/hero-trek.jpg'),
        (r'https://via\.placeholder\.com/\d+x\d+\.jpg\?text=trip-mountains\.jpg', 'assets/images/trip-mountains.jpg'),
        (r'https://via\.placeholder\.com/\d+x\d+\.jpg\?text=trip-beach\.jpg', 'assets/images/trip-beach.jpg'),
        (r'https://via\.placeholder\.com/\d+x\d+\.jpg\?text=trip-waterfall\.jpg', 'assets/images/trip-waterfall.jpg'),
    ]
    
    for pattern, replacement in placeholder_patterns:
        if re.search(pattern, content):
            # Check if we have the image
            img_name = Path(replacement).name
            if any(img_name.lower() in img.lower() for img in downloaded_images):
                content = re.sub(pattern, replacement, content)
                replacements += 1
                print(f"  ✓ Updated: {img_name}")
    
    # Write updated HTML
    if content != original_content:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ Updated {replacements} image references in HTML")
    else:
        print(f"\n⚠ No placeholder images found to update (they may already be updated)")

def validate_no_broken_images():
    """Check HTML for broken image references."""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all img src attributes
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    img_sources = re.findall(img_pattern, content)
    
    print(f"\n🔍 Validating {len(img_sources)} image references...")
    
    broken = []
    local_images = get_local_images()
    
    for src in img_sources:
        if src.startswith('http'):
            # Don't validate external URLs, but flag placeholder URLs
            if 'placeholder' in src:
                print(f"  ⚠ Placeholder URL (not replaced): {src}")
                broken.append(src)
            else:
                print(f"  ✓ External URL: {src}")
        else:
            # Check if local file exists
            local_path = Path(src)
            if local_path.exists():
                print(f"  ✓ Exists: {src}")
            else:
                print(f"  ❌ BROKEN: {src}")
                broken.append(src)
    
    if broken:
        print(f"\n⚠️  Found {len(broken)} potential broken images!")
        return False
    else:
        print(f"\n✅ All image references are valid!")
        return True

def main():
    print("=" * 60)
    print("  S3 Image Downloader & Web Deployer")
    print("=" * 60)
    print(f"\n📋 Configuration:")
    print(f"  S3 Bucket: {S3_BUCKET}")
    print(f"  Region: {S3_REGION}")
    print(f"  Local Path: {IMAGES_DIR.resolve()}")
    print()
    
    try:
        # Connect to S3
        print("🔐 Connecting to S3...\n")
        s3_client = setup_s3_client()
        
        # Verify connection by listing bucket contents
        s3_client.head_bucket(Bucket=S3_BUCKET)
        print("✅ Successfully connected to S3!\n")
        
        # List images in S3
        image_keys = list_s3_images(s3_client)
        
        if not image_keys:
            print("❌ No images found in S3 bucket!")
            return
        
        # Download images
        downloaded, failed = download_images(s3_client, image_keys)
        
        if not downloaded:
            print("❌ No images were downloaded successfully!")
            return
        
        # Update HTML references
        update_html_references(downloaded)
        
        # Validate no broken images
        all_valid = validate_no_broken_images()
        
        print("\n" + "=" * 60)
        if all_valid and downloaded:
            print("✅ SUCCESS: All images deployed!")
            print("=" * 60)
            print(f"\nNext steps:")
            print(f"1. Commit the changes: git add -A && git commit -m 'Add travel images from S3'")
            print(f"2. Push to GitHub: git push")
            print(f"3. Wait for GitHub Actions to deploy")
            print(f"4. Visit: https://trekkersntourers.com to verify")
        else:
            print("⚠️  Deployment completed with warnings")
            print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
