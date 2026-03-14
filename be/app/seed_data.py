"""
Archivo: be/app/seed_data.py
Descripción: Script de seed para cargar datos iniciales (roles, tipos de documentos).

¿Qué?
  Exporta 2 funciones:
  - seed_roles(): Inserta 3 roles (admin, employee, client) con UUIDs fijos
  - seed_type_documents(): Inserta 6 tipos de documentos (CC, TI, Pasaporte, etc.)
  Usa db.merge() para evitar duplicados (INSERT ... ON CONFLICT equivalente)
  Verifica count() antes de insertar (skip si ya existen)
  
¿Para qué?
  - Garantizar datos iniciales desde código Python (no solo SQL)
  - Facilitar testing (crear BD desde cero con seed_roles())
  - Alternativa a scripts SQL (seed_data.py puede llamarse desde main.py)
  - Logs claros: ✅ OK, 🔄 Insertando, ❌ Error
  
¿Impacto?
  MEDIO — Se ejecuta en startup del backend (main.py lifespan).
  Si falla seed_roles(), usuarios no pueden crearse (FK constraint falla).
  Modificar UUIDs rompe: scripts que hardcodean UUIDs (crear_usuario_ronald.py).
  Dependencias: models/role.py, models/type_document.py, database.py (SessionLocal)
"""

import uuid
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.type_document import TypeDocument
from app.models.order import Order, OrderStatus
from app.models.user import User
from app.utils.security import hash_password

logger = logging.getLogger(__name__)


def seed_roles(db: Session) -> bool:
    """
    Inserta los 3 roles principales si no existen.
    
    Return:
        True si se insertaron o ya existían, False si hubo error.
    """
    try:
        # Verificar si ya existen los roles
        if db.query(Role).count() > 0:
            print(f"✅ Roles ya existen ({db.query(Role).count()} encontrados)")
            return True
        
        print("🔄 Insertando roles iniciales...")
        
        roles = [
            Role(
                id=uuid.UUID("10000000-0000-0000-0000-000000000001"),
                name="admin",
                description="Administrador del sistema"
            ),
            Role(
                id=uuid.UUID("20000000-0000-0000-0000-000000000001"),
                name="employee",
                description="Empleado de la fábrica"
            ),
            Role(
                id=uuid.UUID("30000000-0000-0000-0000-000000000001"),
                name="client",
                description="Cliente — gestión de pedidos"
            ),
        ]
        
        for role in roles:
            db.merge(role)  # USE MERGE para evitar duplicados
        
        db.commit()
        print("✅ Roles insertados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error insertando roles: {str(e)}")
        db.rollback()
        return False


def seed_type_documents(db: Session) -> bool:
    """
    Inserta los tipos de documentos principales si no existen.
    
    Return:
        True si se insertaron o ya existían, False si hubo error.
    """
    try:
        # Verificar si ya existen
        if db.query(TypeDocument).count() > 0:
            print(f"✅ Tipos de documentos ya existen ({db.query(TypeDocument).count()} encontrados)")
            return True
        
        print("🔄 Insertando tipos de documentos...")
        
        type_docs = [
            TypeDocument(
                id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
                name="Cédula de Ciudadanía (CC)"
            ),
            TypeDocument(
                id=uuid.UUID("00000000-0000-0000-0000-000000000002"),
                name="Tarjeta de Identidad (TI)"
            ),
            TypeDocument(
                id=uuid.UUID("00000000-0000-0000-0000-000000000003"),
                name="Pasaporte"
            ),
            TypeDocument(
                id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
                name="Cédula de Extranjería (CE)"
            ),
            TypeDocument(
                id=uuid.UUID("00000000-0000-0000-0000-000000000005"),
                name="Permiso por Protección Temporal (PPT)"
            ),
            TypeDocument(
                id=uuid.UUID("00000000-0000-0000-0000-000000000006"),
                name="Documento de Identificación Personal (DIPS)"
            ),
        ]
        
        for doc_type in type_docs:
            db.merge(doc_type)  # USE MERGE para evitar duplicados
        
        db.commit()
        print("✅ Tipos de documentos insertados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error insertando tipos de documentos: {str(e)}")
        db.rollback()
        return False


