"""Middleware to handle exceptions and return a JSON response with status code 400"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions and return a JSON response with status code 400"""

    def __init__(self, app: FastAPI ) -> None:
        super().__init__(app)

    async def dispatch(self, request, call_next):
        """Middleware to handle exceptions and return a JSON response with status code 400"""
        try:
            return await call_next(request)
        except Exception as e: # pylint: disable=broad-except,unused-variable
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "An error occurred. Please try again."},
            )
