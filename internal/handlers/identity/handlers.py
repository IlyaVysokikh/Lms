
from fastapi import APIRouter, Depends, status
from punq import Container

from configs.container import get_container
from internal.exceptions.identity.password_mismatch_exception import PasswordMismatchException
from internal.exceptions.identity.user_not_found import UserNotFoundException
from internal.handlers.identity.schema.login_schema import LoginSchema
from internal.handlers.identity.schema.token_pair_schema import TokenPairSchema
from internal.usecase.identity.login_usecase import LoginUseCase

router = APIRouter(prefix="/api/v1/identity", tags=["identity"])

@router.post(
    "/login",
    summary="Login user",
    description="Endpoint to login user.",
    responses={
    }
)
async def register_user(
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