def seed_orders(db: Session) -> bool:
    """
    Inserta órdenes mayoristas de prueba si no existen.
    
    Cada orden puede tener múltiples estilos (items) con tallas y cantidades.
    Mínimo 12 pares por estilo/talla.
    
    Return:
        True si se insertaron o ya existían, False si hubo error.
    """
    try:
        # Verificar si ya existen
        if db.query(Order).count() > 0:
            print(f"✅ Órdenes ya existen ({db.query(Order).count()} encontradas)")
            return True
        
        print("🔄 Insertando órdenes mayoristas de prueba...")
        
        from app.models.order import OrderItem
        
        now = datetime.now(timezone.utc)
        
        orders = [
            # Orden 1: Pendiente con 2 estilos
            Order(
                id=uuid.uuid4(),
                order_code="ORD-001",
                customer_name="Calzado Pérez",
                contact_person="Juan Pérez",
                contact_email="juan.perez@calzadoperez.com",
                contact_phone="+57 310 234 5678",
                contact_address="Cra 15 #45-23, Bogotá",
                total_items=150,
                delivery_date=now + timedelta(days=15),
                notes="Cliente mayorista preferencial. Requiere empaque especial.",
                status=OrderStatus.PENDING,
                created_at=now - timedelta(days=5),
            ),
            # Orden 2: En Producción con 1 estilo
            Order(
                id=uuid.uuid4(),
                order_code="ORD-002",
                customer_name="Distribuidora Bogotá",
                contact_person="María Rodríguez",
                contact_email="maria@distribuidorabog.com",
                contact_phone="+57 320 555 1234",
                contact_address="Av. 68 #50-40, Bogotá",
                total_items=200,
                delivery_date=now + timedelta(days=20),
                notes="Pedido urgente. Prioridad alta.",
                status=OrderStatus.IN_PRODUCTION,
                created_at=now - timedelta(days=2),
            ),
            # Orden 3: Listo con múltiples estilos
            Order(
                id=uuid.uuid4(),
                order_code="ORD-003",
                customer_name="Zapatos al Mayor",
                contact_person="Carlos López",
                contact_email="carlos@zapatosalmayor.com",
                contact_phone="+57 315 777 3333",
                contact_address="Calle 10 #25-60, Medellín",
                total_items=96,
                delivery_date=now + timedelta(days=8),
                notes="Revisar calidad especialmente en puntadas.",
                status=OrderStatus.COMPLETED,
                created_at=now - timedelta(days=4),
            ),
            # Orden 4: Entregada
            Order(
                id=uuid.uuid4(),
                order_code="ORD-004",
                customer_name="Tiendas Elite",
                contact_person="Patricia Moreno",
                contact_email="patricia@tiendas-elite.com",
                contact_phone="+57 300 444 2222",
                contact_address="Cra 7 #12-80, Cali",
                total_items=120,
                delivery_date=now - timedelta(days=2),
                notes="Entrega confirmada.",
                status=OrderStatus.DELIVERED,
                created_at=now - timedelta(days=10),
            ),
            # Orden 5: Cancelada
            Order(
                id=uuid.uuid4(),
                order_code="ORD-005",
                customer_name="Calzados Centrales",
                contact_person="Roberto Gómez",
                contact_email="roberto@calzadoscentrales.com",
                contact_phone="+57 312 666 7777",
                contact_address="Cra 50 #30-15, Barranquilla",
                total_items=60,
                delivery_date=None,
                notes="Cancelado por cambio de especificaciones.",
                status=OrderStatus.CANCELLED,
                created_at=now - timedelta(days=7),
            ),
        ]
        
        # Agregar items (líneas de pedido) a cada orden
        items_map = {
            0: [  # Orden 1: For One y Super Star
                OrderItem(id=uuid.uuid4(), style_name="For One", style_category="Caballero", size="39", quantity=50),
                OrderItem(id=uuid.uuid4(), style_name="For One", style_category="Caballero", size="40", quantity=50),
                OrderItem(id=uuid.uuid4(), style_name="Super Star", style_category="Caballero", size="41", quantity=50),
            ],
            1: [  # Orden 2: Puma California
                OrderItem(id=uuid.uuid4(), style_name="Puma California", style_category="Caballero", size="38", quantity=100),
                OrderItem(id=uuid.uuid4(), style_name="Puma California", style_category="Caballero", size="39", quantity=100),
            ],
            2: [  # Orden 3: Nike Runner
                OrderItem(id=uuid.uuid4(), style_name="Nike Runner", style_category="Caballero", size="40", quantity=48),
                OrderItem(id=uuid.uuid4(), style_name="Nike Runner", style_category="Caballero", size="41", quantity=48),
            ],
            3: [  # Orden 4: Adidas Classic
                OrderItem(id=uuid.uuid4(), style_name="Adidas Classic", style_category="Dama", size="35", quantity=60),
                OrderItem(id=uuid.uuid4(), style_name="Adidas Classic", style_category="Dama", size="36", quantity=60),
            ],
            4: [  # Orden 5: Elegance Pro
                OrderItem(id=uuid.uuid4(), style_name="Elegance Pro", style_category="Caballero", size="42", quantity=60),
            ],
        }
        
        for idx, order in enumerate(orders):
            if idx in items_map:
                order.items = items_map[idx]
            db.merge(order)
        
        db.commit()
        print("✅ Órdenes mayoristas insertadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error insertando órdenes: {str(e)}")
        db.rollback()
        return False


