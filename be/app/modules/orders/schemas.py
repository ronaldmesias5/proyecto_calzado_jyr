"""
Módulo: schemas.py (Orders)
Descripción: Esquemas Pydantic para validación y serialización de órdenes.
¿Para qué? Definir estructura de datos para solicitudes/respuestas de órdenes.
¿Impacto? Valida datos de entrada y serializa respuestas API.
"""

from datetime import datetime
from uuid import UUID
from typing import List

from pydantic import BaseModel, Field

from app.models.order import OrderStatus


# ────────────────────────────────────────────────
# Esquemas para OrderItem (línea de pedido)
# ────────────────────────────────────────────────

class OrderItemResponse(BaseModel):
    """Esquema para mostrar una línea de pedido."""
    id: UUID
    style_name: str
    style_category: str | None = None
    size: str
    quantity: int

    class Config:
        from_attributes = True


class OrderItemCreateRequest(BaseModel):
    """Esquema para crear una línea de pedido."""
    style_name: str = Field(..., min_length=1, max_length=255, description="Nombre del estilo")
    style_category: str | None = Field(None, max_length=100, description="Categoría del estilo")
    size: str = Field(..., min_length=1, max_length=10, description="Talla")
    quantity: int = Field(..., gt=0, description="Cantidad de pares (mínimo 12)")

    class Config:
        from_attributes = True


# ────────────────────────────────────────────────
# Esquemas para Order
# ────────────────────────────────────────────────

class OrderResponse(BaseModel):
    """Esquema para mostrar una orden en listados."""
    id: UUID
    order_code: str
    customer_name: str
    contact_person: str
    contact_email: str | None
    contact_phone: str | None
    total_items: int
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True


class OrderDetailResponse(BaseModel):
    """Esquema detallado de una orden con todos sus items."""
    id: UUID
    order_code: str
    customer_name: str
    contact_person: str
    contact_email: str | None
    contact_phone: str | None
    contact_address: str | None
    total_items: int
    delivery_date: datetime | None
    notes: str | None
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Esquema para respuesta de listado paginado de órdenes."""
    total: int = Field(..., description="Total de órdenes en la base de datos")
    page: int = Field(..., description="Página actual (1-indexed)")
    page_size: int = Field(..., description="Cantidad de órdenes por página")
    total_pages: int = Field(..., description="Total de páginas")
    items: List[OrderResponse] = Field(..., description="Órdenes en esta página")


class OrderCreateRequest(BaseModel):
    """Esquema para crear una nueva orden."""
    order_code: str = Field(..., min_length=1, max_length=50, description="Código único de la orden")
    customer_name: str = Field(..., min_length=1, max_length=255, description="Nombre del cliente")
    contact_person: str = Field(..., min_length=1, max_length=255, description="Persona de contacto")
    contact_email: str | None = Field(None, max_length=255, description="Email de contacto")
    contact_phone: str | None = Field(None, max_length=20, description="Teléfono de contacto")
    contact_address: str | None = Field(None, max_length=500, description="Dirección de entrega")
    delivery_date: datetime | None = Field(None, description="Fecha estimada de entrega")
    notes: str | None = Field(None, description="Notas especiales del cliente")
    items: List[OrderItemCreateRequest] = Field(default_factory=list, description="Líneas del pedido")

    class Config:
        from_attributes = True


class OrderUpdateStatusRequest(BaseModel):
    """Esquema para actualizar el estado de una orden."""
    status: OrderStatus = Field(..., description="Nuevo estado de la orden")

    class Config:
        from_attributes = True
