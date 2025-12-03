# 🚀 Backend API - Gestor Fiscal Personal

API REST construida con FastAPI para la gestión fiscal personal en México.

## 🛠️ Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar Playwright browsers

```bash
playwright install chromium
```

### 4. Configurar variables de entorno

```bash
cp ../.env.example .env
# Editar .env con tus configuraciones
```

### 5. Inicializar base de datos

```bash
# Crear primera migración
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head
```

## 🚀 Ejecución

### Modo desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Con Docker Compose

```bash
cd ..
docker-compose up -d
```

## 📋 Estructura

```
backend/
├── app/
│   ├── api/              # Endpoints de API
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py        # Autenticación
│   │       │   ├── users.py       # Gestión de usuarios
│   │       │   ├── fiscal.py      # Perfil fiscal
│   │       │   ├── documents.py   # Documentos (TODO)
│   │       │   └── sat.py         # Integración SAT (TODO)
│   │       └── router.py
│   ├── automation/       # Automatización SAT
│   │   ├── sat_automation.py   # Web scraping
│   │   ├── rfc_validator.py    # Validación RFC/CURP
│   │   └── ocr_service.py      # OCR para documentos
│   ├── core/             # Configuración central
│   │   ├── config.py     # Settings
│   │   ├── database.py   # SQLAlchemy
│   │   ├── security.py   # JWT, encryption
│   │   └── redis.py      # Cache
│   ├── models/           # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── fiscal_profile.py
│   │   ├── sat_credentials.py
│   │   ├── document.py
│   │   └── notification.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── user.py
│   │   ├── fiscal_profile.py
│   │   ├── document.py
│   │   └── sat.py
│   ├── workers/          # Celery workers
│   │   ├── celery_app.py
│   │   └── tasks/
│   │       ├── sat_tasks.py
│   │       ├── document_tasks.py
│   │       └── notification_tasks.py
│   └── main.py           # FastAPI app
├── alembic/              # Migraciones DB
├── storage/              # Almacenamiento local
├── tests/                # Tests (TODO)
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🔑 Endpoints Principales

### Autenticación
- `POST /api/v1/auth/register` - Registro
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Usuario actual

### Usuarios
- `GET /api/v1/users/profile` - Ver perfil
- `PUT /api/v1/users/profile` - Actualizar perfil
- `POST /api/v1/users/change-password` - Cambiar contraseña

### Perfil Fiscal
- `GET /api/v1/fiscal/profile` - Ver perfil fiscal
- `POST /api/v1/fiscal/profile` - Crear perfil fiscal
- `PUT /api/v1/fiscal/profile` - Actualizar perfil
- `POST /api/v1/fiscal/validate-rfc` - Validar RFC
- `POST /api/v1/fiscal/lookup-curp` - Buscar por CURP

## 🔧 Celery Workers

### Iniciar worker

```bash
celery -A app.workers.celery_app worker --loglevel=info
```

### Iniciar beat (tareas programadas)

```bash
celery -A app.workers.celery_app beat --loglevel=info
```

### Flower (monitoring)

```bash
celery -A app.workers.celery_app flower
```

## 📝 Migraciones

### Crear nueva migración

```bash
alembic revision --autogenerate -m "descripción"
```

### Aplicar migraciones

```bash
alembic upgrade head
```

### Revertir migración

```bash
alembic downgrade -1
```

## 🔐 Seguridad

- JWT para autenticación
- Bcrypt para passwords
- Fernet para cifrado de documentos sensibles
- CORS configurado
- Rate limiting (TODO)

## 🧪 Testing

```bash
pytest
pytest --cov=app tests/
```

## 📚 Documentación API

Una vez iniciado el servidor:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 🐳 Docker

```bash
docker build -t sat-backend .
docker run -p 8000:8000 sat-backend
```
