# 🏛️ Cómo Funciona el Gestor Fiscal SAT

## 📐 Arquitectura

```
┌─────────────────┐      HTTP/REST      ┌──────────────────┐
│                 │  ←─────────────────→ │                  │
│   STREAMLIT     │    requests.post()   │    FASTAPI       │
│   (Frontend)    │    localhost:8501    │    (Backend)     │
│                 │                      │                  │
└─────────────────┘                      └────────┬─────────┘
                                                  │
                                                  │ SQLAlchemy
                                                  ↓
                                         ┌─────────────────┐
                                         │   PostgreSQL    │
                                         │   (Base Datos)  │
                                         └─────────────────┘
```

## 🔗 Conexión Frontend ↔ Backend

### Frontend hace peticiones HTTP:
```python
# frontend/streamlit_app.py

API_BASE_URL = "http://localhost:8000/api/v1"

# Login
response = requests.post(f"{API_BASE_URL}/auth/login", json={
    "username": email,
    "password": password
})

# Get user profile
response = requests.get(f"{API_BASE_URL}/auth/me", 
    headers={"Authorization": f"Bearer {token}"})
```

### Backend responde con JSON:
```python
# backend/app/api/v1/endpoints/auth.py

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm):
    user = authenticate_user(form_data.username, form_data.password)
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
```

## 🗄️ Base de Datos

### 1. Modelos definen la estructura:
```python
# backend/app/models/user.py

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    # ... más campos
```

### 2. SQLAlchemy crea las tablas:
```python
# backend/create_tables.py

from app.core.database import engine, Base
from app.models import *

Base.metadata.create_all(bind=engine)
# ↑ Esto lee todos los modelos y crea:
#   CREATE TABLE users (id SERIAL, email VARCHAR, ...)
#   CREATE TABLE fiscal_profiles (...)
#   etc.
```

### 3. Configuración de conexión:
```bash
# .env
DATABASE_URL=postgresql://x@localhost:5432/sat_db
```

```python
# backend/app/core/database.py

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

## 🔐 Autenticación (JWT)

### Flujo completo:

1. **Usuario se registra:**
   ```
   POST /api/v1/auth/register
   { "email": "user@example.com", "password": "secret" }
   ```

2. **Backend hashea contraseña:**
   ```python
   hashed_password = get_password_hash(password)  # bcrypt
   user = User(email=email, hashed_password=hashed_password)
   db.add(user)
   ```

3. **Usuario hace login:**
   ```
   POST /api/v1/auth/login
   { "username": "user@example.com", "password": "secret" }
   ```

4. **Backend verifica y genera JWT:**
   ```python
   verify_password(password, user.hashed_password)  # ✓
   token = create_access_token({"sub": str(user.id)})  # JWT
   return {"access_token": token}
   ```

5. **Frontend guarda token:**
   ```python
   st.session_state.token = data["access_token"]
   ```

6. **Requests posteriores incluyen token:**
   ```python
   headers = {"Authorization": f"Bearer {token}"}
   requests.get("/api/v1/users/me", headers=headers)
   ```

7. **Backend valida token:**
   ```python
   @router.get("/me")
   def get_current_user(current_user: User = Depends(get_current_user_dep)):
       return current_user  # Token válido ✓
   ```

## 🔒 Seguridad de Credenciales SAT

### Las credenciales se encriptan antes de guardar:

```python
# backend/app/core/security.py

from cryptography.fernet import Fernet

cipher = Fernet(settings.ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted: str) -> str:
    return cipher.decrypt(encrypted.encode()).decode()
```

### Al guardar credenciales SAT:
```python
encrypted_password = encrypt_data(sat_password)
sat_creds = SATCredentials(
    user_id=user.id,
    encrypted_password=encrypted_password  # Se guarda encriptado
)
db.add(sat_creds)
```

### Al usar credenciales:
```python
# Recuperar y desencriptar
sat_creds = db.query(SATCredentials).filter_by(user_id=user_id).first()
real_password = decrypt_data(sat_creds.encrypted_password)

