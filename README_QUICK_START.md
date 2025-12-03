# 🏛️ Gestor Fiscal Personal SAT - Guía Rápida

## 🚀 Inicio Rápido (3 comandos)

```bash
# 1. Instalar dependencias de sistema (solo una vez)
sudo pacman -S libxml2 libxslt postgresql docker docker-compose

# 2. Hacer ejecutable el script de inicio
chmod +x run.sh

# 3. ¡Ejecutar!
./run.sh
```

Eso es todo! El script se encarga de:
- ✅ Crear el entorno virtual
- ✅ Instalar dependencias
- ✅ Iniciar PostgreSQL y Redis
- ✅ Aplicar migraciones
- ✅ Iniciar Backend API
- ✅ Iniciar Frontend Streamlit

## 🌐 Acceso

Una vez iniciado, abre tu navegador:

- **Frontend (Aplicación)**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/api/v1/docs

## 👤 Primera Vez

1. Abre http://localhost:8501
2. Ve a la pestaña "Registrarse"
3. Crea tu cuenta
4. ¡Comienza a gestionar tu información fiscal!

## ⚙️ Configuración Avanzada

Si necesitas cambiar configuraciones, edita `.env`:

```bash
nano .env
```

Variables importantes:
- `DATABASE_URL`: Conexión a PostgreSQL
- `JWT_SECRET_KEY`: Secreto para tokens (cámbialo en producción)
- `ENCRYPTION_KEY`: Llave para encriptar credenciales

Para generar una llave de encriptación segura:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 🛑 Detener los Servicios

Presiona `Ctrl+C` en la terminal donde ejecutaste `./run.sh`

O ejecuta:

```bash
docker-compose down
```

## 📦 Ejecutar Solo Partes Específicas

### Solo Backend:
```bash
source .venv/bin/activate
cd backend
uvicorn app.main:app --reload --port 8000
```

### Solo Frontend:
```bash
source .venv/bin/activate
cd frontend
streamlit run streamlit_app.py
```

### Solo Worker (Celery):
```bash
source .venv/bin/activate
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

### Solo Tareas Programadas:
```bash
source .venv/bin/activate
cd backend
celery -A app.workers.celery_app beat --loglevel=info
```

## 🔧 Comandos Útiles

### Ver logs en tiempo real:
```bash
# Backend
tail -f backend.log

# Frontend
tail -f frontend.log
```

### Crear una nueva migración:
```bash
cd backend
alembic revision --autogenerate -m "Descripción del cambio"
alembic upgrade head
```

### Resetear base de datos:
```bash
docker-compose down -v
docker-compose up -d postgres redis
cd backend
alembic upgrade head
```

## 🐛 Solución de Problemas

### "No se puede conectar al servidor"
- Verifica que el backend esté corriendo: `curl http://localhost:8000/health`
- Revisa logs: `tail -f backend.log`

### "Error de base de datos"
- Verifica PostgreSQL: `docker-compose ps`
- Reinicia: `docker-compose restart postgres`

### "lxml build error"
- Instala dependencias: `sudo pacman -S libxml2 libxslt`
- Reinstala: `pip install --no-cache-dir lxml`

### Puerto ya en uso
- Cambia el puerto en `run.sh` o detén el proceso:
  ```bash
  lsof -ti:8000 | xargs kill -9  # Backend
  lsof -ti:8501 | xargs kill -9  # Frontend
  ```

## 📚 Próximos Pasos

1. **Completa tu perfil fiscal** en la app
2. **Agrega tus credenciales SAT** (se guardan encriptadas)
3. **Descarga automáticamente** tu constancia fiscal
4. **Gestiona documentos** (e.firma, CFDIs, etc.)
5. **Recibe alertas** de vencimientos y obligaciones

## 🔐 Seguridad

- Las contraseñas se hashean con bcrypt
- Las credenciales SAT se encriptan con AES-256 (Fernet)
- Los tokens JWT expiran automáticamente
- Nunca compartas tu archivo `.env`

## 💡 Tips

- El frontend se actualiza automáticamente cuando cambias el código
- Usa `--reload` en uvicorn para desarrollo (ya incluido en run.sh)
- Los logs se guardan en `backend.log` y `frontend.log`
- Streamlit tiene un modo oscuro (⚙️ en la esquina superior derecha)

## 📞 Ayuda

Si tienes problemas:
1. Revisa los logs: `tail -f backend.log frontend.log`
2. Verifica servicios: `docker-compose ps`
3. Consulta la documentación API: http://localhost:8000/api/v1/docs
