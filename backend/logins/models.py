from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(Uuid, default=uuid.uuid4, primary_key=True)
    username : Mapped[str] = mapped_column(String(30), nullable=False)
    email : Mapped[str] = mapped_column(String(130), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(250), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user", server_default="user")