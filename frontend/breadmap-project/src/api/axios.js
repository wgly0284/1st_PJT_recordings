import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/', // Django 백엔드 서버 주소
});

// API 요청을 보내기 전에 헤더에 토큰을 추가하는 인터셉터
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default apiClient;
