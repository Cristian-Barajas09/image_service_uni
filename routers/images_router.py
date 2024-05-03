from fastapi import APIRouter
from fastapi import UploadFile
from fastapi.responses import FileResponse
from fastapi import HTTPException
from fastapi import status
from services.image_service import ImageService

from database.config import engine

router = APIRouter()


@router.get("/")
def get_images():
    service = ImageService(engine)
    return {
        "data": [
            {
                "id": image.id,
                "name": image.name,
                "url": image.url
            } for image in service.get_images()
        ]
    }

@router.get("/{file_name}")
async def get_image(file_name: str):
    sevice = ImageService(engine)

    image = await sevice.get_image(file_name)

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    return FileResponse(image.realPath,media_type=image.contentType)

@router.post("/")
async def create_image(
    image: UploadFile
):
    service = ImageService(engine)
    return await service.save_image(image)

@router.put("/image_id}")
async def update_image(image_id: int):
    

    return {"image": image_id}

@router.delete("/{image_id}")
def delete_image(image_id: int):
    return {"image": image_id}