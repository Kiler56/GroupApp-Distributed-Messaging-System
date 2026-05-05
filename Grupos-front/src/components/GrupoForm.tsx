import React, { useState } from 'react';
import { useGrupoStore } from '../hooks/useGrupoStore';
import { useCreateGrupo, useUpdateGrupo } from '../hooks/useGrupos';

export const GrupoForm: React.FC = () => {
  const { selectedGrupo, isModalOpen, setModalOpen, setSelectedGrupo } = useGrupoStore();
  const createMutation = useCreateGrupo();
  const updateMutation = useUpdateGrupo();

  const [nombre, setNombre] = useState(selectedGrupo?.nombre || '');
  const [descripcion, setDescripcion] = useState(selectedGrupo?.descripcion || '');
  const [privado, setPrivado] = useState(selectedGrupo?.privado || false);
  const [requiereInvitacion, setRequiereInvitacion] = useState(selectedGrupo?.requiere_invitacion || false);

  React.useEffect(() => {
    if (selectedGrupo) {
      setNombre(selectedGrupo.nombre);
      setDescripcion(selectedGrupo.descripcion || '');
      setPrivado(selectedGrupo.privado);
      setRequiereInvitacion(selectedGrupo.requiere_invitacion);
    } else {
      setNombre('');
      setDescripcion('');
      setPrivado(false);
      setRequiereInvitacion(false);
    }
  }, [selectedGrupo]);

  if (!isModalOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      nombre,
      descripcion,
      privado,
      requiere_invitacion: requiereInvitacion
    };

    try {
      if (selectedGrupo) {
        await updateMutation.mutateAsync({ id: selectedGrupo.id_grupo, grupo: payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
      setModalOpen(false);
      setSelectedGrupo(null);
    } catch (error) {
      alert("Error al procesar el grupo. Verifica la conexion.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
        <div className="bg-gray-100 p-4 border-b">
          <h2 className="text-xl font-bold text-gray-800">
            {selectedGrupo ? 'Editar Grupo' : 'Crear Nuevo Grupo'}
          </h2>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">Nombre del Grupo</label>
            <input 
              type="text" 
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              className="w-full border-gray-300 border p-3 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" 
              placeholder="Ej: Amigos de la Uni"
              required 
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">Descripcion</label>
            <textarea 
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              className="w-full border-gray-300 border p-3 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all h-24 resize-none"
              placeholder="¿De que trata este grupo?"
            />
          </div>

          <div className="space-y-3 pt-2">
            <label className="flex items-center gap-3 cursor-pointer group">
              <div className="relative flex items-center">
                <input 
                  type="checkbox" 
                  checked={privado}
                  onChange={(e) => setPrivado(e.target.checked)}
                  className="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
              </div>
              <div className="text-sm">
                <p className="font-medium text-gray-800">Grupo Privado</p>
                <p className="text-gray-500 text-xs">Solo personas con el ID pueden verlo</p>
              </div>
            </label>

            <label className="flex items-center gap-3 cursor-pointer group">
              <div className="relative flex items-center">
                <input 
                  type="checkbox" 
                  checked={requiereInvitacion}
                  onChange={(e) => setRequiereInvitacion(e.target.checked)}
                  className="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
              </div>
              <div className="text-sm">
                <p className="font-medium text-gray-800">Requiere Invitacion</p>
                <p className="text-gray-500 text-xs">Los administradores deben aprobar nuevos miembros</p>
              </div>
            </label>
          </div>

          <div className="flex justify-end gap-3 mt-8">
            <button 
              type="button" 
              onClick={() => {
                setModalOpen(false);
                setSelectedGrupo(null);
              }}
              className="px-5 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg font-bold shadow-lg shadow-blue-200 transition-all active:scale-95"
            >
              {selectedGrupo ? 'Guardar Cambios' : 'Crear Grupo'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
