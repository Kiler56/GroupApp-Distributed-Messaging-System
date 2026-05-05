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
    <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-md flex items-center justify-center p-4 z-50 transition-all">
      <div className="bg-white rounded-[2.5rem] shadow-2xl w-full max-w-lg overflow-hidden border border-white/20 transform animate-in fade-in zoom-in duration-300">
        <div className="bg-indigo-600 p-8 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-4 -mr-4 w-32 h-32 bg-white/10 rounded-full blur-2xl"></div>
          <h2 className="text-3xl font-black tracking-tight relative z-10">
            {selectedGrupo ? 'Editar comunidad' : 'Nueva comunidad'}
          </h2>
          <p className="text-indigo-100 text-sm font-medium mt-1 relative z-10 opacity-80">
            {selectedGrupo ? 'Actualiza los detalles de tu grupo' : 'Crea un espacio para compartir con otros'}
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="p-10 space-y-8">
          <div className="space-y-6">
            <div>
              <label className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-1">Identidad</label>
              <input 
                type="text" 
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                className="input-field !bg-slate-50 border-none focus:!bg-white shadow-inner" 
                placeholder="Ej: Desarrolladores Backend"
                required 
              />
            </div>

            <div>
              <label className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-1">Propósito</label>
              <textarea 
                value={descripcion}
                onChange={(e) => setDescripcion(e.target.value)}
                className="input-field !bg-slate-50 border-none focus:!bg-white shadow-inner h-32 resize-none"
                placeholder="Describe de qué trata este espacio..."
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <label className={`flex flex-col p-4 rounded-2xl border-2 transition-all cursor-pointer ${privado ? 'border-indigo-600 bg-indigo-50/30' : 'border-slate-100 bg-slate-50/50 hover:bg-slate-50'}`}>
                <div className="flex items-center gap-3 mb-1">
                  <input 
                    type="checkbox" 
                    checked={privado}
                    onChange={(e) => setPrivado(e.target.checked)}
                    className="w-5 h-5 rounded-full border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className={`font-black text-xs uppercase tracking-wider ${privado ? 'text-indigo-700' : 'text-slate-500'}`}>Privado</span>
                </div>
                <span className="text-[10px] text-slate-400 font-medium px-8 leading-tight">Solo visible para miembros invitados</span>
              </label>

              <label className={`flex flex-col p-4 rounded-2xl border-2 transition-all cursor-pointer ${requiereInvitacion ? 'border-indigo-600 bg-indigo-50/30' : 'border-slate-100 bg-slate-50/50 hover:bg-slate-50'}`}>
                <div className="flex items-center gap-3 mb-1">
                  <input 
                    type="checkbox" 
                    checked={requiereInvitacion}
                    onChange={(e) => setRequiereInvitacion(e.target.checked)}
                    className="w-5 h-5 rounded-full border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className={`font-black text-xs uppercase tracking-wider ${requiereInvitacion ? 'text-indigo-700' : 'text-slate-500'}`}>Seguro</span>
                </div>
                <span className="text-[10px] text-slate-400 font-medium px-8 leading-tight">Requiere aprobación de administrador</span>
              </label>
            </div>
          </div>

          <div className="flex items-center gap-4 pt-4">
            <button 
              type="button" 
              onClick={() => { setModalOpen(false); setSelectedGrupo(null); }}
              className="flex-1 px-6 py-4 text-xs font-black text-slate-400 hover:text-slate-600 uppercase tracking-widest transition-colors"
            >
              Cerrar
            </button>
            <button 
              type="submit" 
              className="flex-[2] btn-primary shadow-indigo-200"
            >
              {selectedGrupo ? 'Actualizar' : 'Crear comunidad'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
