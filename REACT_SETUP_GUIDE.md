REACT_SETUP_GUIDE.md# React Conversion & Deployment Guide

## Project Status: Static HTML → React + GitHub Actions CI/CD + AWS Deployment

This guide walks you through converting the Trekkers & Tourers website from static HTML/CSS/JS to a modern React application with fully automated CI/CD via GitHub Actions and deployment to AWS S3 + CloudFront.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Node.js 18+ (https://nodejs.org)
- npm 9+
- Git

### Step 1: Initialize React Project

```bash
# Clone the repo
git clone https://github.com/shreyo-ghosh/trekkersntourers.git
cd trekkersntourers

# Create React app with Vite (faster than CRA)
npm create vite@latest . -- --template react

# Install dependencies
npm install

# Install additional packages needed
npm install react-router-dom react-hook-form
npm install -D css-modules
```

### Step 2: Project Structure

Create this folder structure:

```
src/
├── components/
│   ├── Header/
│   │   ├── Header.jsx
│   │   └── Header.module.css
│   ├── Hero/
│   │   ├── Hero.jsx
│   │   └── Hero.module.css
│   ├── Trips/
│   │   ├── Trips.jsx
│   │   └── Trips.module.css
│   ├── TripCard/
│   │   ├── TripCard.jsx
│   │   └── TripCard.module.css
│   ├── ContactForm/
│   │   ├── ContactForm.jsx
│   │   └── ContactForm.module.css
│   ├── Footer/
│   │   ├── Footer.jsx
│   │   └── Footer.module.css
│   └── common/
│       ├── Button.jsx
│       ├── Card.jsx
│       └── common.module.css
├── pages/
│   └── Home.jsx
├── utils/
│   ├── constants.js (trip data, contact info)
│   └── helpers.js (utility functions)
├── App.jsx
├── App.module.css
├── main.jsx
└── index.css

public/
├── index.html
├── favicon.ico
└── images/ (placeholder images)
```

### Step 3: Run Development Server

```bash
npm run dev
# Opens at http://localhost:5173
```

---

## 📦 Component Conversion

### Header Component (src/components/Header/Header.jsx)

```jsx
import { useState } from 'react';
import styles from './Header.module.css';

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className={styles.siteHeader}>
      <div className={styles.container}>
        <a href="#" className={styles.logo}>
          Trekkers & Tourers
        </a>
        <button 
          className={styles.navToggle}
          onClick={() => setIsOpen(!isOpen)}
        >
          ☰
        </button>
        <nav className={`${styles.mainNav} ${isOpen ? styles.open : ''}`}>
          <ul id="primary-nav">
            <li><a href="#trips">Trips</a></li>
            <li><a href="#why-us">Why Us</a></li>
            <li><a href="#testimonials">Stories</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
```

### Data Constants (src/utils/constants.js)

```javascript
export const TRIPS = [
  {
    id: 1,
    title: 'Weekend Himalayan Trek',
    description: '2N/3D beginner-friendly trek with local guides, homestays and all permits covered.',
    level: 'Easy–Moderate',
    image: 'https://via.placeholder.com/400x300?text=Himalayan+Trek',
    category: 'mountains'
  },
  {
    id: 2,
    title: 'Coastal Beach Escape',
    description: 'Slow travel by the sea with curated stays, cafes and sunrise/sunset experiences.',
    level: 'Relaxed',
    image: 'https://via.placeholder.com/400x300?text=Beach+Getaway',
    category: 'beach'
  },
  {
    id: 3,
    title: 'Waterfall & Forest Trail',
    description: 'Guided day hike through forests ending at hidden waterfalls and natural pools.',
    level: 'Easy',
    image: 'https://via.placeholder.com/400x300?text=Waterfall',
    category: 'waterfall'
  }
];

export const CONTACT_INFO = {
  email: 'hello@trekkersntourers.com',
  instagram: '@trekkersntourers',
  location: 'Bengaluru, India'
};
```

---

## 🔧 GitHub Actions CI/CD Pipeline

The workflow file (`.github/workflows/deploy.yml`) is already created. It:

1. **Builds** on every push and PR
2. **Tests** the React app
3. **Deploys** to AWS S3 on main branch push
4. **Invalidates** CloudFront cache for instant updates

---

## ☁️ AWS Setup Instructions

### Step 1: Create S3 Bucket

1. Go to [AWS S3 Console](https://s3.amazonaws.com)
2. Click "Create bucket"
3. Name: `trekkersntourers.com`
4. Region: `ap-south-1` (or closest to users)
5. **Uncheck** "Block all public access" 
6. Create bucket

### Step 2: Enable Static Website Hosting

1. Select bucket → Properties
2. Scroll to "Static website hosting"
3. Click "Edit"
4. Enable static website hosting
5. Index document: `index.html`
6. Error document: `index.html` (for SPA routing)
7. Save

### Step 3: Add Bucket Policy

1. Go to Bucket → Permissions
2. Click "Edit" under Bucket policy
3. Paste this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::trekkersntourers.com/*"
    }
  ]
}
```

### Step 4: Create CloudFront Distribution

1. Go to [CloudFront Console](https://console.aws.amazon.com/cloudfront)
2. Click "Create distribution"
3. **Origin domain**: Select your S3 bucket
4. **Viewer protocol policy**: Redirect HTTP to HTTPS
5. **Default root object**: `index.html`
6. **Cache behaviors**: 
   - Default TTL: 0
   - Max TTL: 31536000 (1 year for hashed assets)
7. Create distribution (takes ~5-10 minutes)

### Step 5: Create IAM User for GitHub Actions

1. Go to [IAM Console](https://console.aws.amazon.com/iam)
2. Create new user: `github-actions`
3. Attach policies:
   - `AmazonS3FullAccess`
   - `CloudFrontFullAccess`
4. Create access key → Download CSV

---

## 🔐 GitHub Secrets Setup

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add these secrets from your AWS IAM user:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION = ap-south-1
S3_BUCKET_NAME = trekkersntourers.com
CLOUDFRONT_DISTRIBUTION_ID = (from CloudFront console)
```

---

## 📝 Build & Deploy Commands

```bash
# Development
npm run dev

# Build for production
npm run build

# Preview build locally
npm run preview

# Deploy manually (after GitHub Secrets are set)
git push origin main
# GitHub Actions will automatically build and deploy!
```

---

## 💰 AWS Cost Estimation

- **S3 Storage**: ~$0.10/month (assuming <1GB)
- **S3 Requests**: ~$0.01/month (low traffic)
- **CloudFront**: ~$0.20/month (low traffic)
- **Route 53**: Free tier covers DNS
- **Total**: ~$0.31-0.50/month

---

## ✅ Next Steps

1. Convert remaining components (Hero, Trips, ContactForm, Footer)
2. Implement form validation with React Hook Form
3. Add trip filtering functionality
4. Set up GitHub Secrets
5. Test CI/CD pipeline with a test commit
6. Configure custom domain in Route 53

---

## 🆘 Troubleshooting

### GitHub Actions fails to build
- Check Node version (18+)
- Verify all dependencies installed: `npm install`
- Check for syntax errors in src/

### CloudFront shows cached old version
- Go to CloudFront → Invalidations
- Create new invalidation with `/*`
- Wait 2-5 minutes for cache purge

### S3 shows 403 Forbidden
- Verify bucket policy (step 3 above)
- Check CloudFront origin access (should be bucket)

---

## 📚 Resources

- [Vite Documentation](https://vitejs.dev)
- [React Docs](https://react.dev)
- [AWS S3 Static Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [GitHub Actions](https://github.com/features/actions)
