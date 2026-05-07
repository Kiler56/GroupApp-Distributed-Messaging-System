# -*- coding: utf-8 -*-
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import httpx
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/auth/login")

from Grupos.config import AUTH_SERVICE_URL

async def get_current_user(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        try:
            # Validamos el token contra el microservicio de Auth
            response = await client.get(
                f"{AUTH_SERVICE_URL}/auth/profile",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Token invalido o expirado")
            
            data = response.json()
            return data.get("user_id")
            
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Servicio de autenticacion no disponible")
