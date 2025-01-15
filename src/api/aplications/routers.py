from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.aplications.schemas import AplicationRead, AplicationCreate, PaginatedAplications
from api.aplications.service import AplicationService
from core.database import get_async_session

router = APIRouter(prefix="/aplications")
aplication_service = AplicationService()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AplicationRead)
async def create_aplication(
    aplication_data: AplicationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_aplication = await aplication_service.create_aplication(aplication_data, session)
    return new_aplication


@router.get("", status_code=200, response_model=PaginatedAplications)
async def get_applications(
    user_name: Optional[str] = Query(None, description="Filter by user name"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, description="Page size"),
    session: AsyncSession = Depends(get_async_session),
):
    aplications = await AplicationService.get_aplications(session, user_name, page, size)
    return aplications
