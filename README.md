# Sistema de Gestión y Producción de Calzado - CALZADO J&R

**Proyecto Scrum Modular - Entregable Final Revisado**

---

## 📋 Descripción General

Sistema integral para la gestión y producción de calzado, diseñado con una arquitectura modular para escalar eficientemente. El sistema ofrece tres dashboards especializados:
- **Dashboard Jefe**: Supervisión total, validación de clientes, gestión de empleados, catálogo y pedidos.
- **Dashboard Empleados**: Control de tareas asignadas (cortado, guarnecido, solado, emplantillado) y seguimiento de producción.
- **Dashboard Clientes**: Acceso al catálogo dinámico, realización de pedidos y seguimiento en tiempo real.

---

## 🏗️ Estructura del Proyecto

```
scrum/
├── be/                          # 🐍 Backend - FastAPI + Python (uv)
│   ├── app/
│   │   ├── core/                # Configuración, BD, dependencias y seguridad
│   │   ├── models/              # Modelos SQLAlchemy (entidades)
│   │   ├── modules/             # 📦 Módulos de lógica de negocio (feature-based)
│   │   │   ├── auth/            # Registro, login, logout global, consentimientos
│   │   │   ├── admin/           # Gestión de usuarios y validaciones
│   │   │   └── ...              # Catálogo, Pedidos, Producción
│   │   ├── utils/               # Sanitizado, emails, seguridad
│   │   └── main.py              # Punto de entrada
│   ├── pyproject.toml           # Gestión de dependencias (uv)
│   └── .env.example             # Plantilla de variables de entorno
│
├── fe/                          # ⚛️ Frontend - React + TypeScript (Vite + pnpm)
│   ├── src/
│   │   ├── modules/             # 📦 Módulos funcionales
│   │   │   ├── auth/            # Login, Registro (con términos), Password
│   │   │   ├── dashboard-jefe/  # Gestión total (incluye borrar usuarios)
│   │   │   └── ...              # Landing, Clientes, Empleados
│   │   ├── shared/              # Componentes UI, hooks, servicios API
│   │   ├── context/             # AuthContext (estado Global)
│   │   └── types/               # Tipado estricto (espejo del backend)
│   └── package.json             # Dependencias Node.js
│
├── db/                          # 🗄️ Base de Datos
│   └── init/                    # Scripts DDL y Semillas (SQL)
│
├── docs/                        # 📚 Documentación Scrum
│   ├── project-documentation/   # Historias, MER, Arquitectura
│   └── sprints/                 # Backlogs y Estados
│
├── docker-compose.yml           # Orquestación de contenedores
└── .env.example                 # Variables globales de ejemplo
```

---

## 🛠️ Stack Tecnológico

### 🐍 Backend
- **FastAPI**: Alto rendimiento y validación automática con Pydantic.
- **Python 3.12+ (uv)**: Gestión de paquetes moderna y veloz.
- **SQLAlchemy 2.0**: ORM robusto con tipado estático.
- **JWT (python-jose)**: Autenticación segura con versionado de sesiones (Logout Global).

### ⚛️ Frontend
- **React 18+ (Vite)**: Interfaz reactiva y rápida.
- **TypeScript**: Seguridad en tiempo de desarrollo.
- **TailwindCSS 4**: Diseño premium, moderno y responsive.
- **Lucide Icons**: Iconografía profesional.

### 🗄️ Infraestructura y Base de Datos
- **PostgreSQL 17+**: Base de datos relacional robusta.
- **Docker / Docker Compose**: Despliegue consistente en cualquier entorno.

---

## 🚀 Inicio Rápido (Local)

### 1. Variables de Entorno
```bash
cp .env.example .env
```

### 2. Infraestructura (Docker)
Levante la base de datos y/o todo el entorno:
```bash
docker-compose up -d
```

### 3. Backend (Vía uv)
```bash
cd be
uv sync
uv run uvicorn app.main:app --reload
```
*API Docs:* http://localhost:8000/docs

### 4. Frontend (Vía pnpm)
```bash
cd fe
pnpm install
pnpm run dev
```
*App URL:* http://localhost:5173

---

## 🔐 Credenciales de Prueba (Default)

Al iniciar por primera vez, el sistema autosemilla un usuario administrador:
- **Email**: `admin@calzadojyr.com`
- **Contraseña**: `AdminSegura123!`

---

