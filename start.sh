#!/bin/bash
# Start Backend + Frontend

echo "🏛️  Iniciando Gestor Fiscal SAT"
echo ""

# Kill any existing processes
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "streamlit run" 2>/dev/null

# Start backend
echo "🚀 Iniciando Backend..."
cd backend
source ../.venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

sleep 3

# Start frontend
echo "🎨 Iniciando Frontend..."
cd frontend
source ../.venv/bin/activate
streamlit run streamlit_app.py --server.port 8501 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Aplicación corriendo:"
echo "   Frontend: http://localhost:8501"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/v1/docs"
echo ""
echo "📋 Ver logs:"
echo "   tail -f backend.log"
echo "   tail -f frontend.log"
echo ""
echo "🛑 Para detener: pkill -f 'uvicorn|streamlit'"
