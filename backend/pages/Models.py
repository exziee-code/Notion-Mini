from logins.db import Base
from datetime import datetime
from sqlalchemy import Uuid, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
import uuid

class Page(Base):
    __tablename__ = "pages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, default=uuid.uuid4, primary_key=True)
    
    title: Mapped[str] = mapped_column(String(200), default="Untitled")
    
    content: Mapped[str]= mapped_column(Text, default="")
    
    owner_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )