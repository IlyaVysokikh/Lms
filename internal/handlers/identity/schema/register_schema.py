from pydantic import BaseModel


class RegisterSchema(BaseModel):
    name: str
    surname: str
    email: str
    password: str
