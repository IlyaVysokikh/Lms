from dataclasses import dataclass

from internal.exceptions.application_exception import ApplicationException
from internal.exceptions.identity.user_already_exists_exception import UserAlreadyExistsException
from internal.handlers.identity.schema.register_response_schema import RegisterResponseSchema
from internal.handlers.identity.schema.register_schema import RegisterSchema
from internal.services.identity.auth_service import AuthService
from internal.services.identity.user_service import UserService
from internal.services.social.notification_service import NotificationService


@dataclass
class RegisterUseCase:
    user_service: UserService
    auth_service: AuthService
    notification_service: NotificationService

    async def execute(self, register_schema: RegisterSchema) -> RegisterResponseSchema:
        if self.user_service.find_user_by_email(register_schema.email):
            raise UserAlreadyExistsException(register_schema.email)

        hashed_password: bytes = self.auth_service.hash_password(register_schema.password)

        if not self.user_service.save_user(
                register_schema.name,
                register_schema.surname,
                register_schema.email,
                hashed_password
        ):
            raise ApplicationException()

        self.notification_service.send_verification_email(
            to_email=register_schema.email,
            name=register_schema.name,
            surname=register_schema.surname,
        )

        return RegisterResponseSchema(
            email=register_schema.email,
        )



