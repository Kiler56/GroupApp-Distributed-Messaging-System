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
      <div className="container mx-auto">
        <header className="bg-gray-800 text-white p-4 mb-6 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Panel de Grupos</h1>
          <button 
            onClick={() => {
              localStorage.removeItem('token');
              window.location.href = 'http://localhost:5500/login.html';
            }}
            className="text-sm bg-red-600 px-3 py-1 rounded"
          >
            Cerrar Sesion
          </button>
        </header>
        <main>
          <GrupoList />
          <GrupoForm />
        </main>
      </div>
    </QueryClientProvider>
  );
};

export default GruposApp;
