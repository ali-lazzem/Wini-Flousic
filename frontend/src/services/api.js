import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

// Add token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refresh = localStorage.getItem('refresh_token');
        const response = await axios.post('/api/auth/token/refresh/', { refresh });
        localStorage.setItem('access_token', response.data.access);
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export const goalApi = {
  list: () => api.get('/predictions/goals/'),
  create: (data) => api.post('/predictions/goals/', data),
  update: (id, data) => api.put(`/predictions/goals/${id}/`, data),
  delete: (id) => api.delete(`/predictions/goals/${id}/`),
};

export default api;