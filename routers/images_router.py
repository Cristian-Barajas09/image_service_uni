"""Images router"""
from typing import Annotated
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi.responses import FileResponse
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from schemas.image_schema import ImageSchema, DataSchema
from services.image_service import ImageService

from database.config import engine

router = APIRouter()


@router.get("/",response_model=DataSchema)
def get_images(image_service: Annotated[ImageService,Depends()]):
    """Get images"""
    image_service.set_engine(engine)

    return DataSchema(data=[
        ImageSchema(**{
            "path": f"/images/{image.name}",
            "name": image.name
        }) for image in image_service.get_images()
    ])

@router.get("/{file_name}",response_class=FileResponse)
async def get_image(file_name: str,image_service: Annotated[ImageService,Depends()]):
    """Get image"""
    image_service.set_engine(engine)

    image = await image_service.get_image(file_name)

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    return FileResponse(image.realPath,media_type=image.contentType)



@router.post("/",response_model=ImageSchema)
async def create_image(
    image: UploadFile, image_service: Annotated[ImageService,Depends()]
):
    """Create image"""
    image_service.set_engine(engine)

    image_result = await image_service.save_image(image)

    return ImageSchema(
        **image_result["data"]
    )

@router.put("/image_id}")
async def update_image(image_id: int):
    """Update image"""

    return {"image": image_id}

@router.delete("/{image_id}")
def delete_image(image_id: int):
    """Delete image"""
    return {"image": image_id}
