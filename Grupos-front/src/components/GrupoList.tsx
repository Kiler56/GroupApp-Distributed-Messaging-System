import React from 'react';
import { useGrupos, useDeleteGrupo } from '../hooks/useGrupos';
import { useGrupoStore } from '../hooks/useGrupoStore';
import { navigateToMessages } from '../helpers/navigation';

export const GrupoList: React.FC = () => {
  const { data: grupos, isLoading, error } = useGrupos();
  const { mutate: deleteGrupo } = useDeleteGrupo();
  const { setSelectedGrupo, setModalOpen } = useGrupoStore();

  if (isLoading) return <div className="p-8 text-center text-gray-500">Cargando grupos...</div>;
  if (error) return <div className="p-8 text-center text-red-500 font-medium">Error al cargar grupos</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8 bg-white p-4 rounded-xl shadow-sm border">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Panel de Gestion</h2>
          <p className="text-sm text-gray-500">Administra tus grupos y accede a tus conversaciones</p>
        </div>
        <button 
          onClick={() => {
            setSelectedGrupo(null);
            setModalOpen(true);
          }}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg font-bold shadow-lg shadow-blue-100 transition-all active:scale-95 flex items-center gap-2"
        >
          <span className="text-xl">+</span> Nuevo Grupo
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-md border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="px-6 py-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Grupo</th>
                <th className="px-6 py-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Estado</th>
                <th className="px-6 py-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Creado</th>
                <th className="px-6 py-4 text-xs font-bold text-gray-400 uppercase tracking-wider text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {grupos?.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-12 text-center text-gray-400">
                    No tienes grupos creados todavia.
                  </td>
                </tr>
              ) : (
                grupos?.map((grupo) => (
                  <tr 
                    key={grupo.id_grupo} 
                    className="hover:bg-blue-50/50 transition-colors cursor-pointer group"
                    onClick={() => navigateToMessages(grupo.id_grupo)}
                  >
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="font-bold text-gray-700 group-hover:text-blue-600 transition-colors">
                          {grupo.nombre}
                        </span>
                        <span className="text-sm text-gray-500 line-clamp-1 max-w-xs">
                          {grupo.descripcion || 'Sin descripcion'}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        grupo.privado 
                          ? 'bg-amber-100 text-amber-700' 
                          : 'bg-green-100 text-green-700'
                      }`}>
                        {grupo.privado ? 'Privado' : 'Publico'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 font-mono">
                      {new Date(grupo.fecha_creacion).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-3" onClick={(e) => e.stopPropagation()}>
                        <button 
                          onClick={() => {
                            setSelectedGrupo(grupo);
                            setModalOpen(true);
                          }}
                          className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all"
                          title="Editar"
                        >
                          ✎
                        </button>
                        <button 
                          onClick={() => {
                            if (confirm('¿Estas seguro de eliminar este grupo?')) {
                              deleteGrupo(grupo.id_grupo);
                            }
                          }}
                          className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                          title="Eliminar"
                        >
                          🗑
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="mt-4 text-center">
        <p className="text-xs text-gray-400 font-medium uppercase tracking-widest">
          Haz clic en una fila para entrar al chat del grupo
        </p>
      </div>
    </div>
  );
};
