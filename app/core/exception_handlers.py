from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = []
    for error in exc.errors():
        errors.append(
            {
                'message': error['msg'],
                'type': error['type'],
                'field': '.'.join(str(x) for x in error['loc']),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            'error': {
                'message': 'Validation failed',
                'status_code': 422,
                'path': request.url.path,
                'details': {'validation_errors': errors},
            }
        },
    )