## ✨ Características Destacadas (Resumen Final)

- **Cierre de Sesión Global**: Permite al usuario invalidar todos sus tokens activos desde cualquier dispositivo (seguridad RT-004).
- **Cumplimiento Ético y Legal**: Seguimiento estricto del consentimiento de términos y condiciones durante el registro.
- **Gestión Rigurosa de Usuarios**: El "Jefe" puede borrar permanentemente cuentas de empleados o clientes, con protección contra auto-eliminación.
- **Validación de Cuentas**: Los nuevos clientes son bloqueados hasta que el Jefe valida manualmente su identidad y datos comerciales.
- **Diseño Premium**: Interfaz moderna con breadcrumbs dinámicas, modales de confirmación y micro-animaciones.

---

## 👥 Equipo y Autores
- **Ronald Mesias** - Líder de Proyecto / Arquitecto FullStack
- **Andrés** - Scrum Master
- **Santiago** - DB / Infra

---

© 2026 CALZADO J&R - Calidad y Estilo en cada paso.

```

---

## 🎯 Plan de Sprints (10 Sprints = 150 días)

| Sprint | Duración | Historias | Módulo Principal |
|--------|----------|-----------|-----------------|
| **1** | Días 1-15 | HU-001, HU-003 | auth (Registro, Login) |
| **2** | Días 16-30 | HU-002, HU-004 | auth (Validación, Recuperación) |
| **3** | Días 31-45 | HU-006, HU-009 | dashboard-jefe, landing |
| **4** | Días 46-60 | HU-010, HU-011 | dashboard-clientes |
| **5** | Días 61-75 | HU-012, HU-014 | dashboard-clientes |
| **6** | Días 76-90 | HU-015, HU-016 | Producción e Inventario |
| **7** | Días 91-105 | HU-022, HU-024 | dashboard-empleados |
| **8** | Días 106-120 | HU-029, HU-030 | Notificaciones |
| **9** | Días 121-135 | HU-025, HU-026 | dashboard-empleados |
| **10** | Días 136-150 | HU-031, HU-033 | Reportes |

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.12+**
- **FastAPI** - Framework web asincrónico
- **SQLAlchemy 2.0** - ORM
- **Alembic** - Migraciones de BD
- **JWT** - Autenticación

### Frontend
- **React 18+**
- **TypeScript** - Tipado estático
- **Vite** - Build tool
- **TailwindCSS 4+** - Estilos
- **React Router** - Rutas

### Base de Datos
- **PostgreSQL 17+**
- **Docker Compose** - Orquestación

### Testing
- **pytest** + **httpx** (Backend)
- **Vitest** + **Testing Library** (Frontend)

---

## 🚀 Inicio Rápido

### 1. Clonar y configurar

```bash
cd scrum
cp .env.example .env
```

### 2. Levantar contenedores

```bash
docker-compose up -d
```

### 3. Backend


```bash
cd be
uv pip install --system --no-cache -r requirements.txt
uv run uvicorn app.main:app --reload
```

Estará disponible en: `http://localhost:8000`


### 4. Frontend

```bash
cd fe
pnpm install
pnpm run dev
```

Estará disponible en: `http://localhost:5173`

---

## 📚 Documentación de Módulos

### 🔐 Módulo de Autenticación (`fe/src/modules/auth/`)

Cubre las historias:
- **HU-001**: Creación de Cuentas
- **HU-003**: Inicio de Sesión
- **HU-004**: Recuperación de Contraseña
- **HU-002**: Validación de Cuentas (Backend)

**Archivos principales:**
- `pages/LoginPage.tsx` - Pantalla de login
- `pages/RegisterPage.tsx` - Pantalla de registro
- `pages/ForgotPasswordPage.tsx` - Recuperación de contraseña
- `pages/ResetPasswordPage.tsx` - Resetear contraseña
- `pages/ChangePasswordPage.tsx` - Cambiar contraseña
- `services/` - Llamadas a API de autenticación
- `hooks/` - Lógica reutilizable de auth

**Ver documentación completa en:** [docs/sprints/backlog_sprint_1.md](docs/sprints/backlog_sprint_1.md)

---

### 🏠 Módulo de Landing Page (`fe/src/modules/landing/`)

Página inicial pública sin requerir autenticación.

**Historias cubiertas:** (Sprint 3)
- Catálogo público básico
- Información general de la empresa

