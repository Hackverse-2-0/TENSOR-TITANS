/**
 * Utility Functions for PDS Platform
 * Enterprise-grade security implementation
 */

// Security configuration
const SecurityConfig = {
  SESSION_TIMEOUT: 30 * 60 * 1000, // 30 minutes
  TOKEN_VALIDATION_INTERVAL: 5 * 60 * 1000, // 5 minutes
  SUSPICIOUS_ACTIVITY_THRESHOLD: 3,
};

// Check if user is authenticated
function isAuthenticated() {
  return !!localStorage.getItem('access_token');
}

// Get current user data
function getCurrentUser() {
  const userData = localStorage.getItem('user_data');
  return userData ? JSON.parse(userData) : null;
}

// Logout user with proper cleanup
function logout() {
  const user = getCurrentUser();
  const userName = user ? user.username : 'User';
  
  // Call backend logout endpoint to invalidate token
  api.logout().catch(err => console.log('Logout from backend failed:', err));
  
  // Clear all authentication data
  api.clearToken();
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_data');
  localStorage.removeItem('loginAttempts');
  
  // Clear session storage
  sessionStorage.clear();
  
  // Clear IndexedDB and other storage
  if (window.indexedDB) {
    const dbs = ['pds-platform', 'auth-cache'];
    dbs.forEach(dbName => {
      try {
        indexedDB.deleteDatabase(dbName);
      } catch (e) {
        console.log('Could not clear IndexedDB:', e);
      }
    });
  }
  
  // Show logout notification
  showLogoutNotification(userName);
  
  // Redirect after notification is displayed
  setTimeout(() => {
    window.location.replace('login.html');
  }, 2000);
}

