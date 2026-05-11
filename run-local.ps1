# ==========================================
# GroupApp - Script de ejecución INTEGRADO
# ==========================================

Write-Host "Iniciando Ecosistema de GroupApp..." -ForegroundColor Cyan

# 0. Instalar dependencias necesarias
Write-Host "Verificando dependencias..." -ForegroundColor Gray
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart httpx uuid6 pymongo pika

# 1. Auth Service (Backend Principal) - Puerto 8000
Write-Host "Arrancando Auth Service en puerto 8000..." -ForegroundColor Yellow
# Ejecutamos desde la carpeta 'main' para que el modulo 'auth_service' sea localizable
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Auth; python -m uvicorn main:app --port 8000"

# 2. Mensajería Backend - Puerto 8001
Write-Host "Arrancando Mensajeria Service en puerto 8001..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Message; python -m uvicorn app.main:app --port 8001"

# 3. Grupos Service - Puerto 8002
Write-Host "Arrancando Grupos Service en puerto 8002..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn Grupos.main:app --port 8002"

# 4. Frontend de Mensajeria y Login - Puerto 5500
Write-Host "Arrancando Frontend (Mensajes/Login) en puerto 5500..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Message/frontend; python -m http.server 5500"

# 5. Frontend de Grupos - Puerto 5173
Write-Host "Arrancando Grupos Frontend en puerto 5173..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Grupos-front; npm install; npm run dev"

Write-Host "----------------------------------------------------" -ForegroundColor Green
Write-Host "LISTO! Accede a: http://localhost:5500/login.html" -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Green