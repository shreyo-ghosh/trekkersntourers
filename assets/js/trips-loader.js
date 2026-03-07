/**
 * Dynamic Trips Loader
 * Fetches trip data from backend API and populates the trips grid
 */

const API_BASE = 'http://localhost:5000';

async function loadTripsFromS3() {
  try {
    const response = await fetch(`${API_BASE}/api/trips`);
    const data = await response.json();

    if (!data.success) {
      console.error('Failed to load trips:', data.error);
      return;
    }

    const tripsGrid = document.querySelector('.trips-grid');
    if (!tripsGrid) return;

    // Clear current trips
    tripsGrid.innerHTML = '';

    // Add trips from S3
    data.trips.forEach(trip => {
      const tripCard = document.createElement('article');
      tripCard.className = 'trip-card';
      
      // Use proxy endpoint for S3 images
      const mainImage = trip.preview_images[0] 
        ? `${API_BASE}/api/image/${trip.preview_images[0]}` 
        : 'assets/images/placeholder.jpg';
      
      tripCard.innerHTML = `
        <img src="${mainImage}" alt="${trip.name}" />
        <div class="trip-card-content">
          <p>${trip.description}</p>
          <span class="trip-level">${trip.level}</span>
        </div>
      `;
      
      tripCard.addEventListener('click', () => showTripModal(trip));
      tripsGrid.appendChild(tripCard);
    });

    console.log(`✓ Loaded ${data.trips.length} trips from S3`);
  } catch (error) {
    console.error('Error loading trips:', error);
  }
}

function showTripModal(trip) {
  const modal = document.createElement('div');
  modal.className = 'trip-modal';
  modal.innerHTML = `
    <div class="trip-modal-content">
      <button class="trip-modal-close">&times;</button>
      <h2>${trip.name}</h2>
      <p>${trip.description}</p>
      <div style="margin: 20px 0;">
        <strong>Images: ${trip.image_count}</strong>
      </div>
      <button class="btn btn-primary" onclick="location.href='#contact'">Book This Trip</button>
    </div>
  `;

  document.body.appendChild(modal);
  modal.querySelector('.trip-modal-close').onclick = () => modal.remove();
}

// Load trips when DOM is ready
document.addEventListener('DOMContentLoaded', loadTripsFromS3);

// Add styles
const style = document.createElement('style');
style.textContent = `
  .trip-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
  }
  .trip-modal-content {
    background: white;
    padding: 40px;
    border-radius: 12px;
    max-width: 500px;
    width: 90%;
    position: relative;
  }
  .trip-modal-close {
    position: absolute;
    top: 16px;
    right: 16px;
    background: none;
    border: none;
    font-size: 32px;
    cursor: pointer;
    color: #666;
  }
`;
document.head.appendChild(style);
