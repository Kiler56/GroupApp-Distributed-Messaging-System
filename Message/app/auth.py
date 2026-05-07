from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
from app.config import AUTH_SERVICE_URL

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        response = requests.get(
            f"{AUTH_SERVICE_URL}/auth/profile",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_data = response.json()

        return {
            **user_data,
            "token": token
        }

    except Exception as e:
        print("Auth error:", e)
        raise HTTPException(status_code=401, detail="Auth service error")