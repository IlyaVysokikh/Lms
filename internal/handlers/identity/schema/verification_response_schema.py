from pydantic import BaseModel


class VerificationResponseSchema(BaseModel):
    message: str = "Email успешно подтвержден"
    success: bool
