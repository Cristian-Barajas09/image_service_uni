import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
import dotenv
from routers import images_router
from database.config import engine
from middlewares.error_handler import ErrorHandlerMiddleware
from exceptions.image_exceptions import ImageTypeNotSupportedError
SQLModel.metadata.create_all(engine)

app = FastAPI()
dotenv.load_dotenv()

app.include_router(
    images_router.router,
    prefix="/images",
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
        "detail": exc.message
    }