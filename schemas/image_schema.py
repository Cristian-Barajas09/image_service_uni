from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")

class ImageSchema(BaseModel):
    """Image schema"""
    path: str
    name: str

class DataSchema(BaseModel, Generic[T]):
    """Data schema"""
    data: T
