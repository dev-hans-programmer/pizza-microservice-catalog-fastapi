# error_handlers.py

"""
Production-grade error handlers for FastAPI.
Converts exceptions into proper JSON responses with detailed error information.
"""

# import logging
# import re

# from fastapi import Request, status
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# from .exceptions import AppException


# logger = logging.getLogger(__name__)


# async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
#     """Handler for custom application exceptions."""
#     logger.error(
#         f'Application error: {exc.message}',
#         extra={
#             'path': request.url.path,
#             'method': request.method,
#             'details': exc.details,
#         },
#     )

#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             'error': {
#                 'message': exc.message,
#                 'status_code': exc.status_code,
#                 'details': exc.details,
#                 'path': request.url.path,
#             }
#         },
#     )


# async def validation_exception_handler(
#     request: Request, exc: RequestValidationError
# ) -> JSONResponse:
#     """Handler for Pydantic validation errors."""
#     errors = []
#     for error in exc.errors():
#         errors.append(
#             {
#                 'field': '.'.join(str(x) for x in error['loc']),
#                 'message': error['msg'],
#                 'type': error['type'],
#             }
#         )

#     logger.warning(
#         'Validation error',
#         extra={'path': request.url.path, 'method': request.method, 'errors': errors},
#     )

#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             'error': {
#                 'message': 'Validation failed',
#                 'status_code': 422,
#                 'details': {'validation_errors': errors},
#                 'path': request.url.path,
#             }
#         },
#     )


# async def database_exception_handler(
#     request: Request, exc: SQLAlchemyError
# ) -> JSONResponse:
#     """
#     Handler for database errors.
#     Distinguishes between client errors (constraint violations) and server errors.
#     """
#     # Check if this is a unique constraint violation
#     if isinstance(exc, IntegrityError):
#         error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

#         # Try to extract the constraint name or field from the error message
#         constraint_match = re.search(r'Key \(([^)]+)\)', error_msg)
#         field_name = constraint_match.group(1) if constraint_match else 'field'

#         # Check for different types of integrity errors
#         if (
#             'unique constraint' in error_msg.lower()
#             or 'duplicate key' in error_msg.lower()
#         ):
#             logger.warning(
#                 f'Unique constraint violation: {error_msg}',
#                 extra={
#                     'path': request.url.path,
#                     'method': request.method,
#                     'field': field_name,
#                 },
#             )

#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     'error': {
#                         'message': f'Duplicate entry: {field_name} already exists',
#                         'status_code': 400,
#                         'details': {
#                             'type': 'unique_constraint_violation',
#                             'field': field_name,
#                         },
#                         'path': request.url.path,
#                     }
#                 },
#             )

#         elif 'foreign key constraint' in error_msg.lower():
#             logger.warning(
#                 f'Foreign key constraint violation: {error_msg}',
#                 extra={'path': request.url.path, 'method': request.method},
#             )

#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     'error': {
#                         'message': 'Invalid reference: related record does not exist',
#                         'status_code': 400,
#                         'details': {
#                             'type': 'foreign_key_constraint_violation',
#                             'field': field_name,
#                         },
#                         'path': request.url.path,
#                     }
#                 },
#             )

#     # For all other database errors, return 500
#     logger.error(
#         f'Database error: {str(exc)}',
#         extra={'path': request.url.path, 'method': request.method},
#         exc_info=True,
#     )

#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={
#             'error': {
#                 'message': 'Database operation failed',
#                 'status_code': 500,
#                 'details': {'error': 'An internal database error occurred'},
#                 'path': request.url.path,
#             }
#         },
#     )


# async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
#     """Handler for uncaught exceptions."""
#     logger.error(
#         f'Unhandled exception: {str(exc)}',
#         extra={'path': request.url.path, 'method': request.method},
#         exc_info=True,
#     )

#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={
#             'error': {
#                 'message': 'Internal server error',
#                 'status_code': 500,
#                 'details': {},
#                 'path': request.url.path,
#             }
#         },
#     )

# exceptions.py
"""
Custom exception classes for production-grade error handling.
Provides detailed error information and proper HTTP status codes.
"""
# from typing import Any, Dict, Optional


# class AppException(Exception):
#     """Base exception class for all application exceptions."""

#     def __init__(
#         self,
#         message: str,
#         status_code: int = 500,
#         details: Optional[Dict[str, Any]] = None
#     ):
#         self.message = message
#         self.status_code = status_code
#         self.details = details or {}
#         super().__init__(self.message)


# class NotFoundException(AppException):
#     """Resource not found (404)."""

#     def __init__(self, resource: str, identifier: Any):
#         super().__init__(
#             message=f"{resource} not found",
#             status_code=404,
#             details={"resource": resource, "identifier": str(identifier)}
#         )


# class UnauthorizedException(AppException):
#     """User is not authenticated (401)."""

#     def __init__(self, message: str = "Authentication required"):
#         super().__init__(message=message, status_code=401)


# class ForbiddenException(AppException):
#     """User lacks required permissions (403)."""

#     def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict[str, Any]] = None):
#         super().__init__(
#             message=message,
#             status_code=403,
#             details=details or {}
#         )


# class BadRequestException(AppException):
#     """Invalid request data (400)."""

#     def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
#         super().__init__(
#             message=message,
#             status_code=400,
#             details=details or {}
#         )


# class ConflictException(AppException):
#     """Resource conflict, e.g., duplicate entry (409)."""

#     def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
#         super().__init__(
#             message=message,
#             status_code=409,
#             details=details or {}
#         )


# class ValidationException(AppException):
#     """Data validation failed (422)."""

#     def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
#         super().__init__(
#             message=message,
#             status_code=422,
#             details=details or {}
#         )

# in main.py
# Register exception handlers
# app.add_exception_handler(AppException, app_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(SQLAlchemyError, database_exception_handler)
# app.add_exception_handler(Exception, general_exception_handler)
