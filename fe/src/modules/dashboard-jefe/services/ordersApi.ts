/**
 * Módulo: ordersApi.ts
 * Descripción: Servicio para consumir API de órdenes del backend.
 * ¿Para qué? Centralizar llamadas API para operaciones CRUD de órdenes mayoristas.
 * ¿Impacto? Proporciona métodos reutilizables para componentes de órdenes.
 */

import axios from '@/api/axios';

// ────────────────────────────────────────────────
// Tipos
// ────────────────────────────────────────────────

export type OrderStatus = 'Pendiente' | 'En Producción' | 'Listo' | 'Entregado' | 'Cancelado';

export interface OrderItem {
  id: string;
  style_name: string;
  style_category: string | null;
  size: string;
  quantity: number;
}

export interface Order {
  id: string;
  order_code: string;
  customer_name: string;
  contact_person: string;
  contact_email: string | null;
  contact_phone: string | null;
  total_items: number;
  status: OrderStatus;
  created_at: string;
}

export interface OrderDetail extends Order {
  contact_address: string | null;
  delivery_date: string | null;
  notes: string | null;
  updated_at: string;
  items: OrderItem[];
}

export interface OrderListResponse {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  items: Order[];
}

export interface OrderCreateRequest {
  order_code: string;
  customer_name: string;
  contact_person: string;
  contact_email?: string | null;
  contact_phone?: string | null;
  contact_address?: string | null;
  delivery_date?: string | null;
  notes?: string | null;
  items: {
    style_name: string;
    style_category?: string | null;
    size: string;
    quantity: number;
  }[];
}

export interface OrderUpdateStatusRequest {
  status: OrderStatus;
}

// ────────────────────────────────────────────────
// Funciones API
// ────────────────────────────────────────────────

/**
 * Obtiene listado paginado de órdenes.
 * @param page - Número de página (1-indexed)
 * @param page_size - Elementos por página
 * @param status - Filtro por estado (opcional)
 * @param customer_name - Filtro por nombre de cliente (opcional)
 * @returns Promise<OrderListResponse>
 */
export async function getOrders(
  page: number = 1,
  page_size: number = 10,
  status?: OrderStatus | null,
  customer_name?: string | null,
): Promise<OrderListResponse> {
  const params: Record<string, unknown> = { page, page_size };
  if (status) params.status = status;
  if (customer_name) params.customer_name = customer_name;

  const response = await axios.get<OrderListResponse>('/api/v1/admin/orders', { params });
  return response.data;
}

/**
 * Obtiene detalle de una orden específica con todos sus items.
 * @param orderId - UUID de la orden
 * @returns Promise<OrderDetail>
 */
export async function getOrderDetail(orderId: string): Promise<OrderDetail> {
  const response = await axios.get<OrderDetail>(`/api/v1/admin/orders/${orderId}`);
  return response.data;
}

/**
 * Crea una nueva orden mayorista.
 * @param orderData - Datos de la orden a crear
 * @returns Promise<OrderDetail>
 */
export async function createOrder(orderData: OrderCreateRequest): Promise<OrderDetail> {
  const response = await axios.post<OrderDetail>('/api/v1/admin/orders', orderData);
  return response.data;
}

/**
 * Actualiza el estado de una orden.
 * @param orderId - UUID de la orden
 * @param statusUpdate - Nuevo estado
 * @returns Promise<OrderDetail>
 */
export async function updateOrderStatus(
  orderId: string,
  statusUpdate: OrderUpdateStatusRequest,
): Promise<OrderDetail> {
  const response = await axios.patch<OrderDetail>(
    `/api/v1/admin/orders/${orderId}/status`,
    statusUpdate,
  );
  return response.data;
}
