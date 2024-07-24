from pydantic import BaseModel

class ImageSchema(BaseModel):
    path: str
    name: str

class DataSchema(BaseModel):
    data: list[ImageSchema]
