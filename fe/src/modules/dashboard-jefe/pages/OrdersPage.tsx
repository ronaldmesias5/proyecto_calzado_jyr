/**
 * Módulo: OrdersPage.tsx (Rediseñada)
 * Descripción: Página de gestión de pedidos mayoristas del dashboard.
 * ¿Para qué? Mostrar listado de pedidos + vista detallada + info del cliente.
 * ¿Impacto? Interfaz principal para gestión de pedidos mayoristas.
 */

import { useState, useEffect, useCallback } from 'react';
import {
  Package, Filter, Search, Loader2, AlertCircle, Clock, 
  Zap, CheckCircle, Truck, XCircle, ChevronLeft, ChevronRight,
  ArrowRight, Mail, Phone, MapPin, FileText, Plus,
} from 'lucide-react';
import {
  getOrders,
  getOrderDetail,
  updateOrderStatus,
  type Order,
  type OrderDetail,
  type OrderStatus,
  type OrderListResponse,
} from '../services/ordersApi';
import Button from '@/components/ui/Button';

// ────────────────────────────────────────────────
// Tipos locales
// ────────────────────────────────────────────────

interface OrdersPageState {
  orders: Order[];
  selectedOrder: OrderDetail | null;
  loading: boolean;
  detailLoading: boolean;
  error: string | null;
  page: number;
  page_size: number;
  total_pages: number;
  total: number;
  statusFilter: OrderStatus | null;
  clientFilter: string;
  isUpdatingId: string | null;
  totalByStatus: Record<OrderStatus, number>;
}

type View = 'list' | 'detail';

// ────────────────────────────────────────────────
// Componente: Ícono de estado
// ────────────────────────────────────────────────

function StatusIcon({ status }: { status: OrderStatus }) {
  switch (status) {
    case 'Pendiente':
      return <Clock className="w-4 h-4" />;
    case 'En Producción':
      return <Zap className="w-4 h-4" />;
    case 'Listo':
      return <CheckCircle className="w-4 h-4" />;
    case 'Entregado':
      return <Truck className="w-4 h-4" />;
    case 'Cancelado':
      return <XCircle className="w-4 h-4" />;
    default:
      return null;
  }
}

// ────────────────────────────────────────────────
// Componente: Badge de estado
// ────────────────────────────────────────────────

