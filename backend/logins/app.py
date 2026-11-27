from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_db, Base, engine
from .models import User
from .schemas import UserSchema, Login
from .security import HashPassword, verify_password
from contextlib import asynccontextmanager
from .auth import get_token, verify_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.post("/register/")
async def register(data: UserSchema, 
                   db: AsyncSession = Depends(get_db)):
    user = User(username=data.username, 
                email= data.email, 
                hashed_password = HashPassword(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}

@app.post("/user/login/")
async def login(data: Login, db: AsyncSession = Depends(get_db)):
    typed_password = data.password
    user = await db.scalar(select(User).where(User.email == data.email))
    if user is None or not verify_password(typed_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="invalid credientals")
    else:
        return {"Token": get_token(user.id), "Token Type": "bearer"}

@app.get("/user/me")
async def me(data: dict= Depends(verify_token)) -> dict:
    return data