import { create } from 'zustand';
import { Grupo } from '../types';

interface GrupoState {
  selectedGrupo: Grupo | null;
  setSelectedGrupo: (grupo: Grupo | null) => void;
  isModalOpen: boolean;
  setModalOpen: (isOpen: boolean) => void;
}

export const useGrupoStore = create<GrupoState>((set) => ({
  selectedGrupo: null,
  setSelectedGrupo: (grupo) => set({ selectedGrupo: grupo }),
  isModalOpen: false,
  setModalOpen: (isOpen) => set({ isModalOpen: isOpen }),
}));
