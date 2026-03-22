# RNF-001 — Seguridad

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-001                                                |
| **Nombre**        | Seguridad                                              |
| **Categoría**     | Seguridad de la información                            |
| **Prioridad**     | Crítica                                                |
| **Estado**        | Implementado                                           |

### RNF-001.1 — Hashing de contraseñas

Las contraseñas de los usuarios deben almacenarse mediante hashing con el algoritmo **bcrypt**. Nunca se almacenan en texto plano ni se incluyen en respuestas de la API.

### RNF-001.2 — Tokens JWT

La autenticación debe basarse en tokens JWT (JSON Web Tokens) firmados con algoritmo **HS256**:

- **Access token**: duración de 15 minutos.
- **Refresh token**: duración de 7 días.
- La clave secreta debe tener mínimo 32 caracteres y almacenarse en variable de entorno.

### RNF-001.3 — Prevención de enumeración de usuarios

Los mensajes de error en endpoints de autenticación deben ser genéricos:

- En login: "Incorrect email or password" (sin distinguir si el email existe).
- En forgot-password: siempre retornar el mismo mensaje, sin revelar si el email está registrado.

### RNF-001.4 — Validación de entradas

Todas las entradas del usuario deben validarse tanto en el frontend como en el backend:

- Frontend: validación con lógica React antes de enviar.
- Backend: validación con Pydantic (schemas tipados y restrictivos).

### RNF-001.5 — Protección contra inyección SQL

El sistema debe usar SQLAlchemy ORM para todas las consultas a la base de datos. No se permite SQL crudo sin parametrizar.

### RNF-001.6 — CORS (Cross-Origin Resource Sharing)

- En desarrollo: permitir únicamente `http://localhost:5173`.
- En producción: configurar orígenes específicos; nunca usar `allow_origins=["*"]`.

### RNF-001.7 — Variables de entorno

Toda información sensible (claves secretas, credenciales de BD, configuraciones SMTP) debe almacenarse en archivos `.env` no versionados. Se debe proveer un `.env.example` como plantilla.

### RNF-001.8 — Fortaleza de contraseñas

Las contraseñas deben cumplir requisitos mínimos:

- Mínimo 8 caracteres.
- Al menos 1 letra mayúscula.
- Al menos 1 letra minúscula.
- Al menos 1 número.

---

# RNF-002 — Rendimiento

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-002                                                |
| **Nombre**        | Rendimiento                                            |
| **Categoría**     | Rendimiento                                            |
| **Prioridad**     | Alta                                                   |
| **Estado**        | Implementado                                           |

### RNF-002.1 — Tiempo de respuesta de la API

Los endpoints de la API deben responder en menos de **500 milisegundos** en condiciones normales de carga (excluyendo latencia de red).

### RNF-002.2 — Framework asíncrono

El backend debe utilizar un framework asíncrono (FastAPI + Uvicorn) para manejar múltiples solicitudes concurrentes de forma eficiente sin bloquear el event loop.

### RNF-002.3 — Connection pooling

Las conexiones a la base de datos deben gestionarse mediante un pool de conexiones configurado en SQLAlchemy, evitando la creación/destrucción de conexiones por cada solicitud.

### RNF-002.4 — Build optimizado del frontend

El frontend debe compilarse a un bundle optimizado de producción mediante Vite, aplicando:

- Tree-shaking (eliminación de código no utilizado).
- Minificación de JavaScript y CSS.
- Code splitting para carga eficiente.

### RNF-002.5 — Carga del frontend

La aplicación frontend debe cargar completamente (First Contentful Paint) en menos de **3 segundos** en una conexión de banda ancha estándar.

---

# RNF-003 — Usabilidad y Experiencia de Usuario (UX/UI)

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-003                                                |
| **Nombre**        | Usabilidad y Experiencia de Usuario (UX/UI)            |
| **Categoría**     | Usabilidad                                             |
| **Prioridad**     | Alta                                                   |
| **Estado**        | Implementado                                           |

### RNF-003.1 — Diseño responsivo (Mobile-first)

La interfaz debe adaptarse correctamente a distintos tamaños de pantalla:

- Móvil (320px — 768px)
- Tablet (768px — 1024px)
- Desktop (1024px+)

Los formularios de autenticación deben verse y funcionar correctamente en dispositivos móviles.

### RNF-003.2 — Soporte de temas (Dark/Light mode)

La aplicación debe ofrecer tema claro y oscuro con toggle manual, respetando la preferencia del sistema operativo como valor por defecto y persistiendo la elección del usuario.

### RNF-003.3 — Tipografía

Se deben usar exclusivamente fuentes **sans-serif** (`Inter`, `system-ui`, `sans-serif`).

### RNF-003.4 — Colores

Los colores deben ser sólidos y planos. Queda **prohibido** el uso de degradados (`gradient`) en cualquier elemento de la interfaz.

### RNF-003.5 — Botones de acción

Los botones de acción (Guardar, Enviar, etc.) deben estar alineados a la **derecha** del contenedor.

### RNF-003.6 — Feedback visual

- Los formularios deben mostrar mensajes de error claros y específicos debajo de cada campo.
- Las operaciones asíncronas deben mostrar indicadores de carga (loading states).
- Las acciones exitosas deben mostrar alertas de confirmación (tipo success).
- Las acciones fallidas deben mostrar alertas de error (tipo error).

### RNF-003.7 — Transiciones

