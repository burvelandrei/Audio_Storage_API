from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.operations import UserDO
from db.connect import get_session
from schemas.user import UserOut, UserModify
from services.auth import get_current_user, check_admin

router = APIRouter(prefix="/user")


@router.get("/{user_id}/", response_model=UserOut)
async def get_user(
    user_id: int,
    admin: UserOut = Depends(check_admin),
    session: AsyncSession = Depends(get_session),
):
    user = await UserDO.get_by_id(id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


@router.patch("/{user_id}/", response_model=UserOut)
async def update_user(
    user_id: int,
    user_update: UserModify,
    admin: UserOut = Depends(check_admin),
    session: AsyncSession = Depends(get_session),
):
    values_to_update = user_update.dict(exclude_unset=True)

    if not values_to_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update",
        )

    updated_user = await UserDO.update(
        session=session,
        id=user_id,
        **values_to_update,
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return updated_user


@router.delete("/{user_id}/")
async def delete_user(
    user_id: int,
    admin: UserOut = Depends(check_admin),
    session: AsyncSession = Depends(get_session),
):
    await UserDO.delete(id=user_id, session=session)
    return JSONResponse(
        content="Successfully deleted user",
        status_code=status.HTTP_204_NO_CONTENT,
    )
