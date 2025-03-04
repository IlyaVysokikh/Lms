from dataclasses import dataclass

from internal.exceptions.application_exception import ApplicationException

@dataclass
class UserNotVerifiedException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f"Не получилось подтвердить email {self.email}"
