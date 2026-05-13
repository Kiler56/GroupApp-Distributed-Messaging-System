# ==========================================
# GroupApp - Script de ejecución INTEGRADO
# ==========================================

Write-Host "Iniciando Ecosistema de GroupApp..." -ForegroundColor Cyan

# 0. Instalar dependencias necesarias
Write-Host "Verificando dependencias..." -ForegroundColor Gray
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart httpx uuid6 pymongo pika grpcio grpcio-tools protobuf

# 1. Roles Service (gRPC) - Puerto 50051
Write-Host "Arrancando Roles Service (gRPC) en puerto 50051..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m Roles.main"

# 2. Auth Service (Backend Principal + gRPC) - Puerto 8000 / 50052

Write-Host "Arrancando Auth Service (REST: 8000, gRPC: 50052)..." -ForegroundColor Yellow
# Ejecutamos desde la carpeta 'Auth' para que el modulo 'auth_service' sea localizable
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Auth; python -m uvicorn auth_service.main:app --port 8000"


# 2. Mensajería Backend - Puerto 8001
Write-Host "Arrancando Mensajeria Service en puerto 8001..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Message; python -m uvicorn app.main:app --port 8001"

# 3. Grupos Service - Puerto 8002
Write-Host "Arrancando Grupos Service en puerto 8002..." -ForegroundColor Yellow
$env:PYTHONPATH = ".;$env:PYTHONPATH"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn Grupos.main:app --port 8002"

# 4. Media Service - Puerto 8003
Write-Host "Arrancando Media Service en puerto 8003..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd MediaService; python -m uvicorn app.main:app --port 8003"


# 5. Grupos Frontend - Puerto 5173
Write-Host "Arrancando Grupos Frontend en puerto 5173..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Grupos-front; npm install; npm run dev"

Write-Host "----------------------------------------------------" -ForegroundColor Green
Write-Host "LISTO! Entorno iniciado." -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Green

