from fastapi import Depends, APIRouter
from logins.db import get_db
from logins.models import User
from logins.auth import verify_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .Schemas import PageCreate, PageOut
from .Models import Page

router = APIRouter(prefix="/pages", tags=["pages"])

@router.post("/newpage", response_model=PageOut, status_code=201)
async def create_page(
    data: PageCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    page = Page(title=data.title, content= data.content, owner_id= user.id)
    db.add(page)
    await db.commit()
    await db.refresh(page)
    return page

@router.get("/allpages", response_model=list[PageOut])
async def get_pages(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):  
    query = select(Page).where(Page.owner_id == user.id).order_by(Page.created_at.desc())
    pages = (await db.scalars(query)).all()
    return pages