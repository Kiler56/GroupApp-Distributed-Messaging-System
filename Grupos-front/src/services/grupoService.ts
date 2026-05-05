import axios from 'axios';
import { Grupo, GrupoCreate, GrupoUpdate } from '../types';

// En Vite se usa import.meta.env
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';

const api = axios.create({
  baseURL: `${API_URL}/groups`,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const grupoService = {
  getAll: async (): Promise<Grupo[]> => {
    const { data } = await api.get('/');
    return data;
  },

  getById: async (id: string): Promise<Grupo> => {
    const { data } = await api.get(`/${id}`);
    return data;
  },

  create: async (grupo: GrupoCreate): Promise<Grupo> => {
    const { data } = await api.post('/', grupo);
    return data;
  },

  update: async (id: string, grupo: GrupoUpdate): Promise<Grupo> => {
    const { data } = await api.put(`/${id}`, grupo);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/${id}`);
  },
};
