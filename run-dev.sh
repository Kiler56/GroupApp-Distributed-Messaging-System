#!/bin/bash

echo "Iniciando ecosistema GroupApp..."

# 1. Roles Service (gRPC) - Puerto 50051
echo "Iniciando Roles Service (gRPC) en puerto 50051..."
python3 -m Roles.main &

# 2. Auth Service - Puerto 8000 / 50052
echo "Iniciando Auth Service (REST: 8000, gRPC: 50052)..."
(cd Auth && python3 -m uvicorn auth_service.main:app --port 8000) &

# 3. Message Service - Puerto 8001
echo "Iniciando Message Service en puerto 8001..."
(cd Message && python3 -m uvicorn app.main:app --port 8001) &

# 4. Grupos Service - Puerto 8002
echo "Iniciando Grupos Service en puerto 8002..."
export PYTHONPATH=".:$PYTHONPATH"
python3 -m uvicorn Grupos.main:app --port 8002 &

# 5. Media Service - Puerto 8003
echo "Iniciando Media Service en puerto 8003..."
(cd MediaService && python3 -m uvicorn app.main:app --port 8003) &

# 6. Grupos Frontend - Puerto 5173
echo "Iniciando Grupos Frontend en puerto 5173..."
(cd Grupos-front && npm run dev) &

echo "----------------------------------------------------"
echo "Servicios arrancando en segundo plano."
echo "----------------------------------------------------"

wait
