"""
Archivo: be/app/models/order.py
Descripción: Modelo ORM SQLAlchemy para la tabla `order` y `order_item`.

¿Qué?
  Define pedidos de clientes mayoristas: código, cliente, contacto, productos, estado, fechas, notas.
  Cada pedido puede tener múltiples productos/estilos en diferentes tallas.
  
¿Para qué?
  - Almacenar pedidos mayoristas realizados por clientes
  - Trackear estado de producción por estilos/tallas
  - Vincular con inventario y tareas de producción
  - Mantener información del cliente (contacto, teléfono, dirección, notas)
  
¿Impacto?
  CRÍTICO - Base del negocio (pedidos mayoristas = ingresos principales)
  
¿Nota?
  NO maneja precios (cliente mayorista) — solo cantidades por estilo/talla
"""

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class OrderStatus(str, Enum):
    """Estados posibles de un pedido"""
    PENDING = "Pendiente"
    IN_PRODUCTION = "En Producción"
    COMPLETED = "Listo"
    DELIVERED = "Entregado"
    CANCELLED = "Cancelado"


class Order(Base):
    """Modelo ORM para la tabla `order` de pedidos mayoristas."""

    __tablename__ = "order"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Identificación del pedido
    order_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    # Información del cliente (mayorista)
    customer_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nombre de la empresa/cliente mayorista",
    )

    contact_person: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nombre de la persona de contacto",
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    contact_address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Detalles del pedido
    total_items: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Total de pares en todo el pedido",
    )

    # Fechas
    delivery_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Fecha estimada de entrega",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Notas/instrucciones especiales del cliente",
    )

    # Estado
    status: Mapped[str] = mapped_column(
        SQLEnum(OrderStatus),
        nullable=False,
        default=OrderStatus.PENDING,
    )

    # Fechas del sistema
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relación con OrderItem (líneas de pedido)
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Order(code={self.order_code}, customer={self.customer_name}, status={self.status})>"


class OrderItem(Base):
    """Modelo ORM para línea de pedido (estilo/talla/cantidad)."""

    __tablename__ = "order_item"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Relación con pedido
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("order.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Producto/Estilo
    style_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nombre del estilo (ej: For One, Super Star, Puma California)",
    )

    style_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Categoría del estilo (ej: Caballero, Dama, Niño)",
    )

    # Talla y cantidad
    size: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Talla (ej: 39, 40, 41, etc.)",
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Cantidad de pares (mínimo 12 por estilo/talla)",
    )

    # Fechas
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    # Relación inversa con Order
    order: Mapped[Order] = relationship(
        "Order",
        back_populates="items",
    )

    def __repr__(self) -> str:
        return f"<OrderItem(style={self.style_name}, size={self.size}, qty={self.quantity})>"
