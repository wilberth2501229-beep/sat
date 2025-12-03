# 📁 Estructura del Proyecto - Gestor Fiscal Personal

```
sat/
│
├── 📄 README.md                      # Documentación principal
├── 📄 .gitignore                     # Archivos ignorados por Git
├── 📄 .env.example                   # Variables de entorno template
├── 📄 docker-compose.yml             # Orquestación de servicios
│
├── 📂 backend/                       # 🐍 Backend API (FastAPI)
│   ├── 📄 requirements.txt           # Dependencias Python
│   ├── 📄 Dockerfile                 # Container del backend
│   ├── 📄 README.md                  # Docs del backend
│   ├── 📄 alembic.ini                # Config de migraciones
│   │
│   ├── 📂 app/                       # Aplicación principal
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py                # Entry point FastAPI
│   │   │
│   │   ├── 📂 api/                   # 🛣️ Endpoints REST
│   │   │   └── 📂 v1/
│   │   │       ├── 📄 router.py      # Router principal
│   │   │       └── 📂 endpoints/
│   │   │           ├── 📄 auth.py    # Autenticación & JWT
│   │   │           ├── 📄 users.py   # Gestión usuarios
│   │   │           ├── 📄 fiscal.py  # Perfil fiscal
│   │   │           ├── 📄 documents.py (TODO)
│   │   │           └── 📄 sat.py     # Integración SAT (TODO)
│   │   │
│   │   ├── 📂 core/                  # ⚙️ Configuración central
│   │   │   ├── 📄 config.py          # Settings & env vars
│   │   │   ├── 📄 database.py        # SQLAlchemy setup
│   │   │   ├── 📄 security.py        # JWT, encryption, hashing
│   │   │   └── 📄 redis.py           # Cache & rate limiting
│   │   │
│   │   ├── 📂 models/                # 🗄️ Modelos de base de datos
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 user.py            # Usuario, auth
│   │   │   ├── 📄 fiscal_profile.py  # RFC, CURP, régimen
│   │   │   ├── 📄 sat_credentials.py # Credenciales SAT (cifradas)
│   │   │   ├── 📄 document.py        # Documentos del usuario
│   │   │   └── 📄 notification.py    # Notificaciones & audit
│   │   │
│   │   ├── 📂 schemas/               # 📋 Pydantic schemas (DTOs)
│   │   │   ├── 📄 user.py
│   │   │   ├── 📄 fiscal_profile.py
│   │   │   ├── 📄 document.py
│   │   │   └── 📄 sat.py
│   │   │
│   │   ├── 📂 automation/            # 🤖 Web scraping & automatización
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 sat_automation.py  # Playwright para SAT
│   │   │   ├── 📄 rfc_validator.py   # Validación RFC/CURP
│   │   │   └── 📄 ocr_service.py     # OCR Tesseract (INE, docs)
│   │   │
│   │   └── 📂 workers/               # ⚡ Celery background tasks
│   │       ├── 📄 __init__.py
│   │       ├── 📄 celery_app.py      # Celery config
│   │       └── 📂 tasks/
│   │           ├── 📄 sat_tasks.py   # Descarga CFDI, constancias
│   │           ├── 📄 document_tasks.py  # OCR, validación
│   │           └── 📄 notification_tasks.py  # Email, SMS, push
│   │
│   ├── 📂 alembic/                   # 🗂️ Migraciones de BD
│   │   ├── 📄 env.py
│   │   ├── 📄 script.py.mako
│   │   └── 📂 versions/
│   │
│   └── 📂 tests/                     # 🧪 Tests unitarios
│       ├── 📄 conftest.py
│       └── 📄 test_auth.py
│
├── 📂 mobile/                        # 📱 App móvil (Flutter/React Native)
│   └── 📄 README.md                  # TODO: App móvil
│
├── 📂 web/                           # 🌐 Dashboard web (Next.js)
│   └── 📄 README.md                  # TODO: Frontend web
│
├── 📂 docs/                          # 📚 Documentación
│   └── 📄 ARQUITECTURA.md            # Arquitectura detallada
│
├── 📂 scripts/                       # 🔧 Scripts de utilidad
│   ├── 📄 init-project.sh            # Inicialización proyecto
│   └── 📄 start-backend.sh           # Iniciar backend
│
└── 📂 storage/                       # 💾 Almacenamiento local
    └── (documentos cifrados)

```

## 🎯 Componentes Principales

### 1. **Backend API (FastAPI)**
- REST API completa con JWT
- Autenticación y gestión de usuarios
- Perfil fiscal (RFC, CURP, régimen)
- Sistema de documentos cifrados
- Integración con SAT (web scraping)

### 2. **Base de Datos (PostgreSQL)**
- **users**: Usuarios del sistema
- **fiscal_profiles**: Datos fiscales (RFC, régimen, obligaciones)
- **sat_credentials**: Credenciales SAT cifradas + e.firma
- **documents**: Documentos del usuario (INE, constancias, CFDI)
- **notifications**: Sistema de notificaciones
- **audit_logs**: Auditoría de acciones

### 3. **Workers (Celery)**
- **sat_tasks**: Automatización de descarga de CFDI, constancias
- **document_tasks**: Procesamiento OCR, validación, cifrado
- **notification_tasks**: Email, SMS, notificaciones push

### 4. **Automatización SAT**
- **Playwright**: Web scraping del portal SAT
- **RFC Validator**: Validación de RFC y CURP
- **OCR Service**: Extracción de datos de INE y documentos

### 5. **Seguridad**
- **JWT**: Autenticación con tokens
- **Bcrypt**: Hash de contraseñas
- **Fernet**: Cifrado simétrico de documentos
- **AES-256**: Cifrado de credenciales SAT

## 🚀 Flujo de Datos

```
Usuario → API (FastAPI) → Validación → Base de Datos
                        ↓
                    Worker (Celery)
                        ↓
                SAT Automation (Playwright)
                        ↓
                Portal SAT → Descarga
                        ↓
                Cifrado → Almacenamiento
```

## 📊 Casos de Uso Implementados

✅ **Autenticación**
- Registro de usuarios
- Login con JWT
- Refresh tokens

✅ **Perfil Fiscal**
- Crear/actualizar perfil fiscal
- Validación de RFC
- Lookup por CURP

✅ **Gestión de Usuarios**
- Ver/actualizar perfil
- Cambiar contraseña
- Eliminar cuenta

🔄 **En Desarrollo**
- Automatización SAT completa
- Gestión de documentos
- Descarga de CFDI
- Sistema de notificaciones

## 🛠️ Tecnologías Usadas

| Categoría | Tecnología |
|-----------|------------|
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy |
| **Database** | PostgreSQL, Alembic |
| **Cache** | Redis |
| **Workers** | Celery, Flower |
| **Automation** | Playwright, Selenium |
| **OCR** | Tesseract, Pillow |
| **Security** | JWT, Bcrypt, Fernet, Cryptography |
| **Container** | Docker, Docker Compose |
| **Testing** | Pytest, Faker |

## 📝 Próximos Pasos

1. ✅ Estructura base del proyecto
2. ✅ Modelos de base de datos
3. ✅ Endpoints de autenticación
4. 🔄 Completar automatización SAT
5. 🔄 Sistema de documentos
6. 📅 App móvil (Flutter)
7. 📅 Dashboard web (Next.js)
8. 📅 Despliegue en producción

---

**Fecha de creación**: Diciembre 2025
**Stack**: Python + FastAPI + PostgreSQL + Redis + Celery + Playwright
