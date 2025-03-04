from dataclasses import dataclass

from internal.exceptions.identity.email_not_found_exception import EmailNotFoundException
from internal.exceptions.identity.user_not_verified_exception import UserNotVerifiedException
from internal.handlers.identity.schema.verification_response_schema import VerificationResponseSchema
from internal.infrastructure.redis.redis_client import RedisClient
from internal.services.identity.user_service import UserService


@dataclass
class VerifyEmailUseCase:
    redis_client: RedisClient
    user_service: UserService

    def execute(self, token: str) -> VerificationResponseSchema:
        email = self.redis_client.get_key(token)
        if not email:
            raise EmailNotFoundException()

        verified = self.user_service.verify_user(email)
        if not verified:
            raise UserNotVerifiedException(email)

        self.redis_client.delete_key(token)

        return VerificationResponseSchema(success=verified)
