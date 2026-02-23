// Frontend configuration
// Set `window.API_BASE_URL` here to point the frontend to a deployed backend.
// Example: https://pds-backend.herokuapp.com/api/v1 or https://api.yourdomain.com/api/v1

(function () {
  // If you want to override via deployment, replace the value below.
  // When deploying to GitHub Pages + Render, set this to the Render backend URL.
  window.API_BASE_URL = window.API_BASE_URL || 'http://localhost:5000/api/v1';

  // Optional: expose a small config object
  window.APP_CONFIG = window.APP_CONFIG || {
    API_BASE_URL: window.API_BASE_URL,
    FRONTEND_BASE: window.location.origin
  };
})();
