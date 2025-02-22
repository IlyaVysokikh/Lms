from dataclasses import dataclass

from internal.exceptions.application_exception import ApplicationException

@dataclass
class UserNotFoundException(ApplicationException):
    email: str

    @property
    def message(self):
        return f'User with email {self.email} not found'