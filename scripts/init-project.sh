#!/bin/bash

echo "🔧 Inicializando proyecto..."

# Create .env from example
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Archivo .env creado"
    echo "⚠️  Configura las variables de entorno antes de continuar"
fi

# Generate encryption key
echo "🔐 Generando claves de cifrado..."
python3 << EOF
from cryptography.fernet import Fernet
print(f"ENCRYPTION_KEY={Fernet.generate_key().decode()}")
EOF

echo ""
echo "✅ Inicialización completa"
echo ""
echo "Próximos pasos:"
echo "1. Configura las variables de entorno en .env"
echo "2. Ejecuta: docker-compose up -d"
echo "3. Accede a: http://localhost:8000/api/v1/docs"
