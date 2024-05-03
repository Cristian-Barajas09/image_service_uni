from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import images_router
from database.config import engine
from sqlmodel import SQLModel


SQLModel.metadata.create_all(engine)

app = FastAPI()


app.include_router(
    images_router.router,
    prefix="/images",
)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


