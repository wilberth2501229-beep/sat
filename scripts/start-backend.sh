#!/bin/bash

echo "🚀 Iniciando Gestor Fiscal Personal - Backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Install dependencies
echo "📚 Instalando dependencias..."
pip install -r backend/requirements.txt

# Install Playwright
echo "🎭 Instalando Playwright browsers..."
playwright install chromium

# Copy .env if not exists
if [ ! -f ".env" ]; then
    echo "📝 Copiando archivo .env..."
    cp .env.example .env
    echo "⚠️  Por favor, configura las variables de entorno en .env"
fi

# Wait for database
echo "⏳ Esperando base de datos..."
sleep 5

# Run migrations
echo "🗄️  Aplicando migraciones..."
cd backend
alembic upgrade head

# Start server
echo "✅ Iniciando servidor..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
