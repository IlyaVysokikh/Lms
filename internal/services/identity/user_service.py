from dataclasses import dataclass

from internal.infrastructure.postgresql.repositories.user_repository import UserRepository
from internal.models.identity.user import User

@dataclass
class UserService:
    user_repository: UserRepository

    def find_user_by_email(self, email: str) -> User | None:
        return self.user_repository.find_user_by_email(email)

    def save_user(self, name: str, surname: str, email: str, hashed_password: bytes) -> bool:
        return self.user_repository.save_user(name, surname, email, hashed_password)

    def verify_user(self, email: str) -> bool:
        self.user_repository.verify_user(email)