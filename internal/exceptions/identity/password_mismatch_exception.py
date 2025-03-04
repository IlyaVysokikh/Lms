from dataclasses import dataclass

from internal.exceptions.application_exception import ApplicationException

@dataclass
class PasswordMismatchException(ApplicationException):
    @property
    def message(self):
        return "Password mismatch"