from dataclasses import dataclass

from internal.exceptions.application_exception import ApplicationException

@dataclass
class UserAlreadyExistsException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f"User with {self.email} already exists."