function StatusBadge({ status }: { status: OrderStatus }) {
  const statusStyles: Record<OrderStatus, { bg: string; text: string }> = {
    Pendiente: { bg: 'bg-yellow-100', text: 'text-yellow-800' },
    'En Producción': { bg: 'bg-blue-100', text: 'text-blue-800' },
    Listo: { bg: 'bg-green-100', text: 'text-green-800' },
    Entregado: { bg: 'bg-purple-100', text: 'text-purple-800' },
    Cancelado: { bg: 'bg-red-100', text: 'text-red-800' },
  };

  const styles = statusStyles[status];
  return (
    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${styles.bg} ${styles.text}`}>
      <StatusIcon status={status} />
      {status}
    </span>
  );
}

// ────────────────────────────────────────────────
// Componente: Cards de Resumen
// ────────────────────────────────────────────────

function SummaryCards({ totals }: { totals: Record<OrderStatus, number> }) {
  const statuses: OrderStatus[] = ['Pendiente', 'En Producción', 'Listo', 'Entregado', 'Cancelado'];
  const colors: Record<OrderStatus, string> = {
    'Pendiente': 'text-yellow-600',
    'En Producción': 'text-blue-600',
    'Listo': 'text-green-600',
    'Entregado': 'text-purple-600',
    'Cancelado': 'text-red-600',
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      {statuses.map((status) => (
        <div key={status} className="bg-white border border-gray-200 rounded-lg p-4">
          <div className={`flex items-center justify-between mb-2`}>
            <StatusIcon status={status} />
            <span className={`text-sm font-semibold ${colors[status]}`}>{status}</span>
          </div>
          <div className={`text-3xl font-bold ${colors[status]}`}>
            {totals[status]}
          </div>
        </div>
      ))}
    </div>
  );
}

// ────────────────────────────────────────────────
// Componente: Tabla de Órdenes
// ────────────────────────────────────────────────

function OrdersTable({
  orders,
  onSelect,
}: {
  orders: Order[];
  onSelect: (order: Order) => void;
}) {
  if (orders.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
        <Package className="w-12 h-12 mx-auto text-gray-300 mb-3" />
        <p className="text-gray-500 font-medium">No hay pedidos que mostrar</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
      <table className="w-full text-sm">
        <thead className="border-b border-gray-200 bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left font-semibold text-gray-700">ID Pedido</th>
            <th className="px-6 py-3 text-left font-semibold text-gray-700">Cliente</th>
            <th className="px-6 py-3 text-left font-semibold text-gray-700">Contacto</th>
            <th className="px-6 py-3 text-center font-semibold text-gray-700">Productos</th>
            <th className="px-6 py-3 text-left font-semibold text-gray-700">Estado</th>
            <th className="px-6 py-3 text-left font-semibold text-gray-700">Fecha</th>
            <th className="px-6 py-3 text-center font-semibold text-gray-700">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.id} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4 font-mono font-semibold text-gray-900">
                #{order.order_code}
              </td>
              <td className="px-6 py-4 text-gray-900">{order.customer_name}</td>
              <td className="px-6 py-4 text-gray-600">{order.contact_person}</td>
              <td className="px-6 py-4 text-center text-gray-900">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">
                  {order.total_items} pares
                </span>
              </td>
              <td className="px-6 py-4">
                <StatusBadge status={order.status} />
              </td>
              <td className="px-6 py-4 text-gray-600 text-xs">
                {new Date(order.created_at).toLocaleDateString('es-CO')}
              </td>
              <td className="px-6 py-4 text-center">
                <button
                  onClick={() => onSelect(order)}
                  className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 font-medium transition-colors"
                >
                  <ArrowRight className="w-4 h-4" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ────────────────────────────────────────────────
// Componente: Vista de Detalle del Pedido
// ────────────────────────────────────────────────

function OrderDetailView({
  order,
  isUpdating,
  onBack,
  onStatusChange,
}: {
  order: OrderDetail;
  isUpdating: boolean;
  onBack: () => void;
  onStatusChange: (orderId: string, newStatus: OrderStatus) => void;
}) {
  const statuses: OrderStatus[] = ['Pendiente', 'En Producción', 'Listo', 'Entregado', 'Cancelado'];
  const nextStatusMap: Record<OrderStatus, OrderStatus | null> = {
    Pendiente: 'En Producción',
    'En Producción': 'Listo',
    Listo: 'Entregado',
    Entregado: null,
    Cancelado: null,
  };

  const nextStatus = nextStatusMap[order.status];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start gap-4">
        <button
          onClick={onBack}
          className="mt-1 p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ChevronLeft className="w-6 h-6 text-gray-600" />
        </button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold text-gray-900">
            Detalle del Pedido {order.order_code}
          </h1>
          <p className="text-gray-600 text-sm mt-1">Información completa del pedido</p>
        </div>
        <div className="flex gap-2">
          <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium">
            📄 Imprimir
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium flex items-center gap-2">
            <Mail className="w-4 h-4" />
            Email
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Información del Pedido */}
        <div className="lg:col-span-2 space-y-6">
          {/* Datos del Pedido */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Información del Pedido</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-gray-600">ID Pedido</div>
                <div className="text-lg font-mono font-bold text-gray-900">#{order.order_code}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Fecha de Creación</div>
                <div className="text-lg font-bold text-gray-900">
                  {new Date(order.created_at).toLocaleDateString('es-CO')}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Entrega Estimada</div>
                <div className="text-lg font-bold text-gray-900">
                  {order.delivery_date
                    ? new Date(order.delivery_date).toLocaleDateString('es-CO')
                    : 'No definida'}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Total de Productos</div>
                <div className="text-lg font-bold text-gray-900">{order.total_items} pares</div>
              </div>
            </div>

            {order.notes && (
              <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="text-sm font-semibold text-gray-700 mb-1">Notas</div>
                <div className="text-sm text-gray-700">{order.notes}</div>
              </div>
            )}
          </div>

          {/* Tabla de Productos */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Productos</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b border-gray-200 bg-gray-50">
                  <tr>
                    <th className="text-left px-4 py-2 font-semibold">Producto</th>
                    <th className="text-left px-4 py-2 font-semibold">Categoría</th>
                    <th className="text-left px-4 py-2 font-semibold">Talla</th>
                    <th className="text-center px-4 py-2 font-semibold">Cantidad</th>
                  </tr>
                </thead>
                <tbody>
                  {order.items.map((item) => (
                    <tr key={item.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="px-4 py-2 text-gray-900 font-medium">{item.style_name}</td>
                      <td className="px-4 py-2 text-gray-600">
                        <span className="bg-gray-100 px-2 py-1 rounded text-xs">
                          {item.style_category || '—'}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-gray-900">{item.size}</td>
                      <td className="px-4 py-2 text-center font-semibold text-gray-900">{item.quantity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Información del Cliente + Acciones */}
        <div className="space-y-6">
          {/* Info del Cliente */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Información del Cliente</h2>
            <div className="space-y-3 text-sm">
              <div>
                <div className="text-xs font-semibold text-gray-600 uppercase">Cliente</div>
                <div className="text-gray-900 font-medium">{order.customer_name}</div>
              </div>
              <div>
                <div className="text-xs font-semibold text-gray-600 uppercase">Contacto</div>
                <div className="text-gray-900 font-medium">{order.contact_person}</div>
              </div>
              {order.contact_phone && (
                <div>
                  <div className="flex items-center gap-2 text-gray-700 mt-3">
                    <Phone className="w-4 h-4" />
                    {order.contact_phone}
                  </div>
                </div>
              )}
              {order.contact_email && (
                <div>
                  <div className="flex items-center gap-2 text-gray-700">
                    <Mail className="w-4 h-4" />
                    {order.contact_email}
                  </div>
                </div>
              )}
              {order.contact_address && (
                <div>
                  <div className="flex items-start gap-2 text-gray-700">
                    <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    {order.contact_address}
                  </div>
                </div>
              )}
            </div>
            <button className="mt-4 w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium">
              👤 Ver Perfil del Cliente
            </button>
          </div>

          {/* Acciones */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Acciones</h2>
            <div className="space-y-3">
              {nextStatus && (
                <button
                  onClick={() => onStatusChange(order.id, nextStatus)}
                  disabled={isUpdating}
                  className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium flex items-center justify-center gap-2"
                >
                  {isUpdating ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Actualizando...
                    </>
                  ) : (
                    <>
                      <Zap className="w-4 h-4" />
                      Cambiar a: {nextStatus}
                    </>
                  )}
                </button>
              )}
              <button className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium text-sm">
                ✏️ Editar Pedido
              </button>
              <button className="w-full px-4 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition-colors font-medium text-sm">
                ❌ Cancelar Pedido
              </button>
              <button className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium text-sm">
                📞 Contactar Cliente
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ────────────────────────────────────────────────
// Componente principal: OrdersPage
// ────────────────────────────────────────────────

export default function OrdersPage() {
  const [view, setView] = useState<View>('list');
  const [state, setState] = useState<OrdersPageState>({
    orders: [],
    selectedOrder: null,
    loading: true,
    detailLoading: false,
    error: null,
    page: 1,
    page_size: 10,
    total_pages: 1,
    total: 0,
    statusFilter: null,
    clientFilter: '',
    isUpdatingId: null,
    totalByStatus: {
      Pendiente: 0,
      'En Producción': 0,
      Listo: 0,
      Entregado: 0,
      Cancelado: 0,
    },
  });

  //  Calcular totales por estado
  const calculateTotals = useCallback(async () => {
    try {
      const statuses: OrderStatus[] = ['Pendiente', 'En Producción', 'Listo', 'Entregado', 'Cancelado'];
      const totals: Record<OrderStatus, number> = {
        Pendiente: 0,
        'En Producción': 0,
        Listo: 0,
        Entregado: 0,
        Cancelado: 0,
      };

      for (const status of statuses) {
        const response = await getOrders(1, 1, status);
        totals[status] = response.total;
      }

      setState((prev) => ({ ...prev, totalByStatus: totals }));
    } catch (err) {
      console.error('Error calculando totales:', err);
    }
  }, []);

  // Cargar órdenes
  const loadOrders = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));
    try {
      const data = await getOrders(
        state.page,
        state.page_size,
        state.statusFilter,
        state.clientFilter || undefined,
      );
      setState((prev) => ({
        ...prev,
        orders: data.items,
        total: data.total,
        total_pages: data.total_pages,
        loading: false,
      }));
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: 'No se pudieron cargar los pedidos. Inténtalo más tarde.',
        loading: false,
      }));
    }
  }, [state.page, state.page_size, state.statusFilter, state.clientFilter]);

  useEffect(() => {
    loadOrders();
    calculateTotals();
  }, [loadOrders, calculateTotals]);

  // Cargar detalle del pedido
  const handleSelectOrder = async (order: Order) => {
    setState((prev) => ({ ...prev, detailLoading: true }));
    try {
      const detail = await getOrderDetail(order.id);
      setState((prev) => ({ ...prev, selectedOrder: detail, detailLoading: false }));
      setView('detail');
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: 'No se pudo cargar el detalle del pedido.',
        detailLoading: false,
      }));
    }
  };

  // Cambiar estado
  const handleStatusChange = async (orderId: string, newStatus: OrderStatus) => {
    setState((prev) => ({ ...prev, isUpdatingId: orderId }));
    try {
      const updated = await updateOrderStatus(orderId, { status: newStatus });
      setState((prev) => ({
        ...prev,
        selectedOrder: updated,
        orders: prev.orders.map((o) => (o.id === orderId ? { ...o, status: newStatus } : o)),
      }));
      await calculateTotals();
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: 'Error al actualizar el estado del pedido.',
      }));
    } finally {
      setState((prev) => ({ ...prev, isUpdatingId: null }));
    }
  };

  // Volver a listado
  const handleBackToList = () => {
    setView('list');
    setState((prev) => ({ ...prev, selectedOrder: null }));
  };

  if (state.detailLoading) {
    return (
      <div className="flex items-center justify-center py-20 gap-3">
        <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
        <p className="text-gray-600 font-medium">Cargando detalle del pedido...</p>
      </div>
    );
  }

  if (view === 'detail' && state.selectedOrder) {
    return (
      <OrderDetailView
        order={state.selectedOrder}
        isUpdating={state.isUpdatingId === state.selectedOrder.id}
        onBack={handleBackToList}
        onStatusChange={handleStatusChange}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
            <Package className="w-8 h-8 text-blue-600" />
            Gestión de Pedidos
          </h1>
          <p className="text-gray-600 text-sm mt-1">
            Administra todos los pedidos mayoristas
          </p>
        </div>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Nuevo Pedido
        </button>
      </div>

      {/* Error Alert */}
      {state.error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600" />
          <p className="text-sm text-red-800">{state.error}</p>
        </div>
      )}

      {/* Summary Cards */}
      <SummaryCards totals={state.totalByStatus} />

      {/* Filtros */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 flex gap-4 flex-wrap items-end">
        <div className="flex-1 min-w-48">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            <Search className="w-4 h-4 inline mr-1" />
            Buscar cliente
          </label>
          <input
            type="text"
            placeholder="Nombre del cliente..."
            value={state.clientFilter}
            onChange={(e) =>
              setState((prev) => ({ ...prev, clientFilter: e.target.value, page: 1 }))
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            <Filter className="w-4 h-4 inline mr-1" />
            Estado
          </label>
          <select
            value={state.statusFilter || ''}
            onChange={(e) =>
              setState((prev) => ({
                ...prev,
                statusFilter: (e.target.value as OrderStatus) || null,
                page: 1,
              }))
            }
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todos</option>
            <option value="Pendiente">Pendiente</option>
            <option value="En Producción">En Producción</option>
            <option value="Listo">Listo</option>
            <option value="Entregado">Entregado</option>
            <option value="Cancelado">Cancelado</option>
          </select>
        </div>
      </div>

      {/* Loading */}
      {state.loading ? (
        <div className="bg-white rounded-lg border border-gray-200 p-12 flex items-center justify-center gap-3">
          <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
          <p className="text-gray-600 font-medium">Cargando pedidos...</p>
        </div>
      ) : (
        <>
          {/* Tabla */}
          <OrdersTable orders={state.orders} onSelect={handleSelectOrder} />

          {/* Paginación */}
          {state.total_pages > 1 && (
            <div className="flex items-center justify-between mt-6">
              <div className="text-sm text-gray-600">
                Página <strong>{state.page}</strong> de <strong>{state.total_pages}</strong>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setState((prev) => ({ ...prev, page: prev.page - 1 }))}
                  disabled={state.page === 1}
                  className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setState((prev) => ({ ...prev, page: prev.page + 1 }))}
                  disabled={state.page === state.total_pages}
                  className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
