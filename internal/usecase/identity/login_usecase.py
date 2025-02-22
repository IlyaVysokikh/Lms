from dataclasses import dataclass

from internal.exceptions.identity.password_mismatch_exception import PasswordMismatchException
from internal.exceptions.identity.user_not_found import UserNotFoundException
from internal.handlers.identity.schema.login_schema import LoginSchema
from internal.handlers.identity.schema.token_pair_schema import TokenPairSchema
from internal.services.identity.auth_service import AuthService


@dataclass
class LoginUseCase:
    auth_service: AuthService

    def execute(self, schema: LoginSchema) -> TokenPairSchema:
        user = self.auth_service.find_user_by_username(schema.email)
        if not user:
            raise UserNotFoundException(schema.email)

        if not self.auth_service.verify_password(schema.password, user.password_hash):
            raise PasswordMismatchException()

        tokens_pair: TokenPairSchema = self.auth_service.create_tokens_pair(user.oid, schema.email)

        return tokens_pair


