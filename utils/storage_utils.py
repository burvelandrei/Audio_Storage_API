import os
import re
import shutil
import logging
import logging.config
from fastapi import FastAPI, UploadFile, HTTPException
from contextlib import asynccontextmanager
from utils.logger import logging_config
from config import settings


logging.config.dictConfig(logging_config)
logger = logging.getLogger("storage_utils")


def create_dir(dir_name: str):
    """Создает директорию, если её нет"""
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logger.info("Created directory")
    except Exception as e:
        logger.error(f"Failed to create directory: {e}")
        raise


def sanitize_filename(filename: str) -> str:
    """Очищает имя файла от небезопасных символов"""
    return re.sub(r"[^\w\-_.]", "_", filename)


async def save_file(
    file: UploadFile,
    user_id: int,
    custom_filename: str | None,
) -> dict:
    """Сохранение файла"""
    user_upload_dir = os.path.join(settings.UPLOAD_DIR, str(user_id))
    create_dir(user_upload_dir)
    original_filename = file.filename
    file_ext = os.path.splitext(original_filename)[1].lower()
    final_filename = (
        f"{sanitize_filename(custom_filename)}{file_ext}"
        if custom_filename
        else original_filename
    )
    filepath = os.path.join(user_upload_dir, final_filename)
    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        raise HTTPException(500, detail="File save error")
    return {
        "filename": final_filename,
        "filepath": filepath,
    }


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_dir(dir_name=settings.UPLOAD_DIR)
    yield
