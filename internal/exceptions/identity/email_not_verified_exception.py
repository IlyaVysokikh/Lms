from dataclasses import dataclass

from internal.exceptions.application_exception import ApplicationException

@dataclass
class EmailNotVerifiedException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"Письмо с инструкцией подтвержения было отравлено на почту {self.email}. Пожалуйста, подвердите аккаунт."