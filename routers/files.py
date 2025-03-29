from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
    Form,
    status,
    HTTPException,
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.operations import AudioFileDO
from db.connect import get_session
from schemas.file import AudioFileOut
from schemas.user import UserOut
from services.auth import get_current_user
from utils.storage_utils import save_file
from config import settings

router = APIRouter(prefix="/files")


# Роутер по созданию файла
@router.post("/upload/")
async def upload_audio(
    file: UploadFile = File(...),
    custom_filename: str = Form(None),
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    saved_file = await save_file(
        file=file, user_id=user.id, custom_filename=custom_filename
    )
    await AudioFileDO.add(
        session=session,
        values={
            "filename": saved_file["filename"],
            "filepath": saved_file["filepath"],
            "owner_id": user.id,
        },
    )

    return JSONResponse(
        content="The file was saved successfully",
        status_code=status.HTTP_201_CREATED,
    )


# Роутер получения всех файлов пользователя
@router.get("/", response_model=list[AudioFileOut])
async def get_list_files(
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    files = AudioFileDO.get_by_owner_id(owner_id=user.id, session=session)
    if not files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No files found for this user",
        )
    return files
