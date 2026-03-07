#!/usr/bin/env python3
"""
Trekkers & Tourers Backend Server
Manages S3 trips integration and designer uploads
"""

from flask import Flask, jsonify, request, render_template_string, send_file
from flask_cors import CORS
import boto3
from pathlib import Path
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# AWS Configuration (use environment variables)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.getenv('S3_BUCKET', 'trekkersntourers.com')
S3_REGION = os.getenv('S3_REGION', 'ap-south-1')
UPLOAD_FOLDER = 'assets/uploads/designs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'pdf', 'figma'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

def get_s3_client():
    """Create S3 client"""
    return boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_s3_folders():
    """Get list of folders in S3 bucket"""
    try:
        s3 = get_s3_client()
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Delimiter='/')
        
        folders = []
        if 'CommonPrefixes' in response:
            for prefix in response['CommonPrefixes']:
                folder_name = prefix['Prefix'].rstrip('/').split('/')[-1]
                if folder_name and not folder_name.startswith('.'):
                    folders.append(folder_name)
        
        return sorted(folders)
    except Exception as e:
        print(f"Error listing S3 folders: {e}")
        return []

def get_folder_images(folder_name):
    """Get first 3 images from a folder for trip preview"""
    try:
        s3 = get_s3_client()
        prefix = f"{folder_name}/"
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
        
        images = []
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                ext = Path(key).suffix.lower()
                if ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
                    images.append(key)
                if len(images) >= 3:
                    break
        
        return images
    except Exception as e:
        print(f"Error getting folder images: {e}")
        return []

