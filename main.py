"""Main module for the FastAPI application."""
import os
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from routers import images_router
from database.config import engine
from middlewares.error_handler import ErrorHandlerMiddleware
from exceptions.image_exceptions import ImageTypeNotSupportedError
from utils import make_url_path

SQLModel.metadata.create_all(engine)

app = FastAPI()
dotenv.load_dotenv()

app.include_router(
    images_router.router,
    prefix=make_url_path("images"),
)


origins = [
    os.getenv("SERVER_URL"),
]

app.add_middleware(ErrorHandlerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ImageTypeNotSupportedError)
async def image_type_not_supported_error_handler(request, exc):
    """Image type not supported error handler"""
    return {
        "detail": exc.message,
        "error": "ImageTypeNotSupportedError",
        "request": request.url,
    }