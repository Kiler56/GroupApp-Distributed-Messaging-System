import React, { useEffect } from 'react';
import './index.css';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { GrupoList } from './components/GrupoList';
import { GrupoForm } from './components/GrupoForm';

const queryClient = new QueryClient();

const GruposApp: React.FC = () => {
  useEffect(() => {
    // Capturar token de la URL
    const params = new URLSearchParams(window.location.search);
    const tokenFromUrl = params.get('token');
    
    if (tokenFromUrl) {
      console.log("Token detectado en URL, guardando...");
      localStorage.setItem('token', tokenFromUrl);
      // Limpiar URL y recargar para estabilizar
      window.history.replaceState({}, document.title, "/");
    }

    const checkAuth = () => {
      const token = localStorage.getItem('token');
      console.log("Validando token en localStorage:", token ? "Presente" : "Ausente");

      if (!token || token === 'undefined' || token === 'null') {
        console.error("Acceso denegado: No se encontro token valido.");
        const AUTH_URL = import.meta.env.VITE_AUTH_URL || 'http://localhost:5500/login.html';
        window.location.href = AUTH_URL;
      }
    };

    checkAuth();
  }, []);


  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen">
        <header className="sticky top-0 z-40 bg-white/70 backdrop-blur-lg border-b border-slate-200/60">
          <div className="container mx-auto px-6 py-4 flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="w-11 h-11 bg-gradient-to-br from-indigo-600 to-violet-700 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-200">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-black text-slate-900 tracking-tight leading-none">GroupApp</h1>
                <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-[0.2em]">Distributed Messaging</span>
              </div>
            </div>
            <button 
              onClick={() => {
                localStorage.removeItem('token');
                window.location.href = 'http://localhost:5500/login.html';
              }}
              className="group flex items-center gap-2 text-sm font-bold text-slate-500 hover:text-rose-600 transition-colors"
            >
              <span>Cerrar Sesión</span>
              <div className="w-8 h-8 rounded-full flex items-center justify-center group-hover:bg-rose-50 transition-colors">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </div>
            </button>
          </div>
        </header>

        <main className="container mx-auto px-6 py-12">
          <div className="max-w-6xl mx-auto">
            <GrupoList />
          </div>
          <GrupoForm />
        </main>
      </div>
    </QueryClientProvider>
  );
};

export default GruposApp;
