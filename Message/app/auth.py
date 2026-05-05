from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        response = requests.get(
            "http://127.0.0.1:8000/auth/profile",
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