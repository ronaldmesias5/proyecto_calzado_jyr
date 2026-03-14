"""
Módulo: router.py (Orders)
Descripción: Rutas API para gestión de órdenes mayoristas en el dashboard del jefe.
¿Para qué? Endpoints GET/POST/PATCH para órdenes: listar, obtener detalle, crear, actualizar estado.
¿Impacto? Maneja toda la lógica de órdenes mayoristas. Requiere autenticación.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, desc, select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.order import Order, OrderStatus
from app.modules.orders.schemas import (
    OrderResponse,
    OrderListResponse,
    OrderDetailResponse,
    OrderCreateRequest,
    OrderUpdateStatusRequest,
)

router = APIRouter(
    prefix="/api/v1/admin/orders",
    tags=["orders"],
)


@router.get("", response_model=OrderListResponse)
def list_orders(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1, description="Página (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    status: OrderStatus | None = Query(None, description="Filtrar por estado"),
    customer_name: str | None = Query(None, description="Filtrar por nombre de cliente (parcial)"),
) -> OrderListResponse:
    """
    Obtiene listado paginado de órdenes.
    
    Parámetros:
    - page: Página actual (default: 1)
    - page_size: Elementos por página (default: 10, máximo: 100)
    - status: Filtrar por estado (ej: "Pendiente", "En Producción")
    - customer_name: Filtrar por nombre de cliente (búsqueda parcial)
    
    Retorna:
    - OrderListResponse con paginación y lista de órdenes
    """
    # Construir query
    query = select(Order)

    if status:
        query = query.where(Order.status == status)

    if customer_name:
        query = query.where(Order.customer_name.ilike(f"%{customer_name}%"))

    # Contar total
    count_query = select(func.count(Order.id)).select_from(Order)
    if status:
        count_query = count_query.where(Order.status == status)
    if customer_name:
        count_query = count_query.where(Order.customer_name.ilike(f"%{customer_name}%"))

    total = db.execute(count_query).scalar() or 0

    # Aplicar paginación
    offset = (page - 1) * page_size
    query = query.order_by(desc(Order.created_at)).offset(offset).limit(page_size)

    result = db.execute(query)
    orders = result.scalars().all()

    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return OrderListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=[OrderResponse.model_validate(order) for order in orders],
    )


@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order_detail(
    order_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> OrderDetailResponse:
    """
    Obtiene detalle completo de una orden (con líneas de pedido).
    
    Parámetros:
    - order_id: UUID de la orden
    
    Retorna:
    - OrderDetailResponse con información completa y items del pedido
    
    Lanza:
    - 404 si la orden no existe
    """
    result = db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    return OrderDetailResponse.model_validate(order)


@router.post("", response_model=OrderDetailResponse)
def create_order(
    order_data: OrderCreateRequest,
    db: Annotated[Session, Depends(get_db)],
) -> OrderDetailResponse:
    """
    Crea una nueva orden con sus líneas de pedido.
    
    Parámetros (JSON body):
    - order_code: Código único de la orden
    - customer_name: Nombre del cliente
    - contact_person: Persona de contacto
    - contact_email: Email (opcional)
    - contact_phone: Teléfono (opcional)
    - contact_address: Dirección (opcional)
    - delivery_date: Fecha estimada (opcional)
    - notes: Notas especiales (opcional)
    - items: Lista de líneas del pedido (estilo, talla, cantidad)
    
    Retorna:
    - OrderDetailResponse con datos de la nueva orden creada
    
    Lanza:
    - 400 si order_code ya existe
    """
    # Verificar que order_code sea único
    existing = db.execute(
        select(Order).where(Order.order_code == order_data.order_code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail=f"El código de orden '{order_data.order_code}' ya existe",
        )

    # Calcular total de items
    total_items = sum(item.quantity for item in order_data.items)

    # Crear la orden
    new_order = Order(
        order_code=order_data.order_code,
        customer_name=order_data.customer_name,
        contact_person=order_data.contact_person,
        contact_email=order_data.contact_email,
        contact_phone=order_data.contact_phone,
        contact_address=order_data.contact_address,
        total_items=total_items,
        delivery_date=order_data.delivery_date,
        notes=order_data.notes,
    )

    # Agregar items
    from app.models.order import OrderItem
    for item_data in order_data.items:
        item = OrderItem(
            style_name=item_data.style_name,
            style_category=item_data.style_category,
            size=item_data.size,
            quantity=item_data.quantity,
        )
        new_order.items.append(item)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return OrderDetailResponse.model_validate(new_order)


@router.patch("/{order_id}/status", response_model=OrderDetailResponse)
def update_order_status(
    order_id: UUID,
    order_update: OrderUpdateStatusRequest,
    db: Annotated[Session, Depends(get_db)],
) -> OrderDetailResponse:
    """
    Actualiza el estado de una orden.
    
    Parámetros:
    - order_id: UUID de la orden
    - status (JSON body): Nuevo estado
    
    Retorna:
    - OrderDetailResponse con datos actualizados
    
    Lanza:
    - 404 si la orden no existe
    """
    result = db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    order.status = order_update.status
    db.commit()
    db.refresh(order)

    return OrderDetailResponse.model_validate(order)
