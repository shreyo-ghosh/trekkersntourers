#!/usr/bin/env python3
"""
Enhanced Image Mapping and HTML Update Script
Intelligently assigns downloaded images to website sections.
"""

from pathlib import Path
import re
import shutil

# Local paths
IMAGES_DIR = Path("assets/images")
HTML_FILE = Path("index.html")

def get_downloaded_images():
    """Get all downloaded images organized by source."""
    images = []
    for img_file in sorted(IMAGES_DIR.glob("*.jpeg")) + sorted(IMAGES_DIR.glob("*.jpg")):
        if img_file.is_file():
            images.append(img_file.name)
    return images

def organize_images_by_trip():
    """Organize images by their trip source."""
    images = get_downloaded_images()
    
    bhutan_images = [img for img in images if "01-11" in img or "9.28" in img or "9.29" in img]
    jaisalmer_images = [img for img in images if "03-06" in img or "11.04" in img or "11.05" in img]
    
    return {
        'bhutan': bhutan_images,
        'jaisalmer': jaisalmer_images,
        'all': images
    }

def create_image_mapping(organized):
    """Create intelligent mapping of images to website sections."""
    mapping = {
        'hero-trek': organized['bhutan'][0] if organized['bhutan'] else organized['all'][0],
        'trip-mountains': organized['bhutan'][3] if len(organized['bhutan']) > 3 else organized['bhutan'][1] if len(organized['bhutan']) > 1 else None,
        'trip-beach': organized['jaisalmer'][0] if organized['jaisalmer'] else None,
        'trip-waterfall': organized['bhutan'][7] if len(organized['bhutan']) > 7 else organized['bhutan'][4] if len(organized['bhutan']) > 4 else None,
        'why-us': organized['bhutan'][2] if len(organized['bhutan']) > 2 else None,
        'highland': organized['jaisalmer'][8] if len(organized['jaisalmer']) > 8 else organized['jaisalmer'][2] if len(organized['jaisalmer']) > 2 else None,
    }
    
    # Filter out None values
    return {k: v for k, v in mapping.items() if v}

def update_html_with_real_images(mapping):
    """Update HTML to reference downloaded images."""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    replacements = 0
    
    print(f"\n🔄 Updating HTML references with real images...")
    print(f"\n📸 Image Mapping:")
    for section, image in mapping.items():
        print(f"  {section:20} → {image}")
    print()
    
    # Update hero section
    if 'hero-trek' in mapping:
        pattern = r'<img src="https://via\.placeholder\.com/\d+x\d+\.jpg\?text=hero-trek\.jpg" alt="Trekkers on a mountain trail"'
        replacement = f'<img src="assets/images/{mapping["hero-trek"]}" alt="Trekkers on a mountain trail"'
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            replacements += 1
            print(f"  ✓ Hero: {mapping['hero-trek']}")
    
    # Update trip-mountains
    if 'trip-mountains' in mapping:
        pattern = r'<img src="https://via\.placeholder\.com/\d+x\d+\.jpg\?text=trip-mountains\.jpg" alt="Mountain trek"'
        replacement = f'<img src="assets/images/{mapping["trip-mountains"]}" alt="Mountain trek"'
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            replacements += 1
            print(f"  ✓ Mountains: {mapping['trip-mountains']}")
    
    # Update trip-beach
    if 'trip-beach' in mapping:
        pattern = r'<img src="https://via\.placeholder\.com/\d+x\d+\.jpg\?text=trip-beach\.jpg" alt="Beach getaway"'
        replacement = f'<img src="assets/images/{mapping["trip-beach"]}" alt="Beach getaway"'
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            replacements += 1
            print(f"  ✓ Beach: {mapping['trip-beach']}")
    
    # Update trip-waterfall
    if 'trip-waterfall' in mapping:
        pattern = r'<img src="https://via\.placeholder\.com/\d+x\d+\.jpg\?text=trip-waterfall\.jpg" alt="Waterfall trail"'
        replacement = f'<img src="assets/images/{mapping["trip-waterfall"]}" alt="Waterfall trail"'
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            replacements += 1
            print(f"  ✓ Waterfall: {mapping['trip-waterfall']}")
    
    # Update why-us section
    if 'why-us' in mapping:
        pattern = r'<img src="https://via\.placeholder\.com/\d+x\d+\.jpg\?text=why-us\.jpg" alt="Happy travelers"'
        replacement = f'<img src="assets/images/{mapping["why-us"]}" alt="Happy travelers"'
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            replacements += 1
            print(f"  ✓ Why Us: {mapping['why-us']}")
    
    # Update highland
    if 'highland' in mapping:
        pattern = r'<img src="assets/images/highland\.jpg"'
        replacement = f'<img src="assets/images/{mapping["highland"]}"'
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            replacements += 1
            print(f"  ✓ Highland: {mapping['highland']}")
    
    # Write updated HTML
    if content != original_content:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ Updated {replacements} image references in HTML")
        return True
    else:
        print(f"\n⚠ No replacements made")
        return False

def validate_no_broken_images():
    """Check HTML for broken image references."""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all img src attributes
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    img_sources = re.findall(img_pattern, content)
    
    print(f"\n🔍 Validating {len(img_sources)} image references...")
    
    broken = []
    local_images = [img.name for img in IMAGES_DIR.glob("*")]
    
    for src in img_sources:
        if src.startswith('http'):
            if 'placeholder' in src:
                print(f"  ⚠ Placeholder URL: {src[:60]}...")
                broken.append(src)
            else:
                print(f"  ✓ External URL: OK")
        else:
            local_path = Path(src)
            if local_path.exists():
                print(f"  ✓ Local: {src}")
            else:
                print(f"  ❌ BROKEN: {src}")
                broken.append(src)
    
    if broken:
        print(f"\n⚠️  Found {len(broken)} broken image references")
        return False
    else:
        print(f"\n✅ All image references are valid!")
        return True

def main():
    print("=" * 70)
    print("  Smart Image Mapping & HTML Update")
    print("=" * 70)
    
    # Get and organize images
    print(f"\n📁 Scanning downloaded images...")
    organized = organize_images_by_trip()
    
    print(f"  ✓ Bhutan trip images: {len(organized['bhutan'])}")
    print(f"  ✓ Jaisalmer trip images: {len(organized['jaisalmer'])}")
    print(f"  ✓ Total images: {len(organized['all'])}")
    
    if not organized['all']:
        print(f"\n❌ No images found in assets/images!")
        return
    
    # Create intelligent mapping
    mapping = create_image_mapping(organized)
    
    # Update HTML
    updated = update_html_with_real_images(mapping)
    
    # Validate
    if updated:
        validate_no_broken_images()
    
    print("\n" + "=" * 70)
    print("✅ Image mapping complete!")
    print("=" * 70)
    print(f"\nNext steps:")
    print(f"1. Commit changes: git add -A && git commit -m 'Add real travel images'")
    print(f"2. Push to GitHub: git push")
    print(f"3. Wait for deployment (check Actions tab)")
    print(f"4. Visit: https://trekkersntourers.com to verify")

if __name__ == "__main__":
    main()
