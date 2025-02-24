from fastapi import APIRouter, UploadFile
import shutil


router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)

# Загрузка картинок в папку с форматом web
@router.post("/hotels")
async def add_hotels_images(name: int, file: UploadFile):
    with open(f"app/static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