---

### 👨‍💼 Dashboard Jefe (`fe/src/modules/dashboard-jefe/`)

Panel administrativo para el jefe de la empresa.

**Historias cubiertas:**
- **HU-002**: Validación y Activación de Cuentas (Sprint 2)
- **HU-006**: Creación de Catálogo (Sprint 3)
- **HU-007**: Clasificación por Categorías (Sprint 3)
- **HU-008**: Gestión de Marcas y Estilos (Sprint 3)

---

### 👷 Dashboard Empleados (`fe/src/modules/dashboard-empleados/`)

Panel para empleados de producción.

**Historias cubiertas:**
- **HU-022**: Asignación de Tareas de Producción (Sprint 7)
- **HU-025**: Confirmación de Finalización de Tareas (Sprint 9)
- **HU-026**: Notificación de Tareas Completadas (Sprint 9)

---

### 🛒 Dashboard Clientes (`fe/src/modules/dashboard-clientes/`)

Panel para clientes mayoristas.

**Historias cubiertas:**
- **HU-010**: Consulta de Catálogo (Sprint 4)
- **HU-011**: Sistema de Filtrado (Sprint 4)
- **HU-012**: Realización de Pedidos (Sprint 5)
- **HU-014**: Consulta de Estado de Pedidos (Sprint 5)

---

### 🔗 Módulo Compartido (`fe/src/shared/`)

Recursos reutilizables en toda la aplicación.

**Contiene:**
- `components/` - Componentes UI reutilizables
- `services/` - Cliente HTTP (axios) y funciones de API
- `hooks/` - Hooks React reutilizables
- `context/` - Contextos globales (AuthContext)
- `styles/` - Estilos CSS globales

---

## 📖 Historias de Usuario

Consulta el documento completo de historias en:
[docs/historias_de_usuario.md](docs/historias_de_usuario.md)

---

## 📝 Backlogs por Sprint

- [Sprint 1 - Autenticación](docs/sprints/backlog_sprint_1.md)
- [Sprint 2 - Gestión de Cuentas](docs/sprints/backlog_sprint_2.md)
- [Sprint 3-10](docs/plan_de_trabajo.md) - Por crear

---

## 🔧 Arquitectura de Backend

### Estructura de carpetas - `be/app/`

```
be/app/
├── models/           # Modelos SQLAlchemy
├── routers/          # Rutas FastAPI por módulo
├── schemas/          # Schemas Pydantic (request/response)
├── services/         # Lógica de negocio
├── utils/            # Funciones auxiliares
├── middleware/       # JWT, CORS, etc
├── config/           # Configuración
└── database.py       # Conexión a BD
```

### Endpoints API

#### Autenticación
```
POST /api/v1/auth/register       - Registro de usuario
POST /api/v1/auth/login          - Iniciar sesión
POST /api/v1/auth/logout         - Cerrar sesión
POST /api/v1/auth/forgot-password - Solicitar recuperación
POST /api/v1/auth/reset-password  - Resetear contraseña
```

#### Administración (Protegido)
```
GET  /api/v1/admin/clients/pending          - Clientes pendientes
PATCH /api/v1/admin/clients/{id}/validate  - Validar cliente
```

---

## 🗄️ Base de Datos

Diagrama ER disponible en: [docs/diagrama ER.drawio](docs/)

**Tablas principales:**
- `users` - Usuarios del sistema
- `roles` - Roles (jefe, empleado, cliente)
- `products` - Catálogo de productos
- `orders` - Pedidos
- `order_details` - Detalle de pedidos
- `tasks` - Tareas de producción
- `inventory` - Inventario

---

## 🧪 Testing

### Backend
```bash
cd be
pytest tests/
```


### Frontend
```bash
cd fe
pnpm run test
```

---

## 🐳 Docker

### Levantar todo
```bash
docker-compose up -d
```

### Servicios disponibles
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Docs API**: http://localhost:8000/docs

### Detener
```bash
docker-compose down
```

---

## 👥 Equipo

- **Ronald** - Arquitecto
- **Andrés** - Scrum Master
- **Santiago** - Bases de Datos

---

## 📚 Recursos

- [Historias de Usuario Completas](docs/historias_de_usuario.md)
- [Plan de Trabajo](docs/plan_de_trabajo.md)
- [Arquitectura del Proyecto](docs/arquitectura_proyecto.md)

---
