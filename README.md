# Trekkers & Tourers - Travel Website

A curated travel booking website for treks, beach getaways, and waterfall escapes across India.

## Features

- **Curated Experiences**: Handpicked itineraries tested by real travelers
- **Transparent Pricing**: Clear inclusions with no surprise costs
- **Expert Support**: End-to-end assistance on stays, permits, and planning
- **Small Groups**: Limited seats to maintain intimate group experiences
- **Contact Form**: Easy enquiry submission for personalized recommendations

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Modern CSS with CSS Variables and Flexbox/Grid
- **Deployment**: AWS S3 + CloudFront (CI/CD from GitHub Actions)- **Domain**: GoDaddy custom domain with DNS pointing to Netlify

## Project Structure

```
.
├── index.html           # Main landing page
├── assets/
│   ├── css/
│   │   └── style.css   # All styling
│   ├── js/
│   │   └── main.js     # Navigation and dynamic content
│   └── img/            # Placeholder for images
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Installation & Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/shreyo-ghosh/trekkersntourers.git
   cd trekkersntourers
   ```

2. Open `index.html` in your browser (no build step required for static site)

3. For editing, use any code editor (VS Code recommended)

## Deployment

This project is configured for automatic deployment on Netlify:

1. Connect GitHub repo to Netlify
2. Netlify auto-detects static site (HTML/CSS/JS)
3. Every push to `main` triggers automatic deployment
4. Custom domain (trekkersntourers.com) points via DNS to Netlify
5. SSL certificate auto-issued by Let's Encrypt

## Mobile Responsive

- Full responsive design for mobile, tablet, and desktop
- Mobile navigation toggle with hamburger menu
- CSS Grid and Flexbox for modern layouts

## Future Enhancements

- [ ] Backend integration for contact form submissions
- [ ] Payment gateway integration
- [ ] User authentication for bookings
- [ ] Real image galleries for trips
- [ ] Booking calendar system
- [ ] Reviews and ratings from past travelers

## Contact

**Email**: hello@trekkersntourers.com  
**Instagram**: @trekkersntourers  
**Location**: Bengaluru, India

## License

This project is proprietary and not open source.

---

**Note**: Replace placeholder contact details in `index.html` with actual business information before deployment.
