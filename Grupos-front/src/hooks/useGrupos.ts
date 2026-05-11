import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { grupoService } from '../services/grupoService';
import { GrupoCreate, GrupoUpdate } from '../types';

export const useGrupos = () => {
  return useQuery({
    queryKey: ['grupos'],
    queryFn: grupoService.getAll,
  });
};

export const useMyGrupos = () => {
  return useQuery({
    queryKey: ['my-grupos'],
    queryFn: grupoService.getMyGroups,
  });
};

export const useGrupo = (id: string) => {
  return useQuery({
    queryKey: ['grupos', id],
    queryFn: () => grupoService.getById(id),
    enabled: !!id,
  });
};

export const useCreateGrupo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (newGrupo: GrupoCreate) => grupoService.create(newGrupo),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['grupos'] });
      queryClient.invalidateQueries({ queryKey: ['my-grupos'] });
    },
  });
};

export const useUpdateGrupo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, grupo }: { id: string; grupo: GrupoUpdate }) =>
      grupoService.update(id, grupo),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['grupos'] });
      queryClient.invalidateQueries({ queryKey: ['my-grupos'] });
      queryClient.invalidateQueries({ queryKey: ['grupos', data.id_grupo] });
    },
  });
};

export const useDeleteGrupo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => grupoService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['grupos'] });
      queryClient.invalidateQueries({ queryKey: ['my-grupos'] });
    },
  });
};

export const useJoinGrupo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => grupoService.join(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['grupos'] });
      queryClient.invalidateQueries({ queryKey: ['my-grupos'] });
    },
  });
};

export const useLeaveGrupo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => grupoService.leave(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['grupos'] });
      queryClient.invalidateQueries({ queryKey: ['my-grupos'] });
    },
  });
};
