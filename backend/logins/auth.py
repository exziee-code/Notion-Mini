import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import uuid
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from .models import User
from .db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

bearer = HTTPBearer()
load_dotenv()

secret_key = os.getenv("SECRET_KEY")

def get_token(user_id: uuid.UUID):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

async def verify_token(cred: HTTPAuthorizationCredentials= Depends(bearer),
                 db: AsyncSession = Depends(get_db)) -> dict:
    token = cred.credentials
    try:
        payload = jwt.decode(token, secret_key, algorithms="HS256")
        user_id = payload["sub"]
        user = await db.scalar(select(User).where(User.id == uuid.UUID(user_id)))
        if user is None:
            raise ValueError
    except InvalidTokenError, ValueError, KeyError:
        raise HTTPException(status_code=401, detail="invalid crediental")

    return {"id": user.id, "name": user.username, "email": user.email}