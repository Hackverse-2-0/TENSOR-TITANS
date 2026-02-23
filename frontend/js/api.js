/**
 * API Service
 * Handles all communication with the Python Flask backend
 */

class APIClient {
  constructor(baseURL = null) {
    // Prefer configured global API base URL from frontend/js/config.js
    const globalBase = (window && window.API_BASE_URL) ? window.API_BASE_URL : null;
    this.baseURL = baseURL || globalBase || 'http://localhost:5000/api/v1';
    this.token = localStorage.getItem('access_token');
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('access_token', token);
  }

  getToken() {
    return this.token;
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_data');
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  async request(method, endpoint, data = null) {
    const url = `${this.baseURL}${endpoint}`;
    const options = {
      method,
      headers: this.getHeaders()
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);
      const result = await response.json();

      if (!response.ok) {
        if (response.status === 401) {
          this.clearToken();
          window.location.href = '/login.html';
        }
        throw new Error(result.error || 'API request failed');
      }

      return result;
    } catch (error) {
      console.error(`API Error [${method} ${endpoint}]:`, error);
      throw error;
    }
  }

  // Authentication endpoints
  async register(username, email, password, role = 'shop_manager', shop_id = null) {
    return this.request('POST', '/auth/register', {
      username,
      email,
      password,
      role,
      shop_id
    });
  }

  async login(username, password) {
    const result = await this.request('POST', '/auth/login', {
      username,
      password
    });
    if (result.access_token) {
      this.setToken(result.access_token);
      localStorage.setItem('user_data', JSON.stringify(result.user));
    }
    return result;
  }

  async logout() {
    try {
      // Call backend logout endpoint to invalidate token
      return await this.request('POST', '/auth/logout');
    } catch (error) {
      // Even if backend logout fails, proceed with client-side cleanup
      console.error('Backend logout failed:', error);
      return { success: false };
    }
  }

  async getCurrentUser() {
    return this.request('GET', '/auth/me');
  }

  async getUser(userId) {
    return this.request('GET', `/auth/users/${userId}`);
  }

  async listUsers(limit = 50, offset = 0, role = null) {
    let endpoint = `/auth/users?limit=${limit}&offset=${offset}`;
    if (role) {
      endpoint += `&role=${role}`;
    }
    return this.request('GET', endpoint);
  }

  async deactivateUser(userId) {
    return this.request('POST', `/auth/users/${userId}/deactivate`);
  }

  // Shop endpoints
  async createShop(shopData) {
    // Accept either object format or individual parameters
    if (typeof shopData === 'string') {
      // Legacy format: createShop(code, name, location, lat, lon)
      return this.request('POST', '/shops', {
        shop_code: arguments[0],
        shop_name: arguments[1],
        location: arguments[2],
        latitude: arguments[3],
        longitude: arguments[4]
      });
    }
    return this.request('POST', '/shops', shopData);
  }

  async listShops(limit = 50, offset = 0) {
    return this.request('GET', `/shops?limit=${limit}&offset=${offset}`);
  }

  async getShop(shopId) {
    return this.request('GET', `/shops/${shopId}`);
  }

  async updateShop(shopId, data) {
    return this.request('PUT', `/shops/${shopId}`, data);
  }

  async deleteShop(shopId) {
    return this.request('DELETE', `/shops/${shopId}`);
  }

  async getShopStats(shopId) {
    return this.request('GET', `/shops/${shopId}/stats`);
  }

  // Data ingestion endpoints
  async ingestStockData(shopId, stocks) {
    return this.request('POST', '/data/ingest/stock', {
      shop_id: shopId,
      stocks
    });
  }

  async ingestBiometricLogs(shopId, biometricLogs) {
    return this.request('POST', '/data/ingest/biometric', {
      shop_id: shopId,
      biometric_logs: biometricLogs
    });
  }

  async ingestDeliverySchedules(shopId, deliveries) {
    return this.request('POST', '/data/ingest/delivery', {
      shop_id: shopId,
      deliveries
    });
  }

  // Anomaly detection endpoints
  async detectAnomalies(shopId) {
    return this.request('POST', `/anomalies/detect/${shopId}`);
  }

  async getAnomalies(shopId, severity = null, anomalyType = null, status = null, limit = 50, offset = 0) {
    let endpoint = `/anomalies/${shopId}?limit=${limit}&offset=${offset}`;
    if (severity) endpoint += `&severity=${severity}`;
    if (anomalyType) endpoint += `&anomaly_type=${anomalyType}`;
    if (status) endpoint += `&status=${status}`;
    return this.request('GET', endpoint);
  }

  async resolveAnomaly(anomalyId, status, notes) {
    return this.request('POST', `/anomalies/${anomalyId}/resolve`, {
      status,
      resolution_notes: notes
    });
  }

  async getAnomalyStats(shopId) {
    return this.request('GET', `/anomalies/stats/${shopId}`);
  }

  // Data retrieval endpoints
  async getStocks(shopId = null, limit = 50, offset = 0) {
    let endpoint = `/database/stocks?limit=${limit}&offset=${offset}`;
    if (shopId) endpoint += `&shop_id=${shopId}`;
    return this.request('GET', endpoint);
  }

  async getBiometricLogs(shopId = null, limit = 50, offset = 0) {
    let endpoint = `/database/biometric-logs?limit=${limit}&offset=${offset}`;
    if (shopId) endpoint += `&shop_id=${shopId}`;
    return this.request('GET', endpoint);
  }

  async getDeliveries(shopId = null, limit = 50, offset = 0) {
    let endpoint = `/database/deliveries?limit=${limit}&offset=${offset}`;
    if (shopId) endpoint += `&shop_id=${shopId}`;
    return this.request('GET', endpoint);
  }

  async getAllAnomalies(shopId = null, limit = 50, offset = 0) {
    let endpoint = `/database/anomalies?limit=${limit}&offset=${offset}`;
    if (shopId) endpoint += `&shop_id=${shopId}`;
    return this.request('GET', endpoint);
  }

  async getDatabaseStats(shopId = null) {
    let endpoint = '/database/stats';
    if (shopId) endpoint += `?shop_id=${shopId}`;
    return this.request('GET', endpoint);
  }

  async exportStocks(shopId = null) {
    let endpoint = '/database/export/stocks';
    if (shopId) endpoint += `?shop_id=${shopId}`;
    return this.request('GET', endpoint);
  }

  async exportBiometric(shopId = null) {
    let endpoint = '/database/export/biometric';
    if (shopId) endpoint += `?shop_id=${shopId}`;
    return this.request('GET', endpoint);
  }

  async exportDeliveries(shopId = null) {
    let endpoint = '/database/export/deliveries';
    if (shopId) endpoint += `?shop_id=${shopId}`;
    return this.request('GET', endpoint);
  }

  // Health check
  async healthCheck() {
    return this.request('GET', '/health');
  }
}

// Export for use in modules
const api = new APIClient();
