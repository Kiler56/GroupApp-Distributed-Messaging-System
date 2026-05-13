import axios from 'axios';

const AUTH_URL = import.meta.env.VITE_AUTH_URL;

const api = axios.create({
  baseURL: `${AUTH_URL}/auth`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface User {
  user_id: number;
  username: string;
  email: string;
}

export const authService = {
  login: async (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const { data } = await api.post('/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return data;
  },

  register: async (userData: any) => {
    const { data } = await api.post('/register', userData);
    return data;
  },

  getProfile: async (token: string): Promise<User> => {
    const { data } = await api.get('/profile', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return data;
  },

  getUserById: async (userId: number): Promise<{ id: number; username: string }> => {
    const { data } = await api.get(`/verify/${userId}`);
    return data;
  },

  getAllUsers: async (): Promise<any[]> => {
    const token = localStorage.getItem('token');
    const { data } = await api.get('/users', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return data;
  },

  getUserByEmail: async (email: string): Promise<any> => {
    const { data } = await api.get(`/user-by-email/${email}`);
    return data;
  },
};