@app.route('/api/image/<path:image_key>', methods=['GET'])
def get_image(image_key):
    """Proxy endpoint to serve S3 images"""
    try:
        s3 = get_s3_client()
        response = s3.get_object(Bucket=S3_BUCKET, Key=image_key)
        return send_file(
            response['Body'],
            mimetype=response.get('ContentType', 'image/jpeg'),
            as_attachment=False
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/trips', methods=['GET'])
def get_trips():
    """Get all trip offerings from S3 folders"""
    try:
        folders = get_s3_folders()
        
        trips = []
        for folder in folders:
            images = get_folder_images(folder)
            if images:
                trip = {
                    'id': folder.lower().replace(' ', '-'),
                    'name': folder.replace('_', ' ').title(),
                    'folder': folder,
                    'preview_images': images,
                    'image_count': len(get_all_folder_images(folder)),
                    'description': f"Curated experience in {folder}. Small groups, local guides, authentic experiences.",
                    'level': 'Moderate'
                }
                trips.append(trip)
        
        return jsonify({
            'success': True,
            'trips': trips,
            'count': len(trips)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_all_folder_images(folder_name):
    """Get all images in a folder"""
    try:
        s3 = get_s3_client()
        prefix = f"{folder_name}/"
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
        
        images = []
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                ext = Path(key).suffix.lower()
                if ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
                    images.append(key)
        
        return images
    except Exception as e:
        return []

@app.route('/api/trips/<trip_id>/images', methods=['GET'])
def get_trip_images(trip_id):
    """Get all images for a specific trip"""
    try:
        folders = get_s3_folders()
        folder_name = next((f for f in folders if f.lower().replace(' ', '-') == trip_id), None)
        
        if not folder_name:
            return jsonify({'success': False, 'error': 'Trip not found'}), 404
        
        images = get_all_folder_images(folder_name)
        return jsonify({
            'success': True,
            'trip': folder_name,
            'images': images,
            'count': len(images)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/designs', methods=['GET'])
def get_designs():
    """Get all uploaded Figma designs"""
    try:
        designs = []
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                designs.append({
                    'id': filename.replace('.', '_'),
                    'name': filename,
                    'url': f'/api/designs/{filename}',
                    'size': os.path.getsize(filepath),
                    'uploaded': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                })
        
        return jsonify({
            'success': True,
            'designs': sorted(designs, key=lambda x: x['uploaded'], reverse=True)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/designs/<filename>', methods=['GET'])
def get_design(filename):
    """Download a design file"""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/designs/upload', methods=['POST'])
def upload_design():
    """Upload a Figma design"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'message': 'Design uploaded successfully',
            'filename': filename,
            'url': f'/api/designs/{filename}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    """Admin dashboard for uploads"""
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Designer Admin - Trekkers & Tourers</title>
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
          --primary: #146ef5;
          --primary-dark: #0d5ecb;
          --text-primary: #1a1a1a;
          --text-secondary: #666;
          --border-light: #e8e8e8;
          --bg-light: #f8f9fa;
          --white: #ffffff;
          --success: #10b981;
          --error: #ef4444;
        }
        body {
          font-family: 'Inter', sans-serif;
          background: var(--bg-light);
          color: var(--text-primary);
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header {
          background: var(--primary);
          color: white;
          padding: 20px 0;
          margin-bottom: 40px;
        }
        h1 { font-size: 32px; font-weight: 700; }
        h2 { font-size: 24px; font-weight: 700; margin: 32px 0 16px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 32px; }
        .card {
          background: white;
          padding: 32px;
          border-radius: 12px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .upload-area {
          border: 2px dashed var(--border-light);
          border-radius: 8px;
          padding: 40px;
          text-align: center;
          transition: all 0.3s;
          cursor: pointer;
        }
        .upload-area:hover {
          border-color: var(--primary);
          background: var(--bg-light);
        }
        .upload-area.dragover {
          border-color: var(--primary);
          background: rgba(20, 110, 245, 0.05);
        }
        .upload-icon { font-size: 48px; margin-bottom: 16px; }
        input[type="file"] { display: none; }
        .btn {
          padding: 12px 24px;
          border: none;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }
        .btn-primary {
          background: var(--primary);
          color: white;
        }
        .btn-primary:hover { background: var(--primary-dark); }
        .btn-secondary {
          background: var(--bg-light);
          color: var(--primary);
          border: 1px solid var(--border-light);
        }
        .btn-secondary:hover { background: white; }
        .file-list { list-style: none; }
        .file-item {
          padding: 12px;
          border-bottom: 1px solid var(--border-light);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .file-item:last-child { border-bottom: none; }
        .file-name { font-weight: 500; }
        .file-date { font-size: 12px; color: var(--text-secondary); }
        .trips-list { list-style: none; }
        .trip-item {
          padding: 16px;
          background: var(--bg-light);
          border-radius: 8px;
          margin-bottom: 12px;
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .trip-info { flex: 1; }
        .trip-name { font-weight: 600; }
        .trip-count { font-size: 12px; color: var(--text-secondary); }
        .badge {
          display: inline-block;
          padding: 4px 12px;
          background: var(--primary);
          color: white;
          border-radius: 20px;
          font-size: 12px;
          font-weight: 600;
        }
        .alert {
          padding: 16px;
          border-radius: 8px;
          margin-bottom: 16px;
        }
        .alert-success { background: #d1fae5; color: #065f46; }
        .alert-error { background: #fee2e2; color: #7f1d1d; }
        .loading { text-align: center; color: var(--text-secondary); }
        .spinner {
          border: 3px solid var(--bg-light);
          border-top-color: var(--primary);
          border-radius: 50%;
          width: 24px;
          height: 24px;
          animation: spin 0.6s linear infinite;
          display: inline-block;
          margin-right: 8px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
      </style>
    </head>
    <body>
      <header>
        <div class="container">
          <h1>🎨 Designer Admin Panel</h1>
          <p>Upload Figma designs and manage trip content</p>
        </div>
      </header>

      <div class="container">
        <div class="grid">
          <!-- Upload Section -->
          <div class="card">
            <h2>Upload Figma Design</h2>
            <div id="uploadArea" class="upload-area">
              <div class="upload-icon">📁</div>
              <p><strong>Drag & drop your design here</strong></p>
              <p style="font-size: 14px; color: var(--text-secondary); margin-top: 8px;">or click to browse</p>
              <p style="font-size: 12px; color: var(--text-secondary); margin-top: 12px;">PNG, JPG, WebP, PDF, Figma files up to 50MB</p>
            </div>
            <input type="file" id="fileInput" accept=".png,.jpg,.jpeg,.webp,.pdf,.figma" />
            <div id="uploadStatus" style="margin-top: 16px;"></div>
          </div>

          <!-- Uploaded Designs Section -->
          <div class="card">
            <h2>Uploaded Designs</h2>
            <ul id="designsList" class="file-list">
              <li class="file-item">
                <span class="loading"><span class="spinner"></span>Loading...</span>
              </li>
            </ul>
          </div>

          <!-- Trips Section -->
          <div class="card">
            <h2>Available Trips (from S3)</h2>
            <ul id="tripsList" class="trips-list">
              <li class="file-item">
                <span class="loading"><span class="spinner"></span>Loading...</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const uploadStatus = document.getElementById('uploadStatus');
        const designsList = document.getElementById('designsList');
        const tripsList = document.getElementById('tripsList');

        // Upload functionality
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
          e.preventDefault();
          uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
          uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
          e.preventDefault();
          uploadArea.classList.remove('dragover');
          fileInput.files = e.dataTransfer.files;
          handleFileUpload();
        });
        
        fileInput.addEventListener('change', handleFileUpload);

        async function handleFileUpload() {
          const file = fileInput.files[0];
          if (!file) return;

          const formData = new FormData();
          formData.append('file', file);

          uploadStatus.innerHTML = '<div class="loading"><span class="spinner"></span>Uploading...</div>';

          try {
            const response = await fetch('/api/designs/upload', {
              method: 'POST',
              body: formData
            });
            const data = await response.json();

            if (data.success) {
              uploadStatus.innerHTML = '<div class="alert alert-success">✓ ' + data.message + '</div>';
              fileInput.value = '';
              loadDesigns();
              setTimeout(() => uploadStatus.innerHTML = '', 3000);
            } else {
              uploadStatus.innerHTML = '<div class="alert alert-error">✗ ' + data.error + '</div>';
            }
          } catch (error) {
            uploadStatus.innerHTML = '<div class="alert alert-error">✗ Upload failed: ' + error.message + '</div>';
          }
        }

        async function loadDesigns() {
          try {
            const response = await fetch('/api/designs');
            const data = await response.json();

            if (data.success && data.designs.length > 0) {
              designsList.innerHTML = data.designs.map(design => `
                <li class="file-item">
                  <div>
                    <div class="file-name">📄 ${design.name}</div>
                    <div class="file-date">${new Date(design.uploaded).toLocaleString()}</div>
                  </div>
                  <a href="${design.url}" class="btn btn-secondary">Download</a>
                </li>
              `).join('');
            } else {
              designsList.innerHTML = '<li class="file-item"><p style="color: var(--text-secondary);">No designs uploaded yet</p></li>';
            }
          } catch (error) {
            designsList.innerHTML = '<li class="file-item"><p style="color: var(--text-secondary);">Error loading designs</p></li>';
          }
        }

        async function loadTrips() {
          try {
            const response = await fetch('/api/trips');
            const data = await response.json();

            if (data.success && data.trips.length > 0) {
              tripsList.innerHTML = data.trips.map(trip => `
                <li class="trip-item">
                  <div class="trip-info">
                    <div class="trip-name">${trip.name}</div>
                    <div class="trip-count">${trip.image_count} images in folder</div>
                  </div>
                  <span class="badge">${trip.level}</span>
                </li>
              `).join('');
            } else {
              tripsList.innerHTML = '<li class="file-item"><p style="color: var(--text-secondary);">No trips found. Upload folders to S3!</p></li>';
            }
          } catch (error) {
            tripsList.innerHTML = '<li class="file-item"><p style="color: var(--text-secondary);">Error loading trips</p></li>';
          }
        }

        // Load on page load
        loadDesigns();
        loadTrips();
      </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/', methods=['GET'])
def index():
    """Serve main page"""
    return "Trekkers & Tourers API Server - Visit /admin for designer panel"

if __name__ == '__main__':
    print("Starting Trekkers & Tourers Backend Server...")
    print("Admin Panel: http://localhost:5000/admin")
    print("API Endpoints:")
    print("  GET  /api/trips")
    print("  GET  /api/trips/<trip_id>/images")
    print("  GET  /api/designs")
    print("  POST /api/designs/upload")
    app.run(debug=True, port=5000)