def seed_admin(db: Session) -> bool:
    """
    Inserta un usuario jefe (empleado con cargo de jefe) si no existe.
    
    Return:
        True si se insertó o ya existía, False si hubo error.
    """
    try:
        # Verificar si ya existe el usuario jefe
        existing_jefe = db.query(User).filter(User.email == "ronald.jefe@gmail.com").first()
        if existing_jefe:
            print(f"✅ Jefe ya existe ({existing_jefe.email})")
            return True
        
        # Obtener rol employee
        employee_role = db.query(Role).filter(Role.name == "employee").first()
        if not employee_role:
            print("❌ Rol employee no existe")
            return False
        
        print("🔄 Insertando usuario jefe...")
        
        jefe_user = User(
            id=uuid.uuid4(),
            email="ronald.jefe@gmail.com",
            name="Ronald",
            last_name="Jefe",
            phone="+57 312 345 6789",
            hashed_password=hash_password("Test123456!"),
            role_id=employee_role.id,
            occupation="jefe",
            is_active=True,
            is_validated=True,
            validated_at=datetime.now(timezone.utc),
        )
        
        db.add(jefe_user)
        db.commit()
        print("✅ Usuario jefe insertado exitosamente")
        print("   Email: ronald.jefe@gmail.com")
        print("   Contraseña: Test123456!")
        return True
        
    except Exception as e:
        print(f"❌ Error insertando jefe: {str(e)}")
        db.rollback()
        return False


def seed_all(db: Session) -> None:
    """
    Ejecuta todos los seeds de forma idempotente.
    Se ejecuta automáticamente en el startup del backend.
    """
    try:
        print("📦 Iniciando proceso de seed de datos...")
        
        success = True
        success = seed_roles(db) and success
        success = seed_type_documents(db) and success
        success = seed_admin(db) and success
        success = seed_orders(db) and success
        
        if success:
            print("🎉 Todos los seeds completados exitosamente")
        else:
            print("⚠️  Algunos seeds no se completaron correctamente")
    
    except Exception as e:
        print(f"💥 Error fatal en seed: {str(e)}")
