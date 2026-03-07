Guidelines for adding images

- Filenames: use lowercase, hyphens and descriptive names, e.g. `highland.jpg`, `hero-beach.webp`.
- Recommended sizes:
  - Hero / large banner: 1600×900 (webp/jpeg), ~200–400 KB after compression
  - Content images: 1200×800 or 800×600
  - Thumbnails: 400×300
- Formats:
  - Use WebP for best compression where supported: `.webp` (fallback to `.jpg` or `.jpeg`)
  - Use `.jpg` for photos if you need maximum compatibility
- Compression: run images through an optimizer (e.g., Squoosh.app, tinyjpg.com) to reduce size while keeping quality
- Accessibility: add descriptive alt text in HTML (avoid filenames as alt text)
- Steps to add an image to the site:
  1. Save your optimized image to `assets/images/`, e.g. `assets/images/highland.jpg`.
  2. In `index.html` replace placeholder paths or the example `assets/images/highland.jpg` with your filename if different.
  3. Preview locally (open `index.html` in a browser or run a simple static server).
  4. Add, commit and push to your Git repo:
     - `git add assets/images/<your-image>`
     - `git commit -m "Add highland image for upcoming trip"`
     - `git push`
- Hosting note: If you use GitHub Pages, images in the repository will be served automatically.

If you want, I can add a small sample placeholder image or help optimize images you provide.