// Show logout notification
function showLogoutNotification(userName) {
  const notification = document.createElement('div');
  notification.className = 'logout-notification';
  notification.innerHTML = `
    <div class="logout-notification-content">
      <div class="logout-icon">👋</div>
      <div class="logout-message">
        <h3>Logged Out Successfully</h3>
        <p>Goodbye, ${userName}!</p>
        <p class="logout-subtitle">You have been safely logged out. Redirecting to login page...</p>
      </div>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  // Animate notification
  setTimeout(() => {
    notification.classList.add('show');
  }, 10);
}

// Check authentication and redirect if needed
function checkAuth() {
  if (!isAuthenticated()) {
    window.location.replace('login.html');
    return false;
  }
  return true;
}

// Setup authentication security (prevents unauthorized access)
function setupAuthenticationSecurity() {
  // Immediate auth check
  if (!isAuthenticated()) {
    window.location.replace('login.html');
    return;
  }
  
  // Setup session tracking
  setupSessionTracking();
  
  // Setup browser security
  setupBrowserSecurity();
  
  // Setup periodic token validation
  setupTokenValidation();
  
  // Setup tab/window monitoring
  setupTabMonitoring();
}

// Monitor active session
function setupSessionTracking() {
  sessionStorage.setItem('authSessionStart', Date.now());
  sessionStorage.setItem('authTabActive', 'true');
  sessionStorage.setItem('lastActivityTime', Date.now());
  
  // Update last activity on user interaction
  ['mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event => {
    document.addEventListener(event, () => {
      sessionStorage.setItem('lastActivityTime', Date.now());
    }, { passive: true });
  });
  
  // Check for session timeout
  setInterval(() => {
    const lastActivity = parseInt(sessionStorage.getItem('lastActivityTime')) || Date.now();
    const timeSinceActivity = Date.now() - lastActivity;
    
    if (timeSinceActivity > SecurityConfig.SESSION_TIMEOUT) {
      logout();
    }
  }, 60000); // Check every minute
}

// Setup browser security
function setupBrowserSecurity() {
  // Push history state for back button protection
  window.history.pushState({ authenticated: true, timestamp: Date.now() }, null, window.location.href);

  // Detect back button
  window.addEventListener('popstate', (event) => {
    if (!event.state || !event.state.authenticated) {
      logout();
    }
  });

  // Prevent page restore from cache
  if (performance && performance.navigation) {
    if (performance.navigation.type === 2) {
      // Page was restored from bfcache
      logout();
      return;
    }
  }

  // Disable scroll restoration to prevent cache issues
  if (window.history.scrollRestoration) {
    window.history.scrollRestoration = 'manual';
  }
}

// Setup periodic token validation
function setupTokenValidation() {
  setInterval(async () => {
    try {
      // Validate token is still valid
      const token = api.getToken();
      if (!token) {
        logout();
        return;
      }
      
      // Call a health check endpoint to ensure session is still valid
      await api.healthCheck();
    } catch (error) {
      console.log('Token validation failed:', error);
      logout();
    }
  }, SecurityConfig.TOKEN_VALIDATION_INTERVAL);
}

// Setup tab and window monitoring
function setupTabMonitoring() {
  // Detect tab switching
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      sessionStorage.setItem('authTabActive', 'false');
      sessionStorage.setItem('authTabLeftTime', Date.now());
    } else {
      const wasInactive = sessionStorage.getItem('authTabActive') === 'false';
      
      if (wasInactive) {
        // User switched tabs and came back - force logout for security
        logout();
        return;
      }
      
      sessionStorage.setItem('authTabActive', 'true');
    }
  });

  // Detect window focus changes
  window.addEventListener('blur', () => {
    sessionStorage.setItem('authTabActive', 'false');
    sessionStorage.setItem('authWindowBlurred', Date.now());
  });

  window.addEventListener('focus', () => {
    if (sessionStorage.getItem('authTabActive') === 'false') {
      logout();
    }
  });

  // Detect page unload
  window.addEventListener('beforeunload', () => {
    sessionStorage.setItem('authTabActive', 'false');
  });
}

// Format date with Indian locale
function formatDate(date) {
  if (typeof date === 'string') {
    date = new Date(date);
  }
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Format number with Indian numbering system
function formatNumber(num) {
  return num.toLocaleString('en-IN');
}

// Truncate text
function truncateText(text, length = 50) {
  if (text.length > length) {
    return text.substring(0, length) + '...';
  }
  return text;
}

// Show loading spinner
function showLoading(element) {
  element.innerHTML = '<div class="spinner"></div> Loading...';
}

// Get severity badge class
function getSeverityClass(severity) {
  return `severity-${severity || 'low'}`;
}

// Get status badge class
function getStatusClass(status) {
  return `status-${status || 'open'}`;
}

// Create a status indicator element
function createStatusIndicator(status, label) {
  return `
    <span class="status-indicator">
      <span class="status-dot ${getStatusClass(status)}"></span>
      ${label || status}
    </span>
  `;
}

// Create a severity badge
function createSeverityBadge(severity) {
  return `<span class="badge ${getSeverityClass(severity)}">${severity.toUpperCase()}</span>`;
}

// Toggle dropdown menu
function toggleDropdown(event) {
  event.preventDefault();
  const menu = event.target.nextElementSibling;
  if (menu && menu.classList.contains('dropdown-menu')) {
    menu.classList.toggle('active');
  }
}

// Build header
function buildHeader() {
  const user = getCurrentUser();
  if (!user) return;

  const header = document.createElement('header');
  header.innerHTML = `
    <div class="header-top">
      <div class="container">
        <div class="govt-info">
          <span>🇮🇳 Government of India</span>
          <span>Ministry of Consumer Affairs, Public Distribution & Food</span>
        </div>
        <span id="current-time"></span>
      </div>
    </div>
    <nav class="nav-main">
      <div class="container">
        <div class="logo-section">
          <a href="dashboard.html" class="logo">
            <div class="logo-icon">📊</div>
            <div class="logo-text">
              <h1>PDS Platform</h1>
              <p>Leak Detection System</p>
            </div>
          </a>
        </div>
        
        <ul class="nav-links">
          <li><a href="dashboard.html">Dashboard</a></li>
          <li><a href="anomalies.html">Anomalies</a></li>
          <li><a href="shops.html">Shops</a></li>
          <li><a href="data-ingestion.html">Data Ingestion</a></li>
        </ul>

        <div class="user-section">
          <div class="user-menu">
            <button class="user-menu-btn" onclick="toggleDropdown(event)">
              👤 ${user.username}
            </button>
            <div class="dropdown-menu">
              <a href="profile.html">My Profile</a>
              <a href="settings.html">Settings</a>
              ${user.role === 'admin' ? '<a href="admin.html">Admin Panel</a>' : ''}
              <button onclick="logout()">Logout</button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  `;

  document.body.insertBefore(header, document.body.firstChild);

  // Update time
  updateCurrentTime();
  setInterval(updateCurrentTime, 1000);
}

// Update current time
function updateCurrentTime() {
  const timeEl = document.getElementById('current-time');
  if (timeEl) {
    const now = new Date();
    timeEl.textContent = now.toLocaleString('en-IN');
  }
}

// Build footer
function buildFooter() {
  const footer = document.createElement('footer');
  footer.innerHTML = `
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h4>About PDS</h4>
          <a href="#">Overview</a>
          <a href="#">Mission & Vision</a>
          <a href="#">Key Features</a>
        </div>
        <div class="footer-section">
          <h4>Support & Help</h4>
          <a href="#">Help Center</a>
          <a href="#">Contact Us</a>
          <a href="#">FAQ</a>
        </div>
        <div class="footer-section">
          <h4>Legal & Policy</h4>
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Service</a>
          <a href="#">Security</a>
        </div>
        <div class="footer-section">
          <h4>Government Links</h4>
          <a href="#">Ministry Website</a>
          <a href="#">Official Government</a>
          <a href="#">Citizen Services</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Government of India. All rights reserved.</p>
        <p>This is an official government website of the Ministry of Consumer Affairs, Public Distribution & Food.<br>
        Last Updated: <span id="last-updated">${new Date().toLocaleDateString('en-IN')}</span></p>
      </div>
    </div>
  `;

  document.body.appendChild(footer);
}

// Initialize main page
function initializePage() {
  if (!checkAuth()) return;
  buildHeader();
  buildFooter();
}

// Display error message
function showError(message, container = null) {
  const alert = document.createElement('div');
  alert.className = 'alert alert-danger';
  alert.textContent = message;
  
  if (container) {
    container.insertAdjacentElement('afterbegin', alert);
  } else {
    document.body.insertAdjacentElement('afterbegin', alert);
  }

  setTimeout(() => alert.remove(), 5000);
}

// Display success message
function showSuccess(message, container = null) {
  const alert = document.createElement('div');
  alert.className = 'alert alert-success';
  alert.textContent = message;
  
  if (container) {
    container.insertAdjacentElement('afterbegin', alert);
  } else {
    document.body.insertAdjacentElement('afterbegin', alert);
  }

  setTimeout(() => alert.remove(), 4000);
}

// Show modal
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
  }
}

// Hide modal
function hideModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
  }
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
  const dropdowns = document.querySelectorAll('.dropdown-menu.active');
  dropdowns.forEach(dropdown => {
    if (!dropdown.parentElement.contains(e.target)) {
      dropdown.classList.remove('active');
    }
  });
});

// Handle modal close button
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-close')) {
    const modal = e.target.closest('.modal');
    if (modal) {
      modal.classList.remove('active');
    }
  }
});

// Close modal when clicking outside
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal')) {
    e.target.classList.remove('active');
  }
});

// Export functions for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    isAuthenticated,
    getCurrentUser,
    logout,
    checkAuth,
    setupAuthenticationSecurity,
    formatDate,
    formatNumber,
    truncateText,
    showLoading,
    getSeverityClass,
    getStatusClass,
    createStatusIndicator,
    createSeverityBadge,
    toggleDropdown,
    buildHeader,
    buildFooter,
    initializePage,
    showError,
    showSuccess,
    showLogoutNotification,
    showModal,
    hideModal
  };
}
