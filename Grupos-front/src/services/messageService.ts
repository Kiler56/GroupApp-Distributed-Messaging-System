import axios from 'axios';

const MSG_URL = import.meta.env.VITE_MSG_URL || 'http://localhost:8001';
const MEDIA_URL = import.meta.env.VITE_MEDIA_URL || 'http://localhost:8003';
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';

const api = axios.create({
  baseURL: MSG_URL,
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

export interface Message {
  id_mensaje?: number;
  chat_id: string;
  sender_id: number;
  type: 'text' | 'image';
  content: string;
  timestamp?: string;
}

export const messageService = {
  getMessages: async (chatId: string): Promise<Message[]> => {
    const { data } = await api.get(`/messages/${chatId}`);
    return data;
  },

  getGroupUsers: async (groupId: string): Promise<any[]> => {
    const { data } = await axios.get(`${API_URL}/users-groups/${groupId}/usuarios`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return data;
  },

  sendMessage: async (message: Partial<Message>): Promise<Message> => {
    const { data } = await api.post('/messages/send', message);
    return data;
  },

  uploadMedia: async (file: File, expectedViews: number) => {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await axios.post(`${MEDIA_URL}/media/upload?expected_views=${expectedViews}`, formData);
    return data;
  },

  getMediaUrl: (mediaId: string, userId: number) => `${MEDIA_URL}/media/${mediaId}?user_id=${userId}`,
};
