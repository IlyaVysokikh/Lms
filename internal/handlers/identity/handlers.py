from fastapi import APIRouter, Depends, status
from punq import Container

from configs.container import get_container
from internal.exceptions.application_exception import ApplicationException
from internal.exceptions.identity.password_mismatch_exception import PasswordMismatchException
from internal.exceptions.identity.user_not_found import UserNotFoundException
from internal.handlers.identity.schema.login_schema import LoginSchema
from internal.handlers.identity.schema.register_response_schema import RegisterResponseSchema
from internal.handlers.identity.schema.register_schema import RegisterSchema
from internal.handlers.identity.schema.token_pair_schema import TokenPairSchema
from internal.usecase.identity.login_usecase import LoginUseCase
from internal.usecase.identity.register_usecase import RegisterUseCase
from internal.usecase.identity.verify_email_usecase import VerifyEmailUseCase

router = APIRouter(prefix="/api/v1/identity", tags=["identity"])

@router.post(
    "/login",
    summary="Login user",
    description="Endpoint to login user.",
    responses={
        200: {
            "description": "Successful login",
            "model": TokenPairSchema
        },
        400: {
            "description": "Password mismatch",
            "content": {
                "application/json": {
                    "example": {"message": "Password does not match."}
                }
            }
        },
        403: {
            "description": "User is not verify email",
            "content": {
                "application/json": {
                    "example": {"message": "Письмо с инструкцией подтвержения было отравлено на почту {self.email}. Пожалуйста, подвердите аккаунт."}
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"message": "User not found."}
                }
            }
        }
    }
)
async def login_user_handler(
        login_schema: LoginSchema,
        container: Container = Depends(get_container)
) -> TokenPairSchema:

    use_case = container.resolve(LoginUseCase)
    try:
        result = await use_case.execute(login_schema)
    except UserNotFoundException as ex:
        raise ex
    except PasswordMismatchException as ex:
        raise ex
    return result


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register user",
    description="Endpoint to register user.",
    responses={
        201: {
            "description": "Successful registration",
            "model": RegisterResponseSchema
        },
        400: {
            "description": "User already exists",
            "content": {
                "application/json": {
                    "example": {"message": "User with email already exists."}
                }
            }
        },
    }
)
async def register_user_handler(
        register_schema: RegisterSchema,
        container: Container = Depends(get_container)
):
    use_case = container.resolve(RegisterUseCase)

    try:
        result = await use_case.execute(register_schema)
    except ApplicationException as ex:
        raise ex

    return result


@router.get(
    "verify",
    summary="Verify user email",
    description="Endpoint to verify user email.",
    responses={
        200: {
            "description": "Successful registration",
            "model": RegisterResponseSchema
        }
    }
)
async def verify_user_handler(token: str, container: Container = Depends(get_container)):
    use_case = container.resolve(VerifyEmailUseCase)

    try:
        result = await use_case.execute(token)
    except ApplicationException as ex:
        raise ex

    return result