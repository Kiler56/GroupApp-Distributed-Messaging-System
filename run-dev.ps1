# ==========================================
# GroupApp - Script de ejecución INTEGRADO
# ==========================================

Write-Host "Iniciando Ecosistema de GroupApp..." -ForegroundColor Cyan

# 0. Instalar dependencias necesarias
Write-Host "Verificando dependencias..." -ForegroundColor Gray
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart httpx uuid6 pymongo pika grpcio grpcio-tools protobuf

# 1. Roles Service (gRPC) - Puerto 50051
Write-Host "Arrancando Roles Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Roles; .\run-dev.ps1"

# 2. Auth Service (Backend Principal + gRPC) - Puerto 8000 / 50052
Write-Host "Arrancando Auth Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Auth; .\run-dev.ps1"

# 2. Mensajería Backend - Puerto 8001
Write-Host "Arrancando Mensajeria Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Message; .\run-dev.ps1"

# 3. Grupos Service - Puerto 8002
Write-Host "Arrancando Grupos Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Grupos; .\run-dev.ps1"

# 4. Media Service - Puerto 8003
Write-Host "Arrancando Media Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd MediaService; .\run-dev.ps1"



# 5. Frontend de Mensajeria y Login - Puerto 5500

Write-Host "Arrancando Frontend (Mensajes/Login) en puerto 5500..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Message/frontend; python -m http.server 5500"

# 5. Frontend de Grupos - Puerto 5173
Write-Host "Arrancando Grupos Frontend en puerto 5173..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Grupos-front; npm install; npm run dev"

Write-Host "----------------------------------------------------" -ForegroundColor Green
Write-Host "LISTO! Accede a: http://localhost:5500/login.html" -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Green