Los elementos interactivos (botones, inputs, toggles) deben tener transiciones suaves en hover y focus (`transition-colors`, `duration-200`).

### RNF-003.8 — Iconografía

Los campos de formulario deben incluir iconos contextuales en su lado izquierdo (email → sobre, password → candado, etc.) usando la librería `lucide-react` para mejorar la identificación visual inmediata.

### RNF-003.9 — Consistencia visual

Todos los componentes de formulario deben usar el mismo componente base (`InputField`, `Button`, `Alert`) para garantizar consistencia en toda la aplicación.

---

# RNF-004 — Accesibilidad

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-004                                                |
| **Nombre**        | Accesibilidad                                          |
| **Categoría**     | Accesibilidad                                          |
| **Prioridad**     | Media                                                  |
| **Estado**        | Implementado                                           |

### RNF-004.1 — Etiquetas en formularios

Todos los campos de formulario deben tener una etiqueta `<label>` asociada mediante `htmlFor`/`id`, de modo que los lectores de pantalla anuncien correctamente el propósito de cada campo.

### RNF-004.2 — Atributos ARIA

- Los campos con error deben incluir `aria-invalid="true"`.
- Los mensajes de error deben estar conectados al campo mediante `aria-describedby`.
- Los mensajes de error deben tener `role="alert"` para que los lectores de pantalla los anuncien.
- Los iconos decorativos deben tener `aria-hidden="true"`.
- Los botones sin texto visible (toggle de tema) deben tener `aria-label` descriptivo.

### RNF-004.3 — Contraste de colores

Los colores de texto y fondo deben cumplir el nivel **AA** de WCAG (Web Content Accessibility Guidelines), tanto en tema claro como en tema oscuro.

### RNF-004.4 — Navegación por teclado

Todos los elementos interactivos (inputs, botones, enlaces) deben ser accesibles y operables mediante teclado (Tab, Enter, Escape).

### RNF-004.5 — Toggle de visibilidad de contraseña

Los campos de contraseña deben incluir un botón para mostrar/ocultar el texto, con `aria-label` que indique la acción actual ("Mostrar contraseña" / "Ocultar contraseña").

---

# RNF-005 — Mantenibilidad y Calidad de Código

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-005                                                |
| **Nombre**        | Mantenibilidad y Calidad de Código                     |
| **Categoría**     | Mantenibilidad                                         |
| **Prioridad**     | Alta                                                   |
| **Estado**        | Implementado                                           |

### RNF-005.1 — Cobertura de tests

- **Backend**: cobertura mínima del 80% en módulos de lógica de negocio (pytest + pytest-cov).
- **Frontend**: tests unitarios para componentes críticos y flujos de autenticación (Vitest + Testing Library).

### RNF-005.2 — Tipado estricto

- **Python**: type hints obligatorios en parámetros y retornos de todas las funciones.
- **TypeScript**: `strict: true` en `tsconfig.json`; nunca usar `any` de forma explícita salvo justificación documentada.

### RNF-005.3 — Linting y formateo

- **Backend**: `ruff` para linting y formateo, siguiendo PEP 8 con línea máxima de 100 caracteres.
- **Frontend**: ESLint + Prettier para linting y formateo automático.

### RNF-005.4 — Separación de responsabilidades

La arquitectura debe seguir una separación clara:

- **Backend**: Routers (endpoints) → Services (lógica de negocio) → Models (BD) → Schemas (validación).
- **Frontend**: Pages (vistas) → Components (UI reutilizable) → Hooks (lógica) → Context (estado global) → API (comunicación HTTP).

### RNF-005.5 — Comentarios pedagógicos

Cada archivo y bloque de código significativo debe incluir comentarios en español que respondan:

- **¿Qué?** — Descripción del elemento.
- **¿Para qué?** — Propósito y justificación.
- **¿Impacto?** — Consecuencias de su presencia o ausencia.

### RNF-005.6 — Convenciones de nomenclatura

- **Código**: nomenclatura en inglés (variables, funciones, clases, endpoints, tablas).
- **Documentación**: comentarios y documentación en español.
- **Commits**: formato Conventional Commits en inglés con cuerpo What/For/Impact.

### RNF-005.7 — Principios de diseño

El código debe adherirse a:

- **DRY** (Don't Repeat Yourself)
- **KISS** (Keep It Simple, Stupid)
- **YAGNI** (You Aren't Gonna Need It)
- **Fail Fast** (validar inputs al inicio)

---

# RNF-006 — Compatibilidad y Portabilidad

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-006                                                |
| **Nombre**        | Compatibilidad y Portabilidad                          |
| **Categoría**     | Compatibilidad                                         |
| **Prioridad**     | Media                                                  |
| **Estado**        | Implementado                                           |

### RNF-006.1 — Navegadores soportados

La aplicación frontend debe funcionar correctamente en las últimas dos versiones estables de:

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Safari

### RNF-006.2 — Resoluciones de pantalla

La interfaz debe ser funcional desde **320px** de ancho (móviles pequeños) hasta **2560px** (monitores ultrawide).

### RNF-006.3 — Sistema operativo del servidor

El backend debe ejecutarse correctamente en sistemas Linux (entorno de desarrollo y producción).

### RNF-006.4 — Containerización

La base de datos debe ejecutarse en contenedores Docker para garantizar reproducibilidad del entorno de desarrollo.

### RNF-006.5 — Versiones mínimas de runtime

- **Python**: 3.12+
- **Node.js**: 20 LTS+
- **PostgreSQL**: 17+
