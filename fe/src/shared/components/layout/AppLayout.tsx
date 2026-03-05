/**
 * Archivo: components/layout/AppLayout.tsx
 * Descripción: Layout para las páginas protegidas (dashboard, perfil, etc.).
 * ¿Para qué? Proveer la estructura común para las páginas internas del sistema.
 */

import { Link, Outlet } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { LogOut, User } from "lucide-react";

export function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="flex min-h-screen flex-col bg-[#f9fafb]">
      {/* Header del dashboard */}
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
          <Link to="/dashboard" className="flex items-center gap-2">
            <span className="font-bold" style={{ color: '#000', fontFamily: 'Montserrat, sans-serif', letterSpacing: 1, fontSize: '1.1rem' }}>CALZADO J&R</span>
          </Link>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <User className="h-4 w-4" />
              <span>{user?.full_name}</span>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-1 rounded-lg px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 hover:text-red-600"
            >
              <LogOut className="h-4 w-4" />
              Salir
            </button>
          </div>
        </div>
      </header>

      {/* Línea decorativa azul */}
      <div className="h-1 bg-[#1e40af]" />

      {/* Contenido de la página */}
      <main className="mx-auto w-full max-w-7xl flex-1 px-6 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white py-4 text-center">
        <p className="text-sm text-gray-500">
          CALZADO J&R - Calidad y Estilo a tu Alcance
        </p>
        <p className="text-xs text-gray-400">
          Bogotá, Colombia | Tel: +57 601 234 5678
        </p>
      </footer>
    </div>
  );
}
