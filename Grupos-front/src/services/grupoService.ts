import axios from 'axios';
import { Grupo, GrupoCreate, GrupoUpdate } from '../types';

// En Vite se usa import.meta.env
const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
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
    const { data } = await api.get('/groups');
    return data;
  },

  getMyGroups: async (): Promise<Grupo[]> => {
    const { data } = await api.get('/my-groups');
    return data;
  },

  getById: async (id: string): Promise<Grupo> => {
    const { data } = await api.get(`/groups/${id}`);
    return data;
  },

  getSubgroups: async (id: string): Promise<Grupo[]> => {
    const { data } = await api.get(`/groups/${id}/subgroups`);
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

  getRoles: async (id: string): Promise<any[]> => {
    const { data } = await api.get(`/${id}/roles`);
    return data;
  },

  createRole: async (id_grupo: string, nombre: string): Promise<any> => {
    const { data } = await api.post(`/${id_grupo}/roles`, { nombre });
    return data;
  },

  updateRole: async (id_grupo: string, id_rol_grupo: string, nombre: string): Promise<any> => {
    const { data } = await api.put(`/${id_grupo}/roles/${id_rol_grupo}`, { nombre });
    return data;
  },

  deleteRole: async (id_grupo: string, id_rol_grupo: string): Promise<void> => {
    await api.delete(`/${id_grupo}/roles/${id_rol_grupo}`);
  },

  getAllResources: async (): Promise<any[]> => {
    const { data } = await api.get(`/resources/all`);
    return data;
  },

  assignPermission: async (id_grupo: string, id_rol_grupo: string, id_recurso: string): Promise<void> => {
    await api.post(`/${id_grupo}/roles/${id_rol_grupo}/permissions/${id_recurso}`);
  },

  removePermission: async (id_grupo: string, id_rol_grupo: string, id_recurso: string): Promise<void> => {
    await api.delete(`/${id_grupo}/roles/${id_rol_grupo}/permissions/${id_recurso}`);
  },

  updateUserRole: async (id_grupo: string, id_usuario: number, id_rol_grupo: string): Promise<void> => {
    await api.put(`/users-groups/${id_grupo}/usuarios/${id_usuario}`, { id_rol_grupo, id_usuario: String(id_usuario), id_estado: 'ACTIVO' });
  },

  removeUser: async (id_grupo: string, id_usuario: number): Promise<void> => {
    await api.delete(`/users-groups/${id_grupo}/usuarios/${id_usuario}`);
  },

  addUserToGroup: async (id_grupo: string, id_usuario: number, id_rol_grupo: string): Promise<void> => {
    const baseUrl = import.meta.env.VITE_API_URL;
    await axios.post(`${baseUrl}/users-groups/${id_grupo}/usuarios`, {
        id_usuario: String(id_usuario),
        id_rol_grupo: id_rol_grupo,
        id_estado: 'ACTIVO'
    }, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    });
  },

  inviteByEmail: async (id_grupo: string, email: string): Promise<any> => {
    const { data } = await api.post(`/${id_grupo}/invite`, { email });
    return data;
  },

  join: async (id_grupo: string): Promise<any> => {
    const { data } = await api.post(`/users-groups/${id_grupo}/join`);
    return data;
  },

  leave: async (id_grupo: string): Promise<any> => {
    const { data } = await api.delete(`/users-groups/${id_grupo}/leave`);
    return data;
  }
};

