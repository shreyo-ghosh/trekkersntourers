# Travel Images Setup Guide

This document provides a complete guide for integrating your 13 travel images into the Trekkers & Tourers website.

## What's Been Prepared

✅ **Images Folder Structure Created**
- Created: `/assets/images/` directory
- Created: `IMAGE_GUIDE.md` with detailed instructions
- Current Status: Folder ready for image upload

## How to Upload Your 13 Travel Images

### Step 1: Navigate to the Images Folder
1. Go to: https://github.com/shreyo-ghosh/trekkersntourers/tree/main/assets/images
2. Click **"Add file"** button
3. Select **"Upload files"**

### Step 2: Rename Your Images

Before uploading, rename your 13 images to match the website sections. Here's the mapping:

#### **Required Images (4 images)**
1. **hero-trek.jpg** - Homepage hero section (mountain/trek with light rays)
2. **trip-mountains.jpg** - Weekend Himalayan Trek card
3. **trip-beach.jpg** - Coastal Beach Escape card  
4. **trip-waterfall.jpg** - Waterfall & Forest Trail card
5. **why-us.jpg** - "Why Travel With Us" section (happy travelers)

#### **Additional Images (up to 8 more)**
- `gallery-1.jpg` through `gallery-8.jpg`
- Or name them based on your content:
  - `hero-secondary-1.jpg`
  - `testimonial-1.jpg`
  - `destination-1.jpg`
  - etc.

### Step 3: Upload Files
1. Drag and drop your renamed image files into the upload area
2. Or click "select" to browse your computer
3. Ensure all filenames match exactly (case-sensitive)
4. Commit with message: "Add travel images for website"

### Step 4: Update HTML References

After uploading, update the image references in `index.html`:

Replace all lines like:
```html
<img src="assets/images/800x600.jpg?text=hero-trek.jpg" ...
```

With:
```html
<img src="assets/images/hero-trek.jpg" ...
```

Specific lines to update in index.html:
- **Line ~37**: Hero image → `src="assets/images/hero-trek.jpg"`
- **Line ~48**: Mountains → `src="assets/images/trip-mountains.jpg"`
- **Line ~55**: Beach → `src="assets/images/trip-beach.jpg"`
- **Line ~62**: Waterfall → `src="assets/images/trip-waterfall.jpg"`
- **Line ~82**: Why Us → `src="assets/images/why-us.jpg"`

### Step 5: Verify Deployment

1. After committing HTML changes, GitHub Actions will automatically deploy
2. Check the "Actions" tab to see the build status
3. Visit your deployed site at: `https://shreyo-ghosh.github.io/trekkersntourers/`
4. Verify all images display correctly

## Image Requirements

- **Format**: JPG or PNG
- **Recommended Size**: 800x600px (width x height)
- **Aspect Ratio**: 4:3 (maintains consistency)
- **File Size**: < 500KB per image (for fast loading)
- **Dimensions**: Consider 1200x900px for high-quality displays

## Optimization Tips

### Before Uploading:
1. **Compress Images**:
   - Use TinyPNG (tinypng.com) or similar tool
   - Reduce file size while maintaining quality
   - Target: 200-300KB per image

2. **Resize Images**:
   - Use online tools like Squoosh (squoosh.app)
   - Standardize to 800x600px
   - Maintains consistent look across site

3. **Format Conversion**:
   - Convert to JPG for photos
   - Use PNG for images needing transparency

### Batch Processing:
If you have 13 images to optimize:
```bash
# Using ImageMagick (if installed locally)
for img in *.jpg; do
  convert "$img" -resize 800x600 -quality 85 "optimized-$img"
done
```

## File Structure After Upload

```
trekkersntourers/
├── assets/
│   ├── css/
│   ├── images/           ← Your images go here
│   │   ├── hero-trek.jpg
│   │   ├── trip-mountains.jpg
│   │   ├── trip-beach.jpg
│   │   ├── trip-waterfall.jpg
│   │   ├── why-us.jpg
│   │   ├── gallery-1.jpg
│   │   └── ...
│   └── js/
├── index.html           ← Update image src attributes here
└── ...
```

## Troubleshooting

### Images Not Showing?
- **Check file names**: Ensure they match exactly (case-sensitive)
- **Check paths**: Should be `assets/images/filename.jpg`
- **Check browser cache**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- **Check GitHub deployment**: Wait 2-3 minutes for deploy to complete

### Build Failed?
- Check the "Actions" tab for error messages
- Ensure HTML syntax is correct after editing
- Test locally if possible with `python -m http.server`

### Images Too Large?
- Use TinyPNG or similar compression tool
- Reduce dimensions to 800x600px
- Convert to JPG format if using PNG

## Quick Checklist

- [ ] 13 images prepared and renamed
- [ ] Images compressed to < 500KB each
- [ ] Images resized to 800x600px (recommended)
- [ ] Images uploaded to `/assets/images/`
- [ ] `index.html` updated with new filenames
- [ ] GitHub Actions build completed successfully
- [ ] Website deployed and images visible

## Support

For more details about image setup, see `/assets/images/IMAGE_GUIDE.md`

---

**Last Updated**: December 25, 2025
**Status**: Ready for image upload
