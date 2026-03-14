"""
Módulo: main.py
Descripción: Punto de entrada de la aplicación FastAPI — configura y arranca el servidor.
¿Para qué? Crear la instancia principal de FastAPI, configurar CORS, incluir routers.
¿Impacto? Este es el archivo que Uvicorn ejecuta. Sin él, no hay servidor.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.admin.router import router as admin_router
from app.modules.type_document.router import router as type_document_router
from app.modules.dashboard_jefe.router import router as dashboard_jefe_router
from app.modules.orders.router import router as orders_router

# Importar modelos para que SQLAlchemy los registre en Base.metadata
from app.models import role, user, password_reset_token, type_document, order  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Gestiona el ciclo de vida de la aplicación FastAPI."""
    print("🚀 CALZADO J&R — Backend iniciando...")
    
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas verificadas / creadas correctamente.")
    
    # Cargar datos iniciales
    db = SessionLocal()
    try:
        from app.seed_data import seed_all
        seed_all(db)
    except Exception as e:
        print(f"⚠️  Error: {str(e)}")
    finally:
        db.close()
    
    print(f"📡 CORS habilitado para: {settings.FRONTEND_URL}")
    print("✨ Sistema listo.")
    
    yield
    
    print("🛑 CALZADO J&R — Backend cerrando...")


app = FastAPI(
    title="CALZADO J&R API",
    description=(
        "👟 Sistema de gestión y producción de calzado. "
        "Incluye registro, login, cambio y recuperación de contraseña. "
        "Proyecto educativo — SENA."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────────
# 📍 Incluir routers
# ────────────────────────────

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(type_document_router)
app.include_router(dashboard_jefe_router)
app.include_router(orders_router)

# ────────────────────────────
# 📍 Endpoint raíz de bienvenida
# ────────────────────────────
@app.get("/", tags=["root"], summary="Bienvenida API")
async def root():
    """Mensaje de bienvenida en la raíz de la API."""
    return {"message": "API de Calzado J&R funcionando. Visita /docs para la documentación."}


# ────────────────────────────
# 📍 Endpoint de salud (health check)
# ────────────────────────────
@app.get(
    "/api/v1/health",
    tags=["health"],
    summary="Verificar estado del servidor",
)
async def health_check() -> dict[str, str]:
    """Endpoint de verificación de salud del servidor."""
    return {
        "status": "healthy",
        "project": "CALZADO J&R",
        "version": "0.1.0",
    }
