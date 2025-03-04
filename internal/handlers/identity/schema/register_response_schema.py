from pydantic import BaseModel


class RegisterResponseSchema(BaseModel):
    message: str = "Регистрация прошла успешно. Пожалуйста, проверьте свою электронную почту, чтобы подтвердить свою учетную запись."
    email: str