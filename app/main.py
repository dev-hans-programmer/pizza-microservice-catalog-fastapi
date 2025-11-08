from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from app.api.v1.routes import api_v1_router
from app.core.exception_handlers import validation_exception_handler

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Hello server'}


app.include_router(router=api_v1_router, prefix='/api')


# Adapter with the general Exception signature required by add_exception_handler
def _validation_exception_handler_adapter(request: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        return validation_exception_handler(request, exc)
    # If it's not the expected type, re-raise so other handlers can handle it
    raise exc


app.add_exception_handler(RequestValidationError, _validation_exception_handler_adapter)
