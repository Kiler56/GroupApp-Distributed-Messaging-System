import React from 'react';
import { useGrupos, useMyGrupos, useDeleteGrupo, useJoinGrupo, useLeaveGrupo } from '../hooks/useGrupos';
import { useGrupoStore } from '../hooks/useGrupoStore';
import { useNavigate } from 'react-router-dom';

export const GrupoList: React.FC = () => {
  const navigate = useNavigate();
  const { data: todosLosGrupos, isLoading: loadingTodos } = useGrupos();
  const { data: misGrupos, isLoading: loadingMis } = useMyGrupos();
  const { mutate: deleteGrupo } = useDeleteGrupo();
  const { mutate: joinGrupo } = useJoinGrupo();
  const { mutate: leaveGrupo } = useLeaveGrupo();
  const { setSelectedGrupo, setModalOpen } = useGrupoStore();

  if (loadingTodos || loadingMis) return <div className="p-8 text-center text-gray-500 font-bold">Cargando grupos...</div>;

  const misGruposIds = new Set(misGrupos?.map(g => g.id_grupo));

  return (
    <div className="space-y-10">
      <div className="flex flex-col md:flex-row justify-between items-end md:items-center gap-6">
        <div className="space-y-1">
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Comunidades</h2>
          <p className="text-slate-500 font-medium">Gestiona tus grupos o descubre nuevas conversaciones.</p>
        </div>
        <button 
          onClick={() => {
            setSelectedGrupo(null);
            setModalOpen(true);
          }}
          className="btn-primary !px-8 !py-4 shadow-indigo-200/50"
        >
          <span className="text-2xl">+</span>
          <span>Crear nuevo grupo</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {todosLosGrupos?.length === 0 ? (
          <div className="col-span-full py-20 card-glass rounded-[2rem] flex flex-col items-center justify-center text-center space-y-4">
            <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center text-slate-300">
              <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div className="space-y-1">
              <p className="text-xl font-bold text-slate-400">No hay grupos activos</p>
              <p className="text-slate-400 text-sm">Sé el primero en crear una comunidad</p>
            </div>
          </div>
        ) : (
          todosLosGrupos?.map((grupo) => {
            const esMiembro = misGruposIds.has(grupo.id_grupo);
            
            return (
              <div 
                key={grupo.id_grupo}
                className={`group relative card-glass rounded-[2rem] p-8 flex flex-col h-[280px] hover:-translate-y-1 duration-500 ${!esMiembro && grupo.privado ? 'opacity-60 cursor-not-allowed' : ''}`}
              >
                <div className="flex justify-between items-start mb-6">
                  <div className={`px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-[0.15em] shadow-sm ${
                    grupo.privado 
                      ? 'bg-amber-50 text-amber-600 border border-amber-100' 
                      : 'bg-emerald-50 text-emerald-600 border border-emerald-100'
                  }`}>
                    {grupo.privado ? 'Privado' : 'Público'}
                  </div>
                  
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
                    <button 
                      onClick={(e) => { e.stopPropagation(); setSelectedGrupo(grupo); setModalOpen(true); }}
                      className="w-9 h-9 flex items-center justify-center bg-white text-slate-400 hover:text-indigo-600 rounded-xl shadow-sm border border-slate-100 transition-colors"
                      title="Configurar"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </button>
                    <button 
                      onClick={(e) => { e.stopPropagation(); if (confirm('¿Eliminar grupo?')) deleteGrupo(grupo.id_grupo); }}
                      className="w-9 h-9 flex items-center justify-center bg-white text-slate-400 hover:text-rose-600 rounded-xl shadow-sm border border-slate-100 transition-colors"
                      title="Eliminar"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h3 className="text-2xl font-black text-slate-800 line-clamp-1 group-hover:text-indigo-600 transition-colors">{grupo.nombre}</h3>
                  <p className="text-slate-500 font-medium text-sm line-clamp-2 h-10 leading-relaxed">
                    {grupo.descripcion || 'Esta comunidad no tiene una descripción todavía.'}
                  </p>
                </div>

                <div className="flex items-center justify-between mt-auto pt-6 border-t border-slate-50">
                  <div className="flex flex-col">
                    <span className="text-[10px] font-black text-slate-300 uppercase tracking-widest">Creado</span>
                    <span className="text-xs font-bold text-slate-500 italic">
                      {new Date(grupo.fecha_creacion).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                  </div>
                  
                  {esMiembro ? (
                    <div className="flex gap-2">
                      <button 
                        onClick={() => navigate(`/chat/${grupo.id_grupo}`)}
                        className="bg-indigo-600 text-white hover:bg-indigo-700 px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-wider shadow-lg shadow-indigo-100 transition-all transform active:scale-95"
                      >
                        Mensajes
                      </button>
                      <button 
                        onClick={() => { if (confirm('¿Abandonar grupo?')) leaveGrupo(grupo.id_grupo); }}
                        className="w-10 h-10 flex items-center justify-center text-slate-300 hover:text-rose-500 hover:bg-rose-50 rounded-xl transition-all"
                        title="Abandonar grupo"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                      </button>
                    </div>
                  ) : (
                    !grupo.privado && (
                      <button 
                        onClick={() => joinGrupo(grupo.id_grupo)}
                        className="bg-slate-900 text-white hover:bg-black px-8 py-2.5 rounded-xl text-xs font-black uppercase tracking-wider transition-all transform active:scale-95 shadow-lg shadow-slate-200"
                      >
                        Unirse
                      </button>
                    )
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
      
      <div className="flex justify-center pt-10">
        <div className="px-6 py-3 bg-white border border-slate-100 rounded-2xl shadow-sm">
           <p className="text-[10px] text-slate-400 font-black uppercase tracking-[0.3em]">
            {todosLosGrupos?.length || 0} Comunidades activas
          </p>
        </div>
      </div>
    </div>
  );
};
