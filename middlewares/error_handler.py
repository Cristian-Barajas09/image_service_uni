"""Middleware to handle exceptions and return a JSON response with status code 400"""
from starlette.middleware import Middleware
from fastapi import status
from fastapi.responses import JSONResponse

class ErrorHandlerMiddleware(Middleware):
    """Middleware to handle exceptions and return a JSON response with status code 400"""
    async def dispatch(self, request, call_next):
        """Middleware to handle exceptions and return a JSON response with status code 400"""
        try:
            return await call_next(request)
        except Exception as e: # pylint: disable=broad-except,unused-variable
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "An error occurred. Please try again."},
            )
