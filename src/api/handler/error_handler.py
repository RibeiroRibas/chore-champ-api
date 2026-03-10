from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.forbidden_error import ForbiddenError
from src.infra.http.errors.codes.infra_error_codes import InfraErrorCodes
from src.infra.http.errors.http_client_error import HttpClientError
from src.domain.errors.internal_error import InternalError
from src.domain.errors.models.error_model import ErrorModel
from src.domain.errors.not_found_error import NotFoundError
from src.domain.errors.unauthorized_error import UnauthorizedError


def add_error_handler(app: FastAPI):
    @app.exception_handler(UnauthorizedError)
    async def unauthorized_error_handler(_, exc: UnauthorizedError):
        return JSONResponse(
            status_code=401,
            content=ErrorModel(code=exc.code).model_dump()
        )

    @app.exception_handler(InternalError)
    async def internal_error_handler(_, exc: InternalError | Exception):
        return JSONResponse(
            status_code=500,
            content=ErrorModel(code=exc.code).model_dump()
        )

    @app.exception_handler(Exception)
    async def internal_error_handler(_, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=ErrorModel(code=InfraErrorCodes.UNMAPPED_ERROR.code()).model_dump()
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(_, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content=ErrorModel(code=exc.code).model_dump()
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_error_handler(_, exc: BadRequestError):
        return JSONResponse(
            status_code=400,
            content=ErrorModel(code=exc.code).model_dump()
        )

    @app.exception_handler(ForbiddenError)
    async def forbidden_error_handler(_, exc: ForbiddenError):
        return JSONResponse(
            status_code=403,
            content=ErrorModel(code=exc.code).model_dump()
        )

    @app.exception_handler(HttpClientError)
    async def forbidden_error_handler(_, exc: HttpClientError):
        if exc.status_code == 400:
            return JSONResponse(
                status_code=400,
                content=ErrorModel(code=InfraErrorCodes.HTTP_CLIENT_EXTERNAL_DATA_ERROR.code()).model_dump()
            )
        elif exc.status_code == 401:
            return JSONResponse(
                status_code=401,
                content=ErrorModel(code=InfraErrorCodes.HTTP_CLIENT_EXTERNAL_DATA_ERROR.code()).model_dump()
            )
        elif exc.status_code == 403:
            return JSONResponse(
                status_code=403,
                content=ErrorModel(code=InfraErrorCodes.HTTP_CLIENT_EXTERNAL_DATA_ERROR.code()).model_dump()
            )
        elif exc.status_code == 404:
            return JSONResponse(
                status_code=404,
                content=ErrorModel(code=InfraErrorCodes.HTTP_CLIENT_EXTERNAL_DATA_ERROR.code()).model_dump()
            )
        else:
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorModel(code=InfraErrorCodes.HTTP_CLIENT_EXTERNAL_DATA_ERROR.code()).model_dump()
            )