# Usar en automatización
sat_automation = SATAutomation()
await sat_automation.login_sat(rfc, real_password)
```

## 🚀 Inicio de la Aplicación

### Opción 1 - Script automático:
```bash
./start.sh
```

Esto ejecuta:
1. Mata procesos previos
2. Inicia backend en puerto 8000 (background)
3. Inicia frontend en puerto 8501 (background)
4. Logs van a `backend.log` y `frontend.log`

### Opción 2 - Manual (2 terminales):

**Terminal 1 - Backend:**
```bash
cd backend
source ../.venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
source ../.venv/bin/activate
streamlit run streamlit_app.py --server.port 8501
```

## 📊 Flujo Completo de Uso

### 1. Usuario abre http://localhost:8501

### 2. Se registra:
```
Frontend → POST /api/v1/auth/register → Backend
Backend → Hashea password → Guarda en PostgreSQL
Backend → Responde OK
Frontend → Muestra mensaje de éxito
```

### 3. Hace login:
```
Frontend → POST /api/v1/auth/login → Backend
Backend → Verifica credenciales
Backend → Genera JWT token
Backend → Responde {"access_token": "eyJ0..."}
Frontend → Guarda token en session_state
```

### 4. Completa perfil fiscal:
```
Frontend → PUT /api/v1/fiscal/profile (con token) → Backend
Backend → Valida JWT
Backend → Guarda RFC, CURP, régimen en tabla fiscal_profiles
Backend → Responde con perfil actualizado
Frontend → Actualiza UI
```

### 5. Conecta credenciales SAT:
```
Frontend → POST /api/v1/fiscal/sat-credentials (con token) → Backend
Backend → Encripta contraseña SAT con Fernet
Backend → Guarda en tabla sat_credentials
Backend → Responde OK
Frontend → Muestra "Credenciales guardadas ✓"
```

### 6. Descarga documentos (futuro):
```
Frontend → POST /api/v1/documents/download-cfdi → Backend
Backend → Recupera credenciales SAT (desencripta)
Backend → Lanza tarea Celery background
Celery Worker → Usa Playwright para entrar al portal SAT
Celery Worker → Descarga CFDIs
Celery Worker → Guarda en tabla documents
Backend → Notifica al usuario
Frontend → Muestra documentos en tabla
```

## 🛠️ Tecnologías

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| Frontend | Streamlit | Interfaz web interactiva |
| Backend | FastAPI | API REST con validación |
| Base de Datos | PostgreSQL | Almacenamiento persistente |
| ORM | SQLAlchemy | Mapeo objeto-relacional |
| Auth | JWT + bcrypt | Autenticación segura |
| Encriptación | Fernet (AES-256) | Proteger credenciales |
| Cache | Redis | Sesiones y rate limiting |
| Workers | Celery | Tareas background (futuro) |
| Automatización | Playwright | Web scraping SAT (futuro) |
| OCR | Tesseract | Lectura de PDFs (futuro) |

## 🔧 Mantenimiento

### Ver qué está corriendo:
```bash
ps aux | grep -E "uvicorn|streamlit"
```

### Ver logs en tiempo real:
```bash
tail -f backend.log
tail -f frontend.log
```

### Detener todo:
```bash
pkill -f "uvicorn|streamlit"
```

### Reiniciar solo backend:
```bash
pkill -f uvicorn
cd backend && source ../.venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

### Recrear base de datos:
```bash
dropdb sat_db
createdb sat_db
cd backend && python create_tables.py
```

## 📝 Variables de Entorno Importantes

```bash
# .env (raíz del proyecto)

# Conexión a PostgreSQL
DATABASE_URL=postgresql://x@localhost:5432/sat_db

# Secreto para JWT (cambiar en producción)
JWT_SECRET_KEY=tu-secreto-super-seguro

# Llave para encriptar credenciales SAT (generar con Fernet)
ENCRYPTION_KEY=tu-llave-fernet-generada

# Redis para cache
REDIS_URL=redis://localhost:6379/0
```

### Generar ENCRYPTION_KEY:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 🎯 Resumen

- **Frontend y Backend son independientes**, se comunican por HTTP
- **Base de datos se crea una vez** con `create_tables.py`
- **Autenticación usa JWT** para mantener sesión
- **Credenciales SAT se encriptan** con AES-256 antes de guardar
- **Dos procesos deben estar corriendo** (backend + frontend)
- **Script `start.sh` automatiza todo** el inicio
