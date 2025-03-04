from dataclasses import dataclass

from internal.exceptions.application_exception import ApplicationException

@dataclass
class EmailNotFoundException(ApplicationException):
    @property
    def message(self) -> str:
        return f"Не смогли найти аккаунт для подтверждения"