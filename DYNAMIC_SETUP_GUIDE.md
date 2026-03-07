# Dynamic Trips & Designer Interface Setup

## Overview

You now have a complete backend system that:
1. **Dynamically loads trips** from S3 folders (Bhutan, Jaisalmer, etc.)
2. **Admin panel** for your designer to upload Figma designs
3. **API endpoints** for managing content

## Architecture

```
Frontend (index.html)
    ↓
trips-loader.js (fetches trips API)
    ↓
Backend (backend_server.py)
    ↓
S3 Bucket (folders with images)
```

## Running Locally

### Step 1: Start the Backend Server

```bash
cd c:\Users\SHREYO\Documents\GitHub\trekkersntourers
C:\Users\SHREYO\Documents\GitHub\trekkersntourers\.venv\Scripts\python.exe backend_server.py
```

The server will start on **http://localhost:5000**

### Step 2: In a new terminal, keep the web server running

```bash
cd c:\Users\SHREYO\Documents\GitHub\trekkersntourers
python -m http.server 8000
```

### Step 3: Access the interfaces

- **Main Website**: http://localhost:8000
- **Designer Admin Panel**: http://localhost:5000/admin
- **API**: http://localhost:5000/api/trips

## Designer Upload Interface

Your designer can access the admin panel at: **http://localhost:5000/admin**

Features:
- ✅ Drag & drop Figma designs
- ✅ Upload PNG, JPG, WebP, PDF files
- ✅ See all uploaded designs
- ✅ View all S3 trips available
- ✅ Download any uploaded design

## How It Works

### 1. Adding New Trips

Simply upload a new folder with images to your S3 bucket:
- Create folder in S3: `your-bucket/Nepal/` 
- Add images to the folder
- Refresh website → "Nepal" appears as new trip

The system automatically:
- Reads all S3 folders
- Extracts preview images
- Creates trip cards
- Links to all images in that folder

### 2. S3 Folder Structure

```
trekkersntourers.com/
├── assets/bhutan/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── jaisalmer/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── [NEW_TRIP]/
    ├── image1.jpg
    └── ...
```

Any new folder automatically becomes a trip!

### 3. Designer Uploads

When your designer uploads a Figma design through the admin panel:
- Files go to: `assets/uploads/designs/`
- Can be PNG, JPG, WebP, PDF, or .figma files
- Max 50MB per file
- Uploads timestamped automatically

## API Endpoints

### Get All Trips from S3
```
GET http://localhost:5000/api/trips

Response:
{
  "success": true,
  "trips": [
    {
      "id": "bhutan",
      "name": "Bhutan",
      "folder": "Bhutan",
      "preview_images": ["assets/bhutan/img1.jpg", ...],
      "image_count": 14,
      "description": "Curated experience in Bhutan...",
      "level": "Moderate"
    }
  ],
  "count": 2
}
```

### Get All Images for a Trip
```
GET http://localhost:5000/api/trips/bhutan/images

Response:
{
  "success": true,
  "trip": "Bhutan",
  "images": ["assets/bhutan/img1.jpg", ...],
  "count": 14
}
```

### Get Uploaded Designs
```
GET http://localhost:5000/api/designs

Response:
{
  "success": true,
  "designs": [
    {
      "id": "20260307_212837_design",
      "name": "20260307_212837_design.png",
      "url": "/api/designs/20260307_212837_design.png",
      "size": 1234567,
      "uploaded": "2026-03-07T21:28:37"
    }
  ]
}
```

### Upload a Design
```
POST http://localhost:5000/api/designs/upload

Body: multipart/form-data with "file" field

Response:
{
  "success": true,
  "message": "Design uploaded successfully",
  "filename": "20260307_212837_design.png",
  "url": "/api/designs/20260307_212837_design.png"
}
```

## Deployment

### Production Deployment (Netlify + Heroku)

1. **Backend (Python) on Heroku**
   ```bash
   # Add Procfile
   echo "web: gunicorn backend_server:app" > Procfile
   
   # Create requirements.txt
   pip freeze > requirements.txt
   
   # Deploy
   heroku create your-app-name
   heroku config:set AWS_ACCESS_KEY=xxxxx
   heroku config:set AWS_SECRET_KEY=xxxxx
   git push heroku main
   ```

   Backend URL: `https://your-app-name.herokuapp.com`

2. **Frontend on Netlify** (current setup)
   - Update `trips-loader.js` API_BASE to Heroku URL
   - Push to GitHub
   - Auto-deploys

3. **Update trips-loader.js**
   ```javascript
   const API_BASE = 'https://your-app-name.herokuapp.com'; // Production
   ```

## Troubleshooting

### Trips not loading?
1. Check backend is running: `http://localhost:5000/api/trips`
2. Check AWS credentials are correct
3. Check S3 bucket contains folders with images
4. Browser console for errors

### Designer can't upload?
1. Ensure `/assets/uploads/designs/` folder exists
2. Check file type is allowed
3. Check file size < 50MB

### CORS errors?
- Already configured in backend (Flask-CORS)
- Production: Update CORS settings as needed

## Environment Variables

For production deployment:
```
AWS_ACCESS_KEY=your_key
AWS_SECRET_KEY=your_secret
```

## File Structure

```
trekkersntourers/
├── index.html (main website)
├── backend_server.py (Flask backend)
├── assets/
│   ├── js/
│   │   ├── trips-loader.js (fetches trips dynamically)
│   │   └── main.js
│   ├── css/
│   │   └── style.css
│   ├── images/ (local images from S3)
│   └── uploads/
│       └── designs/ (designer uploads)
└── README.md
```

## Features Summary

✅ **Dynamic Trip Offerings** - Add trips by uploading folders to S3  
✅ **Designer Upload Panel** - Beautiful interface for Figma designs  
✅ **Real-time Updates** - Changes on S3 appear on website immediately  
✅ **RESTful API** - Easy to extend with more features  
✅ **Responsive** - Works on mobile, tablet, desktop  
✅ **Scalable** - Backend can handle 1000s of trips + designs  

## Next Steps

1. Start both servers (backend on 5000, frontend on 8000)
2. Test designer panel at `/admin`
3. Add new folders to S3 and watch trips appear
4. When ready, deploy backend to Heroku + frontend to Netlify

Questions? Check logs in the terminal running the backend server! 🚀
