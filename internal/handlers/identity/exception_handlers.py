from starlette.requests import Request
from starlette.responses import JSONResponse

from internal.exceptions.identity.password_mismatch_exception import PasswordMismatchException
from internal.exceptions.identity.user_not_found import UserNotFoundException


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message()},
    )


async def password_mismatch_exception_handler(request: Request, exc: PasswordMismatchException) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": exc.message()},
    )