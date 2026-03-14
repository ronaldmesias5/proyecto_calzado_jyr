import { Outlet } from 'react-router-dom';
import AdminSidebar from './AdminSidebar';
import AdminHeader from './AdminHeader';

export default function AdminLayout() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar sticky */}
      <AdminSidebar />
      
      {/* Contenido principal */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Header sticky */}
        <AdminHeader />
        
        {/* Contenido con scroll */}
        <main className="flex-1 p-6 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
