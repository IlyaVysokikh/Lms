from dataclasses import dataclass

from internal.exceptions.identity.email_not_verified_exception import EmailNotVerifiedException
from internal.exceptions.identity.password_mismatch_exception import PasswordMismatchException
from internal.exceptions.identity.user_not_found import UserNotFoundException
from internal.handlers.identity.schema.login_schema import LoginSchema
from internal.handlers.identity.schema.token_pair_schema import TokenPairSchema
from internal.services.identity.auth_service import AuthService
from internal.services.identity.user_service import UserService


@dataclass
class LoginUseCase:
    auth_service: AuthService
    user_service: UserService

    def execute(self, schema: LoginSchema) -> TokenPairSchema:
        user = self.user_service.find_user_by_email(schema.email)
        if not user:
            raise UserNotFoundException(schema.email)

        if not user.verified:
            raise EmailNotVerifiedException(schema.email)

        if not self.auth_service.verify_password(schema.password, user.password_hash):
            raise PasswordMismatchException()

        tokens_pair: TokenPairSchema = self.auth_service.create_tokens_pair(user.oid, schema.email)

        return tokens_pair


