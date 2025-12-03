# 🍎 Solución de Problemas en macOS

## Error de PostgreSQL al ejecutar setup.sh

Si recibes el error:
```
Error: Failure while executing; /bin/launchctl bootstrap gui/501 exited with 5.
```

### Solución rápida:

```bash
# 1. Detener cualquier instancia de PostgreSQL
brew services stop postgresql@15
brew services stop postgresql

# 2. Limpiar servicios de launchctl
launchctl remove homebrew.mxcl.postgresql@15 2>/dev/null
launchctl remove homebrew.mxcl.postgresql 2>/dev/null

# 3. Desinstalar versiones conflictivas (si es necesario)
brew uninstall --force postgresql@15 postgresql

# 4. Reinstalar PostgreSQL
brew install postgresql@15

# 5. Iniciar el servicio
brew services start postgresql@15

# 6. Verificar que funciona
psql postgres -c "SELECT version();"

# 7. Crear la base de datos
createdb sat_db
```

### Alternativa: Usar PostgreSQL existente

Si ya tienes PostgreSQL instalado de otra forma:

```bash
# 1. Verificar que está corriendo
psql postgres -c "SELECT 1"

# 2. Si funciona, solo crea la base de datos
createdb sat_db

# 3. Actualiza el .env con tu configuración
nano .env
# Cambia la línea DATABASE_URL según tu setup
```

### Verificación de servicios

```bash
# Ver servicios de Homebrew
brew services list

# Debe mostrar:
# postgresql@15  started
# redis          started
```

### Configuración manual paso a paso

Si el script automático falla, ejecuta estos comandos:

```bash
# 1. Instalar dependencias (sin servicios automáticos)
brew install postgresql@15 redis libxml2 libxslt

# 2. Inicializar PostgreSQL manualmente (si es necesario)
initdb /opt/homebrew/var/postgresql@15

# 3. Iniciar servicios manualmente
pg_ctl -D /opt/homebrew/var/postgresql@15 start
brew services start redis

# 4. Crear base de datos
createdb sat_db

# 5. Continuar con el resto del setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 6. Crear tablas
python backend/create_tables.py

# 7. Ejecutar la aplicación
./start.sh
```

## Problemas comunes adicionales

### Redis no inicia

```bash
# Reiniciar Redis
brew services restart redis

# Verificar
redis-cli ping
# Debe responder: PONG
```

### Python version incorrecta

```bash
# Instalar Python 3.13
brew install python@3.13

# Usar esa versión
python3.13 -m venv .venv
source .venv/bin/activate
```

### Permisos de PostgreSQL

```bash
# Si hay problemas de permisos
sudo chown -R $(whoami) /opt/homebrew/var/postgresql@15
```

## Soporte

Si ninguna de estas soluciones funciona, por favor reporta:
1. Salida de `brew services list`
2. Salida de `psql postgres -c "SELECT version();"`
3. Contenido de `/opt/homebrew/var/log/postgresql@15.log`
