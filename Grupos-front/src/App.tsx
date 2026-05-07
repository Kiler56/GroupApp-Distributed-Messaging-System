import React, { useEffect, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { GrupoList } from './components/GrupoList';
import { GrupoForm } from './components/GrupoForm';
import { AuthPage } from './components/AuthPage';
import { ChatPage } from './components/ChatPage';
import { authService, User } from './services/authService';
import './index.css';

const queryClient = new QueryClient();

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) return <Navigate to="/login" />;
  return <>{children}</>;
};

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authService.getProfile(token).then(setUser).catch(() => {
        localStorage.removeItem('token');
        window.location.href = '/login';
      });
    }
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
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
          
          <div className="flex items-center gap-6">
            {user && (
              <div className="text-right hidden sm:block">
                <p className="text-sm font-bold text-slate-900">{user.username}</p>
                <p className="text-[10px] text-slate-500 font-medium">{user.email}</p>
              </div>
            )}
            <button 
              onClick={() => {
                localStorage.removeItem('token');
                window.location.href = '/login';
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
        </div>
      </header>

      <main className="container mx-auto px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <GrupoList />
        </div>
        <GrupoForm />
      </main>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<AuthPage />} />
          <Route path="/" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          <Route path="/chat/:groupId" element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          } />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
